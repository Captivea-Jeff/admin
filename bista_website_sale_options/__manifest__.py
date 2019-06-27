# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    "name": "Bista website sale options",
    "version": "11.0.1.0.0",
    "author": "Bista Solutions Pvt. Ltd.",
    "maintainer": "Bista Solutions Pvt. Ltd.",
    "website": "https://www.bistasolutions.com",
    "category": "Web",
    "license": "AGPL-3",
    'summary': """This module contains following features
                1. Hide sale options module within 5 second.
                2. Add product specification master in product view""",
    "depends": [
        "website",
        "website_sale",
        "website_sale_options",
        "maq_prod_variant_unpublish",
        "ecommerce_category",
        "sale",
        'maq_custom_theme',
        'maqabim_website_sale',
        'maqabim_website_popup'
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/product_sale_view_inherit.xml',
        'views/product_specification_views.xml',
        "views/website_sale_options.xml",
        "data/data.xml"
    ],
    #    "qweb": [
    #        "static/src/xml/website_sale.xml",
    #    ],
    # "images": ["static/description/groupexpand.png"],
    "installable": True,
}
