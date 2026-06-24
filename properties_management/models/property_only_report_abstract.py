from odoo import models, api


class PropertyReport(models.AbstractModel):
    """Abstract model responsible for sending data retrieved from db to template"""
    _name = 'report.properties_management.property_only_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """sends the data retrieved from db to template"""
        docs = self.env['property.report'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'properties.management',
            'docs': docs,
            'data': data,
            'property_name':data['report'][0].get('p_name'),
        }
