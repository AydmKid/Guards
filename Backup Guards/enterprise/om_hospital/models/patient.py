from datetime import date
from odoo import api, fields, models

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = ""
    _rec_name = "name"

    name = fields.Char(string= "Name", tracking=True)
    date_of_brith = fields.Date(string="Date Of Birth")
    ref = fields.Char(string= "Refernce")
    age = fields.Integer(string = "Age", compute='_compute_age', tracking=True)
    gender = fields.Selection([('male','Male'),('female','Famele')] , string="Gender", tracking=True)
    active = fields.Boolean(string="Active" ,default=True)
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string = "Tags")
    
    @api.model
    def create(self,vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient,self).create(vals)

    @api.depends('date_of_brith')
    def _compute_age(self):
        print("self.....", self)
        for rec in self:
            today= date.today()
            if rec.date_of_brith:
                rec.age = today.year - rec.date_of_brith.year
            else:
                rec.age = 0