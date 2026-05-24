from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')

    @api.constrains('email', 'related_patient_id')
    def _check_patient_email(self):
        for rec in self:
            if rec.email:
                patient = self.env['hms.patient'].search([('email', '=', rec.email)])
                if patient:
                    raise ValidationError(
                        f'Cannot link this customer. Email "{rec.email}" already exists in patient: {patient.first_name} {patient.last_name}'
                    )

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError(
                    'Cannot delete a customer linked to a patient.'
                )
        return super().unlink()
