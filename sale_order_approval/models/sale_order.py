# -*- coding: utf-8 -*-

from odoo import models,fields,api
from odoo.exceptions import UserError


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    state=fields.Selection(selection_add=[('approved','Approved')])
    approving_user=fields.Many2one('res.users',string='Approving user')


    def action_approve_btn(self):
        for record in self:

            if  self.env.user != record.approving_user:
                raise UserError("selected user should approve")

            self.write({
                'state':'approved'
            })

    @api.depends('state', 'order_line.invoice_status')
    def _compute_invoice_status(self):
        for record in self:
            if record.state=='approved':
                record.invoice_status=='to invoice'
        return  super()._compute_invoice_status()

    def _create_invoices(self, grouped=False, final=False, date=None):
        for record in self:
            if record.state!='approved':
                raise UserError('only approved state')
        return super()._create_invoices( grouped=False, final=False, date=None)

