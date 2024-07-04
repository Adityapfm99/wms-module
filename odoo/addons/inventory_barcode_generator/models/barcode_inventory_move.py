import logging

_logger = logging.getLogger(__name__)

from odoo import models, fields, api
from odoo.exceptions import UserError

class BarcodeInventoryMove(models.TransientModel):
    _name = 'barcode.inventory.move'
    _description = 'Barcode Inventory Move'

    barcode = fields.Char(string="Barcode")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", required=True, default=1.0)
    location_id = fields.Many2one('stock.location', string="Source Location",required=True,store=True)
    location_dest_id = fields.Many2one('stock.location', string="Destination Location", required=True)

    @api.onchange('barcode')
    def _onchange_barcode(self):
        if self.barcode:
            _logger.info(f"Searching for product with barcode: {self.barcode}")
            product = self.env['product.product'].search([('barcode', '=', self.barcode)], limit=1)
            _logger.info(f"Product search result: {product.id if product else 'None'}")
            if product:
                _logger.info(f"Product found: {product.name}")
                self.product_id = product.id
                self.location_id = self._get_latest_product_location(product.id)
                if self.location_id:
                    _logger.info(f"Latest stock quant location: {self.location_id.id}")
                else:
                    _logger.info("No stock quant found for the product.")
                self.write({
                    'product_id': self.product_id.id,
                    'location_id': self.location_id.id if self.location_id else False
                })
            else:
                _logger.info("No product found")
                self.product_id = False
                self.location_id = False
                self.write({
                    'product_id': False,
                    'location_id': False
                })
                return {
                    'warning': {
                        'title': "No Product Found",
                        'message': "No product found with the given barcode."
                    }
                }

    def _get_latest_product_location(self, product_id):
        stock_quant = self.env['stock.quant'].search([('product_id', '=', product_id)], limit=1, order='in_date desc')
        return stock_quant.location_id if stock_quant else False
    
    def action_move_inventory(self):
        self.ensure_one()
        _logger.info(f"Form data: product_id={self.product_id.id}, location_id={self.location_id.id}, location_dest_id={self.location_dest_id.id}, quantity={self.quantity}")

        if not self.product_id:
            raise UserError("No product found for the given barcode.")
        if not self.location_id:
            raise UserError("No source location found for the product.")
        
        move = self.env['stock.move'].create({
            'name': 'Barcode Inventory Move',
            'product_id': self.product_id.id,
            'product_uom_qty': self.quantity,
            'product_uom': self.product_id.uom_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
        })
        
        _logger.info(f"Created stock move: {move.name}")
        
        move._action_confirm()
        move._action_assign()
        move._action_done()
        
        _logger.info(f"Stock move {move.name} done")
        
        return {'type': 'ir.actions.act_window_close'}