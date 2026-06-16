from odoo import fields,models
from odoo.exceptions import ValidationError


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def action_send_mail(self):
        print(self)
        # res = super().action_send_mail()

        for rec in self.env['sale.order'].search([('id','in',self.env.context.get('active_ids'))]):
            print(123,rec)
            print(321,rec.order_line.product_template_id)
            if not rec.order_line.product_template_id:
                raise ValidationError('no products')
            else:
                super().action_send_mail()



