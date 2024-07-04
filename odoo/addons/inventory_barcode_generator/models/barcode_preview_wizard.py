from odoo import models, fields, api

class BarcodePreviewWizard(models.TransientModel):
    _name = 'barcode.preview.wizard'
    _description = 'Barcode Preview Wizard'

    product_id = fields.Many2one('product.template', string='Product', required=True)
    barcode_image = fields.Binary(related='product_id.barcode_image', string='Barcode Image', readonly=True)

    def action_print(self):
        return self.env.ref('inventory_barcode_generator.action_report_barcode').report_action(self.product_id)
