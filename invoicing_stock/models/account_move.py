# -*- coding: utf-8 -*-
from odoo import models, fields, Command
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    delivery_orders_id = fields.Many2one("stock.picking", string="Delivery orders", tracking=True)

    def assign_product_btn(self):
        for product in self.delivery_orders_id.move_ids:
            self.invoice_line_ids = [(Command.create({
                'product_id': product.product_id.id,
                'quantity': product.quantity,
            }))]
        products = {}
        # for line in self.invoice_line_ids:
        #     product=line.product_id.id
        #     if product in products:
        #         raise ValidationError('Product is already added')
        #     else:
        #         products[product]=line
        print(len(self.invoice_line_ids))
        if len(self.invoice_line_ids) > 1:
            raise ValidationError('Product is already added')

    def action_post(self):

        for rec in self.invoice_line_ids:
            if rec.quantity <= 0:
                self.message_post(body='Minimum of one quantity should be there')
                # raise ValidationError('Minimum of one quantity should be there')
        return super().action_post()

    # def action_register_payment(self,ctx=None):
    #     res=super().action_register_payment()
    #     print(ctx)
    #     return res



