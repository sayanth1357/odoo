# -*- coding: utf-8 -*-
from odoo import models, fields
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
   # def action_report_truck_booking(self):

        query="""select rs.name as subscription ,rp.name,rsc.credit_amount, rsc.state from recurring_subscription_credit
                 as rsc inner join recurring_subscription as rs on rsc.company_id=rs.company_id inner join res_partner as rp on
                 rp.id=rs.customer_id ; 
               """
        if self.subscription_id:
            query+="""where rsc.name='%s' """ % self.subscription_id.id
        if self.state:
            query+="""where rsc.state='%s' """ %self.state

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data = {'date': self.read()[0],'report': report}
        print(data)
        return self.env.ref('recurring_subscription.action_report_recurring_subscription_credit_form').report_action(None, data=data)

