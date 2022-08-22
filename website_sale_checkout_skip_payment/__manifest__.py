{
    "name": "Website Sale Checkout Skip Payment",
    "summary": "Skip payment for logged users in checkout process",
    "version": "15.0.1.1.0",
    "category": "Website",
    "website": "https://github.com/OCA/e-commerce",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website_sale"],
    "data": [
        "views/website_sale_skip_payment.xml",
        "views/website_sale_template.xml",
        "views/partner_view.xml",
    ],
}
