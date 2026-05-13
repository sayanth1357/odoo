{
    'name': 'Real Estate',
    'application': True,
    'depends':['base'],
    'data':[
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
                
        'views/property_type_views.xml',

        'views/property_tag.xml',


        'views/menu.xml'

    ]
}