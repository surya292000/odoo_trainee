# -*- coding: utf-8 -*-
{
    'name': "Material Request",
    'depends': ['base', 'product', 'purchase', 'stock'],
    'data': [
            "security/material_request_groups.xml",
            "security/ir.model.access.csv",
             "views/material_request_lines_views.xml",
             "views/material_request_views.xml",
             "views/material_request_menu.xml"
             ],
    'application': True,
    "sequence": 1
}
