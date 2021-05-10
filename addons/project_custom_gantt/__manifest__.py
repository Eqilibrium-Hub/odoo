# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Linto CT (Contact : odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################

{
    'name': 'Project Gantt View',
    'version': '14.0.1.0.0',
    'summary': 'Gantt view, Project management',
    'live_test_url': 'https://www.youtube.com/watch?v=yVJkTzMF4ZI&list=PLeJtXzTubzj_wOC0fzgSAyGln4TJWKV4k&index=48',
    'category': 'Project',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': [
        'base',
        'web',
        'custom_gantt_view',
        'project'
    ],
    'website': 'https://www.cybrosys.com',
    'data': [
        'views/project_task.xml'
    ],
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'price': 10.00,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': False,
}
