{
    'name': 'Hospital Management System',
    'version': '1.0',
    'summary': 'Manage hospital patients',
    'author': 'HMS',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hms_patient_views.xml',
        'views/hms_department_views.xml',
        'views/hms_doctors_views.xml',
    ],
    'installable': True,
    'application': True,
}
