# -*- coding: utf-8 -*-
from odoo import models,fields
class ProductTemplate(models.Model):

    _inherit = 'product.template'

    def action_open_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Automatic Purchase Order',
            'res_model': 'purchase.order.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_product_id':self.id,
                        'default_seller_ids':self.seller_ids}
        }
