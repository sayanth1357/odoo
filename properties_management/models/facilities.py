# -*- coding: utf-8 -*-
from odoo import fields,models

class Facilities(models.Model):
    """ Facilities """
    _name = 'facilities.facilities'
    _description = 'Facilities'
    _rec_name = 'facility_name'
    facility_name=fields.Char(string="Facility Name")
    facility_ids=fields.Many2many('properties.management',string='Property Id',)
    property_id=fields.Many2one('properties.management',string='Property Id')
    property_name=fields.Char(related='facility_ids.property_name',string='Property Name',)