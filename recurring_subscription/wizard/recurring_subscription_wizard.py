# -*- coding: utf-8 -*-
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from dateutil.utils import today

from odoo import models, fields

class RecurringSubscriptionWizard(models.TransientModel):
   _name = 'recurring.subscription.wizard'
   _description = 'Wizard for recurring subscription report'

   from_date=fields.Date(string='from')
   to_date=fields.Date(string='to')
   subscription_id=fields.Many2one('recurring.subscription',string='Subscription')
   report=fields.Selection(selection=[('daily','Daily'),
                                      ('weekly','Weekly'),
                                      ('monthly','Monthly'),
                                      ('yearly','Yearly')],string='report')
   partner_id=fields.Many2one('res.partner',string='partner')
   today=fields.Date.today()
   
   def action_report_subscription(self):



        query="""select rs.name as subscription, rs.customer_id as customer ,rs.product_id, rs.recurring_amount ,rs.status 
                from recurring_subscription as rs inner join res_partner as rp on rp.id = rs.customer_id
               """

        if self.subscription_id:
            query+="""where rs.name='%s' """ % self.subscription_id.id

        if self.report=='daily':
            query+="""where rs.date >= '%s' """%self.today
        elif self.report=='weekly':
            query+="""where rs.date >= '%s' """%(today()-relativedelta(weeks=7))
        elif self.report=='monthly':
            query+="""where rs.date >= '%s' """%(today()-relativedelta(months=1))
        elif self.report=='yearly':
            query+="""where rs.date >= '%s' """%(today()-relativedelta(years=1))

        if self.from_date:
            query += """ where rs.date >= '%s' and rs.date <= '%s'""" %( self.from_date,self.to_date)
        # if self.from_date:
        #     query += """ where tb.date >= '%s' and tb.date <= '%s'""" % self.date_from,% self.date_to
        # if self.report=='daily':
        #     query+=""""""
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data = {'date': self.read()[0],'report': report}
        print("5432",data)
        return self.env.ref('recurring_subscription.action_report_recurring_subscription_form').report_action(None, data=data)

