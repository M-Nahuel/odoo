#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2013-2015 Akretion (http://www.akretion.com)

{
    'name': 'France - FEC Export',
    'icon': '/l10n_fr/static/description/icon.png',
    'category': 'Accounting/Localizations/Reporting',
    'summary': "Fichier d'Échange Informatisé (FEC) for France",
    'author': "Akretion,Odoo Community Association (OCA)",
    'depends': ['l10n_fr', 'account'],
    'data': [
        'security/ir.model.access1.csv',
        'security/security.xml',
        'wizard/account_fr_fec_view.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
