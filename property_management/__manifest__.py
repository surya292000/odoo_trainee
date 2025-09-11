# -*- coding: utf-8 -*-
{
    'name': "Property Management",
    'depends': ['base', 'mail', 'sale', 'website', 'portal'],
    'data': ["security/property_management_groups.xml",
             "security/property_management_security.xml",
             "security/ir.model.access.csv",

             "data/ir_sequence_data.xml",
             "data/property_facilities_data.xml",
             "data/property_details_datas.xml",
             "data/action_cron_test_method.xml",
             "data/mail_template_data.xml",

             "wizard/property_report_wizard_views.xml",

             "report/ir_actions_report.xml",
             "report/property_rental_report_template.xml",

             "views/property_facility_views.xml",
             "views/property_details_views.xml",
             "views/property_rental_lease_views.xml",
             "views/property_rental_lease_lines_views.xml",
             "views/res_partner_views.xml",
             "views/web_menu.xml",
             "views/website_template.xml",
             "views/website_portal.xml",
             "views/property_management_menu.xml"
             ],
    'assets': {
    'web.assets_frontend': [
        'property_management/static/src/js/action_manager.js',
        'property_management/static/src/js/custom_website.js',
    ],},

    'application': True,
    "sequence": 1
}
