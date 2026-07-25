# -*- coding: utf-8 -*-
from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import fields,models,api,_
from odoo.exceptions import ValidationError


class Student(models.Model):
    """manage student data related to the hostel"""
    _name = "student"
    _description = "Student"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string="Name", required=True, help='Name of the student')
    student_id = fields.Char('Student ID', help='Student ID number',
                             default= lambda self:_("New"))
    # address = fields.Char('Address',help='')
    street = fields.Char('Street',help='Street address')
    street2 = fields.Char('Street2', help='Secondary street address')
    city = fields.Char('City', help='City address')
    country_id = fields.Many2one('res.country','Country',
                                 help='country name')
    state_id = fields.Many2one('res.country.state','State',
                               domain="[('country_id','=',country_id)]",
                               help='state name')
    zip = fields.Char('ZIP', help='PIN code')
    dob = fields.Date('DOB', help='date of birth')



    room_id = fields.Many2one('hostel.room','Room' ,
                              tracking=True, help='Room number ',readonly=True,
                              default='Not assigned')



    email = fields.Char('Email',tracking=True, help='email id')
    image = fields.Image('Image')
    receive_email = fields.Boolean('Receive Email')
    company_id = fields.Many2one('res.company', 'Company')
    age = fields.Integer('Age',compute="_compute_age")

    @api.model_create_multi
    def create(self, vals_list):
        """Method overwrites default create method to assign student
        id sequence to our model automatically at creation"""
        for vals in vals_list:
            if vals.get("student_id","New") == "New":
                vals["student_id"] = (self.env['ir.sequence'].next_by_code('student') or
                                      "New")
        return super().create(vals_list)

    @api.depends('dob')
    def _compute_age(self):
        """Method calculates age of student based on date of birth provided"""
        for record in self:
            if record.dob and record.dob <= date.today():
                years = relativedelta(date.today(), record.dob).years
                record.age = years

            else:
                print("no")
                record.age = 0

    def student_action_alot_room(self):
        """Allocate room for students """
        print('allocate')
        rooms = self.env['hostel.room'].search([])
        print(rooms)
        flag=0
        for record in rooms:
            if record.no_of_beds != 0 and record.no_of_beds - record.slots_filled !=0 :
                print(record.no_of_beds - record.slots_filled)
                print("hiii")
                print(record.slots_filled)
                self.room_id = record
                record.slots_filled +=1
                flag=1
                break
        if flag == 0:
            print("jjjj")
            raise ValidationError("No rooms available!")
        return True