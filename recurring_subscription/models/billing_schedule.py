# -*- coding: utf-8 -*-
from email.policy import default

from odoo import fields,models,api
from odoo.orm.decorators import onchange


class BillingSchedule(models.Model):
    _name = 'billing.schedule'
    _description = 'Billing schedule'
    _rec_name = 'billing_name'

    simulation_boolean=fields.Boolean(string="Simulation")
    # start_date = fields.Date(string="Start date")
    # end_date = fields.Date(string="End date")
    billing_name=fields.Char(string='Name')
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
    credits_ids=fields.One2many('recurring.subscription.credit','recurring_subscription_id'
                                ,string='Credits',compute='_compute_credits_ids')

    def action_rec_sub(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "recurring.subscription",
            "name": "billing.schedule",
            "views": [[False, "list"], [False, "form"]],
            "domain": [('id','in',self.recurring_subscription_ids.ids)]
        }

    @api.depends('recurring_subscription_ids')
    def _compute_total_credit_amount(self):
        sum = 0
        for record in self:
            for rec in record.recurring_subscription_ids:
                if rec.status == 'confirm':
                    for line in rec.recurring_subscription_credit_ids:
                        sum += line.credit_amount
            record.total_credit_amount = sum





    @api.depends('recurring_subscription_ids')
    def _compute_credits_ids(self):
        for record in self:
                print(record)
                credits=record.recurring_subscription_ids.mapped('recurring_subscription_credit_ids')
                print(credits)
                self.update({
                    'credits_ids': [(fields.Command.set(credits.ids))]
                })

    # @api.onchange('recurring_subscription_ids')
    # def _onchange_recurring_subscription_ids(self):
    #     if self.recurring_subscription_ids:
    #         credits=self.env['recurring.subscription'].search(['recurring_subscription_credit_ids','in',self.ids])
    #         print(credits)
    #         self.update({
    #             'credits_ids': [(fields.Command.set(credits.ids))]
    #         })
        # for record in self:
        #         print(123,record.recurring_subscription_ids)
        #         credits=record.recurring_subscription_ids.mapped('recurring_subscription_credit_ids')
        #         print(record.credits_ids)
        #         record.update({
        #                 'credits_ids': [(fields.Command.set(credits.ids))]
        #             })

    # @api.onchange('recurring_subscription_ids')
    # def _onchange_recurring_subscription_ids(self):
    #     for record in self:
    #         if record.recurring_subscription_ids:
    #             credits=record.recurring_subscription_ids.mapped('recurring_subscription_credit_ids')
    #             self.update({
    #                 'credits_ids':credits.ids
    #             })
    #


