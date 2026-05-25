# -*- coding: utf-8 -*-
{
    'name': 'Recurring Subscription',
    'author':'cybrosys',
    'description': """This module contains the common features of recurring subscription""",
    'depends': ['base','product','mail','contacts','crm','account'],
    'data':[
        'security/ir.model.access.csv',
        'security/subscription_security.xml',
        'views/recurring_subscription_views.xml',
        'views/recurring_subscription_credit_view.xml',
        'data/sequence_data.xml',
        'views/billing_schedule_view.xml',
        'views/product_order_lines_view.xml',
        'views/partner_account_id_view.xml',
        'views/res_partner_view.xml',
        'views/crm_lead_view.xml',
        'views/recurring_subscription_menu.xml',
        'data/demo_data.xml',
        'data/mail_template_data.xml',
        'data/ir_cron_data.xml',
    ],


    'installable':True,
    'application': True
}