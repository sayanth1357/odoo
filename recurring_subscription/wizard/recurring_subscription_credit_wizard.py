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

        # # if self.subscription_id:
        # #     query += """where rs.id ='%s' """ % self.subscription_id.id
        # if self.state=='fully approved':
        #     query+=""" where rsc.state == '%s' """ %self.state
        # # elif self.state=='fully approved':
        # #     query+=""" where rsc.state=='%s' """ %self.state
        # # elif self.state=='confirmed':
        # #     query+="""where rsc.state=='%s' """ %self.state
        # # elif self.state=='first approved':
        # #     query+="""where rsc.state=='%s' """ %self.state
        # # elif self.state=='fully approved':
        # #     query+="""where rsc.state=='%s' """ %self.state
        # # elif self.state=='rejected':
        # #     query+="""where rsc.state=='%s' """ %self.state


        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)

        # name1 = []
        # for record in report:
        #     if record['name'] not in name1:
        #         name1.append(record['name'])
        # print(4567, name1)


        state1 = []
        for rec in report:
            if rec['state'] not in state1:
                state1.append(rec['state'])
        print(state1)



        data = {'report': report,'length':len(state1),'state':state1,}
        print(9876,report)
        print(8876,data)



        return self.env.ref('recurring_subscription.action_report_recurring_subscription_credit_form').report_action(None, data=data)

