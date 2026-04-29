from odoo import models, fields, api


class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'appointment'
    date = fields.Date(string='Date')
    time = fields.Selection([(' 9:00 am', '9:00 AM'), ('10:00 am', '10:00 AM'), ('11:00 am', '11:00 AM'),
                             ('2:00 pm', '2:00 PM'), ('3:00 pm', '3:00 PM'), ('4:00 pm', '4:00 PM')])
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default='draft' ,tracking=True)
    reason = fields.Text(string='Reason for visiting')
    add_note = fields.Text(string='Additional Note')
    appointment_seq = fields.Char(string='Sereal No')

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    patient_age = fields.Integer(string="Age", related="patient_id.age", store=True, readonly=True)
    patient_sl= fields.Char(string="patient sl", related="patient_id.patient_seq", store=True, readonly=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    doctor_fees = fields.Float(string='Fees', related="doctor_id.consultation_fee", store=True, readonly=True)
    doctor_sl= fields.Char(string="dictor sl", related="doctor_id.doctor_seq", store=True, readonly=True)
    specialization = fields.Char(string='Specialization Name', compute='_compute_specialization_label')

     # doctor specialization view on appointment recipt pdf
    @api.depends('doctor_id.specialization')
    def _compute_specialization_label(self):
        for rec in self:
            label = ''
            if rec.doctor_id.specialization:
                selection_dict = dict(rec.doctor_id._fields['specialization'].selection)
                label = selection_dict.get(rec.doctor_id.specialization, '')
            rec.specialization = label

        # Sequence generator
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('appointment_seq', 'new') == 'new':
                vals['appointment_seq'] = self.env['ir.sequence'].next_by_code('appointment.sequence') or 'new'
        return super().create(vals_list)

     # State button change
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def _Swarup(self):
        return print('swarup is king')

    def action_open_cancel_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'cancel_appointment_wizard',
            'res_model': 'appointment.cancel.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_appointment_id': self.id},
        }

    # def name_search(self, name='', args=None, operator='ilike', limit=100):
    #     args = args or []
    #     domain = ['|', ('name', operator, name), ('id', operator, name)]
    #     recs = self.search(domain + args, limit=limit)
    #     return recs.name_get()

