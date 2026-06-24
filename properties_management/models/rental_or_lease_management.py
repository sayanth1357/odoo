# -*- coding: utf-8 -*-
from email.policy import default

from odoo import models, fields, api, _
from odoo.orm.commands import Command


class RentalOrLeaseManagement(models.Model):
    """Rental or Lease Management"""
    _name = 'rental.lease.management'
    _description = 'Rental or Lease Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'reference_id'

    reference_id = fields.Char(string='Reference Id', copy=False, readonly=True,
                               index='trigram',
                               default=lambda self: _('New'), help="Reference Id")
    current_date = fields.Date(compute='_compute_current_date', string="Current Date")
    property_name = fields.Char(related='rent_ids.property_name', string='Property Name')
    property_id = fields.Many2one(related='rent_ids.property_id', string="Property Id", ondelete='restrict')
    tenant_id = fields.Many2one('res.partner', string="Tenant", required=True)
    state_type = fields.Selection(related='rent_ids.state_type', string="Status", required=True)
    approval_state = fields.Selection(
        [('To Approve', 'To Approve'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    payment_state = fields.Selection([
        ('to_invoice', 'To Invoice'),
        ('not_paid', 'Not_Paid'),
        ('paid', 'Paid'),
        ('cancel', "Canceled")], string="Payment State", compute='_compute_payment_state')
    state = fields.Selection(
        [('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Invoiced', 'Invoiced'), ('Closed', 'Closed'),
         ('Returned', 'Returned'),
         ('Expired', 'Expired')], string="State")
    attachment_id = fields.Many2one('ir.attachment')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    rental_id = fields.Many2one('rent.lease.record')
    rental_date = fields.Integer(related='rent_ids.days', string="Rental Date")
    lease_date = fields.Integer(related='rent_ids.days', string="Lease Date")
    rent_ids = fields.One2many(
        comodel_name='rent.lease.record',
        inverse_name='rent_id',
        string="rent",
        copy=True, required=True)
    invoice_ids = fields.One2many('account.move', 'rent_id')
    smart_button = fields.Char(string="Smart Button")
    active = fields.Boolean(default=True)
    rent_amount=fields.Float(related='rent_ids.rental_amount', string="Rental Amount")
    lease_amount=fields.Float(related='rent_ids.lease_amount', string="Rental Amount")
    from_date=fields.Date(related='rent_ids.from_date', string="From Date")
    to_date=fields.Date(related='rent_ids.to_date', string="To Date")
    @api.model_create_multi
    def create(self, vals):
        """Overrides the default create method"""
        for rec in vals:
            code = self.env['ir.sequence'].next_by_code('rental.lease.management')
            rec['reference_id'] = code
            return super(RentalOrLeaseManagement, self).create(vals)

    @api.depends('rental_amount', 'lease_amount')
    def _compute_effective_amount(self):
        """computes the effective amount of the rental and lease"""
        for rec in self:
            if rec.state_type == 'Rent':
                rec.effective_amount = rec.rental_amount
            elif rec.state_type == 'Lease':
                rec.effective_amount = rec.leased_amount
            else:
                rec.effective_amount = 0

    @api.depends('from_date', 'to_date')
    def _compute_effective_days(self):
        """computes the effective days of the rental and lease"""
        for rec in self:
            property_id = fields.Many2one('properties.management', string="Property Id")
            if rec.state_type == 'Rent':
                rec.effective_days = rec.days
                property_id.effective_days = self.effective_days

            elif rec.state_type == 'Lease':
                rec.effective_days = rec.days
                property_id.effective_days = self.effective_days

            else:
                rec.effective_days = 0

    @api.depends()
    def _compute_current_date(self):
        """computes the current date which is later used to check the late payment"""
        for rec in self:
            rec.current_date = fields.Date.today()

    def button_confirm(self):
        """sets the state to confirmed on clicking the button"""
        self.write({'state': "Confirmed"})
        template = self.env.ref('properties_management.property_confirmation_mail')
        email_values = {'email_from': self.env.user.email,
                        'email_to': self.tenant_id.email}
        template.send_mail(self.id, force_send=True, email_values=email_values)

    def button_closed(self):
        """sets the state to closed on clicking the button"""
        self.write({'state': "Closed"})
        template = self.env.ref('properties_management.property_closing_mail')
        email_values = {'email_from': self.env.user.email,
                        'email_to': self.tenant_id.email}
        template.send_mail(self.id, force_send=True, email_values=email_values)

    def button_returned(self):
        """sets the state to returned on clicking the button"""
        self.write({'state': "Returned"})

    def button_expired(self):
        """sets the state to expired on clicking the button"""
        # self.write({'state': "Expired"})
        for record in self.env['rental.lease.management'].search([]):
            if record.state == 'Closed':
                if record.state_type == 'Rent':
                    if record.rental_date == record.current_date:
                        record.write({'state': "Expired"})
                        template = record.env.ref('properties_management.property_expired_mail')
                        email_values = {'email_from': record.env.user.email,
                                        'email_to': record.tenant_id.email}
                        template.send_mail(record.id, force_send=True, email_values=email_values)
                        print("The rented property has expired.")

                    else:
                        print("The rented property is not expired.")

                elif record.state_type == 'Lease':
                    if record.lease_date == record.current_date:
                        record.write({'state': "Expired"})
                        template = record.env.ref('properties_management.property_expired_mail')
                        email_values = {'email_from': record.env.user.email,
                                        'email_to': record.tenant_id.email}
                        template.send_mail(record.id, force_send=True, email_values=email_values)
                        print("The leased property has expired.")

                    else:
                        print("The leased property has not expired.")
                else:
                    print("state_type is invalid")
            else:
                return False

    def action_button_invoice(self):
        """action for the create invoice button"""
        self.write({'state': "Invoiced"})
        for rec in self:
            self.write({'payment_state': "to_invoice"})
            for property in rec.rent_ids:
                records = self.env['account.move'].search(
                    ['&', ('partner_id', '=', rec.tenant_id.id), ('state', '=', 'draft')])
                if len(records) > 0:
                    """the if condition is used for creating a new record """

                    records.write({
                        'move_type': 'out_invoice',
                        'invoice_date': fields.Date.today(),
                        'partner_id': rec.tenant_id.id,
                        'rent_id': rec.id,
                        'invoice_line_ids': [Command.create({
                            'name': property.property_id.name,
                            'quantity': property.days,
                            'price_unit': property.effective_amount,
                        })], })



                else:
                    self.env['account.move'].create({
                        'move_type': 'out_invoice',
                        'invoice_date': fields.Date.today(),
                        'rent_id': rec.id,
                        'partner_id': rec.tenant_id.id,
                        'invoice_line_ids': [
                            Command.create({
                                'name': property.property_id.name,
                                'quantity': property.days,
                                'price_unit': property.effective_amount,
                            })],
                    })

    def action_view_invoice_info(self):
        """invoice smart button action"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "name": _("Invoice Info"),
            "views": [[False, "list"], [False, "form"]],
            "domain": [('rent_id', '=', self.id)],
        }

    invoice_count = fields.Integer(string="Invoices", compute='compute_invoice_count', default=0)

    def compute_invoice_count(self):
        """function for computing the invoice count"""
        for record in self:
            record.invoice_count = self.env['account.move'].search_count([('partner_id', '=', self.tenant_id)])

    #
    def late_payment(self):
        """function used for the scheduled action for sending late payment reminders"""
        for record in self.env['rental.lease.management'].search([]):

            if record.state_type == 'Rent':
                if (record.current_date >= record.rental_date) and (record.payment_state != 'paid') and (
                        record.state == 'Invoiced'):
                    template = record.env.ref('properties_management.property_late_payment_mail')
                    email_values = {'email_from': record.env.user.email,
                                    'email_to': record.tenant_id.email}
                    template.send_mail(record.id, force_send=True, email_values=email_values)
            else:
                if (record.current_date >= record.rent_ids.leased_time) and (record.payment_state != 'paid') and (
                        record.state == 'Invoiced'):
                    template = record.env.ref('properties_management.property_late_payment_mail')
                    email_values = {'email_from': record.env.user.email,
                                    'email_to': record.tenant_id.email}
                    template.send_mail(record.id, force_send=True, email_values=email_values)

    @api.depends('invoice_ids')
    def _compute_payment_state(self):
        """function used to compute payment state"""
        for record in self:
            record.payment_state = False
            if (record.invoice_ids.payment_state) == 'paid':
                self.write({'payment_state': 'paid'})
                self.write({'state': 'Closed'})
            elif (record.invoice_ids.payment_state) == 'not_paid':
                self.write({'payment_state': 'not_paid'})
            elif (record.invoice_ids.payment_state) == 'canceled':
                self.write({'payment_state': 'canceled'})

    def submit_approval_button(self):
        """function for submitting approval button"""
        for record in self:
            record.write({'approval_state': 'To Approve'})

    def approved_button(self):
        """function for approve button"""
        for record in self:
            record.write({'approval_state': 'Approved'})
            record.write({'state': 'Draft'})

    def reject_button(self):
        """function for reject button"""
        for record in self:
            record.write({'approval_state': 'Rejected'})
