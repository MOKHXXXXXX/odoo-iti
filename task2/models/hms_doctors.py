from odoo import models, fields

class HmsDoctors(models.Model):
    _name = 'hms.doctors'
    _description = 'Hospital Doctors'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    image = fields.Image(string='Image')
