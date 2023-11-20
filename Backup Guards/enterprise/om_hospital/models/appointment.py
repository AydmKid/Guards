from odoo import api, fields, models

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital.Appointment"
    _rec_name = "patient_id"
    
    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient")
    gender = fields.Selection([('male','Male'),('female','Famele')] , string="Gender", related='patient_id.gender')
    appointment_time = fields.Datetime(string="Appointment Time", default=fields.Datetime.now)
    bookinf_date = fields.Date(string="booking Date", default=fields.Date.context_today)
    ref = fields.Char(string="Reference")
    perscription = fields.Html(string="Perscription")
    priority  = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state  = fields.Selection([
        ('draft', 'draft'),
        ('in_consultation', 'in_consultation'),
        ('done', 'done'),
        ('cancelled', 'cancelled')], default='draft', string="Status", required = True)
    doctor_id  = fields.Many2one('res.users', string="Docotor")
    pharmacy_line_ids  = fields.One2many('appointment.pharmacy.lines','appointment_id', string="Pharmacy Lines")
    hide_sales_price = fields.Boolean(string="Side Sales Prcie")
    progress = fields.Integer(string="Progress", compute="_compute_progress")


    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        print("Button Clicked !")
        return{
            'effect':{
                
                'message':'Click Successfull',
                'type' : 'rainbow_man'
            }
        }

    def action_notification(self):
       for rec in self:
        rec.name.user_id.notify_success(message="hello")
    
    def action_in_consiltation(self):
        for rec in self:
            rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
    
    def action_in_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == "draft":
                progress = 25
            elif rec.state == "in_consultation":
                progress = 50
            elif rec.state == "done":
                progress = 100
            else :
                progress = 0 
            rec.progress = progress


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment.Pharmacy"

    porduct_id = fields.Many2one('product.product')
    price_unit = fields.Float(string="Price")
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment',string="Appointment")