# -*- coding: utf-8 -*-

from odoo import fields,models,api


class SaleOrderLine(models.Model):

    _inherit = 'sale.order'

    is_vip=fields.Boolean(string='VIP customer', related='partner_id.is_vip')


    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for record in self:
            for rec in record.order_line:
                if record.partner_id.is_vip:
                    disc = (record.partner_id.vip_discount/rec.price_unit)*100
                    sub=rec.price_unit - record.partner_id.vip_discount

                    rec.write({
                        'discount':disc,
                        'price_subtotal': sub,

                    })
                else:
                    rec.discount = 0