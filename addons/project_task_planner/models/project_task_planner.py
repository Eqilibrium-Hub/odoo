# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.tools.safe_eval import safe_eval


class ProjectTaskPlanner(models.TransientModel):
    _name = 'project.task.planner'
    _description = 'Project Task Planner'

    @api.depends("current_number", "total_number", "tasks")
    def _compute_task_id(self):
        for task in self:
            tasks = safe_eval(task.tasks)
            all_tasks = [act["task_id"] for act in tasks if act["number"] == self.current_number]
            task_id = all_tasks and all_tasks[0] or False
            if task_id == task.task_id:
                task.current_task_id = task_id
                return
            task.current_task_id = task_id
            task.task_id = task_id
            task.date_todo = task.current_task_id.date_assign
            task.task_deadline = task.current_task_id.date_deadline
            task.priority = task.current_task_id.priority
            task.description = task.current_task_id.description

    tasks = fields.Char(string="Tasks")
    current_task_id = fields.Many2one(
        "project.task",
        string="Task Name",
        compute='_compute_task_id',

    )
    task_name = fields.Char(related='current_task_id.name')
    task_id = fields.Integer()
    current_number = fields.Integer(string="Number")
    total_number = fields.Integer(string="Total")
    project_id = fields.Many2one("project.project", related="current_task_id.project_id")
    project_name = fields.Char(related='current_task_id.project_id.name')
    description = fields.Html(string='Description')
    date_todo = fields.Date(string='To-Do Date')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Important'),
        ('2', 'High'),
        ('3', 'very High')
    ], string="Priority")
    task_deadline = fields.Date(string='Task Deadline')

    """
          Function executed while clicking Task Planner menu in Internal Projects
           It passes all Internal project tasks
    """
    def start_task_planner(self):
        domain = [('project_id.is_solar_project', '=', False), ('project_id.is_template', '=', False), ('date_assign', '=', False)]
        task_ids = self.env["project.task"].search(domain, order="date_deadline, id")
        if task_ids:
            tsk_ids = []
            itera = 0
            for task in task_ids:
                tsk_ids.append({
                    "task_id": task.id,
                    'planning_done': False,
                    "number": itera,
                })
                itera += 1
            task_planner_id = self.create({
                "tasks": tsk_ids,
                "current_number": 0,
                "total_number": len(tsk_ids)
            })
            action = self.env.ref("project_task_planner.task_planner_action").read()[0]
            action["res_id"] = task_planner_id.id
            # action["context"] = {'form_view_initial_mode': 'edit'}
        else:
            raise UserError(_("There are no Tasks for Planning"))
        return action

    def systray_task_planner(self):
        domain = [('date_assign', '=', False)]
        task_ids = self.env["project.task"].search(domain, order="date_deadline, id")
        if task_ids:
            tsk_ids = []
            itera = 0
            for task in task_ids:
                tsk_ids.append({
                    "task_id": task.id,
                    'planning_done': False,
                    "number": itera,
                })
                itera += 1
            task_planner_id = self.create({
                "tasks": tsk_ids,
                "current_number": 0,
                "total_number": len(tsk_ids)
            })
            action = self.env.ref("project_task_planner.task_planner_action").read()[0]
            action["res_id"] = task_planner_id.id
            # action["context"] = {'form_view_initial_mode': 'edit'}
        else:
            raise UserError(_("There are no Tasks for Planning"))
        return action

    """
        Function executed while clicking Task Planner menu in Solar Projects
        It passes all solar project tasks
    """
    def start_solar_project_task_planner(self):
        domain = [('project_id.is_solar_project', '=', True), ('project_id.is_template', '=', False), ('date_assign', '=', False)]
        task_ids = self.env["project.task"].search(domain, order="date_deadline, id")
        if task_ids:
            tsk_ids = []
            itera = 0
            for task in task_ids:
                tsk_ids.append({
                    "task_id": task.id,
                    'planning_done': False,
                    "number": itera,
                })
                itera += 1
            task_planner_id = self.create({
                "tasks": tsk_ids,
                "current_number": 0,
                "total_number": len(tsk_ids)
            })
            action = self.env.ref("project_task_planner.task_planner_action").read()[0]
            action["res_id"] = task_planner_id.id
            action["context"] = {'form_view_initial_mode': 'edit'}
        else:
            raise UserError(_("There are no Tasks for Planning"))
        return action

    def _get_next_task(self):
        self.ensure_one()
        tasks = safe_eval(self.tasks)
        number = False
        for act in tasks:
            if act["number"] > self.current_number:
                number = act["number"]
                break
        return number

    def _get_previous_task(self):
        self.ensure_one()
        tasks = safe_eval(self.tasks)
        tasks = list(reversed(tasks))
        number = False
        for act in tasks:
            if act["number"] < self.current_number:
                number = act["number"]
                break
        return number

    def action_skip(self):
        self.ensure_one()
        self.current_number = self._get_next_task()

    def action_previous(self):
        self.ensure_one()
        self.current_number = self._get_previous_task()

    def action_done(self):
        self.ensure_one()
        vals = {
            'priority': self.priority,
            'description': self.description,
            'date_assign': self.date_todo,
            'date_deadline': self.task_deadline
        }
        self.current_task_id.update(vals)
        tasks = safe_eval(self.tasks)
        for task in tasks:
            if task['task_id'] == self.current_task_id.id:
                tasks.remove(task)
        self.tasks = tasks
        self.action_skip()

    def systray_get_today_tasks(self):
        query = """SELECT id, date_assign, user_id, name, count(*), project_id
                           FROM project_task
                           WHERE user_id = %(user_id)s AND date_assign::date = %(today)s
                           GROUP BY id;
                           """
        self.env.cr.execute(query, {
            'today': fields.Date.context_today(self),
            'user_id': self.env.uid,
        })
        task_data = self.env.cr.dictfetchall()
        for data in task_data:
            project = self.env['project.project'].browse(data['project_id'])
            data.update({'icon': '/project/static/description/icon.png', 'project_name': project.name})
        return task_data

    def view_my_week_tasks(self):
        action = self.env.ref("project_task_planner.action_view_user_tasks_this_week_all").read()[0]
        return action


