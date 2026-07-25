# -*- coding:utf-8 -*-
from datetime import datetime

from odoo import models, api
from odoo.exceptions import ValidationError


class ReportStudentStudentReport_Student_Student(models.AbstractModel):
    """abstract model to provide data for report"""

    _name = "report.hostel.report_student_student"
    _description = "Student Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        """Get values for the report from wizard"""
        print(123456789)

        wizard_record = self.env['student.student.report'].browse(docids)
        filter_data = {}
        params = []
        query = """SELECT st.student_id AS student_id,st.name AS name,
                           st.monthly_payment AS monthly_payment,hr.room_no AS room_id,
                   st.invoice_status AS invoice_status FROM 
                   student_student  st JOIN hostel_room hr ON st.room_id = hr.id"""
        if wizard_record.room_ids:
            query += """ WHERE hr.id IN %s """
            params.append(tuple(wizard_record.room_ids.ids))
            filter_data['room_ids'] = wizard_record.room_ids.mapped('room_no')
            if wizard_record.student_ids:
                query += """ AND st.id IN %s """
                params.append(tuple(wizard_record.student_ids.ids))
                filter_data['student_ids'] = wizard_record.student_ids.mapped(
                    'name')
        if wizard_record.from_date:
            if wizard_record.student_ids or wizard_record.room_ids:
                query += """ AND"""
            else:
                query += """ WHERE"""
            if wizard_record.to_date:
                query += """ st.create_date BETWEEN %s AND %s"""
                params.append(
                    (wizard_record.from_date).strftime("%Y-%m-%d %H:%M:%S"))
                params.append(
                    (wizard_record.to_date).strftime("%Y-%m-%d %H:%M:%S"))
                filter_data['from_date'] = wizard_record.from_date.strftime(
                    "%Y-%m-%d")
                filter_data['to_date'] = wizard_record.to_date.strftime(
                    "%Y-%m-%d")
            else:
                query += """ st.create_date BETWEEN %s AND %s"""
                params.append(
                    (wizard_record.from_date).strftime("%Y-%m-%d %H:%M:%S"))
                params.append((datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
                filter_data['from_date'] = wizard_record.from_date.strftime(
                    "%Y-%m-%d")
                filter_data['to_date'] = datetime.now().strftime("%Y-%m-%d")
        query += """ AND st.company_id in %s"""
        params.append(tuple(wizard_record.env.companies.ids))
        wizard_record.env.cr.execute(query, params)
        report = wizard_record.env.cr.dictfetchall()
        print(report)
        if not report:
            raise ValidationError("No records matched.")

        is_unique_room = report[0].get('room_id')
        is_unique_name = report[0].get('name')
        for record in report:
            if is_unique_room != record.get('room_id'):
                is_unique_room = False
                break
        for record in report:
            if is_unique_name != record.get('name'):
                is_unique_name = False
                break
        filter_data['is_unique_room'] = is_unique_room
        filter_data['is_unique_name'] = is_unique_name

        docs = {'report': report} | {'filter_data': filter_data}

        return {
            'doc_ids': docids,
            'doc_model': 'student.student',
            'docs': docs,
            'data': data,
        }
