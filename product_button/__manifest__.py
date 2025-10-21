{
    'name': 'Product Form Button',
    'depends': ['base', 'product', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_product.xml',
        'wizard/product_button_wizard.xml',
    ],
}