from odoo import models, fields,api

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(string='Name', required=True)
    doctor_seq = fields.Char(string='Doctor Sequence')
    specialization = fields.Selection([
        ('general', 'General Physician'),
        ('cardiology', 'Cardiologist'),
        ('interventional_cardiology', 'Interventional Cardiologist'),
        ('neurology', 'Neurologist'),
        ('neurosurgery', 'Neurosurgeon'),
        ('orthopedic', 'Orthopedic Specialist'),
        ('orthopedic_surgeon', 'Orthopedic Surgeon'),
        ('pediatric', 'Pediatrician'),
        ('pediatric_surgeon', 'Pediatric Surgeon'),
        ('gynecology', 'Gynecologist'),
        ('obstetrics', 'Obstetrician'),
        ('dermatology', 'Dermatologist'),
        ('ent', 'ENT Specialist'),
        ('ophthalmology', 'Ophthalmologist'),
        ('psychiatry', 'Psychiatrist'),
        ('psychology', 'Psychologist'),
        ('urology', 'Urologist'),
        ('nephrology', 'Nephrologist'),
        ('gastroenterology', 'Gastroenterologist'),
        ('pulmonology', 'Pulmonologist'),
        ('endocrinology', 'Endocrinologist'),
        ('oncology', 'Oncologist'),
        ('hematology', 'Hematologist'),
        ('rheumatology', 'Rheumatologist'),
        ('radiology', 'Radiologist'),
        ('pathology', 'Pathologist'),
        ('anesthesiology', 'Anesthesiologist'),
        ('emergency', 'Emergency Medicine'),
        ('critical_care', 'Critical Care Specialist'),
        ('family_medicine', 'Family Medicine'),
        ('internal_medicine', 'Internal Medicine'),
        ('sports_medicine', 'Sports Medicine Specialist'),
        ('geriatrics', 'Geriatrician'),
        ('infectious_disease', 'Infectious Disease Specialist'),
        ('plastic_surgery', 'Plastic Surgeon'),
        ('cosmetology', 'Cosmetologist'),
        ('dentistry', 'Dentist'),
        ('oral_surgeon', 'Oral & Maxillofacial Surgeon'),
        ('physiotherapy', 'Physiotherapist'),
        ('rehabilitation', 'Rehabilitation Specialist'),
        ('nutrition', 'Nutritionist'),
        ('ayurveda', 'Ayurveda Specialist'),
        ('homeopathy', 'Homeopathy Specialist'),
        ('unani', 'Unani Specialist'),] , string='specialization')
    phone_number = fields.Char(string='Phone Number', required=True)
    email = fields.Char(string='Email', required=True)
    consultation_fee = fields.Float(string=' Fees', required=True, digits=(6, 2))
    experience_years= fields.Integer(string='Exp Years', required=True)
    image = fields.Binary(string='Image')
    preview = fields.Boolean(string='Preview Image', default=False)
    patient_ids = fields.One2many('hospital.patient', 'doctor_id', string='Patients')
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string="Appointments")
    appointment_count = fields.Integer(compute='_compute_appointment_count', string='Number of Appointments')

       # Appointment count and doctor appointment button
    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids)

    def action_view_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('doctor_id', '=', self.id)],
            'context': {'default_doctor_id': self.id}
        }

          # Sequence generator
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('doctor_seq', 'new') == 'new':
                vals['doctor_seq'] = self.env['ir.sequence'].next_by_code('doctor.sequence') or 'new'
        return super().create(vals_list)