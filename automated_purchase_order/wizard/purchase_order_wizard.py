# -*- coding: utf-8 -*-
from odoo import models, fields
class PurchaseOrderWizard(models.TransientModel):
   _name = 'purchase.order.wizard'
   _description = 'Wizard for Automatic Purchase order'
   product_id=fields.Many2one('product.template',string='product')
   quantity=fields.Float(string='Quantity')
   company_id = fields.Many2one('res.company', store=True, string="company", copy="False",
                                default=lambda self: self.env.user.company_id.id)
   currency_id = fields.Many2one("res.currency", string="currency", related='company_id.currency_id',
                                 default=lambda self: self.env.user.company_id.currency_id.id)
   price=fields.Monetary(string='Price')

   def confirm_btn(self):
      product=self.env['product.product'].search([('product_tmpl_id','=',self.product_id.id)],limit=1)
      vendor=product.seller_ids[0].partner_id
      rfq=self.env['purchase.order'].search([('partner_id','=',vendor.id),
                                             ('state','=','draft')],limit=1)

      if not rfq:
            rfq=self.env['purchase.order'].create({
               'partner_id':vendor.id
            })

      if rfq:
          self.env['purchase.order.line'].create({
              'order_id':rfq.id,
              'name':product.name,
              'product_id':product.id,
              'product_qty':self.quantity,
              'price_unit':self.price,
          })
          rfq.button_confirm()

      return {'type': 'ir.actions.act_window_close'}



