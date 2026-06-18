from odoo import fields,models,api
class ResPartner(models.Model):

    _inherit = 'res.partner'

    sequence_id=fields.Char(string='id',copy=False,readonly=True)
    sequence=fields.Boolean(string="sequence")

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
                print(123,vals)
                print(444,rec)
                if rec['sequence']==True:
                    code = self.env['ir.sequence'].next_by_code('res.partner')
                    rec['sequence_id'] = code
        res = super().create(vals)
        return res

    def write(self, vals):
            print(222,self)
            print(333,vals)
            res = super().write(vals)
            for rec in vals:
                if vals.get('sequence'):
                    self['sequence_id'] = self.env['ir.sequence'].next_by_code('res.partner')
            return res


            i
            # print(333,self)
            # print(777,vals)
            #
            # for rec in self:
            #     print(344,rec)
            #     if vals.get('sequence'):
            #                 code = self.env['ir.sequence'].next_by_code('res.partner')
            #                 rec['sequence_id'] = code
            # super().create(vals)
            # return res












