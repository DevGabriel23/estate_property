from odoo import models, fields

class estate_property_tag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Etiqueta de Propiedad'
    
    # SQL Constraints
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'El nombre de la etiqueta de propiedad debe ser único.'),
    ]
    
    name = fields.Char(required=True)
    color = fields.Char(string='Color')
    