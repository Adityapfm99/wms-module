from odoo import models, fields, api

class BarcodeReading(models.TransientModel):
    _name = 'barcode.reading'
    _description = 'Barcode Reading'

    barcode = fields.Char(string="Barcode", required=True)

    @api.onchange('barcode')
    def _onchange_barcode(self):
        if self.barcode:
            product = self.env['product.product'].search([('barcode', '=', self.barcode)], limit=1)
            if product:
                return {
                    'name': 'Product',
                    'type': 'ir.actions.act_window',
                    'res_model': 'product.product',
                    'view_mode': 'form',
                    'res_id': product.id,
                    'target': 'current',
                }
            else:
                return {
                    'warning': {
                        'title': "No Product Found",
                        'message': "No product found with the given barcode."
                    }
                }
