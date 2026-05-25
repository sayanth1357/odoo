# -*- coding: utf-8 -*-

from odoo import fields,models,api

class RecurringSubscriptionCredit(models.Model):
    _name = "recurring.subscription.credit"
    _rec_name = "recurring_subscription_id"
    _description = "Recurring Subscription Credit"
    _inherit = ['mail.thread','mail.activity.mixin']

    recurring_subscription_id=fields.Many2one('recurring.subscription',string="recurring subscription",
                                               tracking=True,required=True )
    name1=fields.Char(string='recurring name',related='recurring_subscription_id.name')
    partner_id=fields.Many2one('res.partner',string="partner" ,
                               related="recurring_subscription_id.customer_id")

    id_establishment=fields.Char(string="Establishment id", related="recurring_subscription_id.id_establishment")
    due_date=fields.Date(string='Due date',related='recurring_subscription_id.due_date')
    company_id=fields.Many2one('res.company',store=True,string="company",copy="False",
                               default=lambda self:self.env.user.company_id.id)
    currency_id=fields.Many2one("res.currency",string="currency",related='company_id.currency_id',
                                default=lambda self:self.env.user.company_id.currency_id.id)
    credit_amount=fields.Monetary(string="Credit amount",default=1)
    state=fields.Selection(selection=[
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('first approved','First approved'),
        ('fully approved','Fully approved'),
        ('rejected','Rejected')]
        ,default='pending',tracking=True)

    date_begin = fields.Date(string='period date', required=True, tracking=True)
    date_end = fields.Date(string='End Date', required=True, tracking=True)
    create_date = fields.Datetime(string='Created on',readonly=True)




    @api.onchange('credit_amount')
    def _onchange_credit_amount(self):
        for record in self:
            if record.recurring_subscription_id:
                if record.credit_amount==0 or record.credit_amount > record.recurring_subscription_id.recurring_amount:
                    record.recurring_subscription_id=False

