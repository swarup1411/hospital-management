from odoo import models, fields

class AppointmentCancelWizard(models.TransientModel):
    _name = 'appointment.cancel.wizard'
    _description = 'Appointment Cancel Wizard'

    appointment_id = fields.Many2one('hospital.appointment',string='Appointment',required=True)

    def action_confirm(self):
        self.appointment_id.write({'state': 'cancel'})
        return {'type': 'ir.actions.act_window_close'}

