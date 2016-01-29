from openerp import models, fields, api, _
import datetime
from datetime import date
import pytz

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