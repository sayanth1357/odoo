# -*- coding: utf-8 -*-
from odoo import models,fields
class ResUsers(models.Model):
    _inherit = 'res.users'

    hide_specific_menu=fields.Many2many('ir.ui.menu',string='Hide specific menu')
