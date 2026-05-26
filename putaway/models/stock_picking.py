# -*- coding: utf-8 -*-

from odoo import models
class StockPicking(models.Model):

    _inherit = 'stock.picking'


    def button_validate(self):
        for record in self:
            if record.product_id.weight > 20:
                heavy=self.env['stock.location'].search([('complete_name','=','Heavy Rack')])
                if heavy:
                    record.write({
                        'location_dest_id':heavy
                    })
                return super().button_validate()



