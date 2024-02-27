from odoo import models, fields

class EstateType(models.Model):
    _name = 'estate_type'
    _description = 'Real Estate Type'
    _order = 'name'
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'El tipo de propiedad debe ser unico'),
    ]

    name = fields.Char(string='Nombre', required=True)
    property_ids = fields.One2many("estate", "type_id", string='Propiedades')