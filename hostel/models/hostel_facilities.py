# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HostelFacilities(models.Model):
    """Manage hostel facilities"""
    _name = "hostel.facilities"
    _description = "Hostel facilities"

    name = fields.Char('Name', required=True)
    charge = fields.Float('Charge')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    @api.constrains('charge')
    def _check_charge(self):
        """Method used to check if charge is less than or equal to zero"""
        for record in self:
            if record.charge <= 0:
                raise ValidationError("Charge is less than or equal to zero")
