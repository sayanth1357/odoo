# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsers(models.Model):
    """Inherits the ResUsers model and extends additional fields required"""
    _inherit = 'res.users'

    student_id = fields.Many2one('student.student', 'Student ID',
                                 help="Student ID related to the user if exists.",
                                 check_company=True)
