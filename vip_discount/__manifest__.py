# -*- coding: utf-8 -*-
{
    'name': 'vip discount',
    'author':'cybrosys',
    'description': """This module contains the discount for vip customers""",
    'depends': ['base','contacts','sale'],
    'data':[
       'views/res_partner_view.xml',
        'views/sale_order_view.xml'
    ],


    'installable':True,
    'application': True
}