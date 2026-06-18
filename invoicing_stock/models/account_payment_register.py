from odoo import fields,models

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

   
    def _compute_communication(self):
        for wizard in self:
            delivery=self.line_ids.move_id.delivery_orders_id.name
            if wizard.can_edit_wizard and wizard.installments_mode == 'full' or wizard.custom_user_amount:
                lines = wizard.line_ids
            else:
                lines = wizard._get_total_amounts_to_pay(wizard.batches)['lines']
            wizard.communication = wizard._get_communication(lines)+","+delivery

