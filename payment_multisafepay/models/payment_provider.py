# -*- coding: utf-8 -*-
import logging
import pprint

import requests
from werkzeug import urls

from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('multisafepay', 'Multisafepay')], ondelete={'multisafepay': 'set default'}
    )
    multisafepay_api_key = fields.Char(
        string="Multisafepay API Key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="Multisafepay", groups="base.group_system"
    )

    def _multisafepay_make_request(self, endpoint, data=None, method='POST'):
        """ Make a request at multisafepay endpoint.

                Note: self.ensure_one()

                :param str endpoint: The endpoint to be reached by the request
                :param dict data: The payload of the request
                :param str method: The HTTP method of the request
                :return The JSON-formatted content of the response
                :rtype: dict
                :raise: ValidationError if an HTTP error occurs
                """
        self.ensure_one()
        endpoint = f'/v1/json/{endpoint.strip("/")}'
        url = urls.url_join('https://testapi.multisafepay.com/', endpoint)
        headers = {"accept": "application/json"}
        try:
            response = requests.request(method, url, json=data, headers=headers, timeout=30)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", url, pprint.pformat(data)
                )
                raise ValidationError(
                    "MultiSafePay: " + _(
                        "The communication with the API failed. MultiSafePay gave us the following "
                        "information: %s", response.json().get('detail', '')
                    ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "MultiSafePay: " + _("Could not establish the connection to the API.")
            )
        return response.json()

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'multisafepay':
            return default_codes
        return {'multisafepay'}
