# -*- coding: utf-8 -*-
import base64

from odoo import fields, models


class AccountMove(models.Model):
    """Class inherits and extends the account.move model"""
    _inherit = 'account.move'


    student_id = fields.Many2one('student.student', 'Student',
                                 help='Related student', copy=False,check_company=True)
    room_id = fields.Many2one('hostel.room', 'Student',
                              help='Related room', copy=False,check_company=True)

    def action_post(self):
        """Method extends the invoice confirmation functionality to parent class method"""
        posted = super().action_post()
        invoice_template = self.env['account.move.send']._get_default_pdf_report_id(self)
        pdf_raw = invoice_template._render_qweb_pdf(invoice_template.xml_id, res_ids=self.ids)
        data_record = base64.b64encode(pdf_raw[0])

        ir_values = {
            'name': 'Invoice PDF.pdf',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/x-pdf',
        }
        data_id = self.env['ir.attachment'].create(ir_values)
        template = self.env.ref('hostel.email_template_edi_invoice')
        template.attachment_ids = [(6, 0, [data_id.id])]
        email_values = {'email_from': self.env.user.email}
        template.send_mail(self.id, force_send=True,
                           email_values=email_values)
        template.attachment_ids = [(3,data_id.id)]
        data_id.unlink()
        return posted

    def send_invoice_creation_mail(self, invoice):
        """Send email via scheduled action for invoice creation"""
        # template = self.env.ref('hostel.email_template_edi_invoice')
        template = self.env.ref('hostel.email_template_invoice_created')
        email_values = {'email_from': self.env.user.email}
        template.send_mail(invoice.id, force_send=True,
                           email_values=email_values)
        return True
