from odoo import fields, models, api

             # Inherit
class HospitalPatientInherit(models.Model):
    _inherit = 'hospital.patient'

    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    appointment_count = fields.Integer(compute='_compute_appointment_count', string='Number of Appointments')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')


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
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id}
        }