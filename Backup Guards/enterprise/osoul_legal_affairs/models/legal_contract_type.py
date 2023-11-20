from odoo import _, api, fields, models, tools

class LegalContractType(models.Model):
    _name = "osoul.legal.contract.type"
    _description = ""
    _rec_name = "contract_type"

    contract_type = fields.Char(string="Contract Type")