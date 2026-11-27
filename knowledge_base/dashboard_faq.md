# MediFlow Dashboard FAQ

## 1. What dashboards are available in MediFlow?

MediFlow provides two primary dashboards:
- Patient Dashboard
- Doctor Dashboard

Each dashboard provides functionality based on the authenticated user's role.

## 2. What can patients do from their dashboard?

Patients can:
- View their appointments.
- See appointment details.
- Track appointment status.
- Access appointment-related functionality.
- Follow queue information through the queue tracking feature.

## 3. Can patients view their previous appointments?

Yes. The My Appointments endpoint retrieves all appointments associated with the authenticated patient, ordered by creation time with the newest first.

## 4. What can doctors do from their dashboard?

Doctors can:
- View their appointments for the current day.
- Open individual appointment details.
- Start consultations.
- Complete consultations.
- Mark eligible appointments as no-show.

## 5. How does the doctor dashboard retrieve daily appointments?

The backend identifies the authenticated doctor and retrieves appointments associated with that doctor's slots for the current day in Indian Standard Time (IST).

Appointments are sorted by their scheduled start time.

## 6. Can doctors view appointment details?

Yes. Doctors can retrieve individual appointment details belonging to their own appointments.

## 7. Can doctors start consultations directly?

Doctors can start a consultation when the appointment has CHECKED_IN status and belongs to the authenticated doctor.

After starting the consultation, its status changes to IN_CONSULTATION.

## 8. Can a doctor handle multiple active consultations simultaneously?

MediFlow prevents a doctor from starting another consultation while an existing consultation is active. It uses a PostgreSQL advisory transaction lock to serialize consultation-start operations for that doctor.

## 9. How does a doctor complete a consultation?

The doctor can complete an appointment whose status is IN_CONSULTATION. MediFlow changes its status to DONE and records the consultation completion timestamp.

## 10. What is the no-show feature?

The no-show feature allows doctors to mark an eligible patient appointment as NO_SHOW when the patient has not arrived within the configured grace period.

## 11. When can a doctor mark a patient as no-show?

By default, MediFlow allows a doctor to mark an appointment as no-show only after the scheduled slot start time plus a 10-minute grace period.

The grace period can be configured using the NO_SHOW_GRACE_MINS environment variable. Setting it to 0 disables the time restriction.

Only BOOKED and CHECKED_IN appointments are eligible for this operation.

## 12. Can a doctor manage another doctor's appointments?

No. The backend verifies that the appointment belongs to the authenticated doctor before allowing doctor-specific appointment operations.

## 13. Does MediFlow have an admin dashboard?

No. Although ADMIN is defined as a supported database role, a dedicated admin dashboard is not currently implemented.

## 14. Do patients and doctors have the same dashboard permissions?

No. MediFlow uses role-based access control. Patient and doctor accounts have separate access permissions and workflows.