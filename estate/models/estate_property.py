from calendar import month


from dateutil.relativedelta import relativedelta
from datetime import date
from odoo import fields, models,api
from odoo.exceptions import UserError


class RealEstate(models.Model):
    _name="estate.property"
    _description = "Real Estate"
    name= fields.Char(required=True)
    description= fields.Text()
    postcode=fields.Char()
    # date_availability=fields.Date(copy=False, default=lambda self:fields.Date.today()+timedelta(days=90))
    date_availability=fields.Date(copy=False, default=date.today()+relativedelta(months=3))
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True,copy=False)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection(selection=[('north','North'),('south','South'),('east','East')])
    active=fields.Boolean(default=True)
    status=fields.Selection(selection=[('new','New'),('offer received','Offer Received'),('offer accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')],copy=False,required=True,default='new')
    property_type_id=fields.Many2one('estate.property.type')
    salesman_id=fields.Many2one("res.users",string="Salesman",default=lambda self:self.env.user)
    partner_id=fields.Many2one("res.partner",string="Buyer" ,copy=False)
    property_tag_id=fields.Many2many('estate.property.tag')
    property_offer_ids= fields.One2many('estate.property.offer','property_id')
    best_offer=fields.Float(compute="_compute_best_offer")


    total_area=fields.Float(compute="_compute_total")

    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area= record.living_area + record.garden_area

    @api.depends("property_offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            price_list=record.mapped('property_offer_ids.price')
            if len(price_list)>0:
                record.best_offer=max(price_list)
            else:
                record.best_offer=0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area=10
            self.garden_orientation='north'
        else:
            self.garden_area=0
            self.garden_orientation=False

    def cancel_btn(self):
        for record in self:
            if record.status == "sold":
                raise UserError("its already sold")
            else:
                record.status="cancelled"
        return True

    def sold_btn(self):
        for record in self:
            if record.status == "cancelled":
                raise UserError("cancelled property cannot be sold")
            else:
                record.status="sold"
        return True





