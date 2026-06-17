from docutils.nodes import line

from odoo import fields,models
class SaleOrder(models.Model):

    _inherit = 'sale.order'


    def action_confirm(self):

        products={}
        for line in self.order_line:
            product=line.product_id.id
            print(23456,product)
            if product  in products:
                products[product].product_uom_qty+=line.product_uom_qty
                # products[product].price_unit +=line.price_unit
                products[product].price_unit*=products[product].product_uom_qty
                products[product].price_unit=(products[product].price_unit/ products[product].product_uom_qty)
                # products[product].price_subtotal=( products[product].price_unit * products[product].product_uom_qty)
                # products[product].price_subtotal+=products[product].price_unit
                # print( 1234,products[product].price_subtotal)
                # products[product].price_unit=(products[product].price_unit/products[product].product_uom_qty)

                line.unlink()
            else:
                products[product]=line
                print(998877,products[product])
        super().action_confirm()


