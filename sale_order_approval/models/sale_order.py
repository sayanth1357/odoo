# -*- coding: utf-8 -*-

from odoo import models,fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    state=fields.Selection(selection_add=[('approved','Approved')])
    approving_user=fields.Many2one('res.users',string='Approving user')

    def action_approve_btn(self):
        for record in self:
            if  self.env.user != record.approving_user:
                raise UserError("selected user should approve")

            # if not self.env.user.has_group('sale_order_approval.group_sale_salesman'):
            #     raise UserError("Only users can approve.")
            # self.state = 'approved'

            self.write({
                'state':'approved'
            })


    # def action_confirm(self):
    #     for record in self:
    #         record.write({
    #             'state':'sale'
    #         })

    def _create_invoices(self, grouped=False, final=False, date=None):
        for record in self:
            if record.state!='approved':
                raise UserError('only approved state')
            else:
                return super()._create_invoices()
