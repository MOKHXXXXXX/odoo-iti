from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Image(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age')

    department_id = fields.Many2one('hms.department', string='Department')
    department_capacity = fields.Integer(related='department_id.capacity', string='Department Capacity')
    doctor_ids = fields.Many2many('hms.doctors', string='Doctors')

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], string='State', default='undetermined')

    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='Log History')

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR Checked',
                    'message': 'PCR has been automatically checked because age is less than 30.',
                }
            }

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id and not self.department_id.is_opened:
            self.department_id = False
            return {
                'warning': {
                    'title': 'Department Closed',
                    'message': 'This department is closed. Please select an open department.',
                }
            }

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for rec in self:
            if rec.pcr and rec.cr_ratio == 0:
                raise ValidationError('CR Ratio is mandatory when PCR is checked.')

    def write(self, vals):
        if 'state' in vals:
            new_state = dict(self._fields['state'].selection).get(vals['state'])
            for rec in self:
                rec.log_ids.create({
                    'patient_id': rec.id,
                    'created_by': self.env.user.id,
                    'date': fields.Datetime.now(),
                    'description': f'State changed to {new_state}',
                })
        return super().write(vals)
        
        
    def action_undetermined(self):
        self.state = 'undetermined'

    def action_good(self):
        self.state = 'good'

    def action_fair(self):
        self.state = 'fair'

    def action_serious(self):
        self.state = 'serious'
