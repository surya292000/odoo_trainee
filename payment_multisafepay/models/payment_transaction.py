# -*- coding: utf-8 -*-
import logging
# import pprint

# from werkzeug import urls

from odoo.addons.payment_multisafepay.controllers.main import MultisafepayController

from odoo import models

_logger = logging.getLogger(__name__)

import requests

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        print('hai')

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
            "order_id": "my-order-id-3",
            "currency": "EUR",
            "amount": 100,
            "description": "Test Order Description"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        print('hello')
        response = requests.post(url, json=payload, headers=headers)
        result= response.json()
        print(response.text)
        payment_url = result['data']['payment_url']
        print(payment_url,'payment url')
        return {'api_url': payment_url}

    # def _multisafepay_prepare_payment_request_payload(self):
    #     """ Create the payload for the payment request based on the transaction values.
    #
    #     :return: The request payload
    #     :rtype: dict
    #     """
    #     user_lang = self.env.context.get('lang')
    #     base_url = self.provider_id.get_base_url()
    #     redirect_url = urls.url_join(base_url, MultisafepayController._return_url)
    #     webhook_url = urls.url_join(base_url, MultisafepayController._webhook_url)
    #     decimal_places = CURRENCY_MINOR_UNITS.get(
    #         self.currency_id.name, self.currency_id.decimal_places
    #     )

        # return {
        #     'description': self.reference,
        #     'amount': {
        #         'currency': self.currency_id.name,
        #         'value': f"{self.amount:.{decimal_places}f}",
        #     },
        #     'locale': user_lang if user_lang in const.SUPPORTED_LOCALES else 'en_US',
        #     'method': [const.PAYMENT_METHODS_MAPPING.get(
        #         self.payment_method_code, self.payment_method_code
        #     )],
        #     # Since Mollie does not provide the transaction reference when returning from
        #     # redirection, we include it in the redirect URL to be able to match the transaction.
        #     'redirectUrl': f'{redirect_url}?ref={self.reference}',
        #     'webhookUrl': f'{webhook_url}?ref={self.reference}',
        # }
