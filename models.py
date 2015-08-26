# -*- coding: utf-8 -*-

from datetime import date, timedelta
from openerp import models, fields, api
from togglib import get_summary, get_dashboard, get_current


class res_users(models.Model):
    _inherit = 'res.users'

    toggl_key = fields.Char(string='Toggl API Key')


class LandingReport(models.AbstractModel):
    _name = 'report.toggl.landing'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        return report_obj.render('toggl.landing', {})


class DayReport(models.AbstractModel):
    _name = 'report.toggl.day_summary'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        summary = get_summary(date.today().strftime('%Y-%m-%d'))
        return report_obj.render('toggl.summary', {'summary': summary})


class YesterdayReport(models.AbstractModel):
    _name = 'report.toggl.yesterday_summary'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        t = date.today() - timedelta(days=1)
        summary = get_summary(t.strftime('%Y-%m-%d'))
        return report_obj.render('toggl.summary', {'summary': summary})


class DashboardReport(models.AbstractModel):
    _name = 'report.toggl.dashboard'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        dashboard = get_dashboard()
        return report_obj.render('toggl.dashboard', {'dashboard': dashboard})


class CurrentReport(models.AbstractModel):
    _name = 'report.toggl.current'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        users = self.env['res.users'].search([])
        data = []
        for user in users:
            if not user.toggl_key:
                continue
            user_current = get_current(user.toggl_key)
            user_current.update(user=user.name)
            data.append(user_current)
        return report_obj.render('toggl.current', {'current': data})