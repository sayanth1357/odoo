# -*- coding: utf-8 -*-
{
    'name': 'purchase order attachment',
    'author':'cybrosys',
    'description': """This module contains mandatory attachment before confirming purchase order""",
    'depends': ['base','contacts','purchase'],
    'data':[
        'views/res_config_settings_views.xml',
    ],


    'installable':True,
    'application': True
}