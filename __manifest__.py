{
    'name': 'Venta de Bienes',
    'version': '0.1',
    'author': 'Gabriel Ramón',
    'description': 'Módulo de venta de bienes raíces',
    'depends': [
        'base',
        'account',
        'mail',
    ],
    'data': [
        "security/ir.model.access.csv",
        # Views for the estate_property module
        "views/estate_property_offer_view.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_property_view.xml",
        # Views for the freight.expense model
        "views/freight_expense_view.xml",
        # Views for the estate_menus model
        "views/estate_menus.xml",
    ],
    'application': True,
    'installable': True,
}