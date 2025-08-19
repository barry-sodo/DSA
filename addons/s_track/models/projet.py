from odoo import models, fields,api # type: ignore
from odoo.exceptions import ValidationError # type: ignore

class Projet(models.Model):
    _name = "projet.projet"
    _description = "Projet"

    name = fields.Char(string="Projet", required=True)
    description = fields.Text(string="Description")
    personnel_ids = fields.Many2many('personnel.personnel', string="Assigné à")
    date_debut = fields.Date(string="Date de début")
    date_fin = fields.Date(string="Date de fin")
    tache_ids = fields.One2many('tache.tache', 'projet_id', string='Tâches')
    etat = fields.Selection([
        ('a_faire', 'À faire'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
    ], default='a_faire', string="État")
    @api.constrains('date_debut', 'date_fin')
    def _check_dates_coherence(self):
        for rec in self:
            if rec.date_debut and rec.date_fin and rec.date_debut > rec.date_fin:
                raise ValidationError("La date de début ne peut pas être postérieure à la date de fin.")
            

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