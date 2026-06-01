# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    def button_confirm(self):
        state=self.env['ir.config_parameter'].sudo().get_param('purchase.require_attachment')
        if state:
                attachments = self.env['ir.attachment'].search([('res_model', '=', self._name),
                                                                ('res_id', 'in', self.ids), ])

                attachment_type = ('application/pdf','image/jpeg','image/png')
                invalid_attach=attachments.filtered(lambda attachment:attachment.mimetype not in attachment_type)

                if not attachments:
                        raise UserError('Atleast one attachment is required')
                if  invalid_attach:
                    raise ValidationError('Attachment should be pdf or image format')

        return super().button_confirm()





