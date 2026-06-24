# -*- coding: utf-8 -*-
from odoo import fields, models,_,api

class AccountMove(models.Model):
    _inherit= ['account.move','mail.thread','mail.activity.mixin']

    account_id = fields.Many2one('account.move', string="Account")
    rent_id = fields.Many2one('rental.lease.management', string="Property Id")
    tenant_id=fields.Many2one(related='rent_id.tenant_id', string="Tenant Id")
    payment_status = fields.Selection([
        ('to_invoice', 'To Invoice'),
        ('not_paid', 'Not_Paid'),
        ('paid', 'Paid'),
        ('cancel', "Canceled"),
    ])
    def action_post(self):
        """action for the confirm button in the invoice record"""
        print("working")
        res=super(AccountMove, self).action_post()
        for rec in self:
            rec.account_id=self.id
        return res


