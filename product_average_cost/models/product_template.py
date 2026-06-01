from odoo import models,fields,api

class PurchaseOrder(models.Model):

    _inherit = 'product.template'

    average_cost=fields.Monetary(string='Average cost',compute='_compute_average_cost')

    def _compute_average_cost(self):
        for record in self:
            purchase_line=self.env['purchase.order.line'].search([('price_subtotal','=',self.id),
                                                                  ('state','=','purchase')])
            total=purchase_line.mapped('price_unit_product_uom')
            print(total)
            qty=purchase_line.mapped('product_uom_qty')
            print(qty)
            total_new=sum(total)
            print(total_new)
            total_qty=sum(qty)
            print(total_qty)
            avg=total_new/total_qty
            print(avg)
            record.write({
                'average_cost':avg
            })




