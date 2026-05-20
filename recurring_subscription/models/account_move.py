from odoo import fields,models
class AccountMove(models.Model):
    _inherit = 'account.move'

    billing_id=fields.Many2one('billing.schedule',string='billing')