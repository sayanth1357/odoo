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