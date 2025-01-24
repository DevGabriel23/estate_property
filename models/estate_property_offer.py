
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta de Propiedad"
    
    price = fields.Float(string='Precio', required=True)
    status = fields.Selection(
        string='Estado',
        selection=[
            ('accepted', 'Aceptada'),
            ('refused', 'Rechazada')
        ]
    )
    validity = fields.Integer(string='Validez (días)', default=7)

    # Relationship
    partner_id = fields.Many2one('res.partner', string='Comprador', required=True, domain=[('customer_rank', '>', 0)])
    property_id = fields.Many2one('estate.property', string='Propiedad', required=True)

    
    # Compute fields
    deadline = fields.Date(string='Fecha Límite', compute='_compute_deadline', inverse='_inverse_deadline')
    
    # Computed methods
    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.deadline = date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.deadline - date).days
    
    # Methods
    def action_confirm(self):
        # Check if the offer is still valid
        if "refused" in self.mapped("status"):
            raise UserError("Las ofertas rechazadas no pueden aceptarse.")
        
        # Refuse all other offers
        for record in self.property_id.offer_ids:
            record.status = 'refused'
        
        # Update property data
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id.id
        
        return self.write({"status": "accepted"})
    
    def action_refuse(self):
        self.status = 'refused'