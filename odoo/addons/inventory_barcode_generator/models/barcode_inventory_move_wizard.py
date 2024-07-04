from odoo import models, fields, api
from odoo.exceptions import UserError

class BarcodeInventoryMoveWizard(models.TransientModel):
    _name = 'barcode.inventory.move.wizard'
    _description = 'Barcode Inventory Move Wizard'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    location_id = fields.Many2one('stock.location', string="Source Location", required=True)
    location_dest_id = fields.Many2one('stock.location', string="Destination Location", required=True)
    quantity = fields.Float(string="Quantity", required=True, default=1.0)

    def action_move_inventory(self):
        print("929292929292929292929")
        if not self.product_id or not self.location_id or not self.location_dest_id:
            raise UserError("Missing required fields for inventory move.")

        move = self.env['stock.move'].create({
            'name': 'Barcode Inventory Move',
            'product_id': self.product_id.id,
            'product_uom_qty': self.quantity,
            'product_uom': self.product_id.uom_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
        })

        move._action_confirm()
        move._action_assign()
        move._action_done()

        return {'type': 'ir.actions.act_window_close'}
