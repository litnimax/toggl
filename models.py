# -*- coding: utf-8 -*-

from datetime import date
from openerp import models, fields, api
from togglib import get_summary, get_dashboard


class SummaryReport(models.AbstractModel):
    _name = 'report.toggl.summary'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        summary = get_summary(date.today().strftime('%Y-%m-%d'))
        return report_obj.render('toggl.summary', {'summary': summary})


class DashboardReport(models.AbstractModel):
    _name = 'report.toggl.dashboard'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        dashboard = get_dashboard()
        return report_obj.render('toggl.dashboard', {'dashboard': dashboard})