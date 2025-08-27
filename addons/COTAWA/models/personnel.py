from odoo import models, fields, api # type: ignore
import re
from odoo.exceptions import ValidationError # type: ignore

class Personnel(models.Model):
    _name = 'personnel.personnel'
    _description = 'Personnel'

    name = fields.Char(string="Nom", required=True)
    prenom = fields.Char(string="Prénom", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Numéro de téléphone", size=8)
    matricule = fields.Char(string="Matricule",readonly=True,copy=False,index=True)
    direction_id = fields.Many2one('direction.direction', string="Direction")
    image_1920 = fields.Image(string="Photo")
    display_name = fields.Char(string="Nom complet", compute="_compute_display_name", store=True)
    roles = fields.Selection([('agent', 'Agent'),('chef_service', 'Chef de service'),], string="Rôle", required=True, default='agent')
    user_id = fields.Many2one( 'res.users', string="Utilisateur lié",ondelete='set null')

    @api.depends('name', 'prenom')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name or ''} {rec.prenom or ''}".strip()

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email:
                pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                if not re.match(pattern, rec.email):
                    raise ValidationError("L'adresse e-mail est invalide.")

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and not re.match(r'^\d{8}$', record.phone):
                raise ValidationError("Le numéro de téléphone doit contenir 8 chiffres.")

    def _assign_user_group(self, user, role):
        agent_group = self.env.ref('COTAWA.group_agent')
        chef_group = self.env.ref('COTAWA.group_chef_service')

        if role == 'agent':
            group = agent_group
        elif role == 'chef_service':
            group = chef_group
        else:
            group = False

        if group and user:
            user.groups_id = [(3, agent_group.id), (3, chef_group.id)]
            user.groups_id = [(4, group.id)]

  
    @api.model
    def create(self, vals):
        if not vals.get('matricule'):
            vals['matricule'] = self.env['ir.sequence'].next_by_code('personnel.personnel') or '/'

        if not vals.get('user_id') and vals.get('email'):
            user_vals = {
                'name': f"{vals.get('name', '')} {vals.get('prenom', '')}".strip(),
                'login': vals['email'],
                'email': vals['email'],
            }
            user = self.env['res.users'].create(user_vals)
            vals['user_id'] = user.id

        record = super(Personnel, self).create(vals)
        if record.user_id and record.roles:
            record._assign_user_group(record.user_id, record.roles)

        if record.user_id:
            template = self.env.ref('COTAWA.mail_template_user_signup_custom', raise_if_not_found=False)
            if template:
                user_singleton = self.env['res.users'].browse(record.user_id.id)
                template.with_user(self.env.user).send_mail(user_singleton.id, force_send=True)

        return record

    def write(self, vals):
        res = super(Personnel, self).write(vals)

        for record in self:
            if not record.user_id and (vals.get('email') or record.email):
                email = vals.get('email') or record.email
                user_vals = {
                    'name': f"{record.name} {record.prenom}".strip(),
                    'login': email,
                    'email': email,
                }
                user = self.env['res.users'].create(user_vals)
                record.user_id = user.id
                record._assign_user_group(user, record.roles)

                template = self.env.ref('COTAWA.mail_template_user_signup_custom', raise_if_not_found=False)
                if template:
                    user_singleton = self.env['res.users'].browse(record.user_id.id)
                    template.with_user(self.env.user).send_mail(user_singleton.id, force_send=True)
                    
            elif ('roles' in vals or 'user_id' in vals) and record.user_id and record.roles:
                record._assign_user_group(record.user_id, record.roles)

        return res
