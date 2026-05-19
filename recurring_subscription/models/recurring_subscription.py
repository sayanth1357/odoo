# -*- coding: utf-8 -*-

from datetime import timedelta,date
from odoo import fields,models,api
from odoo.exceptions import ValidationError
import re

class RecurringSubscription(models.Model):
    _name="recurring.subscription"
    _description="Recurring Subscription"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    id_order=fields.Char(string='Order id',copy=False,readonly=True)
    name=fields.Char(string="Name", required=True, tracking=True)
    description= fields.Text(string="Description")
    id_establishment=fields.Char(string="Establishment id",required=True)
    date=fields.Date(string="Date" ,tracking=True,default=date.today())
    due_date=fields.Date(default=date.today()+timedelta(days=15), string="Due Date")
    billing_schedule=fields.Many2one('billing.schedule',string="Billing schedule")
    next_billing=fields.Date(string="Next Billing")
    is_lead=fields.Boolean(string="Is Lead")
    company_id=fields.Many2one('res.company',store=True,string="company",copy="False",
                               default=lambda self:self.env.user.company_id.id)
    currency_id=fields.Many2one("res.currency",string="currency",related='company_id.currency_id',
                                default=lambda self: self.env.user.company_id.currency_id.id)
    recurring_amount=fields.Monetary(string="Recurring amount" ,tracking=True,default=1)
    status=fields.Selection(selection=[('draft','Draft'),
                                       ('confirm','Confirm'),
                                       ('done','Done'),
                                       ('cancel','Cancelled')],
                            default='draft',tracking=True,readonly=True)
    customer_id=fields.Many2one("res.partner",string="Customer" ,copy=False,required=True)
    product_id=fields.Many2one("product.template",string="Product" ,required=True)
    terms_and_condition=fields.Html(string='Terms and condition')
    count=fields.Integer(string="count",compute="_compute_count")

    recurring_subscription_credit_ids=fields.One2many("recurring.subscription.credit",
                                                      inverse_name='recurring_subscription_id',
                                                      compute="_compute_recurring_subscription_credit_ids",
                                                      store=True)
    order_lines_ids=fields.One2many('product.order.lines',inverse_name="order_lines_id", string="product")
    product_filter_ids=fields.Many2many('product.template',string="Product filter")

    @api.model_create_multi
    def create(self,vals):
        for rec in vals:
            code=self.env['ir.sequence'].next_by_code('recurring.subscription')
            rec['id_order'] = code
        res=super().create(vals)
        print(res)
        return res

    def action_confirm_btn(self):
        self.write({
            'status':'confirm'
        })

    def action_cancel_btn(self):
        self.write({
            'status':'cancel'
        })

    def action_done_btn(self):
        # self.write({
        #     'status':'done'
        # })
        template = self.env.ref('recurring_subscription.mail_template_recurring_subscription')
        print(876,template)
        email_values = {
            'email_from': self.env.user.email,
            'email_to': self.customer_id.email,
        }

        print(123,email_values)
        if template:
            template.send_mail(self.id, force_send=True, email_values=email_values)
            self.message_post_with_source(
                template,
                subtype_xmlid='mail.mt_comment',
            )
            print(321)
            self.write({
                   'status':'done'
            })

    @api.constrains('id_establishment')
    def _check_id_establishment(self):
        pattern=r'^(?=(?:.*[A-Za-z]){3}).*(?=(?:.*\d){3}).*(?=(?:.*[^A-Za-z0-9]){2}).*$'
        for record in self:
            if record.id_establishment:
                if not re.match(pattern,record.id_establishment):
                    raise ValidationError("must contain 3 alphabet ,3 numbers, 2 special characters")


    @api.depends('recurring_subscription_credit_ids.date_end','due_date')
    def _compute_recurring_subscription_credit_ids(self):
        for record in self:
            credits = record.recurring_subscription_credit_ids.filtered(lambda rec:
                                                                        rec.date_end < rec.due_date)
            self.update({
                'recurring_subscription_credit_ids': [(fields.Command.set(credits.ids))]
            })


    @api.depends('product_filter_ids','order_lines_ids.quantity','order_lines_ids.product_template_id')
    def _compute_count(self):
        for record in self:
            sum=0
            for rec in record.order_lines_ids:
                if rec.product_template_id in record.product_filter_ids:
                    sum+=rec.quantity
            record.count=sum



    @api.onchange('id_establishment')
    def _onchange_id_establishment(self):
        for record in self:
            if record.id_establishment:
                partner=self.env['res.partner'].search([('id_establishment','=',record.id_establishment)],limit=1)
                if partner:
                    record.customer_id=partner
                else:
                    raise ValidationError('no partner found')
