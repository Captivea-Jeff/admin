# -*- coding: utf-8 -*-
# Part of BistaSolutions. See LICENSE file for full copyright and licensing details.
{
    'name': 'MAQ Point of Sale Calculator',
    'version': '15.0.1.0.0',
    'summary': 'Point of sale',
    'description': """
    MAQ Point of Sale Calculator code
    """,
    'category': 'POS',
    'website': 'https://www.bistasolutions.com/',
    'depends': ['point_of_sale', 'maq_point_of_sale'],
    'data': [
        'data/data.xml',
        # 'views/assets.xml',
        'views/product_product_form_view.xml',
        'views/pos_config_view.xml',
        'views/pos_order_view.xml',
        'views/stock_picking_view.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            '/maq_pos_calculator/static/src/scss/style.scss',
            "/maq_pos_calculator/static/src/js/models.js",
            "/maq_pos_calculator/static/src/js/CannabisWeightWarning.js",
            '/maq_pos_calculator/static/src/js/OrderWeightWidget.js',
        ],
        'web.assets_qweb': [
            '/maq_pos_calculator/static/src/xml/*.xml',
        ],
    },

    'installable': True,
    'application': False,
    'auto_install': False,
}
