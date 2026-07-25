# -*- coding:utf-8 -*-
from datetime import datetime

from odoo import models, api
from odoo.exceptions import ValidationError


class ReportLeaveRequestReport_Leave_Request(models.AbstractModel):
    """abstract model to provide data for report"""
    _name = "report.hostel.report_leave_request"
    _description = "Leave Request Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        """Get values for the report from wizard"""
        print
        wizard_record = self.env['leave.request.report'].browse(docids)

        params = []
        filter_data = {}
        query = """SELECT st.name AS student_id,hr.room_no AS room_id , 
                           lr.leave_date AS leave_date, lr.arrival_date AS arrival_date,
                           (lr.arrival_date::date - lr.leave_date::date) AS duration 
                           FROM leave_request lr JOIN student_student st ON 
                           lr.student_id = st.id JOIN hostel_room hr ON st.room_id = hr.id 
                           WHERE lr.status ='approved'"""
        if wizard_record.room_ids:
            query += """ AND hr.id IN %s"""
            params.append(tuple(wizard_record.room_ids.ids))
            filter_data['room_ids'] = wizard_record.room_ids.mapped('room_no')
            if wizard_record.student_ids:
                query += """ AND lr.student_id IN %s"""
                params.append(tuple(wizard_record.student_ids.ids))
                filter_data['student_ids'] = wizard_record.student_ids.mapped(
                    'name')
        if wizard_record.start_date:
            filter_data['start_date'] = wizard_record.start_date
            if wizard_record.arrival_date:
                query += """ AND lr.leave_date >= %s AND lr.arrival_date <= %s"""
                params.append(wizard_record.start_date.strftime("%Y-%m-%d"))
                params.append(wizard_record.arrival_date.strftime("%Y-%m-%d"))
                filter_data['arrival_date'] = wizard_record.arrival_date
            else:
                query += """ AND lr.leave_date >= %s AND lr.arrival_date <= %s"""
                params.append(wizard_record.start_date.strftime("%Y-%m-%d"))
                params.append(datetime.now().strftime("%Y-%m-%d"))
                filter_data['arrival_date'] = datetime.now().strftime(
                    "%Y-%m-%d")

        query += """ AND st.company_id in %s"""
        params.append(tuple(wizard_record.env.companies.ids))
        wizard_record.env.cr.execute(query, params)
        wizard_record.env.cr.execute(query, params)
        report = wizard_record.env.cr.dictfetchall()
        if not report:
            raise ValidationError("No records matched.")
        print(1234567,report)
        docs = {'report': report} | {'filter_data': filter_data}

        return {
            'doc_ids': docids,
            'doc_model': 'leave.request',
            'docs': docs,
            'data': data
        }
