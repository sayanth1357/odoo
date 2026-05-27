# -*- coding: utf-8 -*-

from odoo import fields,models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_vip=fields.Boolean(string='VIP')
    vip_discount=fields.Float(string='VIP Discount')