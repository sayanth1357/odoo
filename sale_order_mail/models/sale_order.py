from odoo import fields,models
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):

    _inherit = 'sale.order'


    # def action_quotation_send(self):
    #   res=super().action_quotation_send()
    #   for rec in self:
    #         if not rec.order_line.product_id:
    #             raise ValidationError('no products')
    #   return res

# def action_send_mail