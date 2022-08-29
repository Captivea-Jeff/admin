# -*- coding: utf-8 -*-

{
    'name': 'Theme Search Bar',
    'category': 'Custom',
    'summary': 'Theme Search bar product list',
    'version': '11.0.1.0.0',
    'author': 'Bista Solutions',
    'website': 'http://www.bistasolutions.com',
    'license': 'AGPL-3',
    'description': """
    Theme Search bar product list
        """,
    'depends': [
        'website_sale',
    ],
    'data': [
        'view/header.xml'
    ],
    'assets': {
        # 'website.assets_frontend': [
        'web.assets_frontend': [
            '/maq_search_bar/static/src/scss/website_search.scss',
            '/maq_search_bar/static/src/js/website_search.js',
        ],
    },
    'installable': True,
    'application': True,
}
