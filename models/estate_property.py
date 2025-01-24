from odoo import models, fields, api
from odoo.exceptions import UserError

class estate_property(models.Model):
    _name = 'estate.property'
    _description = 'Registro de Ventas'
    
    # Inherit mail.thread to add the "Chatter" feature
    _inherit = ['mail.thread']
    
    # SQL Constraints
    _sql_constraints = [
        (
            'check_property_expected_price', # Constraint name
            'CHECK(expected_price <= 0)', # SQL condition
            'El precio esperado debe ser estrictamente positivo.' # Error message
        ),
        ('check_property_selling_price', 'CHECK(selling_price <= 0)', 'El precio de venta debe ser positivo.'),
        ('unique_property_name', 'UNIQUE(name)', 'El nombre de la propiedad debe ser único.'),
    ]
    
    # Basic fields 
    name = fields.Char(required=True, tracking=True)
    description = fields.Text(string='Descripción')
    postcode = fields.Char(string='Código Postal')
    date_availability = fields.Date(string='Fecha de Disponibilidad')
    expected_price = fields.Float(string='Precio Esperado')
    selling_price = fields.Float(string='Precio de Venta', tracking=True)
    bedrooms = fields.Integer(string='Habitaciones')
    living_area = fields.Integer(string='Sala')
    facades = fields.Integer(string='Fachadas')
    garage = fields.Boolean(string='Garaje')
    garden = fields.Boolean(string='Jardín')
    garden_area = fields.Integer(string='Área de Jardín')
    garden_orientation = fields.Selection(
        string='Orientación del Jardín',
        selection=[
            ('norte', 'Norte'),
            ('sur', 'Sur'),
            ('este', 'Este'),
            ('oeste', 'Oeste')
        ]
    )
    
    # Fields that can only be changed with "Actions" (buttons)
    state = fields.Selection(
        string='Estado',
        selection=[
            ('cancel', 'Cancelado'),
            ('sold', 'Vendido')
        ],
        tracking=True,
    )
    
    # Computed fields
    area_total = fields.Float(string='Área Total', compute='_compute_area_total')
    best_price = fields.Float(string='Mejor Precio', compute='_compute_best_price', storage=True)
    best_price_partner = fields.Char(string='Mejor Comprador', compute='_compute_best_price', storage=True)
    
    # Relationships
    property_type_id = fields.Many2one("estate.property.type", string='Tipo de Propiedad')
    partner_id = fields.Many2one("res.partner", string='Buyer')
    user_id = fields.Many2one("res.users", string='Salesman', default=lambda self: self.env.user)
    
    tag_ids = fields.Many2many("estate.property.tag", string='Etiquetas')
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    
    # Compute methods
    @api.depends('living_area', 'garden_area')
    def _compute_area_total(self):
        for record in self:
            record.area_total = record.living_area + record.garden_area
        
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = 0
            record.best_price_partner = ''
            if record.offer_ids:
                price_partner = {offer.price: offer.partner_id.name for offer in record.offer_ids}
                record.best_price = max([offer.price for offer in record.offer_ids])
                record.best_price_partner = price_partner[record.best_price]
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = 'norte'
    
    # Methods
    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Las propiedades canceladas no pueden venderse.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Las propiedades vendidas no pueden cancelarse.")
        return self.write({"state": "canceled"})