from odoo import models, fields

class EstateTag(models.Model):
    _name = 'estate_tag'
    _description = 'Real Estate Tag'
    _order = 'name'
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'El nombre de la etiqueta debe ser unico'),
    ]

    name = fields.Char(string='Tags', required=True)
