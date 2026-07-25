# -*- coding: utf-8 -*-
import io
import json
from datetime import datetime

import xlsxwriter

from odoo import fields, models
from odoo.tools import json_default


class StudentStudentReport(models.TransientModel):
    """Wizard to print the students record as PDF report"""
    _name = "student.student.report"
    _description = "Student Report Wizard"

    student_ids = fields.Many2many('student.student', string="Student",
                                   help="student to be included in the report")
    room_ids = fields.Many2many('hostel.room', string="Room",
                                help="rooms to be included in the report")
    from_date = fields.Datetime('From', help="Date period start")
    to_date = fields.Datetime('To', help="Date period end")

    def _set_filename(self):
        """method that return and sets the file name for the printed PDF report"""
        return datetime.now().strftime("%Y/%m/%d")

    def action_print_pdf(self):
        """print PDF report via call to the report action"""

        return self.env.ref('hostel.action_report_students1').report_action(
            self.ids,
            data={})

    def action_print_xlsx(self):
        """print xlsx report, call the controller via returning the action"""

        filter_data = {}
        params = []
        query = """SELECT st.student_id AS student_id,st.name AS name,
                                           st.monthly_payment AS monthly_payment,hr.room_no AS room_id,
                                   st.invoice_status AS invoice_status FROM 
                                   student_student  st JOIN hostel_room hr ON st.room_id = hr.id"""
        if self.room_ids:
            query += """ WHERE hr.id IN %s """
            params.append(tuple(self.room_ids.ids))
            filter_data['room_ids'] = self.room_ids.mapped('room_no')
            if self.student_ids:
                query += """ AND st.id IN %s """
                params.append(tuple(self.student_ids.ids))
                filter_data['student_ids'] = self.student_ids.mapped(
                    'name')
        if self.from_date:
            if self.student_ids or self.room_ids:
                query += """ AND"""
            else:
                query += """ WHERE"""
            if self.to_date:
                query += """ st.create_date BETWEEN %s AND %s"""
                params.append(
                    (self.from_date).strftime("%Y-%m-%d %H:%M:%S"))
                params.append(
                    (self.to_date).strftime("%Y-%m-%d %H:%M:%S"))
                filter_data['from_date'] = self.from_date.strftime(
                    "%Y-%m-%d")
                filter_data['to_date'] = self.to_date.strftime(
                    "%Y-%m-%d")
            else:
                query += """ st.create_date BETWEEN %s AND %s"""
                params.append(
                    (self.from_date).strftime("%Y-%m-%d %H:%M:%S"))
                params.append((datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
                filter_data['from_date'] = self.from_date.strftime(
                    "%Y-%m-%d")
                filter_data['to_date'] = datetime.now().strftime("%Y-%m-%d")
        query += """ AND st.company_id in %s"""
        params.append(tuple(self.env.companies.ids))
        self.env.cr.execute(query, params)
        report = self.env.cr.dictfetchall()

        if not report:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "message": "No records matched.",
                    "type": "warning",
                },
            }

        data = {
            'report': report,
            'filter_data': filter_data,
        }
        report_name = 'Student_Report_' + datetime.now().strftime("%Y-%m-%d")
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'student.student.report',
                     'options': json.dumps(data, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': report_name,
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """ write the data in the EXCEL report"""

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        sheet.merge_range('C2:G3', 'STUDENT REPORT', head)
        format_column_head = workbook.add_format(
            {
                "bold": 1,
                "border": 2,
                "border_color": '#3a6491',
                "align": "center",
                "valign": "vcenter",
                'font_color': 'white',
                'bg_color': '#3a6491',
            }
        )
        format_content = workbook.add_format(
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
        if data['filter_data'] != False:
            if data['filter_data'].get('room_ids'):
                sheet.write(4, 2, 'ROOM', filter_data_format)
                filter_string = ""
                for i, room in data['filter_data'].get('room_ids'):
                    filter_string = filter_string + str(room) + ', '
                sheet.merge_range('D5:G5', filter_string)
            if data['filter_data'].get('student_ids'):
                sheet.write(5, 2, 'STUDENT', filter_data_format)
                filter_string = ""
                for room in data['filter_data'].get('student_ids'):
                    filter_string = filter_string + str(room) + ', '
                sheet.merge_range('D6:G6', filter_string)
            if data['filter_data'].get('from_date'):
                sheet.write(6, 2, 'PERIOD', filter_data_format)
                filter_string = str(
                    data['filter_data'].get('from_date')) + ' : ' + str(
                    data['filter_data'].get('to_date'))
                sheet.merge_range('D7:G7', filter_string)

        sheet.write(8, 2, 'SL.NO', format_column_head)
        sheet.write(8, 3, 'NAME', format_column_head)
        sheet.write(8, 4, 'PENDING AMOUNT', format_column_head)
        sheet.write(8, 5, 'ROOM', format_column_head)
        sheet.write(8, 6, 'INVOICE STATUS', format_column_head)
        for i, name in enumerate(data['report'],
                                 start=9):
            sheet.set_row(i, 20)
            sheet.write(i, 2, -8 + i, format_content)
            sheet.write(i, 3, name.get('name'), format_content)
            sheet.write(i, 4, name.get('monthly_payment'), format_content)
            sheet.write(i, 5, name.get('room_id'), format_content)
            sheet.write(i, 6, name.get('invoice_status'), format_content)
        sheet.set_column(2, 6, 20)
        sheet.set_row(8, 22)
        sheet.autofit()
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return None
