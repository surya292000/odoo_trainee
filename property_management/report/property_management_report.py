from odoo import models,api

class PropertyLeaseReport(models.AbstractModel):
    _name = 'report.property_management.property_rental_report_template'
    _description = 'Property Lease Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('qwertyu', data)
        return {
            'doc_ids': docids,
            'doc_model': 'property.rental.lease',
            # 'docs': data.get('records', []),
            'docs': data,
            'data': data['report']

        }