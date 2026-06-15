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
        # for rec in self:

        if self.bulk_product_ids and self.quantity :
               print(self.bulk_product_ids)
               print(654,self.quantity)
               print(321,self.id)
               for line in self.bulk_product_ids:
                   print(432,line)
                   self.env['purchase.order.line'].create({
                       'order_id': self.id,
                       'product_id': line.product_variant_id.id,
                       'product_qty': self.quantity,
                   #     # 'order_line':[Command.create({
                   #     #             'product_id': rec.bulk_product_ids,
                   #     #             'product_qty': rec.quantity,

                       # })]

                    })

               print(self.bulk_product_ids)
               print(self.quantity)
