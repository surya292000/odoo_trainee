# -*- coding: utf-8 -*-
import logging
# import pprint

# from werkzeug import urls

from odoo import models

_logger = logging.getLogger(__name__)

import requests

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):

        url = "https://testapi.multisafepay.com/v1/json/orders?api_key=8acfb15b1f60d7634e7d1c9edfc5a3d20264fc98"

        payload = {
            "payment_options": {
                "close_window": False,
                "notification_method": "POST",
                "notification_url": "https://www.example.com/webhooks/payment",
                "redirect_url": "https://www.example.com/order/success",
                "cancel_url": "https://www.example.com/order/failed"
            },
            "customer": {
                "locale": "en_US",
                "disable_send_email": False
            },
            "checkout_options": {"validate_cart": False},
            "days_active": 30,
            "seconds_active": 2592000,
            "type": "redirect",
            "gateway": "APPLEPAY",
            "order_id": "my-order-id-1",
            "currency": "EUR",
            "amount": 100,
            "description": "Test Order Description"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return {'api_url': payment_url}
