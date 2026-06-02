# -*- coding: utf-8 -*-
{
    'name': 'Automated purchase order',
    'author':'cybrosys',
    'description': """This module creates PO automatically""",
    'depends': ['base','purchase'],
    'data':[
        'views/product_template_view.xml',
        'wizard/purchase_order_wizard_views.xml',
        'security/ir.model.access.csv',
    ],


    'installable':True,
    'application': True
}