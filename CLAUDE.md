# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Odoo 18 custom module repository for a Hospital Management System. It contains three interconnected modules for managing patients, doctors, and appointments.

## Module Architecture

### Module Dependencies
```
patient_management (base module)
    ↓
doctor_appoinment (depends on patient_management)

my_portal (depends on portal, base, website - standalone)
```

### Module Details

1. **patient_management** - Core patient records
   - Model: `hospital.patient` - Patient records with demographics, contact info
   - Features: Auto-generated sequence (Pat/001), age calculation from DOB, mail tracking

2. **doctor_appoinment** - Doctor and appointment management
   - Model: `hospital.doctor` - Doctor profiles with specializations, fees
   - Model: `hospital.appointment` - Appointment scheduling with state workflow (draft → confirm → done/cancel)
   - Model: `appointment.cancel.wizard` - Transient model for cancellation confirmation
   - Features: Doctor-patient relationships, appointment reports, automated sequences

3. **my_portal** - Portal frontend with currency converter
   - Controller: `CurrencyConverterPortal` - Routes to `/my/currency-converter`
   - Static JS: Currency conversion using open.er-api.com exchange rates

## Common Development Commands

### Running Odoo Server
```bash
# From Odoo source directory
python odoo-bin -c C:\Users\swaru\OneDrive\Documents\odoo\odoo18\custom\odoo_practic_project\odoo.conf
```

### Updating Modules
```bash
# Update specific module after code changes
python odoo-bin -c <path_to_odoo.conf> -u patient_management
python odoo-bin -c <path_to_odoo.conf> -u doctor_appoinment
python odoo-bin -c <path_to_odoo.conf> -u my_portal

# Update all modules
python odoo-bin -c <path_to_odoo.conf> -u all
```

### Database Configuration (from odoo.conf)
- Database: `hospital_db`
- Port: `2026`
- User: `odoo_user`
- Host: `localhost:5433`

## Key Patterns

### Sequence Generation
Sequences are defined in `data/sequence.xml` and auto-generate on record creation:
- Patient: `patient.sequence` → Pat/001
- Doctor: `doctor.sequence` → Doc/001  
- Appointment: `appointment.sequence` → Appt/001

### State Workflow Pattern
Appointments use standard Odoo state pattern with button methods:
```python
def action_confirm(self):
    for rec in self:
        rec.state = 'confirm'
```

### Wizard Pattern
Transient models for user confirmations (see `cancel_appointment_wizard.py`):
- Define as `models.TransientModel`
- Return `{'type': 'ir.actions.act_window_close'}` on completion
- Open via `action_open_cancel_wizard()` returning `ir.actions.act_window`

### Report Generation
QWeb reports defined in `reports/` directory:
- Paper format: `reports/paper_formet_apt.xml` (note: "formet" spelling)
- Report action + template in separate XML files

### Related Field Pattern
Computed related fields for cross-model data display:
```python
patient_age = fields.Integer(related="patient_id.age", store=True, readonly=True)
```

## File Organization

Standard Odoo module structure per module:
```
module_name/
├── __init__.py
├── __manifest__.py          # Dependencies and data file loading order
├── models/
│   ├── __init__.py
│   └── *.py                 # Model definitions
├── views/
│   └── *.xml                # Views, menus, actions
├── data/
│   └── *.xml                # Sequences, scheduled actions
├── security/
│   └── ir.model.access.csv  # Access rights
├── reports/
│   └── *.xml                # QWeb reports and paper formats
├── wizard/                  # Transient model wizards
│   ├── __init__.py
│   ├── *.py
│   └── *_view.xml
├── static/
│   ├── description/
│   │   └── icon.png
│   └── src/
│       └── js/
│           └── *.js         # Frontend assets
└── controler/               # Note: spelled "controler" not "controller"
    └── *.py                 # HTTP route controllers
```

## Model Relationships

```
hospital.patient (patient_management)
    ├── doctor_id → hospital.doctor
    └── patient_seq (auto-generated)

hospital.doctor (doctor_appoinment)
    ├── patient_ids → One2many hospital.patient
    ├── appointment_ids → One2many hospital.appointment
    └── doctor_seq (auto-generated)

hospital.appointment (doctor_appoinment)
    ├── patient_id → Many2one hospital.patient
    ├── doctor_id → Many2one hospital.doctor
    ├── patient_age/patient_sl (related to patient_id)
    ├── doctor_fees/doctor_sl (related to doctor_id)
    └── appointment_seq (auto-generated)
```

## Security Notes

- Access control files: `security/ir.model.access.csv`
- Current setup grants full CRUD permissions (1,1,1,1) to base users
- No record-level rules (ir.rule) currently implemented

## Portal/Routing

Portal routes in `my_portal/controler/portal.py`:
- `/my/currency-converter` - Currency converter page

Note: Controller directory is spelled `controler` (not `controller`).

## Specialization Values

Doctor model has extensive selection field for `specialization` with 50+ medical specialties defined. When displaying selection labels in reports/views, use the compute pattern seen in `appointment.py:_compute_specialization_label()`.
