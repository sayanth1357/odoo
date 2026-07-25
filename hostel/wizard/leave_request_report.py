# -*- coding:utf-8 -*-
import io
import json
from datetime import datetime

import xlsxwriter

from odoo import fields, models
from odoo.tools import json_default


class LeaveRequestReport(models.TransientModel):
    """ wizard to print the leave requests PDF report"""
    _name = "leave.request.report"
    _description = "Leave Request Report Wizard"

    student_ids = fields.Many2many('student.student', string="Student",
                                   help="Student names")
    room_ids = fields.Many2many('hostel.room', string="Room",
                                help="Room filter for  the report")
    start_date = fields.Date('Start',
                             help="starting leave date of leave record")
    arrival_date = fields.Date('Arrival', help="Arrival date of leave record")

    def _set_filename(self):
        """method that return and sets the file name for the printed PDF report"""
        return datetime.now().strftime("%Y/%m/%d")

    def action_print_pdf(self):
        """method to print leave requests PDF report."""
        return self.env.ref('hostel.action_report_leave_request').report_action(
            self.ids, data={})

    def action_print_xlsx(self):
        """method to print leave requests XLSX report."""

        params = []
        filter_data = {}
        query = """SELECT st.name AS student_id,hr.room_no AS room_id , 
                                   lr.leave_date AS leave_date, lr.arrival_date AS arrival_date,
                                   (lr.arrival_date::date - lr.leave_date::date) AS duration 
                                   FROM leave_request lr JOIN student_student st ON 
                                   lr.student_id = st.id JOIN hostel_room hr ON st.room_id = hr.id 
                                   WHERE lr.status ='approved'"""
        if self.room_ids:
            query += """ AND hr.id IN %s"""
            params.append(tuple(self.room_ids.ids))
            filter_data['room_ids'] = self.room_ids.mapped('room_no')
            if self.student_ids:
                query += """ AND lr.student_id IN %s"""
                params.append(tuple(self.student_ids.ids))
                filter_data['student_ids'] = self.student_ids.mapped(
                    'name')
        if self.start_date:
            filter_data['start_date'] = self.start_date
            if self.arrival_date:
                query += """ AND lr.leave_date >= %s AND lr.arrival_date <= %s"""
                params.append(self.start_date.strftime("%Y-%m-%d"))
                params.append(self.arrival_date.strftime("%Y-%m-%d"))
                filter_data['arrival_date'] = self.arrival_date
            else:
                query += """ AND lr.leave_date >= %s AND lr.arrival_date <= %s"""
                params.append(self.start_date.strftime("%Y-%m-%d"))
                params.append(datetime.now().strftime("%Y-%m-%d"))
                filter_data['arrival_date'] = datetime.now().strftime(
                    "%Y-%m-%d")

        query += """ AND st.company_id in %s"""
        params.append(tuple(self.env.companies.ids))
        self.env.cr.execute(query, params)
        self.env.cr.execute(query, params)
        report = self.env.cr.dictfetchall()
        if not report:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "message": "No records matched.",
                    "type": "warning"
                }
            }

        data = {'report': report} | {'filter_data': filter_data}
        report_name = "Leave_Request_Report_" + datetime.now().strftime(
            "%Y_%m_%d")
        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'leave.request.report',
                'options': json.dumps(data, default=json_default),
                'output_format': 'xlsx',
                'report_name': report_name
            },
            'report_type': 'xlsx'
        }

    def get_xlsx_report(self, data, response):
        """ get and write the data to EXCEL report."""

        output_buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(output_buffer, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        worksheet.merge_range('D3:I4', 'LEAVE REQUEST', head)
        worksheet.merge_range('D5:I6', 'REPORT', head)
        column_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'white',
            'bg_color': '#3a6491',
            'font_size': 13,
        })
        content_format = workbook.add_format(
            {
                "border": 2,
                "border_color": '#3a6491',
                "align": "center",
                "valign": "vcenter",
            }
        )
        filter_data_format = workbook.add_format(
            {
                'bold': 1,
                "align": "center",

            }
        )
        if data['filter_data']:
            if data['filter_data'].get('room_ids'):
                filter_string = ' '
                for room in data['filter_data'].get('room_ids'):
                    filter_string += room + (', '
                                             '')
                worksheet.write(7, 3, 'ROOM', filter_data_format)
                worksheet.merge_range('E8:I8', filter_string)
            if data['filter_data'].get('room_ids'):
                filter_string = ' '
                for student in data['filter_data'].get('student_ids'):
                    filter_string += student + ', '
                worksheet.write(8, 3, 'STUDENT', filter_data_format)
                worksheet.merge_range('E9:I9', filter_string)

            if data['filter_data'].get('start_date'):
                worksheet.write(9, 3, 'PERIOD', filter_data_format)
                filter_string = ' ' + str(
                    data['filter_data'].get('start_date')) + ' : ' + str(
                    data['filter_data'].get('arrival_date'))
                worksheet.merge_range('E10:I10', filter_string)
        worksheet.write('D11', 'SL NO.', column_format)
        worksheet.write('E11', 'STUDENT', column_format)
        worksheet.write('F11', 'ROOM', column_format)
        worksheet.write('G11', 'START DATE', column_format)
        worksheet.write('H11', 'ARRIVAL DATE', column_format)
        worksheet.write('I11', 'DURATION', column_format)
        for i, record in enumerate(data['report'], start=11):
            worksheet.set_row(i, 20)
            worksheet.write(i, 3, i - 10, content_format)
            worksheet.write(i, 4, record.get('student_id'), content_format)
            worksheet.write(i, 5, record.get('room_id'), content_format)
            worksheet.write(i, 6, record.get('leave_date'), content_format)
            worksheet.write(i, 7, record.get('arrival_date'), content_format)
            worksheet.write(i, 8, record.get('duration'), content_format)
        worksheet.set_column(3, 8, 20)
        workbook.close()
        output_buffer.seek(0)
        response.stream.write(output_buffer.read())
        output_buffer.close()
        return None
