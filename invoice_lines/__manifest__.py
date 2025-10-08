{
    'name': 'Invoice Lines',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move.xml',
    ],
}