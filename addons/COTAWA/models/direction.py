from odoo import models, fields # type: ignore

class Direction(models.Model):
    _name = 'direction.direction'
    _description = 'Direction'
    
    name = fields.Char(string="Direction", required=True)
    description = fields.Text(string="Description")
    personnel_ids = fields.One2many('personnel.personnel', 'direction_id', string='Agents')
