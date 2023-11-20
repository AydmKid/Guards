from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class LegalContracts(models.Model):
    _name = "osoul.legal.contracts"
    _description = ""
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "contract_no"

    contract_date = fields.Date(string="Contract Date", tracking=True)
    contract_subject = fields.Char(string="Contract Subject", tracking=True)
    contract_no = fields.Char(string="Contract Number", tracking=True)
    first_party = fields.Selection(
        [("arabian_co", "Arabian Co"), ("assir_poultry", "Assir Poultry")],
        default="arabian_co",
        tracking=True,
    )
    second_party = fields.Many2one(
        comodel_name="res.partner",
        string="Second party",
        tracking=True,
        ondelete="restrict",
    )
    vat = fields.Char(related="second_party.vat")
    mobile = fields.Char(related="second_party.mobile")
    company_type = fields.Selection(related="second_party.company_type")
    first_party_responsable = fields.Many2one(
        comodel_name="res.users",
        string="First Party Responsable",
        tracking=True,
        ondelete="restrict",
    )
    second_party_responsable = fields.Many2one(
        comodel_name="res.partner",
        string="Second Party Responsable",
        tracking=True,
        ondelete="restrict",
    )
    contract_type = fields.Many2one(
        comodel_name="osoul.legal.contract.type",
        string="Contract Type",
        tracking=True,
        ondelete="restrict",
    )
    contract_conditions = fields.Text(string="Contract Conditions", tracking=True)
    contract_fees = fields.Float(string="Contract Fees", tracking=True)
    contract_file = fields.Binary(string="Contract File", tracking=True)
    contract_start_date = fields.Date(string="Contract Start Date", tracking=True)
    contract_end_date = fields.Date(string="Contract End Date", tracking=True)
    contract_period = fields.Integer(
        string="Contract Period", compute="_compute_contract_period", store=True
    )
    contract_end_counter = fields.Integer(
        compute="_compute_contract_end_counter", store=True
    )
    end_contract_alarm = fields.Date(string="Contract Alarm", tracking=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("contract_running", "Contract Running"),
            ("contract_end", "Contract End"),
            ("contract_cancelled", "Contract Cancelled"),
        ],
        default="draft",
        tracking=True,
    )

    @api.depends("contract_start_date", "contract_end_date")
    def _compute_contract_period(self):
        for record in self:
            if record.contract_start_date and record.contract_end_date:
                period = record.contract_end_date - record.contract_start_date
                if period.days < 0:
                    raise ValidationError(
                        "Contract Start Date cannot be later than Contract End Date"
                    )
                record.contract_period = period.days
            else:
                record.contract_period = 0

    @api.depends("contract_end_date")
    def _compute_contract_end_counter(self):
        today = fields.Date.today()
        for record in self:
            if record.contract_end_date:
                remaining_days = record.contract_end_date - today
                record.contract_end_counter = remaining_days.days
            else:
                record.contract_end_counter = 0

    def action_button_contract_running(self):
        self.state = "contract_running"

    def action_button_contract_end(self):
        self.state = "contract_end"

    def action_button_contract_cancelled(self):
        self.state = "contract_cancelled"
