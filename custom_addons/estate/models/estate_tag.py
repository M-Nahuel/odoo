from odoo import models, fields

class EstateTag(models.Model):
    _name = 'estate_tag'
    _description = 'Real Estate Tag'

    name = fields.Char(string='Tags', required=True)

    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'El nombre de la etiqueta debe ser unico')
    ]