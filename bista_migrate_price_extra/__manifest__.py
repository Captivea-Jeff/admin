# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    "name": "Bista Migrate Price Extra",
    "version": "12",
    "author": "Bista Solutions Pvt. Ltd.",
    "maintainer": "Bista Solutions Pvt. Ltd.",
    "website": "https://www.bistasolutions.com",
    "category": "Web",
    "license": "AGPL-3",
    'summary': """This module contains following features
                1. Migrate price_extra field from V11 product_attribute_price to product_template_attribute_value in V12.""",
    "depends": ['stock'],
    "data": [
        "wizard/migrate_price_extra_view.xml",
    ],
    #    "qweb": [
    #    ],
    "installable": True,
}

