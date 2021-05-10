# -*- coding: utf-8 -*-

from odoo import models, api, _


class ProjectTasks(models.Model):
    _inherit = 'project.task'

    @api.model
    def create(self, vals):
        res = super(ProjectTasks, self).create(vals)
        self.env['bus.bus'].sendone(
            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
            {'type': 'task_updated', 'task_created_created': True})
        return res
