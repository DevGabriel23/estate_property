from odoo import fields, models

class freight_expense(models.Model):
    _name = 'freight.expense'
    _description = 'Gastos de Flete'
    
    _inherit = ['account.move']
    
    maintenance_expense = fields.Float(string='Gastos de mantenimiento')
    authorized_expense = fields.Float(string='Gasto autorizado')