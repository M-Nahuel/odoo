from odoo import models, fields

class EstateType(models.Model):
    _name = 'estate_type'
    _description = 'Real Estate Type'
    _order = 'name'
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'El tipo de propiedad debe ser unico'),
    ]

    name = fields.Char(string='Nombre', required=True)
    property_ids = fields.One2many("estate", "property_type_id", string='Propiedades')
    # sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.Many2many("estate_offer", string="Ofertas", compute="_compute_offer")
    offer_count = fields.Integer(compute='_compute_offer', string='Contador')


    def _compute_offer(self):
        data = self.env['estate_offer'].read_group(
            [('property_id.state', '!=', 'cancelado'), ('property_type_id', '!=', False)],
            ['ids:array_agg(id)', 'property_type_id'],
            ['property_type_id'],
        )
        mapped_count = {d['property_type_id'][0]: d['property_type_id_count'] for d in data}
        mapped_ids = {d['property_type_id'][0]: d['ids'] for d in data}
        for prop_type in self:
            prop_type.offer_count = mapped_count.get(prop_type.id, 0)
            prop_type.offer_ids = mapped_ids.get(prop_type.id, [])

    def action_view_offers(self):
        res = self.env.ref('estate.estate_offer_action').read()[0]
        res['domain'] = [('id', 'in', self.offer_ids.ids)]
        return res