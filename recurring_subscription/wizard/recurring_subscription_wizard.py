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



        query="""select rs.name, rp.name as customer ,rs.total_credit_applied  ,pt.name as product , rs.recurring_amount ,rs.status 
                from recurring_subscription as rs inner join res_partner as rp on rp.id = rs.customer_id inner join 
				product_template as pt on pt.id=rs.product_id;"""

        if self.subscription_id:
            query+="""where rs.id ='%s' """ % self.subscription_id.id

        today = fields.Date.today()
        if self.report=='daily':
            query+="""where  rs.date >= '%s' """%today
        elif self.report=='weekly':
            query+="""where rs.date >= '%s' """%(today-timedelta(days=7))
        elif self.report=='monthly':
            query+="""where rs.date >= '%s' """%(today-timedelta(days=30))
        elif self.report=='yearly':
            query+="""where rs.date >= '%s' """%(today-timedelta(days=365))


        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        data = {'report': report}
        print("5432",data)

        return self.env.ref('recurring_subscription.action_report_recurring_subscription_form').report_action(None,data=data)


