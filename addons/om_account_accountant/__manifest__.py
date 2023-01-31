# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'CloudBI ERP Accounting',
    'version': '14.0.5.3.0',
    'category': 'Accounting',
    'summary': 'Accounting Reports, Asset Management and Account Budget For CloudBI ERP Platform',
    'live_test_url': 'https://www.youtube.com/watch?v=Kj4hR7_uNs4',
    'sequence': '1',
    'website': 'https://www.eqilibriumsolutions.com',
    'author': 'Eqilibrium Solutions',
    'maintainer': 'Eqilibrium Solutions',
    'license': 'LGPL-3',
    'support': 'support@eqilibriumsolutions.com',
    'depends': ['accounting_pdf_reports',
                'om_account_asset',
                'om_account_budget',
                'om_account_bank_statement_import'
                ],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'security/account_security.xml',
        'wizard/change_lock_date.xml',
        'views/fiscal_year.xml',
        'views/account.xml',
        'views/account_type.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'qweb': [],
}
