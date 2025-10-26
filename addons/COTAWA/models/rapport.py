from odoo import models, fields, api # type: ignore

class Rapport(models.Model):
    _name = 'rapport.rapport'
    _description = 'Rapport'
    _rec_name = 'name'

    name = fields.Char(
        string='Titre du rapport',
        required=True,
        help="Titre du rapport ou résumé du contenu."
    )

    session_id = fields.Many2one(
        'session.session',
        string="Session",
        required=True,
        default=lambda self: self.env['session.session'].search([('etat', '=', 'active')], limit=1),
        help="Session liée à ce rapport."
    )

    contenu = fields.Html(
        string="Contenu du rapport",
        required=True,
        help="Contenu détaillé du rapport avec mise en forme HTML."
    )

    date_creation = fields.Datetime(
        string="Date de création",
        default=fields.Datetime.now,
        readonly=True
    )

    auteur_id = fields.Many2one(
        'res.users',
        string="Auteur",
        default=lambda self: self.env.user,
        readonly=True
    )

    def action_export_pdf(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": f"/rapport/{self.id}/pdf",
            "target": "new",  
        }
