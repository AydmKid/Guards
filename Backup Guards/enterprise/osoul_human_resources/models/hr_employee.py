from odoo import _, api, fields, models, tools


class OsoulHumanResources(models.Model):
    _inherit = 'hr.employee'

    management_name = fields.Many2one(comodel_name="osoul.hr.managements", string="Management", ondelete='restrict', tracking=True)
    # HUMAN RESOURCES
    employment_no = fields.Char(string="Employment No", tracking=True)
    #emp_no_id = fields.Many2one('osoul.security.supplier.enter.permission',string="Emp No", tracking=True)
    e_name = fields.Many2one(string='name',comodel_name='osoul.security.supplier.enter.permission',ondelete='restrict')
    hire_date = fields.Date(string="Hire Date", tracking=True)
    join_date = fields.Date(string="Join Date", tracking=True)
    contracting_party = fields.Many2one(comodel_name="osoul.hr.contractors", string="Contracting Party", ondelete='restrict', tracking=True)
    # PRIVATE INFORMATION
    citizen = fields.Selection([('citizen', 'Citizen'), ('not_citizen', 'Not Citizen')], string="Citizen", tracking=True)
    religion = fields.Selection([('muslim', 'Muslim'), ('not_muslim', 'Not Muslim')], string="Religion", tracking=True)
    # ACCOMMODATION
    housing = fields.Selection([('hosted', 'Hosted'), ('not_hosted', 'Not Hosted')], default="not_hosted", readonly=True, tracking=True)
    # SECURITY 
    in_out_status = fields.Selection([('draft', 'Draft'),
                                      ('inside_osoul', 'Inside Osoul'),
                                      ('outside_osoul', 'Outside Osoul')], default="draft", readonly=True, tracking=True)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        domain = args + ['|', ("employment_no", operator, name), ("name", operator, name)]
        return super(OsoulHumanResources, self).search(domain, limit=limit).name_get()
        