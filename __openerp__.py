{
    'name': "Project Report",
    'version': '1.2',
    'depends': ['report','project'],
    'author': "Quentin Tawry, AbAKUS it-solutions PGmbH",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'project',
    'description': 
    """
This modules adds a report and wizard on projects in order to print a beautiful report containing all information an data for this project.

It is possible to see Issues, Tasks (summarized or fully detailed) as well as charts for some inf.

This module has been developed by Quentin TAWRY @ AbAKUS it-solutions
    """,
    'data': [
        'wizard/project_report_view.xml',
        'view/project_project_view.xml',
        'project_report_data.xml',
        'report/project_report.xml',
        'security/ir.model.access.csv',
    ],
}
