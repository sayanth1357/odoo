# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class LeaveRequest(models.Model):
    """handle leave request from students"""
    _name = "leave.request"
    _rec_name = "student_id"
    _description = "Leave request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    student_id = fields.Many2one('student.student', 'Student',
                                 help='Student name', required=True,
                                 ondelete="cascade", check_company=True)
    leave_date = fields.Date('Leave Date', help='Leave date', required=True,
                             copy=False)
    arrival_date = fields.Date('Arrival Date', help='Arrival date',
                               required=True, copy=False)
    status = fields.Selection(
        selection=[('new', 'New'), ('submitted', 'Submitted'),
                   ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='new', help='Leave request status', copy=False, tracking=True)

    @api.constrains("leave_date", "arrival_date")
    def _check_dates(self):
        """constraint for checking leave date if not less than arrival date"""
        if self.leave_date > self.arrival_date:
            raise ValidationError(
                "Leave date should not be greater than arrival date!")

    def action_approve_leave(self):
        """Method to approve the leave request."""
        for record in self:
            if record.status == 'submitted':
                record.write({'status': 'approved'})
        return True

    def action_submit_request(self):
        """Action to submit the leave request"""
        self.write({'status': 'submitted'})
        return True

    def action_reject_request(self):
        """Action to reject the leave request"""
        self.write({'status': 'rejected'})
        return True
