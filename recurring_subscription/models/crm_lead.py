from odoo import models,fields
class CrmLead(models.Model):
    _inherit = 'crm.lead'

    id_order=fields.Char(string='Order id' ,required=True)
    _unique_order_id = models.Constraint(
        'unique (id_order)',
        "The order id name must be unique!",
    )