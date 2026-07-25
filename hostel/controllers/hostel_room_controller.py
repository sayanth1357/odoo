# -*- coding:utf-8-*-

from odoo import http
from odoo.http import request


class HostelRoomController(http.Controller):
    """class to handle the snippet management for hostel rooms."""
    @http.route('/hostel_room/get_room_data', auth="public", type="jsonrpc", webiste=True)
    def get_room_data(self):
        """method to pass room data to template."""
        room_data = request.env['hostel.room'].search_read([],["room_no","room_type_id","total_rent","state","image"],limit=7)
        return {'room_data' : room_data}
    @http.route('/room/details/<int:room_id>', type="http", auth="user", website=True)
    def room_details(self,room_id):
        """Render room details """
        room= request.env['hostel.room'].browse(room_id)
        images = request.env['ir.attachment'].search([('res_model','=','hostel.room'),('res_id','=',room_id),('mimetype','in',['image/jpg','image/jpeg','image/png'])])
        return request.render('hostel.hostel_room_details',{'room':room,'images':images})