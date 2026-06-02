# -*- coding: utf-8 -*-

from odoo import models, fields
class ResConfigSettings(models.TransientModel):
   _inherit = 'res.config.settings'

   require_attachment=fields.Boolean(string='Require Attachment on Purchase Order Confirmation' ,
                                     config_parameter='purchase.require_attachment')


