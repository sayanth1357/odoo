# -*- coding: utf-8 -*-
from odoo import models, fields

class RecurringSubscriptionWizard(models.TransientModel):
   _name = 'recurring.subscription.wizard'
   _description = 'Wizard for recurring subscription report'

   date_from=fields.Date(string='Date from')
   date_to=fields.Date(string='Date to')
   subscription_id=fields.Many2one('recurring.subscription',string='Subscription')
   report=fields.Selection(selection=[('daily','Daily'),('weekly','Weekly'),('monthly','Monthly'),('yearly','Yearly')],string='report')
   partner_id=fields.Many2one('res.partner',string='partner')

   def action_report_subscription(self):
   # def action_report_truck_booking(self):

        query="""select customer_id,name from recurring_subscription"""
        # if self.from_date:
        #     query += """ where tb.date >= '%s' and tb.date <= '%s'""" % self.date_from,% self.date_to
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data = {'date': self.read()[0],'report': report}
        print(data)
        return self.env.ref('recurring_subscription.action_report_recurring_subscription_form').report_action(None, data=data)

