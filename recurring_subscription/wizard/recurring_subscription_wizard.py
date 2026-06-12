# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields
import io
import json
from odoo.tools import date_utils, json_default
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class RecurringSubscriptionWizard(models.TransientModel):
   _name = 'recurring.subscription.wizard'
   _description = 'Wizard for recurring subscription report'

   subscription_id=fields.Many2one('recurring.subscription',string='Subscription')
   report=fields.Selection(selection=[('daily','Daily'),
                                      ('weekly','Weekly'),
                                      ('monthly','Monthly'),
                                      ('yearly','Yearly')],string='report')
   partner_id=fields.Many2one('res.partner',string='partner')
   # today=fields.Date.today()


   
   def action_report_subscription(self):



        # query="""select rs.name, rp.name as customer ,rs.total_credit_applied  ,pt.name as product , rs.recurring_amount ,rs.status
        #         from recurring_subscription  rs inner join res_partner  rp on rp.id = rs.customer_id inner join
		# 		product_template  pt on pt.id=rs.product_id
		# 		where 1=1
		# 		"""
        # print(query)
        query = """select rs.name, rp.name as customer ,rs.total_credit_applied ,rs.terms_and_condition as term ,pt.name->>'en_US' as product , rs.recurring_amount ,rs.status
                         from recurring_subscription  rs inner join res_partner  rp on rp.id = rs.customer_id inner join
        		 		product_template  pt on pt.id=rs.product_id
        		 		where 1=1
        		 		
        		 		"""

        if self.subscription_id:
            query+="""and rs.id ='%s' """ % self.subscription_id.id

        today = fields.Date.today()
        if self.report=='daily':
            query+="""and  rs.date >= '%s' """%today
        elif self.report=='weekly':
            query+="""and rs.date >= '%s' """%(today-timedelta(days=7))
        elif self.report=='monthly':
            query+="""and rs.date >= '%s' """%(today-timedelta(days=30))
        elif self.report=='yearly':
            query+="""and rs.date >= '%s' """%(today-timedelta(days=365))
        if self.partner_id:
            query+="""and rp.id='%s' """%self.partner_id.id


        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        sub = []
        for record in report:

            if record['status'] not in sub:
                sub.append(record['status'])

        print(3499, sub)

        name1=[]
        for record in report:
            if record['name'] not in name1:
                name1.append(record['name'])
        print(4567,name1)

        terms=False
        if self.subscription_id:
            terms=self.subscription_id.terms_and_condition
            print(terms)

        data = {'report': report,'length':len(sub),'subs':sub,'name_len':len(name1),'subname':name1,'term':terms, }

        print("5432",data)

        return self.env.ref('recurring_subscription.action_report_recurring_subscription_form').report_action(None,data=data)



   def action_print_xlsx(self):
       """
       Returns report action for the XLSX Attendance report
       Raises: ValidationError: if From Date > To Date
       Raises: ValidationError: if there is no attendance records
       Returns:
           dict:  the XLSX report action
       """


       data = {
           'subscription_id': self.subscription_id.id,
           'report': self.report,
       }
       return {
               'type': 'ir.actions.report',
               'data': {'model': 'recurring.subscription.wizard',
                        'options': json.dumps(data, default=json_default),
                        'output_format': 'xlsx',
                        'report_name': 'Attendance Report',
                        },
               'report_type': 'xlsx',
           }


   def get_xlsx_report(self, data, response):
       """
       Print the XLSX report
       Returns: None
       """

       query = """select rs.name, rp.name as customer ,rs.total_credit_applied ,rs.terms_and_condition as term ,
                                pt.name->>'en_US' as product , rs.recurring_amount ,rs.status
                                from recurring_subscription  rs inner join res_partner  rp on rp.id = rs.customer_id inner join
                                product_template  pt on pt.id=rs.product_id
                                where 1=1
               		 		"""
       if data.get('subscription_id'):
           query += """and rs.id ='%s' """ % data.get('subscription_id')

       today = fields.Date.today()
       if data.get('report') == 'daily':
           query += """and  rs.date >= '%s' """ % today
       elif data.get('report') == 'weekly':
           query += """and rs.date >= '%s' """ % (today - timedelta(days=7))
       elif data.get('report') == 'monthly':
           query += """and rs.date >= '%s' """ % (today - timedelta(days=30))
       elif data.get('report') == 'yearly':
           query += """and rs.date >= '%s' """ % (today - timedelta(days=365))
       # if data.get('report'):
       #     query += """and rp.id='%s' """ % self.partner_id.id

       self.env.cr.execute(query)
       docs = self.env.cr.dictfetchall()
       print(data)

       output = io.BytesIO()
       workbook = xlsxwriter.Workbook(output, {'in_memory': True})
       sheet = workbook.add_worksheet()
       head = workbook.add_format(
           { 'bold': True, 'border':1,'align':'centre'})
       border = workbook.add_format({'border': 1})
       sheet.set_column(3, 1, 15)
       sheet.set_column(4, 1, 25)
       sheet.set_column(6, 1, 25)

       sheet.merge_range('A2:G3', 'Subscription Report', head)
       sheet.write('A5','SL.No',head)
       sheet.write('B5', 'Name',head)
       sheet.write('C5', 'Customer',head)
       sheet.write('D5', 'Product',head)
       sheet.write('E5', 'Amount ',head)
       sheet.write('F5', 'Total credit applied ',head)
       sheet.write('G5', 'Status ',head)

       row=5
       sl_no=1
       for record in docs:
           sheet.write(row,0,sl_no,border)
           sheet.write(row,1,record['name'],border)
           sheet.write(row,2,record['customer'],border)
           sheet.write(row,3,record['product'],border)
           sheet.write(row,4,record['recurring_amount'],border)
           sheet.write(row,5,record['total_credit_applied'],border)
           sheet.write(row,6,record['status'],border)
           row+=1
           sl_no+=1
       workbook.close()
       output.seek(0)
       response.stream.write(output.read())
       output.close()