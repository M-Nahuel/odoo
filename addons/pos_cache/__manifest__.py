# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "pos_cache",

    'summary': "Enable a cache on products for a lower POS loading time.",

    'description': """
This creates a product cache per POS config. It drastically lowers the
time it takes to load a POS session with a lot of products.
    """,

    'category': 'Sales/Point of Sale',
    'version': '1.0',
    'depends': ['point_of_sale'],
    'data': [
        'data/pos_cache_data.xml',
        'security/ir.model.access1.csv',
        'views/pos_cache_views.xml',
        ],
    'assets': {
        'point_of_sale.assets': [
            'pos_cache/static/**/*',
        ],
    },
    'license': 'LGPL-3',
}
