# -*- coding: utf-8 -*-

{
    'name': 'Project Task Planner',
    'version': '14.0.1.0',
    'category': 'Productivity',
    'summary': 'Project Task Planner',
    'description': "",
    'website': 'https://www.odoo.com/page/crm',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/assets.xml',
        'views/project_task_planner_views.xml'
    ],
    'qweb': [
        'static/src/xml/systray_tasks_menu.xml'
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False
}
