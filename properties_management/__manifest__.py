# -*- coding: utf-8 -*-
{
    'name': 'properties_management',
    'version': '1.0',
    'depends': ['base', 'contacts', 'mail','account'],
    'description': """A property management module.""",
    'sequence': 0,
    'data': [
        'Security/security_groups.xml',
        'Security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/record_rules.xml',
        'data/ir_sequence_rental_data.xml',
        'data/ir_cron_expiry.xml',
        'data/ir_cron_late_payment.xml',
        'views/properties_sequences.xml',
        'views/property_management_views.xml',
        'views/facilities_views_form.xml',
        'views/rental_leased_form.xml',
        'views/rent_lease_record_views.xml',
        'views/properties_management_menu.xml',
        'views/property_owner_views.xml',
        'data/email_templates.xml',
        'report/property_report.xml',
        'report/property_report_template.xml',
        'report/property_only_report.xml',
        'wizard/property_xlsx_report_views.xml',
        'wizard/property_report_views.xml',

    ],
'assets': {
        'web.assets_backend': [
            'properties_management/static/src/js/action_manager.js'
        ],
    },
    'demo':['demo/property_demo.xml'],
    'author': 'odoo_basics',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    # 'auto_install': True,
}





