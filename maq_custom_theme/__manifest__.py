# -*- coding: utf-8 -*-


{
    "name": "Bista Maq Custom Theme",
    "version": "12.0.1.0.0",
    "author": "Bista Solutions Pvt. Ltd.",
    "maintainer": "Bista Solutions Pvt. Ltd.",
    "website": "https://www.bistasolutions.com",
    "category": "Custom",
    "license": "AGPL-3",
    'description': """In this module customize product details page""",
    'summary': '',
    "depends": ['website_sale', 'website_product_page_layout_73lines','portal'],
    "data": [
        "views/products_template.xml",
        "views/assets.xml",
        'views/product_details_template.xml',
        "views/portal_template.xml",
        "views/template.xml",
    ],
    "installable": True,
    "application": True,
}

