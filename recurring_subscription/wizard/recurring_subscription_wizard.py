# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields

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
        query = """select rs.name, rp.name as customer ,rs.total_credit_applied ,rs.terms_and_condition as terms ,pt.name->>'en_US' as product , rs.recurring_amount ,rs.status
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

        data = {'report': report,'length':len(sub),'subs':sub,'name_len':len(name1),'subname':name1 }

        print("5432",data)



        return self.env.ref('recurring_subscription.action_report_recurring_subscription_form').report_action(None,data=data)




