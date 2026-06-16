# -*- coding: utf-8 -*-
from odoo import models,Command,fields,api
class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    bulk_product_ids=fields.Many2many('product.template',string="bulk product")
    quantity=fields.Integer(string="quantity")


    # @api.onchange('bulk_product_ids','quantity')
    # def _onchange_product_quantity(self):
    #     lines=[]
    #     if self.bulk_product_ids and self.quantity:
    #
    def action_product_btn(self):
        print(self)
        for product in self.bulk_product_ids:
            # for rec in self.order_line:
            #     if rec.product_id == product.product_variant_id.id:
            #        rec.product_qty+=self.quantity
            line=self.order_line.filtered(lambda x:x.product_id.id==product.product_variant_id.id)
            print(1222,line)
            if line:
                line.product_qty+=self.quantity
            else:
                self.order_line = [(Command.create({
                        'product_id':product.product_variant_id.id,
                        'product_qty':self.quantity,
                    }))]

          

