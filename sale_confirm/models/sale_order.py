
from odoo import fields,models
class SaleOrder(models.Model):

    _inherit = 'sale.order'


    def action_confirm(self):
        """merge the order lines if same product """

        products={}
        for line in self.order_line:
            product=line.product_id.id
            print(23456,product)
            if product  in products:
                print(3333,(line.product_uom_qty * line.price_unit))
                price = (products[product].product_uom_qty * products[product].price_unit) + (line.product_uom_qty * line.price_unit)
                print(111111111,products[product].product_uom_qty * products[product].price_unit)
                print(22222,price)
                products[product].product_uom_qty += line.product_uom_qty
                products[product].price_unit = price / products[product].product_uom_qty
                line.unlink()
            else:
                products[product]=line
                print(998877,products[product])
        super().action_confirm()


