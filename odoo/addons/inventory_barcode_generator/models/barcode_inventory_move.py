import logging

_logger = logging.getLogger(__name__)

from odoo import models, fields, api
from odoo.exceptions import UserError

class BarcodeInventoryMove(models.TransientModel):
    _name = 'barcode.inventory.move'
    _description = 'Barcode Inventory Move'

    barcode = fields.Char(string="Barcode")
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string="Quantity", required=True, default=1.0)
    location_id = fields.Many2one('stock.location', string="Source Location",store=True)
    location_dest_id = fields.Many2one('stock.location', string="Destination Location")
    move_line_ids = fields.One2many('barcode.inventory.move.line', 'barcode_inventory_move_id', string='Move Lines')


    @api.onchange('barcode')
    def _onchange_barcode(self):

        if self.barcode:
            _logger.info(f"Searching for product with barcode: {self.barcode}")
            product = self.env['product.product'].search([('barcode', '=', self.barcode)], limit=1)
            _logger.info(f"Product search result: {product.id if product else 'None'}")
            if product:
                _logger.info(f"Product found: {product.name}")
                location_id = self._get_latest_product_location(product.id)
                if location_id:
                    _logger.info(f"Latest stock quant location: {location_id.id}")
                else:
                    _logger.info("No stock quant found for the product.")
                
                new_line = {
                    'product_id': product.id,
                    'quantity': 1.0,  
                    'location_id': location_id.id if location_id else False,
                    'location_dest_id': self.location_dest_id.id if self.location_dest_id else False,
                    'barcode': self.barcode
                }
                self.update({'move_line_ids': [(0, 0, new_line)]})
                self.barcode = ''
            else:
                _logger.info("No product found")
                return {
                    'warning': {
                        'title': "No Product Found",
                        'message': "No product found with the given barcode."
                    }
                }

    def _get_latest_product_location(self, product_id):
        stock_quant = self.env['stock.quant'].search([('product_id', '=', product_id)], limit=1, order='in_date desc')
        return stock_quant.location_id if stock_quant else False
    
    def action_move_inventory1(self):
        if not self.location_dest_id:
            raise UserError("Please select a destination location first1.")
        if not self.move_line_ids:
            raise UserError("No products to move.")

        for line in self.move_line_ids:
            print("======product_id==========",line.product_id)
            _logger.info(f"Attempting to move inventory for product_id={line.product_id.id}, location_id={line.location_id.id}, location_dest_id={line.location_dest_id.id}, quantity={line.quantity}")
            if not line.product_id:
                raise UserError("No product found for the given barcode.")
            if not line.location_id:
                raise UserError("No source location found for the product.")

            move = self.env['stock.move'].create({
                'name': 'Barcode Inventory Move',
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'product_uom': line.product_id.uom_id.id,
                'location_id': line.location_id.id,
                'location_dest_id': line.location_dest_id.id,
            })

            _logger.info(f"Created stock move: {move.name}")

            move._action_confirm()
            move._action_assign()
            move._action_done()

            _logger.info(f"Stock move {move.name} done")

        return {'type': 'ir.actions.act_window_close'}