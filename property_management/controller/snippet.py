from odoo import http
from odoo.http import request

class WebsiteProduct(http.Controller):
    @http.route('/get_product_categories', auth="public", type='json',
                website=True)
    def get_product_category(self):
        """Get the website categories for the snippet."""
        public_categs = request.env[
            'property.details'].sudo().search_read(
            [('owner_id', '=', False)], fields=['name','property_image', 'id']
        )
        values = {
            'categories': public_categs,
        }
        return values

    @http.route('/get_property_details', auth="public", type='http', website=True)
    def get_property_details(self, **post):
        image = post.get('start')
        property_details = request.env['property.details'].read(['name'])

        return property_details
        # pass
