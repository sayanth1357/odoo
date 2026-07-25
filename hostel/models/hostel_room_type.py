# -*- coding: utf-8 -*-
from odoo import fields,models

class HostelRoomType(models.Model):
    """class used to manage room types related to hostel rooms"""
    _name = "hostel.room.type"
    _description = "Hostel Room Types"

    name = fields.Char(string="Name", required=True,
                       help='name of the room type')
    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique'
    )
