# -*- coding: utf-8 -*-
{
    'name': 'MAQ Point of Sale',
    'version': '15.0.1.0.0',
    'summary': 'Point of sale',
    'description': """
    Point of Sale Custom code
    """,
    'category': 'POS',
    'website': 'https://www.bistasolutions.com/',
    'depends': ['point_of_sale'],
    'data': [
        # 'views/assets.xml',
        'views/pos_config_view.xml',
        'views/pos_order_view.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            '/maq_point_of_sale/static/src/js/models.js',
            '/maq_point_of_sale/static/src/js/CustomerVarify.js',

        ],
    },
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
