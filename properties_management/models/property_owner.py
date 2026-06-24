# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    owner_ids=fields.One2many('rental.lease.management','tenant_id',string="Owners")

