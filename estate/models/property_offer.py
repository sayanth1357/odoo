from datetime import timedelta

from odoo import models,fields,api
class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Type Offer'
    price=fields.Float()
    status=fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')], copy=False)
    partner_id=fields.Many2one("res.partner",string="partner",reqUired=True)
    property_id=fields.Many2one('estate.property')
    validity=fields.Integer(default=7)

    date_deadline=fields.Date(compute="_compute_date",inverse="_inverse_date")
    @api.depends('validity')
    def _compute_date(self):
        for record in self:
            createdate=record.create_date.date()
            record.date_deadline=createdate+timedelta(days=record.validity)
    def _inverse_date(self):
        for record in self:
            createdate = record.create_date.date()
            delta=record.date_deadline-createdate
            record.validity=delta.days

