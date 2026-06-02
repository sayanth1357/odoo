# -*- coding: utf-8 -*-

from odoo import models,fields,api

class ProductTemplate(models.Model):

    _inherit = 'product.template'

    average_cost=fields.Monetary(string='Average cost',compute='_compute_average_cost')

    @api.depends()
    def _compute_average_cost(self):
        """Fetch the records from purchase order line, store the price and quantity in a variable and calculate sum
            Average cost= total price/ total quantity
            if quantity 0 then average cost is 0 """

        for record in self:
            purchase_line=self.env['purchase.order.line'].search([('product_id.product_tmpl_id','=',record.id),
                                                                  ('order_id.state','=','purchase')])
            total=purchase_line.mapped('price_subtotal')
            qty=purchase_line.mapped('product_uom_qty')
            total_new=sum(total)
            total_qty=sum(qty)
            if total_qty:
                record.average_cost=total_new/total_qty
            else:
                record.average_cost=0