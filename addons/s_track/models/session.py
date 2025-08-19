from odoo import models, fields, api # pyright: ignore[reportMissingImports]

class Session(models.Model):
    _name = 'session.session'
    _description = 'Session'

    name = fields.Char(string="session", readonly=True)
    date_debut = fields.Date(string="Date de début", required=True)
    date_fin = fields.Date(string="Date de fin", required=True)
    etat = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string="État", default='active')

  
    def action_activer(self):
            """Définit l'état sur 'active' et recharge la vue."""
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
            """Définit l'état sur 'inactive' et recharge la vue."""
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



    @api.onchange('date_debut', 'date_fin')
    def _onchange_dates(self):
        if self.date_debut and self.date_fin:
            if self.date_debut > self.date_fin:
                return {
                    'warning': {
                        'title': "Erreur",
                        'message': "La date de début doit être inférieure à la date de fin."
                    }
                }
            self.name = self._generate_name_from_dates()

    def _generate_name_from_dates(self):
        mois_fr = {
            1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril",
            5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août",
            9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
        }
        debut = self.date_debut
        fin = self.date_fin
        return f"{debut.day} {mois_fr[debut.month]} {debut.year} AU {fin.day} {mois_fr[fin.month]} {fin.year}"

    @api.model
    def create(self, vals):
        record = self.new(vals)
        if record.date_debut and record.date_fin:
            vals['name'] = record._generate_name_from_dates()
        return super().create(vals)

    def write(self, vals):
     res = super().write(vals)
     if 'date_debut' in vals or 'date_fin' in vals:
        for rec in self:
            new_name = rec._generate_name_from_dates()
            super(type(rec), rec).write({'name': new_name})  # appel direct à super pour éviter boucle
     return res
   
   