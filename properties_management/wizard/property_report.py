# -*- coding: utf-8 -*

from odoo import fields, models,_
from odoo.exceptions import ValidationError

class PropertyReport(models.TransientModel):
    _name = 'property.report'
    _rec_name = 'property_id'
    _description = 'Property Report'

    property_id = fields.Many2one('properties.management', string='Property Record')
    property_name = fields.Char(related='property_id.property_name', string='Property Name')
    owner_name = fields.Many2one(related='property_id.owner_id', string='Owner Name')
    tenant_id = fields.Many2one('res.partner', string="Tenant",store=True)
    to_date = fields.Date(string='To Date')
    from_date = fields.Date(string='From Date')
    state_type = fields.Selection([('Rent', 'Rent'), ('Lease', 'Lease')])
    state = fields.Selection(
        [('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Invoiced', 'Invoiced'), ('Closed', 'Closed'),
         ('Returned', 'Returned'),
         ('Expired', 'Expired')], string="State")


    def action_report_property_management(self):
        """
        defines the query being passed to the db.
        """
        query = """select pm.id as p_id, pm.property_name as p_name ,rs.name as o_id,rr.state_type as state_type,rp.name as t_id,rl.state as State,rr.total_amount as Total_Amount,rr.from_date,rr.to_date 
        from rent_lease_record as rr
        inner join rental_lease_management as rl on rl.id = rr.rent_id
        inner join properties_management as pm on pm.id = rr.property_id
        inner join res_partner as rs on rs.id=pm.owner_id
        inner join res_partner as rp on rp.id=rl.tenant_id
        where 1=1
        """
        if self.tenant_id:
            query += """ AND rp.id = '%s' """ % (self.tenant_id.id)
        elif self.state:
            query += """ AND rl.state = '%s' """ % (self.state)
        elif self.property_id:
            query += """ AND pm.id = '%s' """ % (self.property_id.id)
        elif self.state_type:
            query += """ AND rr.state_type = '%s' """ % (self.state_type)
        elif self.to_date:
            query += """ AND rr.to_date <= '%s' """ % (self.to_date)
        elif self.from_date:
            query += """ AND rr.from_date >= '%s' """ % (self.from_date)

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        data = {'report': report}
        
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError(_("Invalid Date !"))

        if report==[]:
            raise ValidationError(_(
                "No Records Found !"
            ))

        if self.property_id:
            if (self.state or self.state_type or self.tenant_id or self.from_date or self.to_date)==False:
                return self.env.ref('properties_management.action_property_only_report').report_action(None, data=data)
            else:
                print('in')
                return self.env.ref('properties_management.action_property_report').report_action(None, data=data)
        else:
            print('out')
            return self.env.ref('properties_management.action_property_report').report_action(None, data=data)