# -*- coding: utf-8 -*-
from datetime import date

from odoo import fields, models, api


class HostelRoom(models.Model):
    """Manage Hostel rooms data"""
    _name = "hostel.room"
    _rec_name = "room_no"
    _description = "Hostel Rooms"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    room_no = fields.Char('Room No', help='identifier number for the room',
                          default=lambda self: 'New', readonly=True)
    room_type_id = fields.Many2one('hostel.room.type',
                                   string='Room Type', help='Type of the room',
                                  )
    no_of_beds = fields.Integer('No of Beds', tracking=True,
                                help='Total no of beds in the room')
    rent = fields.Float('Rent', help='Rent amount for the room')
    state = fields.Selection(
        selection=[('empty', 'Empty'), ('cleaning', 'Cleaning'),
                   ('partial', 'Partial'), ('full', 'Full')],
        help='state of the room capacity', compute="_compute_state",
        string="Status", store=True, tracking=True)
    student_ids = fields.One2many('student.student',
                                  'room_id', 'Students', check_company=True)
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  related="company_id.currency_id")
    facilities_ids = fields.Many2many('hostel.facilities',
                                      string='Facilities', check_company=True)
    total_rent = fields.Float('Total Rent', readonly=True,
                              compute="_compute_total_rent",
                              help="Total rent = rent + sum of facility charges")

    invoice_ids = fields.One2many('account.move', 'room_id', check_company=True)
    invoice_count = fields.Integer("count", compute="_compute_invoice_count",
                                   store=True)
    is_cleaning = fields.Boolean(default=False)
    pending_amount = fields.Float("Pending Amount",
                                  compute="_compute_pending_amount")
    active = fields.Boolean(string="Active", default=True)
    last_cleaning = fields.Date(string="Next Cleaning Date")
    image = fields.Image(required=True)

    @api.depends("student_ids", "no_of_beds", "is_cleaning")
    def _compute_state(self):
        """method to set the state of the room capacity
        according students assigned"""
        for record in self:
            if record.is_cleaning:
                record.write({'state': 'cleaning'})
            else:
                slots_assigned = len(list(record.student_ids))
                if slots_assigned == 0:
                    record.write({'state': 'empty'})
                elif slots_assigned == record.no_of_beds:
                    record.write({'state': 'full'})
                else:
                    record.write({'state': 'partial'})

    @api.depends("rent", "facilities_ids")
    def _compute_total_rent(self):
        """method to compute the total rent"""
        for record in self:
            record.total_rent = record.rent
            for rec in record.facilities_ids:
                record.total_rent += rec.charge

    @api.depends("invoice_ids")
    def _compute_invoice_count(self):
        """Compute the count of invoices """
        for record in self:
            record.invoice_count = len(list(record.invoice_ids))

    @api.depends("invoice_ids")
    def _compute_pending_amount(self):
        """compute the pending invoice amount for current room"""
        for record in self:
            record.pending_amount = 0
            for invoice in record.invoice_ids:
                if invoice.payment_state not in ['paid']:
                    record.pending_amount += invoice.amount_residual

    @api.model_create_multi
    def create(self, vals_list):
        """method to overwrite create method the room number format and
        auto create room number at record creation"""
        for vals in vals_list:
            if vals.get('room_no', "New") == "New":
                vals['room_no'] = (self.env['ir.sequence'].next_by_code(
                    'hostel.room')
                                   or "New")
        return super().create(vals_list)

    def _cron_create_invoice(self):
        """ create invoice for monthly room rent """
        hostel_room = self.env['hostel.room'].search([])
        for rooms in hostel_room:
            for student in rooms.student_ids:
                for record in student:
                    records = rooms.env['account.move'].create({
                        'move_type': 'out_invoice',
                        'date': date.today(),
                        'partner_id': record.partner_id.id,
                        'room_id': rooms.id,
                        'student_id': record.id,
                        'state': 'draft',
                        'ref': rooms.room_no,
                        'invoice_line_ids': [(0, 0, {
                            'name': rooms.env.ref('hostel.rent_product').name,
                            'price_unit': rooms.total_rent,
                            'tax_ids': False,
                            'quantity': 1.0,
                            'product_id': rooms.env.ref(
                                'hostel.rent_product').id,
                        })],
                    })
                    self.env['account.move'].send_invoice_creation_mail(records)
        return True

    def action_view_invoice(self):
        """View room invoices"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Room Invoices',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'domain': [('room_id', 'in', self.id)],
        }



