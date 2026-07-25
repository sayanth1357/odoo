# -*- coding: utf-8 -*-
from datetime import date, datetime

from pip._internal.utils._jaraco_text import _

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class StudentStudent(models.Model):
    """manage student data related to the hostel"""
    _name = "student.student"
    _description = "Student"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    name = fields.Char(string="Name", required=True, help='Name of the student',
                       copy=False)
    student_id = fields.Char('Student ID', help='Student ID number',
                             default=lambda self: _("New"), readonly=True,
                             copy=False)
    street = fields.Char('Street', help='Street address')
    street2 = fields.Char('Street2', help='Secondary street address')
    city = fields.Char('City', help='City address')
    country_id = fields.Many2one('res.country', 'Country',
                                 help='country name')
    state_id = fields.Many2one('res.country.state', 'State',
                               domain="[('country_id','=',country_id)]",
                               help='state name')
    zip = fields.Char('ZIP', help='PIN code')
    dob = fields.Date('DOB', help='date of birth', copy=False, required=True)
    room_id = fields.Many2one('hostel.room', 'Room',
                              tracking=True, help='Room number ', readonly=True,
                              check_company=True)
    email = fields.Char('Email', tracking=True, help='email id',
                        copy=False, required=True)
    image = fields.Image('Image', copy=False)
    receive_email = fields.Boolean('Receive Email')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    age = fields.Integer('Age', compute="_compute_age", copy=False)
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 copy=False, check_company=True)
    invoice_ids = fields.One2many('account.move', 'student_id',
                                  check_company=True)
    invoice_count = fields.Integer("count", compute="_compute_invoice_count",
                                   store=True)
    active = fields.Boolean(string="Active", default=True)
    monthly_payment = fields.Float("Monthly Payment",
                                   compute="_compute_monthly_payment",
                                   readonly=True,store=True)
    invoice_status = fields.Selection(
        selection=[('pending', 'Pending'), ('done', 'Done')],
        compute='_compute_invoice_status', readonly=True, store=True)
    user_id = fields.Many2one('res.users', string="User ID",
                              help="User ID related to the student.",
                              readonly=True, check_company=True)

    @api.model_create_multi
    def create(self, vals_list):
        """Method overwrites default create method to assign student
        id sequence to our model automatically at creation as well as create
        a partner record for the student"""
        for vals in vals_list:
            if vals.get("student_id", "New") == "New":
                vals["student_id"] = (
                        self.env['ir.sequence'].next_by_code('student.student')
                        or "New")
        for vals in vals_list:
            record = self.env['res.partner'].create({
                'image_1920': vals.get('image'),
                'name': vals.get('name'),
                'email': vals.get('email'),
                'company_id': vals.get('company_id'),
                'street': vals.get('street'),
                'street2': vals.get('street2'),
                'city': vals.get('city'),
                'zip': vals.get('zip'),
                'state_id': vals.get('state_id'),
                'country_id': vals.get('country_id'),
            })
        vals['partner_id'] = record.id

        return super().create(vals_list)

    @api.depends('dob')
    def _compute_age(self):
        """Method calculates age of student based on date of birth provided"""
        for record in self:
            if record.dob and record.dob <= date.today():
                years = relativedelta(date.today(), record.dob).years
                record.age = years
            else:
                record.age = 0

    @api.depends("invoice_ids")
    def _compute_invoice_count(self):
        """compute the number of invoices in existence for current student"""
        for record in self:
            record.invoice_count = len(list(record.invoice_ids))

    @api.depends("invoice_ids")
    def _compute_monthly_payment(self):
        """compute payment amount for current month for the student"""
        for record in self:
            record.monthly_payment = 0
            for invoice in record.invoice_ids:
                if invoice.payment_state != 'paid' and invoice.date.month == date.today().month:
                    record.monthly_payment += invoice.amount_residual

    @api.depends("invoice_ids")
    def _compute_invoice_status(self):
        """compute overall status of invoices for current student"""
        for record in self:
            if record.invoice_ids:
                for invoice in record.invoice_ids:
                    record.invoice_status = 'done'
                    if invoice.payment_state != 'paid':
                        record.invoice_status = 'pending'
                        break
            else:
                record.invoice_status = 'done'

    def student_action_alot_room(self):
        """Allocate room for students """
        rooms = self.env['hostel.room'].search([])
        is_full_or_no_beds = 0
        for record in rooms:
            slots_assigned = len(list(record.student_ids))
            if (record.no_of_beds != 0 and
                    (record.no_of_beds - slots_assigned) != 0):
                self.room_id = record
                if not self.active:
                    self.active = True
                is_full_or_no_beds = 1
                break
        if is_full_or_no_beds == 0:
            raise ValidationError("No rooms available!")
        return True

    def student_action_vacate_room(self):
        """Method to vacate students from room"""
        temp = self.room_id
        self.room_id = False
        self.active = False
        for record in self:
            if (temp.no_of_beds - len(
                    list(temp.student_ids))) == temp.no_of_beds:
                record.env['cleaning.service'].create({
                    'room_id': temp.id,
                })
                record.room_id.last_cleaning = datetime.now()
        return True

    def action_view_invoice(self):
        """View student invoices"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Student Invoices',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'domain': [('student_id', 'in', self.id)],
        }

    def action_create_user(self):
        """ Create user upon student creation via automated action """

        user = self.env['res.users'].search(
            ['&', ('login', '=', self.email), ('student_id', '=', self.id)])

        if user:
            self.user_id = user.id
        else:
            self.user_id = self.env['res.users'].create({
                'image_1920': self.image,
                'name': self.name,
                'student_id': self.id,
                'email': self.email,
                'login': self.email,
                'company_id': self.company_id.id,
                'street': self.street,
                'street2': self.street2,
                'city': self.city,
                'zip': self.zip,
                'state_id': self.state_id,
                'country_id': self.country_id,
            })

        return True
