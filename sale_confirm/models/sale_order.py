from odoo import fields,models


class SaleOrder(models.Model):

    _inherit = 'sale.order'


    def action_confirm(self):
        print(123,self)
        print(543,self.order_line)
        prod=[]
        for product in self.order_line:
            print(product)
            print(654,product.product_template_id)
            print(765,product.product_uom_qty)
            if product.product_template_id not in prod:
                prod.append(product.product_template_id)
                print(987654,prod)

        super().action_confirm()






            # prod=[]
            # for prod2 in self.order_line:
            #     if product.product_template_id==prod2.product_template_id:
            #         prod.append(prod2)
            #         print( prod.append(prod2))
            #         qty=product.product_uom_qty+prod2.product_uom_qty
            #         self.order_line=[(Command.create({
            #             'product_template_id':prod2.id,
            #             'product_uom_qty':qty,
            #         }))]
            #     else:
            #         super().action_confirm()



            
        # for order in self:
        #     prod=[]
        #     for product in order.order_line:
        #         if product.product_template_id.id not in prod and product.price_unit:
        #             prod.append(product.product_template_id.id)
        #             qty=product.product_uom_qty+product.product_uom_qty
                # if product.product_template_id not in prod:
                #      prod.append(product.product_template_id)
                #      for other_prod in order.order_line:



            #          line = self.order_line.filtered(lambda x: x.product_template_id.id == product.id)
            #          if line:
            #              qty=product.product_uom_qty+product.product_uom_qty
            #              self.order_line = [(Command.create({
            #              'product_id': product.id,
            #              'product_qty': qty,
            #          }))]
            # super().action_confirm()
            #





