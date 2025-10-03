# -*- coding: utf-8 -*-
import logging

from odoo import _

from odoo.addons.payment.const import CURRENCY_MINOR_UNITS

from odoo.exceptions import ValidationError

from odoo.addons.payment_multisafepay.controllers.main import MultiSafePayController

from odoo import models

_logger = logging.getLogger(__name__)

import requests

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        ref = processing_values['reference']
        amount = processing_values['amount']
        currency_id = self.env['res.currency'].browse(1)
        currency_name = currency_id.name
        decimal_places = CURRENCY_MINOR_UNITS.get(self.currency_id.name, self.currency_id.decimal_places)
        amount = int(amount * (10 ** decimal_places))

        url = "https://testapi.multisafepay.com/v1/json/orders?api_key=8acfb15b1f60d7634e7d1c9edfc5a3d20264fc98"

        payload = {
            "payment_options": {
                "close_window": False,
                "notification_method": "POST",
                "notification_url": "https://www.example.com/webhooks/payment",
                "redirect_url": "http://localhost:8018/payment/multisafepay/return",
                "cancel_url": "http://localhost:8018/payment/multisafepay/return"
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
            "order_id": ref,
            "currency": currency_name,
            "amount":  amount,
            "description": "Test Order Description"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        result= response.json()
        print(response.text)
        if result['data']:
            payment_url = result['data']['payment_url']
            return {'api_url': payment_url}

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on multisafepay data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """

        tx = super()._get_tx_from_notification_data(provider_code, notification_data)

        if provider_code != 'multisafepay' or len(tx) == 1:
            return tx

        tx = self.search(
            [('reference', '=', notification_data.get('transactionid')), ('provider_code', '=', 'multisafepay')]
        )
        if not tx:
            raise ValidationError("Multisafepay: " + _(
                "No transaction found matching reference %s.", notification_data.get('transactionid')
            ))

        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on multisafepay data.

        Note: self.ensure_one()

        :param dict notification_data: The notification data sent by the provider
        :return: None
        """

        super()._process_notification_data(notification_data)
        if self.provider_code != 'multisafepay':
            return

        # Update the provider reference.
        self.provider_reference = f'multisafepay-{self.reference}'

        endpoint = f"/orders/{notification_data.get('transactionid')}?api_key={self.provider_id.multisafepay_api_key}"

        payment_data = self.provider_id._multisafepay_make_request(endpoint,
                                                                   f'/payments/{self.provider_reference}', method="GET"
                                                                   )

        # Update the payment state.
        payment_status = payment_data.get('data', {}).get('status')
        if payment_status == 'completed':
            self._set_done()
        elif payment_status in ['initialized', 'cancelled']:
            self._set_canceled("Multisafepay: " + _("Cancelled payment with status: %s", payment_status))
        else:
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                payment_status, self.reference
            )
            self._set_error(
                "Multisafepay: " + _("Received data with invalid payment status: %s", payment_status)
            )
