from odoo import models, api


class PropertyLeaseReport(models.AbstractModel):
    _name = 'report.property_management.property_rental_report_template'
    _description = 'Property Lease Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        records = data.get("records", [])
        tenants = list({rec['tenant_name'] for rec in records})
        single_tenant = len(tenants) == 1
        tenant_name = tenants[0] if single_tenant else False

        return {
            'doc_ids': docids,
            'doc_model': 'property.rental.lease',
            'data': records,
            'single_tenant': single_tenant,
            'tenant_name': tenant_name,
        }
