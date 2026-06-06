# -*- coding: utf-8 -*-

from odoo import models,api
class RecurringSubscriptionCreditAbstract(models.AbstractModel):
    _name = 'report.recurring_subscription.rec_sub_credit_report'
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['recurring.subscription.credit'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription.credit',
            'docs': docs,
            'data': data,
        }