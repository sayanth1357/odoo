# -*- coding: utf-8 -*-
import json
import token

from odoo import http
from odoo.http import request, content_disposition
from odoo.tools import  html_escape


class StudentStudentXLSXReportController(http.Controller):
    """Student XLSX report controller """

    @http.route('/xlsx_reports', type='http', auth='user', csrf=False,methods=['POST'])
    def get_report_xlsx(self, model, options, output_format, report_name):
        """return"""
        session_unique_id = request.session.uid
        report_object = request.env[model].with_user(session_unique_id)
        options = json.loads(options)
        token = 'dummy-because-api-expects-one'
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition',
                         content_disposition(report_name + '.xlsx'))
                    ]
                )
                report_object.get_xlsx_report(options, response)
                response.set_cookie('fileToken', token)
                return response
        except Exception:
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
            }
            return request.make_response(html_escape(json.dumps(error)))
