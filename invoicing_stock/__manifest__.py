# -*- coding: utf-8 -*-

{
    'name': 'invoicing stock',
    'author':'cybrosys',
    'description': """This module contains delivery orders in invoicing """,
    'depends': ['base','account','mail','sale'],
    'data': [
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
        'data/sequence_data.xml'
     ],


    'installable':True,
    'application': True
}