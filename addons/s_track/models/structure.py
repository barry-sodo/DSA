from odoo import models, fields # type: ignore

class Structure(models.Model):
    _name = 'structure.structure'
    _description = 'Structure'

    name = fields.Char(string="Structure", required=True)
    description = fields.Text(string="Description")
