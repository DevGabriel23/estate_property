{
    'name': 'Venta de Bienes',
    'version': '0.1',
    'author': 'Gabriel Ramón',
    'description': 'Módulo de venta de bienes raíces',
    'depends': [
        'base',
        'account',
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/estate_property_offer_view.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_property_view.xml",
        "views/estate_menus.xml",
    ],
    'application': True,
    'installable': True,
}