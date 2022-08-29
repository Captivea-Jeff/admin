# -*- coding: utf-8 -*-

{
    "name": "Maq Website Order Comment",
    "author": "Bista",
    "version": "15.0.1.0.0",
    'license': 'OPL-1',
    "category": "Website",
    "website": "https://www.bistasolutions.com",
    "description": "This module is used for adding order comment at Cart page",
    "summary": "Know your customer's comments, view it on Cart page",
    "depends": ['website_sale', 'website_sale_checkout_skip_payment'],
    'assets': {
        'web.assets_frontend': {
            '/maq_partner_order_comment/static/src/js/website_partner_order_comment.js',
        },
        'web.assets_qweb': {

        },
    },
    "data": [
        'views/sale_order_view_inherit.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
