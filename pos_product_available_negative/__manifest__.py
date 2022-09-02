# Copyright 2016 Stanislav Krotov <https://it-projects.info/team/ufaks>
# Copyright 2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018-2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": "POS: Out-of-stock orders",
    "summary": "Only supervisor can approve POS Order with out-of-stock product",
    "category": "Point Of Sale",
    # "live_test_url": "http://apps.it-projects.info/shop/product/DEMO-URL?version=11.0",
    "images": [],
    "version": "11.0.1.1.1",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "pos@it-projects.info",
    "website": "https://it-projects.info/team/yelizariev",
    "license": "Other OSI approved licence",  # MIT
    "price": 50.00,
    "currency": "EUR",
    "depends": ["pos_product_available"],
    "external_dependencies": {"python": [], "bin": []},
    "data": ["data.xml", "views.xml", "views/assets.xml"],
    "demo": [],
    "qweb": ["static/src/xml/msg_template.xml"],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
