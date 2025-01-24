from odoo import models, fields

class estate_property_type(models.Model):
    _name = 'estate.property.type'
    _description = 'Tipo de Propiedad'
    
    # SQL Constraints
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'El nombre del tipo de propiedad debe ser único.'),
    ]
    
    name = fields.Char(required=True)