# -*- coding: utf-8 -*-

from email.policy import default
from operator import index

from dateutil.relativedelta import relativedelta
from reportlab.lib.validators import inherit

from odoo import fields, models,api
from odoo.orm.decorators import ondelete, readonly


class rent_lease_record(models.Model):
    """ rent and lease record """
    _name = 'rent.lease.record'
    _description = 'Rent Lease Record'
    _inherit=['mail.thread', 'mail.activity.mixin']

    property_id = fields.Many2one('properties.management', string="Property Id",ondelete='cascade')
    rent_id = fields.Many2one('rental.lease.management', string="Rent Id")
    tenant_id=fields.Many2one(related='property_id.tenantss_id',string="Tenant Id",store=True)
    property_name = fields.Char(related='property_id.property_name', string="Property Name")
    state=fields.Selection(related='rent_id.state', string="State")
    state_type = fields.Selection([('Rent', 'Rent'), ('Lease', 'Lease')])
    days=fields.Integer(string="Days",compute='_compute_rental_lease_days')
    rental_amount= fields.Float(related='property_id.rent_amount', string="Rental Amount",compute='Update_rental_amount',readonly=False)
    lease_amount= fields.Float(related='property_id.lease_amount', string="Lease Amount",compute='Update_lease_amount',readonly=False)
    effective_amount=fields.Float(compute='_compute_effective_amount',string="Effective Amount")
    effective_days=fields.Integer(string="Effective Days",compute='_compute_effective_days')
    from_date= fields.Date(string="From date")
    to_date= fields.Date(string="to Date")
    total_amount=fields.Float(string="Total Amount")

    @api.depends('from_date', 'to_date')
    def _compute_rental_lease_days(self):
        print(self.tenant_id)
        """Rent days computation and total amount"""
        for rec in self:
            if rec.state_type == 'Rent':
                print(rec.rent_id)
                rec.days = abs(relativedelta(rec.to_date, rec.from_date).days)
                rec.total_amount = rec.days * rec.rental_amount
            elif rec.state_type == 'Lease':
                rec.days = abs(relativedelta(rec.to_date, rec.from_date).days)
                rec.total_amount = rec.days * rec.lease_amount
            else:
                rec.days = 0
                rec.total_amount = 0

    @api.onchange(rental_amount)
    def _Update_rental_amount(self):
        """function that is responsible for the updation of rental amount, on updation from the rent/lease record"""
        property_id = fields.Many2one('properties.management', string="Property Id")
        property_id.rent_amount=self.rental_amount
        return True


    @api.onchange(lease_amount)
    def _Update_lease_amount(self):
        """function that is responsible for the updation of lease amount, on updation from the rent/lease record"""
        property_id = fields.Many2one('properties.management', string="Property Id")
        property_id.lease_amount=self.lease_amount
        return True


    @api.depends('rental_amount', 'lease_amount')
    def _compute_effective_amount(self):
        """computes the effective amount of the rental and lease"""
        for rec in self:
            if rec.state_type == 'Rent':
                rec.effective_amount=rec.rental_amount
            elif rec.state_type == 'Lease':
                rec.effective_amount=rec.lease_amount
            else:
                rec.effective_amount=0


    @api.depends('from_date', 'to_date')
    def _compute_effective_days(self):
        """computes the effective days of the rental and lease"""
        for rec in self:
            if rec.state_type == 'Rent':
                rec.effective_days = rec.days
            else:
                rec.effective_days = 0

