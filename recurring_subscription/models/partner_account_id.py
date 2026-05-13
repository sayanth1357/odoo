# -*- coding: utf-8 -*-
from odoo import fields,models,api
from odoo.exceptions import ValidationError
import re



class PartnerAccountId(models.Model):
    _name = 'partner.account.id'
    _description = 'Partner Account ID'
    _rec_name = 'id_account'
    partner_id=fields.Many2one('res.partner',string='partner',ondelete='cascade')
    id_account=fields.Char(string='Account ID',ondelete='cascade')
    _unique_id_account = models.Constraint(
        'unique (id_account)',
        "The account id  must be unique!",
    )


    @api.constrains('id_account')
    def _check_id_account(self):
        pattern=r'^(?=(?:.*[A-Za-z]){3}).*(?=(?:.*\d){3}).*(?=(?:.*[^A-Za-z0-9]){2}).*$'
        for record in self:
            if record.id_account:
                if not re.match(pattern,record.id_account):
                    raise ValidationError("must contain 3 alphabet ,3 numbers, 2 special characters")