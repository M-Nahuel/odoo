from odoo import models, fields

class ResUsers(models.Model):
        _inherit = 'res.users'

        property_ids = fields.One2many(
            'estate', 'user_id', string='Propiedades', domain=[('state', 'in', ['nuevo', 'oferta_recibida'])]
        )

        # property_ids = fields.One2many(
        #     'estate',  # Modelo al que se está haciendo referencia
        #     'user_id',  # Campo Many2one en 'estate' que hace referencia a 'res.users'
        #     string='Propiedades'  # Etiqueta del campo en la interfaz
        # domain = "[('state', 'in', ['nuevo', 'cancelado'])]"  # Filtro para mostrar solo propiedades disponibles
        # )
