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
                                      ('yearly','Yearly'),
                                      ('custom','Custom')],string='report')
   from_date=fields.Date(string='From',required=True)
   to_date=fields.Date(string='To',required=True)


   def action_report_subscription(self):

        query = """select rs.name, rp.name as customer ,rs.total_credit_applied ,rs.terms_and_condition as term ,pt.name->>'en_US' as product , rs.recurring_amount ,rs.status
                         from recurring_subscription  rs inner join res_partner  rp on rp.id = rs.customer_id inner join
        		 		product_template  pt on pt.id=rs.product_id
        		 		where 1=1	
        		 		"""

        if self.subscription_id:
            query+="""and rs.id ='%s' """ % self.subscription_id.id


        if self.from_date:
            query += """ and rs.date >= '%s' and rs.date <= '%s'""" % (self.from_date,self.to_date)

        today = fields.Date.today()
        if self.report=='daily':
            query+="""and  rs.date >= '%s' """%today
        elif self.report=='weekly':
            query+="""and rs.date >= '%s' """%(today-timedelta(days=7))
        elif self.report=='monthly':
            query+="""and rs.date >= '%s' """%(today-timedelta(days=30))
        elif self.report=='yearly':
            query+="""and rs.date >= '%s' """%(today-timedelta(days=365))



        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)


        sub = []
        for record in report:
            if record['status'] not in sub:
                sub.append(record['status'])

        name1=[]
        for record in report:
            if record['name'] not in name1:
                name1.append(record['name'])

        terms=False
        if self.subscription_id:
            terms=self.subscription_id.terms_and_condition
            print(terms)

        data = {'report': report,'length':len(sub),'subs':sub,'name_len':len(name1),'subname':name1,'term':terms, }

        print("5432",data)

        return self.env.ref('recurring_subscription.action_report_recurring_subscription_form').report_action(None,data=data)



   def action_print_xlsx(self):
       """
       Returns report action for the XLSX Subscription report
       Returns:
           dict:  the XLSX report action
       """


       data = {
           'subscription_id': self.subscription_id.id,
           'report': self.report,
           'from_date':self.from_date,
           'to_date':self.to_date,
       }
       return {
               'type': 'ir.actions.report',
               'data': {'model': 'recurring.subscription.wizard',
                        'options': json.dumps(data, default=json_default),
                        'output_format': 'xlsx',
                        'report_name': 'Subscription Report',
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
       if data.get('from_date'):
           query += """ and rs.date >= '%s' and rs.date <= '%s'""" % (data.get('from_date'), data.get('to_date'))

       today = fields.Date.today()
       if data.get('report') == 'daily':
           query += """and  rs.date >= '%s' """ % today
       elif data.get('report') == 'weekly':
           query += """and rs.date >= '%s' """ % (today - timedelta(days=7))
       elif data.get('report') == 'monthly':
           query += """and rs.date >= '%s' """ % (today - timedelta(days=30))
       elif data.get('report') == 'yearly':
           query += """and rs.date >= '%s' """ % (today - timedelta(days=365))


       self.env.cr.execute(query)
       docs = self.env.cr.dictfetchall()
       print(data)

       output = io.BytesIO()
       workbook = xlsxwriter.Workbook(output, {'in_memory': True})
       sheet = workbook.add_worksheet()
       head = workbook.add_format(
           { 'bold': True, 'border':1,'align':'centre'})
       border = workbook.add_format({'border': 1})
       

       status_list=[]
       for rec in docs:
           if rec['status'] not in status_list:
               status_list.append(rec['status'])

       sub_list = []
       for rec in docs:
           if rec['name'] not in sub_list:
               sub_list.append(rec['name'])

       sheet.set_column(3, 1, 15)
       sheet.set_column(4, 1, 20)
       sheet.set_column(6, 1, 20)

       sheet.merge_range('A2:G3', 'Subscription Report', head)
       if len(sub_list)==1:
           sheet.merge_range('A4:B4','Name',head)
           sheet.write('C4',sub_list[0],border)

       if len(status_list) == 1:
           sheet.merge_range('A5:B5', 'Status', head)
           sheet.write('C5', status_list[0], border)

       row=6
       col=0
       sheet.write(row,col,'SL.No',head)
       col+=1
       if len(sub_list) != 1:
           sheet.write(row, col, 'Name', head)
           col += 1
       sheet.write(row,col, 'Customer',head)
       col+=1
       sheet.write(row,col, 'Product',head)
       col+=1
       sheet.write(row,col, 'Amount ',head)
       col+=1
       sheet.write(row,col, 'Total credit applied ',head)
       col+=1
       if len(status_list)!=1:
           sheet.write(row,col, 'Status ',head)
           col+=1

       row = 7
       sl_no = 1
       for record in docs:
           col=0
           sheet.write(row, col, sl_no, border)
           col += 1
           if len(sub_list)!=1:
               sheet.write(row, col, record['name'], border)
               col+=1
           sheet.write(row, col, record['customer'], border)
           col += 1
           sheet.write(row, col, record['product'], border)
           col += 1
           sheet.write(row, col, record['recurring_amount'], border)
           col += 1
           sheet.write(row, col, record['total_credit_applied'], border)
           col += 1
           if len(status_list)!=1:
                sheet.write(row, col, record['status'], border)

           row += 1
           sl_no += 1
       workbook.close()
       output.seek(0)
       response.stream.write(output.read())
       output.close()