{
    'name': 'Hospital Managemanet',
    'version': '1.0.0',
    'category': 'Osoul Public Utility',
    'summary': 'Osoul Hospital Management System',
    'description': 'Osoul Hospital Management System',
    'author': 'Osoul Information Technology',
    'depends': ['mail','product'],
    'data': ['menu/menu.xml',
             'views/patient.xml',
             'views/female_patient_view.xml',
             'views/appointment_view.xml',
             'views/patient_tag.xml',
             'wizard/cancel_appointment_view.xml',
             'data/sequence_data.xml',],
    'demo': [],
    'qweb':[],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': -5,
    'license': 'LGPL-3'
}