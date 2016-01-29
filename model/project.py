from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class project_project_report_methods(models.Model):
    _inherit = ['project.project']


    def print_report(self, cr, uid, ids, context=None):
        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'project_report', 'view_project_report_wizard_print')
        self.pool.get('project.report.wizard').reset_stats(cr, uid)
        return {
            'name':_("Print Service Report"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'project.report.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '',
            'context': {'project_ids': ids,}
        }

    def __get_project_report(self):
        cr = self.env.cr
        uid = self.env.user.id
        project_report_obj = self.pool.get('project.report')
        project_report_id = project_report_obj.search(cr, uid, [('id','=',1)])
        if project_report_id:
            return project_report_obj.browse(cr, uid, project_report_id[0])
        raise Exception('Project.report doesn\'t exists')

    def display_issues(self):
        return self.__get_project_report().issues
    def issues_type(self):
        return self.__get_project_report().issues_type
    def display_tasks(self):
        return self.__get_project_report().tasks
    def tasks_type(self):
        return self.__get_project_report().tasks_type
    def get_comments(self):
        return self.__get_project_report().comments
    def display_project_times(self):
        return self.__get_project_report().project_times
    def display_project_info(self):
        return self.__get_project_report().project_info
    def display_charts(self):
        return self.__get_project_report().show_chart