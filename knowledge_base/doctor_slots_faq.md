# MediFlow Doctor Slots FAQ

## 1. What are appointment slots in MediFlow?

Appointment slots represent available time periods associated with a doctor. Each slot has a start time, an end time and a booking status.

## 2. How can I view available slots for a doctor?

Patients can select a doctor and retrieve available slots using the doctor's ID. MediFlow returns future slots that have not already been booked.

## 3. Are past appointment slots displayed?

No. The available-slots endpoint filters out slots whose start time is in the past.

## 4. Are already booked slots displayed as available?

No. MediFlow filters out slots where the isBooked field is true.

## 5. How are available slots sorted?

Available slots are returned in ascending order of their start time, so earlier appointments appear first.

## 6. Can two patients book the same appointment slot?

No. MediFlow uses an atomic conditional database update to claim an available slot. Only one booking request can successfully claim a particular slot.

## 7. What happens if two patients try to book the same slot simultaneously?

The backend uses a conditional update that changes isBooked from false to true. If another request has already claimed the slot, the second request receives a conflict response instead of creating another successful booking.

## 8. Can a patient book a slot in the past?

No. MediFlow checks the slot's start time and rejects booking requests for past slots.

## 9. Are appointment slots unique for each doctor?

Yes. The database enforces a unique constraint on the combination of doctorId and startsAt. This prevents duplicate slots for the same doctor at the same start time.

## 10. Does cancelling an appointment make its slot available again?

No. In the current implementation, cancelling an appointment does not release its associated slot. Cancelled and no-show slots are not automatically made available for rebooking.