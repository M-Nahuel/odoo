from odoo import api, models, fields, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class RealEstate(models.Model):
    _name = "estate"
    _description = "Real Estate"
    _order = 'id desc'
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'El precio esperado debe ser un numero mayor a 0.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'El precio de venta debe ser un numero no negativo.'),
    ]

    name = fields.Char(default="Desconocido",string='Titulo', required=True)
    description = fields.Text(string='Descripcion')
    postcode = fields.Char(string='Codigo Postal')
    active = fields.Boolean(string='Activo', default=True)
    date_availability = fields.Date(string='Fecha de disponibilidad', default=lambda self: (datetime.today() + timedelta(days=90)).strftime('%Y-%m-%d'), copy=False)  # Fecha de disponibilidad predeterminada en 3 meses
    expected_price = fields.Float(string='Precio Esperado', required=True)
    selling_price = fields.Float(string='Precio de Venta', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Numero de Habitaciones', default=2)
    living_area = fields.Integer(string='Area Interior')
    facades = fields.Integer(string='Fachadas')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Jardin')
    garden_area = fields.Integer(string='Area del Jardin')
    garden_orientation = fields.Selection([('norte', 'Norte'), ('sur', 'Sur'), ('este', 'Este'), ('oeste', 'Oeste')], string='Orientacion del Jardin')
    state = fields.Selection([('nuevo', 'Nuevo'), ('oferta_recibida', 'Oferta recibida'), ('oferta_aceptada', 'Oferta aceptada'), ('vendido', 'Vendido'), ('cancelado', 'Cancelado')], string='Estado', default='nuevo', required=True)
    # type_id = fields.Many2one('estate_type', string='Tipo de propiedad')
    user_id = fields.Many2one('res.users', string='Vendedor', default=lambda self: self.env.user) #Verificar parametros a agregar
    buyer_id = fields.Many2one('res.partner', string='Comprador', copy=False) #Verificar parametros a agregar
    tag_ids = fields.Many2many('estate_tag', string='Tags')
    offer_ids = fields.One2many('estate_offer', 'property_id', string='Ofertas')
    total_area = fields.Char(compute='_compute_total', string='Area Total')
    best_price = fields.Char(compute='_compute_max_offer', string='Mejor Oferta')
    property_type_id = fields.Many2one('estate_type', string='Tipo de Propiedad')

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    @api.depends('offer_ids.price')
    def _compute_max_offer(self):
        for offer in self:
            #Agregar condicion para que agregue un precio por defecto porque no ingresa a los registros sin ofertas
            offer.best_price = max(offer.offer_ids.mapped('price')) if offer.offer_ids else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'norte'

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for rec in self:
            if (
                    not float_is_zero(rec.selling_price, precision_rounding=0.01)
                    and float_compare(rec.selling_price, rec.expected_price * 90.0 / 100.0,
                                      precision_rounding=0.01) < 0
            ):
                raise ValidationError('El precio de oferta no puede ser menor al 90% del precio esperado'
                )

    def action_sold(self):
        for propiedad in self:
            if propiedad.state != 'cancelado':
                propiedad.state = 'vendido'
            else:
                raise UserError(_('No puede vender esta propiedad porque ya ha sido cancelada'))

    def action_cancel(self):
        for propiedad in self:
            if propiedad.state != 'vendido':
                propiedad.state = 'cancelado'
            else:
                raise UserError(_('No puede cancelar esta propiedad porque ya ha sido vendida'))

    @api.ondelete(at_uninstall=False)
    def _check_delete(self):
        for prop in self:
            if prop.state not in ['nuevo', 'cancelado']:
                raise UserError("No se puede eliminar una propiedad con estado diferente a 'Nuevo' o 'Cancelado'")

