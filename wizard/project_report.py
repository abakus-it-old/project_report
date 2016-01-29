from openerp import models, fields, api, _
from openerp.osv import osv

class project_report(models.Model):
    _name = 'project.report'

    project_info = fields.Boolean(string="Show the project info")

    project_times = fields.Boolean(string="Show the project times    ")

    start_date = fields.Date(string="Start date")
    end_date = fields.Date(string="End date")
    date_application_creation = fields.Boolean(string="Created tasks/issues")
    date_application_modified = fields.Boolean(string="Modified tasks/issues")
    date_application_closed = fields.Boolean(string="Closed tasks/issues")

    show_chart = fields.Boolean(string="Show Chart")

    tasks = fields.Boolean(string="Tasks")
    tasks_type = fields.Selection([('summary','Summary'),('detailled', 'Detailled')], string='Task type')
    tasks_order = fields.Selection(['All','all'], string="Order by")
    tasks_stage = fields.Selection([("All", "all"), ("Open", "open"), ("Done & Cancelled", "closed")], string="Stages")

    issues = fields.Boolean(string="Issues")
    issues_type = fields.Selection([('summary','Summary'),('detailled', 'Detailled')], string='Issue type')
    issues_order = fields.Selection(['All','all'], string="Order by")
    issues_stage = fields.Selection([("All", "all"), ("Open", "open"), ("Done & Cancelled", "closed")], string="Stages")

    comments = fields.Text(string="Comments")

class project_report_wizard(osv.osv_memory):
    
    def _default_start_date(self):
        cr = self.env.cr
        uid = self.env.user.id
        contract_report_obj = self.pool.get('project.report')
        contract_report_id = contract_report_obj.search(cr, uid, [('id','=',1)])
        if contract_report_id:
            contract_report = contract_report_obj.browse(cr, uid, contract_report_id[0])
            if contract_report and contract_report[0].start_date:
                return contract_report[0].start_date
    
    def _default_end_date(self):
        cr = self.env.cr
        uid = self.env.user.id
        contract_report_obj = self.pool.get('project.report')
        contract_report_id = contract_report_obj.search(cr, uid, [('id','=',1)])
        if contract_report_id:
            contract_report = contract_report_obj.browse(cr, uid, contract_report_id[0])
            if contract_report and contract_report[0].end_date:
                return contract_report[0].end_date
        #return date.today().strftime('%Y-%m-%d')

        
    def save(self, cr, uid, ids, context=None):
        project_report_wizard=self.browse(cr,uid,ids[0])
        project_report_obj = self.pool.get('project.report')
        #contract.report with id 1 is created in project_report.xml as record
        project_report_obj.write(cr,uid,1,{'start_date' : project_report_wizard.start_date,
                                            'end_date':project_report_wizard.end_date,

                                            'project_info':project_report_wizard.project_info,
                                            'project_times':project_report_wizard.project_times,
                                            'date_application_creation':project_report_wizard.date_application_creation,
                                            'date_application_modified':project_report_wizard.date_application_modified,
                                            'date_application_closed':project_report_wizard.date_application_closed,

                                            'show_chart':project_report_wizard.show_chart,
                                            'tasks':project_report_wizard.tasks,
                                            'tasks_order':project_report_wizard.tasks_order,
                                            'tasks_stage':project_report_wizard.tasks_stage,
                                            'tasks_type':project_report_wizard.tasks_type,
                                            'issues':project_report_wizard.issues,
                                            'issues_order':project_report_wizard.issues_order,
                                            'issues_stage':project_report_wizard.issues_stage,
                                            'issues_type':project_report_wizard.issues_type,
                                            'comments':project_report_wizard.comments
                                           })
        return {
                'type': 'ir.actions.act_window_close',
               }
               
               
    def reset_stats(self, cr, uid):
        self.pool.get('project.report').write(cr,uid,1,{   'start_date' : None,
                                                            'end_date': None
                                                        })

    def print_report(self, cr, uid, ids, context=None):
        self.save(cr, uid, ids, context)
        account_ids = context.get('project_ids')
        return self.pool['report'].get_action(cr, uid, account_ids, 'project_report.report_project', context=context)

    _name = 'project.report.wizard'

    start_date = fields.Date(string="Start date", default=_default_start_date)
    end_date = fields.Date(string="End date", default=_default_end_date)

    project_info = fields.Boolean(string="Show the project info")
    project_times = fields.Boolean(string="Show the project times    ")

    date_application_creation = fields.Boolean(string="Created tasks/issues")
    date_application_modified = fields.Boolean(string="Modified tasks/issues")
    date_application_closed = fields.Boolean(string="Closed tasks/issues")

    show_chart = fields.Boolean(string="Show Chart")

    tasks = fields.Boolean(string="Tasks")
    tasks_type = fields.Selection([('summary','Summary'),('detailled', 'Detailled')], string='Task type')
    tasks_order = fields.Selection([('All','all')], string="Order by")
    tasks_stage = fields.Selection([("all", "All"), ("open", "Open"), ("closed", "Done & Cancelled")], string="Stages")

    issues = fields.Boolean(string="Issues")
    issues_type = fields.Selection([('summary','Summary'),('detailled', 'Detailled')], string='Issue type')
    issues_order = fields.Selection([('All','all')], string="Order by")
    issues_stage = fields.Selection([("all", "All"), ("open", "Open"), ("closed", "Done & Cancelled")], string="Stages")

    comments = fields.Text(string="Comments")