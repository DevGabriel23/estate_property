from odoo import models, fields

class estate_property_tag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Etiqueta de Propiedad'
    
    name = fields.Char(required=True)
    color = fields.Char(string='Color')
    