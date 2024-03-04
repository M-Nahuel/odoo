from odoo import api, models, fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class Offer(models.Model):
    _name = 'estate_offer'
    _description = 'Estate Offers'
    _order = 'price desc'
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'El precio de oferta debe ser un numero mayor a 0'),
    ]

    price = fields.Float(string='Precio')
    status = fields.Selection([('accepted','Aceptada'),('refused','Rechazada')], copy=False)
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    property_id = fields.Many2one('estate', required=True)
    validity = fields.Integer(default=7, string='Validez')
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string='Expira')
    property_type_id = fields.Many2one('estate_type', related='property_id.property_type_id', string='Tipo de propiedad', store=True)

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    def action_accept(self):
        if 'accepted' in self.mapped('property_id.offer_ids.status'):
            raise UserError('La oferta ya ha sido aceptada')
        self.write(
            {
                'status': 'accepted',
            }
        )
        return self.mapped('property_id').write(
            {
                'state': 'oferta_aceptada',
                'selling_price': self.price,
                'buyer_id': self.partner_id.id,
            }
        )

    def action_decline(self):
        return self.write(
            {
                'status': 'refused',
            }
        )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            price = vals.get('price')
            existing_offers = self.search([('property_id', '=', property_id)])
            if existing_offers and any(price < offer.price for offer in existing_offers):
                raise UserError("No se puede crear una oferta con un monto menor que una oferta existente")
            property_record = self.env['estate'].browse(property_id)
            property_record.state = 'oferta_recibida'
        return super(Offer, self).create(vals_list)
