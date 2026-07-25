# -*- coding: utf-8 -*-
{
    'name':'Hostel',
    'version': '19.0.0.0.7',
    'summary': 'In development',
    'sequence': 0,
    'description': """
    Hostel Management
    =================
    Module allows to maintain hostel rooms, facilities and manage student data
    """,
    'data':['data/ir_cron_data.xml',
            'data/base_automation_data.xml',
            'data/mail__template_data.xml',
            'data/hostel_facilities_data.xml',
            'data/hostel_room_sequence_data.xml',
            'data/product_product_data.xml',
            'data/student_sequence_data.xml',
            'report/ir_actions_report.xml',
            'report/ir_actions_report_templates.xml',
            'wizard/student_student_report_views.xml',
            'wizard/leave_request_report_views.xml',

            'security/res_groups.xml',
            'security/ir_rules.xml',
            'security/ir.model.access.csv',

            'views/student_registration_views.xml',
            'views/hostel_room_details.xml',
            'views/hostel_room_views.xml',
            'views/student_student_views.xml',
            'views/hostel_room_type_views.xml',
            'views/hostel_facilities_views.xml',
            'views/leave_request_views.xml',
            'views/cleaning_service_views.xml',
            'views/account_move_views.xml',
            'views/hostel_room_snippet_views.xml',
            'views/hostel_room_menu.xml',


            'demo/hostel_facilities_demo.xml',
            'demo/hostel_room_type_demo.xml',
            'demo/hostel_room_demo.xml',
            'demo/student_student_demo.xml',

            ],
    'demo':[
            ],
    'depends': ['base','mail', 'base_automation', 'product','account','contacts','website'],
    'assets' : {
        'web.assets_backend' : [
            'hostel/static/src/js/action_manager.js',],
        'web.assets_frontend' : [
            'hostel/static/src/js/student_registration.js',
            'hostel/static/src/xml/hostel_room_views.xml',
            'hostel/static/src/js/hostel_room.js',
        ],

    } ,
    'installable': True,
    'application': True,
    'author': 'cybrosys',
    'license': 'LGPL-3',
}