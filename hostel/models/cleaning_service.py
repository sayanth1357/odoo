# -*- coding: utf-8 -*-
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api


class CleaningService(models.Model):
    """Manage cleaning service in hostel rooms"""
    _name = "cleaning.service"
    _rec_name = "room_id"
    _description = "Cleaning Service"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    room_id = fields.Many2one("hostel.room", 'Room No.',
                              help="Room No. where service is requested.",
                              copy="False", required=True, check_company=True)
    cleaning_staff = fields.Many2one('res.users', 'Cleaning staff',
                                     tracking=True, check_company=True)
    start_time = fields.Datetime("Start Time")
    state = fields.Selection(
        selection=[('new', 'New'), ('assigned', 'Assigned'), ('done', 'Done')],
        default='new', string='state', help='state of the cleaning request.',
        tracking=True)
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        """check for assignees while creating request ,assigned by the warden"""
        for vals in vals_list:
            if (vals.get('cleaning_staff') != False) and (
                    vals.get('state') == 'new'):
                vals['state'] = 'assigned'
                vals['start_time'] = datetime.now()
        return super().create(vals_list)

    def write(self, vals):
        """check for assignees while writing over a request ,assigned by the warden"""
        if vals.get('cleaning_staff') != False and vals.get('state') == 'new':
            vals['state'] = 'assigned'
            vals['start_time'] = datetime.now()
        return super().write(vals)

    def action_assign_staff(self):
        """Method to assign cleaning staff """
        self.sudo().cleaning_staff = self.env.user
        self.sudo().write({'state': 'assigned'})
        self.sudo().write({'start_time': datetime.now()})
        self.sudo().room_id.is_cleaning = True
        return True

    def action_service_done(self):
        """Method set the state of cleaning as done """
        self.sudo().write({'state': 'done'})
        self.room_id.sudo().is_cleaning = False
        return True

    def _cron_create_daily_request(self):
        """create daily cleaning request as scheduled action via ir.cron"""
        today = datetime.now()
        student_leave_records = self.env['leave.request'].search(
            ['&', '&', ('leave_date', '<=', today),
             ('arrival_date', '>', today),
             ('status', 'in', ['approved'])]).mapped('student_id.id')
        students_count = {}
        rooms = self.env['hostel.room'].search(
            ['&', ('student_ids', '!=', False), '|',
             ('last_cleaning', '<=', datetime.now() + relativedelta(days=-7)),
             ('last_cleaning', '=', False)])
        for room in rooms:
            students_count[room] = len(room.student_ids)
            for student in room.student_ids:
                if student.id in student_leave_records:
                    students_count[room] -= 1
        for room in students_count:
            if students_count[room] == 0 :
                self.env['cleaning.service'].create({
                    'room_id': room.id,
                })
                room.last_cleaning = datetime.now()
        return True
