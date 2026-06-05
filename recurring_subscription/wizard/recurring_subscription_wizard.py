# -*- coding: utf-8 -*-
from odoo import models, fields
class RecurringSubscriptionWizard(models.TransientModel):
   _name = 'recurring.subscription.wizard'
   _description = 'Wizard for recurring subscription report'

   subscription_id=fields.Many2one('recurring.subscription',string='Subscription')
   report=fields.Selection(selection=[('daily','Daily'),('weekly','Weekly'),('monthly','Monthly'),('yearly','Yearly')],string='report')
   partner_id=fields.Many2one('res.partner',string='partner')

   # def pdf_button(self):
   #
   #    name = self.env['recurring.subscription'].search([])
   #    return self.env.ref('recurring_subscription.action_report_recurring_subscription_form').report_action(name)


