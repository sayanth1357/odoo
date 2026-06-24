# -*- coding: utf-8 -*
import io
import json
from urllib import response

import xlsxwriter

from odoo import models,fields,_
from odoo.exceptions import ValidationError
from odoo.tools import json_default


class PropertyReportXlsx(models.TransientModel):
    _name='property.report.xlsx'
    _description='Property Report XLSX'

    property_id=fields.Many2one('properties.management',string='Property')
    property_name=fields.Char(related='property_id.property_name',string='Property Name')
    Owner_id=fields.Many2one(related='property_id.owner_id',string='Owner')
    tenant_id=fields.Many2one('res.partner',string='Tenant')
    from_date=fields.Date(string='From Date')
    to_date=fields.Date(string='To Date')
    state_type = fields.Selection([('Rent', 'Rent'), ('Lease', 'Lease')])
    state = fields.Selection(
        [('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Invoiced', 'Invoiced'), ('Closed', 'Closed'),
         ('Returned', 'Returned'),
         ('Expired', 'Expired')], string="State")

    def action_print_xlsx(self):
        """function  responsible for general validation,passing of filter values and initiates the working of ir.report handlers"""
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError(_("Invalid Date !"))
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'property_id': self.property_id.id,
            'property_name': self.property_name,
            'Owner_id': self.Owner_id.id,
            'tenant_id': self.tenant_id.id,
            'state': self.state,
            'state_type': self.state_type,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'property.report.xlsx',
                     'options': json.dumps(data, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Property Report XLSX',
                     },
            'report_type': 'xlsx',}


    def get_xlsx_report(self, data, response):

        """The query is generated , workbook is instantiated and memory buffer instantiated and then send via http response to be printed as axlsx report"""

        query = """select pm.id as p_id, pm.property_name as p_name ,rs.name as o_id,rr.state_type as state_type,rp.name as t_id,rl.state as State,rr.total_amount as Total_Amount,rr.from_date,rr.to_date 
        from rent_lease_record as rr
        inner join rental_lease_management as rl on rl.id = rr.rent_id
        inner join properties_management as pm on pm.id = rr.property_id
        inner join res_partner as rs on rs.id=pm.owner_id
        inner join res_partner as rp on rp.id=rl.tenant_id
        where 1=1
        """
        if data['tenant_id']:
            query += """ AND rp.id = '%s' """ % (data['tenant_id'])
        if data['state']:
            query += """ AND rl.state = '%s' """ % (data['state'])
        if data['property_id']:
            query += """ AND pm.id = '%s' """ % (data['property_id'])
        if data['state_type']:
            query += """ AND rr.state_type = '%s' """ % (data['state_type'])
        if data['to_date']:
            query += """ AND rr.to_date <= '%s' """ % (data['to_date'])
        if data['from_date']:
            query += """ AND rr.from_date >= '%s' """ % (data['from_date'])


        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('docs')
        cell_format = workbook.add_format(
            {'font_size': '11px', 'align': 'center','bold': True,'bg_color':'#64a4f8','border':2})
        cell_data = workbook.add_format(
            {'font_size': '11px', 'align': 'left', 'border': 1})
        heading = workbook.add_format({'bold':True,'font_size':'20px','align':'center'})
        sheet.set_column('B:B',20)
        sheet.set_column('C:C',20)
        sheet.set_column('D:D',20)
        sheet.set_column('E:E',20)
        sheet.set_column('F:F',20)
        sheet.set_column('G:G',20)
        sheet.set_column('H:H',20)

        sheet.merge_range('D2:F3','PROPERTY REPORT',heading)
        sheet.write('B6', 'PROPERTY NAME', cell_format)
        sheet.write('C6', 'OWNER NAME', cell_format)
        sheet.write('D6', 'TENANT NAME', cell_format)
        sheet.write('E6', 'FROM DATE', cell_format)
        sheet.write('F6', 'TO DATE', cell_format)
        sheet.write('G6', 'STATE TYPE', cell_format)
        sheet.write('H6', 'STATE', cell_format)

        if report == []:
            raise ValidationError(_(
                "No Records Found !"
            ))
        else:
            row = 6
            for record in report:
                col = 1
                sheet.write(row, col, record['p_name'],cell_data)
                col = col + 1
                sheet.write(row, col, record['o_id'],cell_data)
                col = col + 1
                sheet.write(row, col, record['t_id'],cell_data)
                col = col + 1
                sheet.write(row, col, record['from_date'].strftime('%Y-%m-%d'),cell_data)
                col = col + 1
                sheet.write(row, col, record['to_date'].strftime('%Y-%m-%d'),cell_data)
                col = col + 1
                sheet.write(row, col, record['state_type'],cell_data)
                col = col + 1
                sheet.write(row, col, record['state'],cell_data)
                row = row + 1


        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
