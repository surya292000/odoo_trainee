# -*- coding: utf-8 -*-
from odoo import models, api, fields


class PropertyLeaseReport(models.AbstractModel):
    _name = 'report.property_management.property_rental_report_template'
    _description = 'Property Lease Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        records = data.get("records", [])
        tenants = list({rec['tenant_name'] for rec in records})
        single_tenant = len(tenants) == 1
        tenant_name = tenants[0] if single_tenant else False
        currency = self.env.company.currency_id
        date = fields.Datetime.now()

        return {
            'doc_ids': docids,
            'doc_model': 'property.rental.lease',
            'data': records,
            'currency': currency,
            'single_tenant': single_tenant,
            'tenant_name': tenant_name,
            'date': date,
        }
