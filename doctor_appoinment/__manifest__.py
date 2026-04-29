{
    'name': 'Doctor Management',
    'version': '1.0',
    'sequence': 1,
    'author': 'Swarup Mondal',
    'category': 'Services',
    'summary': 'Hospital Management System Odoo ',
    'depends': ['base', 'patient_management'],
    'license': 'LGPL-3',
    'data': [
        # XML views, menus, security, etc.
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/shadule.xml',
        'wizard/cancel_appointment_wizard_view.xml',
        'views/doctor_views.xml',
        'views/appointment_views.xml',
        'views/patient.xml',

        'reports/paper_formet_apt.xml',
        'reports/appointment_details.xml',
        'reports/doctor_card.xml',
        'reports/appointment_recipt.xml',



    ],
    'installable': True,
    'application': True,
}

