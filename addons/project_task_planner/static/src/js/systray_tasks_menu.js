odoo.define('project_task_planner.systray.TasksMenu', function (require) {
"use strict";

var core = require('web.core');
var session = require('web.session');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var QWeb = core.qweb;

const { Component } = owl;

/**
 * Menu item appended in the systray part of the navbar, redirects to the next
 * activities of all app
 */
var TasksMenu = Widget.extend({
    name: 'activity_menu',
    template:'task_planner.systray.ActivityMenu',
    events: {
        'click .o_mail_preview': '_onActivityFilterClick',
        'show.bs.dropdown': '_onTaskMenuShow',
        'hide.bs.dropdown': '_onTaskMenuHide',
        'click .task_planner': '_onStartTaskPlanner',
        'click .view_my_week': '_onViewMyWeekShow',
    },
    start: function () {
        this._$tasksPreview = this.$('.o_mail_systray_dropdown_items');
        Component.env.bus.on('task_updated', this, this._updateCounter);
//        this._updateCounter();
        this._updateActivityPreview();
        return this._super();
    },
    //--------------------------------------------------
    // Private
    //--------------------------------------------------
    /**
     * Make RPC and get current user's activity details
     * @private
     */
    _getActivityData: function () {
        var self = this;

        return self._rpc({
            model: 'project.task.planner',
            method: 'systray_get_today_tasks',
            args: [""],
            kwargs: {context: session.user_context},
        }).then(function (data) {
            self._tasks = data;
            self.activityCounter = data.length;
            console.log('act counter', self.activityCounter);
            self.$('.o_notification_counter').text(self.activityCounter);
            self.$el.toggleClass('o_no_notification', !self.activityCounter);
        });
    },

    /**
     * Update(render) activity system tray view on activity updation.
     * @private
     */
    _updateActivityPreview: function () {
        var self = this;
        self._getActivityData().then(function (){
            self._$tasksPreview.html(QWeb.render('task_planner.systray.Tasks.Previews', {
                widget: self
            }));
        });
    },
    /**
     * update counter based on activity status(created or Done)
     * @private
     * @param {Object} [data] key, value to decide activity created or deleted
     * @param {String} [data.type] notification type
     * @param {Boolean} [data.activity_deleted] when activity deleted
     * @param {Boolean} [data.activity_created] when activity created
     */
    _updateCounter: function (data) {
        if (data) {
            if (data.activity_created) {
                this.activityCounter ++;
            }
            if (data.activity_deleted && this.activityCounter > 0) {
                this.activityCounter --;
            }
            this.$('.o_notification_counter').text(this.activityCounter);
            this.$el.toggleClass('o_no_notification', !this.activityCounter);
        }
    },

    /**
     * Redirect to particular model view
     * @private
     * @param {MouseEvent} event
     */
    _onActivityFilterClick: function (event) {
        // fetch the data from the button otherwise fetch the ones from the parent (.o_mail_preview).
        var data = _.extend({}, $(event.currentTarget).data(), $(event.target).data());

        this.do_action({
            type: 'ir.actions.act_window',
            name: 'Task',
            res_model:  'project.task',
            views: [[false, 'form']],
            res_id: data.res_id
        }, {
            clear_breadcrumbs: true,
        });
    },

    async _onStartTaskPlanner(event) {
        const action_id = await this._rpc({
            model: "project.task.planner",
            method: "systray_task_planner",
            args: [""],
            context: this.getSession().user_context,
        });
        this.do_action(action_id);
    },

    async _onViewMyWeekShow(event) {
        const action_id = await this._rpc({
            model: "project.task.planner",
            method: "view_my_week_tasks",
            args: [""],
            context: this.getSession().user_context,
        });
        this.do_action(action_id);
    },

    /**
     * @private
     */
    _onTaskMenuShow: function () {
        document.body.classList.add('modal-open');
         this._updateActivityPreview();
    },
    /**
     * @private
     */
    _onTaskMenuHide: function () {
        document.body.classList.remove('modal-open');
    },
});
SystrayMenu.Items.push(TasksMenu);

return TasksMenu;
});