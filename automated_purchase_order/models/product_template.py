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
            'context': {'active_ids': self.ids},
        }
