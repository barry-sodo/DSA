{
    'name': 'S-Track',
    'version': '1.0',
    'summary': 'Suivi des tâches et des plateformes',
    'author': 'ANPTIC, Burkina Faso',
    'category': 'Tools',
    'depends': [    
    'base',
    'spreadsheet_dashboard',
    'web',
    'mail',
    'auth_signup',

],
    'data': [
           'views/signup_custom.xml',
        'security/s_track_security.xml',
        'security/ir.model.access.csv',
          'data/sequence.xml', 
             
    'views/plateforme_views.xml',
    'views/session_views.xml',
    'views/projet_views.xml',
    'views/tache_views.xml',
    'views/rapport_views.xml',
    'views/structure_views.xml',
    'views/personnel_views.xml',
    'views/direction_views.xml',
    'views/s_track_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
        's_track/static/src/css/style.css',
     
          
        ],
    },
    'application': True,
}
