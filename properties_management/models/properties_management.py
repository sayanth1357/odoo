# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class PropertiesManagement(models.Model):
    """Property Management"""
    _name = 'properties.management'
    _description = 'Properties Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference Id', copy=False, readonly=True,
                       index='trigram',
                       default=lambda self: _('New'), help="Reference Id")
    company_id = fields.Many2one('res.company', string="Company")
    tenantss_id = fields.Many2one('res.partner', string="Tenant")
    attachment_id = fields.Many2one('ir.attachment')
    rent_id = fields.Many2one('rental.lease.management',string="State", ondelete='cascade')
    prop_name = fields.Char(string='Rental/Leased Info', help="Name of the property")
    owner_id = fields.Many2one('res.partner', string='Owner Name', help="Owner Name and Address.")
    property_name = fields.Char(required=True, string='Property Name', help="Property Name", )
    property_image = fields.Image(string='Property Image', help="Property Image")
    build_date = fields.Datetime(string='Build Date', help="Date of construction of building")
    can_be_sold = fields.Boolean(string='Can be sold', help="Toggle to specify whether the property is for sale")
    lease_amount = fields.Float(string='Lease Amount', help="Amount for leasing the property")
    rent_amount = fields.Float(string='Rent Amount', help="Amount for renting the property")
    description = fields.Char(string='description', help="Description of the property")
    state = fields.Selection([('Draft', 'Draft'), ('leased', 'leased'), ('Rented', 'Rented'), ('sold', 'Sold')],
                             default='Draft',
                             tracking=True, string='State Of Property',
                             help="Refers about the property's current state.")
    active=fields.Boolean(string='Active', default=True)
    address_id = fields.Text(string='Property Address')
    street_address = fields.Char(string='Street Address')
    city = fields.Char(string='City')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    zip_code = fields.Char(string='Zip Code')
    state_id = fields.Many2one('res.country.state', string='State',
                               domain="[('country_id', '=', country_id)]")
    country_id = fields.Many2one('res.country', string='Country')
    facilities_ids = fields.Many2many('facilities.facilities', string='Facilities')
    rental_ids=fields.One2many('rent.lease.record','rent_id','Rental')
    @api.model_create_multi
    def create(self, vals):
        """Overrides the default create method"""
        for rec in vals:
            code = self.env['ir.sequence'].next_by_code('properties.management')
            rec['name'] = code
            return super(PropertiesManagement, self).create(vals)


    def action_rental_lease(self):
        """smart button for rental/lease records"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "rental.lease.management",
            "name": _("Rented/Leased property"),
            "views": [[False, "list"], [False, "form"]],
            "domain": [('property_id', '=', self.name)],
        }

    def action_open_reporting_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Property Report',
            'res_model': 'property.report',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_ids': self.ids},
        }