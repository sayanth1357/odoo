from odoo import fields,models

class EventManagement(models.Model):
    _name='event.management'
    _description = 'Event Management'
    name=fields.Char()
