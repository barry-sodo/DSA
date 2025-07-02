{
    'name': "login",
    'version': '1.0',
    'summary': "Personnalisation simple de la page de connexion avec logo",
    'description': "Module pour créer une page de connexion personnalisée dans Odoo, incluant un logo et un formulaire stylisé.",
    'author': "Saf",
    'category': 'Tools',
    'depends': ['base', 'web'],
   'data': [
    'views/login_templates.xml',
],
'assets': {
    'web.assets_frontend': [
        'login/static/src/css/login_styles.css',
    ],
},

    'installable': True,
    'application': False,
  
}
