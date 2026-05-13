# -*- coding: utf-8 -*-

from odoo import fields,models
class ProductCount(models.Model):
    _name = "product.order.lines"
    _description = "Product order lines"


    order_lines_id=fields.Many2one('recurring.subscription',string='order lines')

    product_template_id = fields.Many2one('product.template',
        string="Product Template",
        readonly=False)
    quantity=fields.Integer(string="Quantity")
    price=fields.Integer(string="Price")

