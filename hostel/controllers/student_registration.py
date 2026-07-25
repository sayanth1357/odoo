# -*- coding:utf-8 -*-
import base64

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request


class StudentRegistrationController(http.Controller):
    """Controller to handle student registration form from website."""
    @http.route('/website/student/register/form',type="http",auth="user", website=True)
    def display_form(self,**kwargs):
        """Method to display -the registration form"""
        rooms = request.env['hostel.room'].sudo().search([('state','!=','full'),
                        ('no_of_beds','!=',0)])
        return request.render('hostel.student_registration_form', {'docs' : rooms})
    @http.route('/website/student/form/submit', type="http", auth="user", website=True, methods=['POST'], csrf=True)
    def submit_form(self, **post):
        """Controller method to submit the registration form and create student record."""
        image =post.get('image').read()
        base64_bytes = base64.b64encode(image)
        base64_string = base64_bytes.decode('utf-8')
        if request.env['student.student'].sudo().search([('name','=',post.get('name')),('email','=',post.get('email'))]):
            raise ValidationError("Student Already Exists!")
        request.env['student.student'].sudo().create({
            'name' : post.get('name'),
            'email' : post.get('email'),
            'dob' : post.get('dob'),
            'image' : base64_string,
            'room_id' : int(post.get('rooms'))if post.get('rooms') else False,
        })
        return request.render('website.contactus_thanks')
    @http.route("/rpc/room_data",type="jsonrpc",auth="user", website=True)
    def rpc_get_room_data(self,room_id):
        """RPC call to fetch room data from  room id"""
        room_data = request.env['hostel.room'].sudo().search([("id",'=',room_id)])
        facilities = room_data.mapped('facilities_ids.name')
        return {'room_type':room_data.room_type_id.name,'facilities':facilities,'rent' : room_data.rent,'total_rent' : room_data.total_rent}
    @http.route("/rpc/autofill_info", type="jsonrpc", auth="user", website=True)
    def rpc_autofill_info(self,uid):
        """autofill username and email in student registration form."""
        user = request.env['res.users'].browse(int(uid))
        return {"name":user.name,"email":user.email}

