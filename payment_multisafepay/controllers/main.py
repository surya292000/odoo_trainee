import logging

import pprint

from odoo import http

from odoo.http import request

_logger = logging.getLogger(__name__)

class MultiSafePayController(http.Controller):

    @http.route('/payment/multisafepay/return', type='http', auth='public', methods=['GET', 'POST'], csrf=False,
                save_session=False
                )
    def _multisafepay_return_from_checkout(self,**data):
        _logger.info("handling redirection from multisafepay with data:\n%s", pprint.pformat(data))
        request.env['payment.transaction'].sudo()._handle_notification_data('multisafepay', data)
        return request.redirect('/payment/status')
