# -*- coding: utf-8 -*-

{
    'name': 'sale order approval',
    'author':'cybrosys',
    'description': """This module contains the sale order approvals""",
    'depends': ['base','sale'],
    'data': [
        'views/sale_order_view.xml',
        'security/sale_approval_security.xml'
    ],

    'installable':True,
    'application': True
}