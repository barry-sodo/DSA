from odoo import models, fields, api # type: ignore
from odoo.exceptions import ValidationError # type: ignore

class Tache(models.Model):
    _name = 'tache.tache'
    _description = 'Tâche de suivi de projet'

    name = fields.Char(string='Taches', required=True)
    projet_id = fields.Many2one('projet.projet', string='Projet')
    session_id = fields.Many2one(
    'session.session',
    string="Session",
    required=True,
    domain=[('etat', '=', 'active')],  
    default=lambda self: self.env['session.session'].search([('etat', '=', 'active')], limit=1)
)

    date_debut = fields.Date(string="Date de début", required=True)
    date_fin = fields.Date(string="Date de fin", required=True)

    #personnel_ids = fields.Many2many('personnel.personnel', string="Assigné à")
    synthese_realisation = fields.Text(string="Synthèse de réalisation")
    etat = fields.Selection([
        ('a_faire', 'À faire'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
    ], default='a_faire', string="État")

    def action_demarrer(self):
        self.ensure_one()
        self.etat = 'en_cours'
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'current',
        }

    def action_terminer(self):
        self.ensure_one()
        self.etat = 'terminee'
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'current',
        }

    def action_revenir_encours(self):
        self.ensure_one()
        self.etat = 'en_cours'
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'current',
        }
    @api.constrains('date_debut', 'date_fin', 'projet_id', 'session_id')
    def _check_date_within_project_or_session(self):
        for rec in self:

            if rec.date_debut and rec.date_fin and rec.date_debut > rec.date_fin:
                raise ValidationError("La date de début doit être inférieure à la date de fin.")

            if rec.projet_id and rec.date_debut and rec.date_fin:
                if (rec.date_debut < rec.projet_id.date_debut) or (rec.date_fin > rec.projet_id.date_fin):
                    raise ValidationError("Les dates de la tâche doivent être comprises dans la période du projet.")

            elif rec.session_id and rec.date_debut and rec.date_fin:
                if (rec.date_debut < rec.session_id.date_debut) or (rec.date_fin > rec.session_id.date_fin):
                    raise ValidationError("Les dates de la tâche doivent être comprises dans la période de la session.")
 