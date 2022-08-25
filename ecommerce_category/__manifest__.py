# -*- coding: utf-8 -*-
{
    'name': "Ecommerce Category",

    'summary': "Adding a rule to allow/disallow categories of products by website",

    'description': "Adding a rule to allow/disallow categories of products by website",

    'author': "Odoo",
    'website': "http://www.odoo.com",

    'category': 'Odoo Customied App',
    'version': '1.2',

    'depends': [
        'website_sale',
        'website',
        'im_livechat',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'views/res_config_settings_views.xml',
        'views/views.xml',
        'views/res_users.xml',
        'views/templates.xml',
        'views/website_views.xml',
        'views/hide_pricing_template.xml',
        'data/mail_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'ecommerce_category/static/src/scss/style.scss',
            'ecommerce_category/static/src/js/website_sale_search.js',
        ],
    },
}