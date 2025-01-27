# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Online Jobs',
    'category': 'Website/Website',
    'sequence': 310,
    'version': '1.0',
    'summary': 'Manage your online hiring process',
    'description': "This module allows to publish your available job positions on your website and keep track of application submissions easily. It comes as an add-on of *Recruitment* app.",
    'depends': ['hr_recruitment', 'website_mail'],
    'data': [
        'security/ir.model.access1.csv',
        'security/website_hr_recruitment_security.xml',
        'data/config_data.xml',
        'views/website_hr_recruitment_templates.xml',
        'views/hr_recruitment_views.xml',
        'views/hr_job_views.xml',
    ],
    'demo': [
        'data/hr_job_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': ['hr_recruitment', 'website_mail'],
    'assets': {
        'web.assets_frontend': [
            'website_hr_recruitment/static/src/scss/**/*',
        ],
        'website.assets_editor': [
            'website_hr_recruitment/static/src/js/**/*',
        ],
        'web.assets_tests': [
            'website_hr_recruitment/static/tests/**/*',
        ],
    },
    'license': 'LGPL-3',
}
