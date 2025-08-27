from odoo import models, fields  # type: ignore

class Rapport(models.Model):
    _name = 'rapport.rapport'
    _description = 'Rapport'

    name = fields.Char(string='Rapport', required=True)
    session_id = fields.Many2one(
    'session.session',
    string="Session",
    default=lambda self: self.env['session.session'].search([('etat', '=', 'active')], limit=1),
    required=True
)

    contenu = fields.Text(string="Contenu", required=True)
