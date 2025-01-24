from odoo import models, fields

class estate_property_type(models.Model):
    _name = 'estate.property.type'
    _description = 'Tipo de Propiedad'
    
    name = fields.Char(required=True)