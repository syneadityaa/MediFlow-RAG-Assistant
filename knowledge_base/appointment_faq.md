# MediFlow Appointment Management FAQ

## 1. How can I book an appointment?

Patients must log in, search for a doctor, select an available future appointment slot and confirm the booking.

## 2. Is login required to book an appointment?

Yes. The appointment booking endpoint is protected and requires an authenticated patient account.

## 3. What happens after booking an appointment?

MediFlow creates an appointment associated with the authenticated patient and selected slot. The appointment initially receives the BOOKED status.

## 4. Can I book an already occupied slot?

No. MediFlow checks the slot's booking status and uses an atomic database update to prevent double booking.

## 5. How can I view my appointments?

Patients can access the My Appointments section after logging in. The backend retrieves appointments belonging to the authenticated patient and displays the newest appointments first.

## 6. Can I cancel my appointment?

Yes. Patients can cancel their own appointments while their status is BOOKED.

## 7. Can I cancel an appointment after checking in?

No. The current backend allows cancellation only when the appointment status is BOOKED. CHECKED_IN appointments cannot be cancelled through the current cancellation endpoint.

## 8. Can I cancel another patient's appointment?

No. The cancellation endpoint checks appointment ownership using the authenticated patient's ID.

## 9. How can I check in for an appointment?

Patients can use the check-in functionality for their own appointments. The check-in endpoint changes the appointment status from BOOKED to CHECKED_IN and records the check-in timestamp.

## 10. Can I check in multiple times?

The check-in operation only accepts appointments whose current status is BOOKED. An appointment already checked in cannot be checked in again.

## 11. What happens after an appointment is checked in?

The appointment status becomes CHECKED_IN. It can then be considered by the doctor's queue management process and the doctor can start the consultation.

## 12. What are the appointment statuses in MediFlow?

MediFlow supports six appointment statuses:

- BOOKED: The appointment has been successfully created.
- CHECKED_IN: The patient has checked in.
- IN_CONSULTATION: The doctor has started the consultation.
- DONE: The consultation has been completed.
- CANCELLED: The patient cancelled the appointment.
- NO_SHOW: The doctor marked the appointment as a no-show.

## 13. Can a patient directly mark an appointment as completed?

No. The doctor completes the consultation through the doctor-side workflow.

## 14. Does MediFlow maintain appointment history?

Yes. The patient appointment endpoint retrieves appointments belonging to the authenticated patient and sorts them by creation time in descending order.