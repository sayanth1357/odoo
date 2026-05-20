# -*- coding: utf-8 -*-

from odoo import fields,models,api
class BillingSchedule(models.Model):
    _name = 'billing.schedule'
    _description = 'Billing schedule'
    _rec_name = 'billing_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    simulation_boolean=fields.Boolean(string="Simulation")
    billing_name=fields.Char(string='Name',tracking=True)
    billing=fields.Char(string='billing')
    date_begin = fields.Date(string='period', required=True, tracking=True)
    date_end = fields.Date(string='End Date', required=True, tracking=True)
    active=fields.Boolean(string="Active" ,default=True)
    customer_id=fields.Many2many('res.partner',string='customer')
    recurring_subscription_ids=fields.Many2many('recurring.subscription',
                                               string="recurring subscription",tracking=True,required=True)
    company_id = fields.Many2one('res.company', store=True, string="company", copy="False",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one("res.currency", string="currency", related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    total_credit_amount=fields.Monetary(string="Total credit amount" ,default=1,compute='_compute_total_credit_amount')
    credits_ids=fields.Many2many('recurring.subscription.credit',string='Credits')
    invoice_ids=fields.Many2many('account.move',string='inv')
    invoice_count = fields.Integer(compute="_compute_invoice_count", string='invoice count')


    def action_rec_sub(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "recurring.subscription",
            "name": "invoices",
            "views": [[False, "list"], [False, "form"]],
            "domain": [('id','in',self.recurring_subscription_ids.ids)]
        }

    def action_rec_sub_invoice(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "name": "billing.schedule",
            "views": [[False, "list"], [False, "form"]],
            "domain": [('id', 'in', self.invoice_ids.ids)]
        }

    @api.depends('recurring_subscription_ids')
    def _compute_total_credit_amount(self):
        sum = 0
        for record in self:
            for rec in record.recurring_subscription_ids:
                if rec.status == 'confirm':
                    for line in rec.recurring_subscription_credit_ids:
                        if line.state=='fully approved':
                            sum += line.credit_amount
            record.total_credit_amount = sum



    @api.depends('recurring_subscription_ids')
    def _compute_credits_ids(self):
        for record in self:
                credits=record.recurring_subscription_ids.mapped('recurring_subscription_credit_ids')
                self.update({
                    'credits_ids': [(fields.Command.set(credits.ids))]
                })



    @api.onchange('recurring_subscription_ids')
    def _onchange_recurring_subscription_ids(self):
            credits=self.env['recurring.subscription.credit'].search([
                ('state','=','fully approved'),
                ('recurring_subscription_id','in',self.recurring_subscription_ids.ids)
            ])
            self.customer_id=self.recurring_subscription_ids.mapped('customer_id')
            self.update({
                            'credits_ids': [(fields.Command.set(credits.ids))]
            })



    def action_create_inv(self):
        line_invoice_ids=[]
        for record in self:
            for rec in record.recurring_subscription_ids:
                credit=self.env['recurring.subscription.credit'].search([('recurring_subscription_id','=',rec.id),
                                                                         ('state','=','fully approved'),
                                                                         ('credit_amount','=',rec.recurring_amount)],limit=1)
                if not credit:
                    credit=self.env['recurring.subscription.credit'].search([('recurring_subscription_id','=',rec.id),
                                                                             ('state', '=', 'fully approved'),
                                                                             ('credit_amount','<=',rec.recurring_amount)],order='id ASC',limit=1)

                print(credit)
                print(record.recurring_subscription_ids)

                invoice_line_ids=[(0,0,{
                    'name':rec.name,
                    'product_id':rec.product_id.product_variant_id.id,
                    # 'name':rec.name,
                    'quantity':1,
                    'price_unit':rec.recurring_amount,
                })]

                if credit:
                    invoice_line_ids.append((0,0,{
                        'name':credit,
                        'quantity':1,
                        'price_unit':-credit.credit_amount,
                    }))
                print(invoice_line_ids)

                invoice=self.env['account.move'].create({
                    'move_type':'out_invoice',
                    'partner_id': rec.customer_id.id,
                    'invoice_line_ids':invoice_line_ids,
                    })

                line_invoice_ids.append(invoice.id)

                record.write({
                    'invoice_ids': line_invoice_ids
                })

                return{
                    'name':'invoices',
                    'type':'ir.actions.act_window',
                    'res_model':'account.move',
                    'view_mode':'form',
                    'view_type':'form',
                    'target':'current',
                    'res_id':invoice.id,
                }


    @api.depends('credits_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    def _create_daily_invoice(self):
        for record in self:
            for rec in record.recurring_subscription_ids:
                print(record)
                if rec.status=='confirm' and rec.due_date < rec.date:
                    print(rec.status)
                    print(rec.due_date)
                    self.action_create_inv