{
    'name': 'Inventory Barcode Generator',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Generate barcodes for inventory products',
    'description': """
        This module allows users to generate barcodes for products in the inventory.
    """,
    'author': 'Aditya',
    'depends': ['base','stock','product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'security/barcode_inventory_move_security.xml',
        'report/product_barcode_report.xml',
        'report/product_barcode_report_template.xml',
        'views/barcode_inventory_move_wizard_view.xml',
        'views/barcode_preview_wizard_view.xml', 
        'views/inventory_views.xml',
        'views/barcode_inventory_move_view.xml',
        'views/barcode_inventory_move_menu.xml',
       
       
    ],
    'installable': True,
    'application': False,
}
