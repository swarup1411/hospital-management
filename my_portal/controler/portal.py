from odoo import http
from odoo.http import request

class CurrencyConverterPortal(http.Controller):

    @http.route('/my/currency-converter', auth='user', website=True)
    def currency_converter(self):
        return request.render(
            'my_portal.portal_currency_page',
            {}
        )
