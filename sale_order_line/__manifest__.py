{
    'name': 'Sale Order From Lines',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_line_views.xml',
        'wizard/sale_order_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
}
