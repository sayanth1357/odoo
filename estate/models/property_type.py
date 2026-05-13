from odoo import models,fields
class RealEstateProperty(models.Model):
    _name="estate.property.type"
    _description = "Real Estate property type"
    name= fields.Char(required=True)
    property_type_id=fields.One2many('estate.property','property_type_id')