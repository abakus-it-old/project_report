from openerp import models, fields, api, _
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class project_project_report_methods(models.Model):
    _inherit = ['project.project']


    def print_report(self, cr, uid, ids, context=None):
        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'project_report', 'view_project_report_wizard_print')
        #self.pool.get('project.report.wizard').reset_stats(cr, uid)
        return {
            'name':_("Print Service Report"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'project.report.wizard',
            'res_id': 1,
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
    def issues_stage(self):
        return self.__get_project_report().issues_stage

    def display_tasks(self):
        return self.__get_project_report().tasks
    def tasks_type(self):
        return self.__get_project_report().tasks_type
    def tasks_stage(self):
        return self.__get_project_report().tasks_stage

    def get_comments(self):
        return self.__get_project_report().comments

    def display_project_times(self):
        return self.__get_project_report().project_times
    def display_project_info(self):
        return self.__get_project_report().project_info

    def display_charts(self):
        return self.__get_project_report().show_chart

    def startdate(self):
        return self.__get_project_report().start_date
    def enddate(self):
        return self.__get_project_report().end_date


    def date_application_creation(self):
        return self.__get_project_report().date_application_creation
    def date_application_modified(self):
        return self.__get_project_report().date_application_modified
    def date_application_closed(self):
        return self.__get_project_report().date_application_closed

    def get_filter_issues(self):
        filter = ['&']

        startdate = self.startdate() if self.startdate() else datetime.now().strftime('%y-%m%d')
        enddate = self.enddate() if self.enddate() else datetime.now().strftime('%y-%m%d')
        created = self.date_application_creation()
        modified = self.date_application_modified()
        closed = self.date_application_closed()

        filter.append(('project_id','=',self.id))

        count = 0 + created + modified + closed
        if (count>=2):
            filter.append('|') # if >= 2

        if created:
            filter.append('&')
            filter.append(('create_date', '>=',startdate))
            filter.append(('create_date','<=',enddate))

        if count == 3:
            filter.append('|') # if = 3

        if modified:
            filter.append('&')
            filter.append(('write_date', '>=',startdate))
            filter.append(('write_date','<=',enddate))
        if closed:
            filter.append('&')
            filter.append(('date_closed', '>=',startdate))
            filter.append(('date_closed','<=',enddate))

        if self.issues_stage() == 'open':
            filter.append(('stage_id.closed', '=', False))
        elif self.issues_stage() == 'closed':
            filter.append(('stage_id.closed', '=', True))
        _logger.debug(filter)

        return filter

    def get_filter_tasks(self):
        filter = ['&']

        startdate = self.startdate() if self.startdate() else datetime.now().strftime('%y-%m%d')
        enddate = self.enddate() if self.enddate() else datetime.now().strftime('%y-%m%d')
        created = self.date_application_creation()
        modified = self.date_application_modified()
        closed = self.date_application_closed()

        filter.append(('project_id','=',self.id))

        count = 0 + created + modified + closed
        if (count>=2):
            filter.append('|') # if >= 2

        if created:
            filter.append('&')
            filter.append(('create_date', '>=',startdate))
            filter.append(('create_date','<=',enddate))

        if count == 3:
            filter.append('|') # if = 3

        if modified:
            filter.append('&')
            filter.append(('write_date', '>=',startdate))
            filter.append(('write_date','<=',enddate))
        if closed:
            filter.append('&')
            filter.append(('date_end', '>=',startdate))
            filter.append(('date_end','<=',enddate))
        if self.tasks_stage() == 'open':
            filter.append(('stage_id.closed', '=', False))
        elif self.tasks_stage() == 'closed':
            filter.append(('stage_id.closed', '=', True))
        _logger.debug(filter)

        return filter
        #return ['&', ('create_date', '>=', '2016-02-11'), ('create_date', '<=', '2016-02-11')]

    @api.multi
    def get_issues_for_report(self):
        cr = self.env.cr
        uid = self.env.user.id
        project_issues = self.pool.get('project.issue').search(cr, uid, self.get_filter_issues())
        project_issues = self.pool.get('project.issue').browse(cr,uid,project_issues)
        _logger.debug('Issues : ')
        _logger.debug(project_issues)
        return project_issues

    @api.multi
    def get_tasks_for_report(self):
        cr = self.env.cr
        uid = self.env.user.id
        project_tasks = self.pool.get('project.task').search(cr, uid, self.get_filter_tasks())
        project_tasks = self.pool.get('project.task').browse(cr,uid,project_tasks)
        _logger.debug('Tasks : ')
        _logger.debug(project_tasks)
        return project_tasks
