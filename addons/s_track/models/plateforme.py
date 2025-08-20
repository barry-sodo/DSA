from odoo import models, fields,api  # type: ignore

class Plateforme(models.Model):
    _name = 'plateforme.plateforme'
    _description = 'Plateforme TIC'

    name = fields.Char(string="plateforme", required=True)
    description = fields.Text(string="Description")
    structure_porteuse_ids = fields.Many2many('structure.structure', string="Structure métier porteuse")
    personnel_ids = fields.Many2many('personnel.personnel','plateforme_personnel_rel',  'plateforme_id', 'personnel_id',string="Équipe technique")
    code_source = fields.Char(string="Code source")
    plan_implantation = fields.Text(string="Plan d'implantation")
    disponibilite = fields.Boolean(string="Disponible ?", default=False)
    conformite_normes = fields.Boolean(string="Conforme aux normes ?", default=False)
    gouvernance = fields.Text(string="Instance de gouvernance")
    perenisation = fields.Text(string="Politique de pérennisation")
    bilan = fields.Text(string="Bilan de mise en œuvre")
    difficulte = fields.Text(string="Difficultés")
    solution_proposee = fields.Text(string="Solution proposée")
    satisfaction_usagers = fields.Text(string="Satisfaction des usagers")
    etat = fields.Selection([
        ('active', 'Actif'),
        ('inactive', 'Inactif'),
        ], string="État", default='inactive')
    
    def action_activer(self):
            self.ensure_one()
            self.etat = 'active'
            return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'res_id': self.id,
                'view_mode': 'form',
                'views': [(False, 'form')],
                'target': 'current',
            }

    def action_desactiver(self):
            self.ensure_one()
            self.etat = 'inactive'
            return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'res_id': self.id,
                'view_mode': 'form',
                'views': [(False, 'form')],
                'target': 'current',
            }
  