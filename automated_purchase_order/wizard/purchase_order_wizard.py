# -*- coding: utf-8 -*-
from odoo import models, fields
class PurchaseOrderWizard(models.TransientModel):
   _name = 'purchase.order.wizard'
   _description = 'Wizard for Automatic Purchase order'

   quantity=fields.Float(string='Quantity')
   price=fields.Float(string='Price')