# -*- coding: utf-8 -*-
import io
import json
from odoo.tools import date_utils, json_default
from odoo import models, fields

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class RecurringSubscriptionCreditWizard(models.TransientModel):
   _name = 'recurring.subscription.credit.wizard'
   _description = 'Wizard for recurring subscription credit report'

   subscription_id=fields.Many2one('recurring.subscription',string='Subscription')
   state = fields.Selection(selection=[
       ('pending', 'Pending'),
       ('confirmed', 'Confirmed'),
       ('first approved', 'First approved'),
       ('fully approved', 'Fully approved'),
       ('rejected', 'Rejected')],string='state'
       )

   def action_credit_report(self):


        # query="""select rs.name as subscription ,rp.name as customer,rsc.credit_amount as amount_applied,
        #      (rs.recurring_amount-rsc.credit_amount) as pending_amount, rsc.state from recurring_subscription_credit
        #     rsc inner join recurring_subscription  rs on rsc.recurring_subscription_id=rs.id inner join res_partner  rp on
        #     rp.id=rs.customer_id """
        query="""select rs.name as subscription ,rp.name as customer,rsc.credit_amount as amount_applied,
             (rs.recurring_amount-(select sum(rsc2.credit_amount) from recurring_subscription_credit rsc2  where
            rsc2.recurring_subscription_id=rs.id and rsc2.id<=rsc.id)) as pending_amount, rsc.state from recurring_subscription_credit
            rsc inner join recurring_subscription  rs on rsc.recurring_subscription_id=rs.id inner join res_partner  rp on
            rp.id=rs.customer_id """

        if self.subscription_id:
            query+="""where rs.id ='%s' """ % self.subscription_id.id
        if self.state:
            query+="""where rsc.state='%s' """%self.state


        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)

        state1 = []
        for rec in report:
            if rec['state'] not in state1:
                state1.append(rec['state'])
        print(state1)



        data = {'report': report,'length':len(state1),'state':state1,}
        print(9876,report)
        print(8876,data)



        return self.env.ref('recurring_subscription.action_report_recurring_subscription_credit_form').report_action(None, data=data)

   def action_credit_xlsx(self):
       """
       Returns report action for the XLSX Attendance report
       Raises: ValidationError: if From Date > To Date
       Raises: ValidationError: if there is no attendance records
       Returns:
           dict:  the XLSX report action
       """

       data = {
           'subscription_id': self.subscription_id.id,
           'state': self.state,
       }
       return {
           'type': 'ir.actions.report',
           'data': {'model': 'recurring.subscription.credit.wizard',
                    'options': json.dumps(data, default=json_default),
                    'output_format': 'xlsx',
                    'report_name': 'Credit Report',
                    },
           'report_type': 'xlsx',
       }

   def get_xlsx_report(self, data, response):
       """
       Print the XLSX report
       Returns: None
       """

       query = """select rs.name as subscription ,rp.name as customer,rsc.credit_amount as amount_applied,
                   (rs.recurring_amount-(select sum(rsc2.credit_amount) from recurring_subscription_credit rsc2  where
                  rsc2.recurring_subscription_id=rs.id and rsc2.id<=rsc.id)) as pending_amount, rsc.state from recurring_subscription_credit
                  rsc inner join recurring_subscription  rs on rsc.recurring_subscription_id=rs.id inner join res_partner  rp on
                  rp.id=rs.customer_id  where 1=1"""

       if data.get('subscription_id'):
           query += """and rs.id ='%s' """ % data.get('subscription_id')
       if data.get('state'):
           query += """and rsc.state='%s' """ % data.get('state')

       self.env.cr.execute(query)
       docs = self.env.cr.dictfetchall()
       print(data)

       output = io.BytesIO()
       workbook = xlsxwriter.Workbook(output, {'in_memory': True})
       sheet = workbook.add_worksheet()
       head = workbook.add_format(
           {'bold': True, 'border': 1,'align':'center'})
       border = workbook.add_format({'border': 1})
       sub1 = []
       for rec in docs:
           if rec['subscription'] not in sub1:
               sub1.append(rec['subscription'])

       state1 = []
       for rec in docs:
           if rec['state'] not in state1:
               state1.append(rec['state'])

       sheet.set_column(3, 1, 15)
       sheet.set_column(4, 1, 25)
       sheet.set_column(6, 1, 15)
       sheet.merge_range('A2:E3', 'Credit Report', head)
       # sheet.merge_range('A2:G3', 'Subscription Report', head)
       if len(sub1) == 1:
           sheet.merge_range('A4:B4', 'Subscription', head)
           sheet.write('C4', sub1[0], border)

       if len(state1) == 1:
           sheet.merge_range('A5:B5', 'Status', head)
           sheet.write('C5', state1[0], border)

       row=6
       col=0
       sheet.write(row,col, 'SL.No', head)
       col+=1
       if len(sub1)!=1:
           sheet.write(row,col, 'Subscription', head)
           col += 1
       sheet.write(row,col, 'Customer', head)
       col += 1
       sheet.write(row,col, 'Amount applied', head)
       col += 1
       sheet.write(row,col, 'Amount pending', head)
       col+=1
       if len(state1)!=1:
        sheet.write(row,col, 'State ', head)


       row = 7
       sl_no = 1
       for record in docs:
           col=0
           sheet.write(row, col, sl_no,border)
           col+=1
           if len(sub1)!=1:
               sheet.write(row, col, record['subscription'],border)
               col += 1
           sheet.write(row, col, record['customer'],border)
           col += 1
           sheet.write(row, col, record['amount_applied'],border)
           col += 1
           sheet.write(row, col, record['pending_amount'],border)
           col += 1
           if len(state1)!=1:
                sheet.write(row, col, record['state'],border)
           row += 1
           sl_no += 1
       workbook.close()
       output.seek(0)
       response.stream.write(output.read())
       output.close()

