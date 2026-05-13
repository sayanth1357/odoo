import random
import string
from odoo import models,fields,api
from odoo.exceptions import ValidationError
import re
class ResPartner(models.Model):
    _inherit = 'res.partner'
    _rec_name = 'account_id'

    id_establishment =fields.Char(string="Establishment id")
    account_id=fields.Many2one('partner.account.id',string='Account id')

    _unique_id_establishment = models.Constraint(
        'unique (id_establishment)',
        "The establishment id  must be unique!",
    )

    _unique_account_id = models.Constraint(
        'unique (account_id)',
        "The account id  must be unique!",
    )


    @api.model_create_multi
    def create(self,vals):
        print(vals)
        print(1234)

        partner = super(ResPartner,self).create(vals)
        print(partner)
        print(23454)

        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        digit = ''.join(random.choices(string.digits, k=3))
        special = ''.join(random.choices('@#$%^&*', k=2))
        account_val = letters + digit + special
        account=self.env['partner.account.id'].create({
            'id_account': account_val,
            'partner_id': partner.id
        })
        partner.write({
            'account_id': account.id
        })

        print(self)
        print(account.id_account)

        # self.account_id=account.id_account
        print(self.account_id)
        print(123,self.account_id)
        return partner

