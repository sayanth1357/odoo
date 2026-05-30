# -*- coding: utf-8 -*-

{
    'name': 'sale order approval',
    'author':'cybrosys',
    'description': """This module contains the sale order approvals""",
    'depends': ['base','sale_management'],
    'data': [
        'views/sale_order_view.xml',
    ],

    'installable':True,
    'application': True
}