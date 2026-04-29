{
    'name': 'Hospital Management',
    'version': '1.0',
    'sequence': 1,
    'author': 'Swarup Mondal',
    'category': 'Services',
    'summary': 'Hospital Management System Odoo Practice Project',
    'depends': ['mail','base',],
    'data': [
        # XML views, menus, security, etc.
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/patient_views.xml',
        'reports/paper_formet.xml',
        'reports/patient_details_report.xml',
        'reports/patient_report.xml',



    ],
    'installable': True,
    'application': True,
}

