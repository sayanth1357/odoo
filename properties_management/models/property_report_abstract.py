# -*- coding: utf-8 -*-

from odoo import models, api

class PropertyReport(models.AbstractModel):
    """Abstract model responsible for sending data retrieved from db to template"""

    _name = 'report.properties_management.property_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """function that send s data over to the template"""
        docs = self.env['property.report'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'properties.management',
            'docs': docs,
            'data': data,
        }
