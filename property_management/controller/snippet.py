from odoo import http
from odoo.http import request

class WebsiteProperty(http.Controller):

    @http.route('/get_product_categories', auth="public", type='json', website=True)
    def get_product_category(self):
        """Get the properties for the snippet."""
        properties = request.env['property.details'].sudo().search_read(
            [('owner_id', '!=', False)], fields=['name', 'property_image', 'id'], order= 'built_date desc'
        )
        # return products, unique_categories

        return {'categories': properties}

    @http.route(['/property/details/<int:property_id>'], auth="public", type='http', website=True)
    def get_property_details(self, property_id, **kwargs):
        """Property details page"""
        property_rec = request.env['property.details'].sudo().browse(property_id)
        if not property_rec.exists():
            return request.not_found()

        values = {
            'property': property_rec,
        }
        return request.render('property_management.property_info_template', values)