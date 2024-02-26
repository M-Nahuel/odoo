from odoo import api, models, fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class Offer(models.Model):
    _name = 'estate_offer'
    _description = 'Estate Offers'
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'El precio de oferta debe ser un numero mayor a 0'),
    ]

    price = fields.Float(string='Precio')
    status = fields.Selection([('accepted','Aceptada'),('refused','Rechazada')], copy=False)
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    property_id = fields.Many2one('estate', required=True)
    validity = fields.Integer(default=7, string='Validez')
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string='Expira')

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