# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    def button_confirm(self):
        attachments = self.env['ir.attachment'].search([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ])
        print(attachments)
        param = self.env['ir.config_parameter'].sudo()
        state = param.get_param('purchase.require_attachment')
        if state:
             if not attachments:
                raise UserError('Atleast one attachment is required')


        return super().button_confirm()
