# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Maqabim Distributors: SO PDF custo + Sticky header for website",
    'summary': "Web",
    'description': """
Maqabim Distributors: SO PDF custo + Sticky header for website
===============================================================
- SO PDF custo + Sticky header for website
    - Delivered' and 'Invoiced quantity SO PDF
    - sticky header
""",
    "author": "Odoo Inc",
    'website': "https://www.odoo.com",
    'category': 'Custom Development',
    'version': '15.0.0.1',
    'depends': ['sale_management', 'website','portal'],
    'data': [
        'views/report_sale.xml',
    ],
'assets': {
        'web.assets_frontend': [
            'maqabim_customization/static/src/css/website.css',
        ],
    },
    'license': 'OEEL-1',
}