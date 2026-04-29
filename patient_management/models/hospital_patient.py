from odoo import fields, models, api
from datetime import date



class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'HospitalPatient'

    name = fields.Char(string='Hospital Name', required=True)
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string=' Age', compute='_compute_age' , store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              string='Gender', required=True)
    blood_group = fields.Selection([('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'),
                                    ('o+', 'O+'), ('o-', 'O-'), ('ab+', 'AB+'), ('ab-', 'AB-')])
    phone_number = fields.Char(string='Phone Number', required=True)
    email = fields.Char(string='Email', required=True)
    address = fields.Text(string='Address', required=True)
    image = fields.Binary(string='Image')
    preview = fields.Boolean(string='Preview Image', default=False)
    patient_seq = fields.Char(string='Patient Sequence', copy=False,readonly=True)

       # Sequence Generator
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('patient_seq', 'new') == 'new':
                vals['patient_seq'] = self.env['ir.sequence'].next_by_code('patient.sequence') or 'new'
        return super().create(vals_list)

      # Date of Birth to age calculator
    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                rec.age = date.today().year - rec.date_of_birth.year
            else:
                rec.age = 0






    # @api.model
    # def create(self, vals):
    #     print("method called")
    #     return super().create(vals)

    # @api.model
    # def default_get(self, fields):
    #     res = super().default_get(fields)
    #     res['age'] = 18
    #     return res

    # @api.onchange('date_of_birth')
    # def _onchange_date_of_birth(self):
    #     if self.date_of_birth:
    #         self.age = 45

    # def write(self, vals):
    #     print("write called from patient",vals)
    #     return super().write(vals)
    #
    # @api.model
    # def default_get(self, fields_list):
    #     res = super().default_get(fields_list)
    #     res['gender'] = 'male'
    #     return res



