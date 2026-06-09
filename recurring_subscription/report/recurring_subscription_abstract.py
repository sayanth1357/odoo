# -*- coding: utf-8 -*-

from odoo import models,api
class RecurringSubscriptionAbstract(models.AbstractModel):
    _name = 'report.recurring_subscription.form_r_s_report'
    @api.model
    def _get_report_values(self, docids, data=None):
        print('docid',docids)
        docs = self.env['recurring.subscription.wizard'].browse(docids)
        print(1233,docs)
        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription',
            'docs': docs,
            'data': data,
        }