# MediFlow Queue Management FAQ

## 1. What is queue management in MediFlow?

Queue management helps patients understand their position in the waiting queue and estimate how long they may need to wait before their consultation begins.

## 2. How does MediFlow calculate queue position?

MediFlow considers booked and checked-in appointments for a doctor. It orders waiting appointments using their scheduled slot times, while handling late check-ins separately.

## 3. What is the difference between queue position and appointment time?

Appointment time is the scheduled start time of a patient's slot. Queue position indicates the patient's current order among appointments waiting for that doctor's consultation.

## 4. How does MediFlow estimate waiting time?

MediFlow uses the doctor's average consultation duration, the time remaining in an active consultation, scheduled appointment times and the order of waiting appointments to calculate estimated waiting times.

## 5. Does MediFlow store waiting-time estimates permanently?

No. Waiting-time estimates are calculated dynamically whenever the queue endpoint is requested. They are not stored as permanent appointment values.

## 6. Does the queue consider an active consultation?

Yes. MediFlow checks whether the doctor currently has an appointment with IN_CONSULTATION status. It estimates the remaining consultation time and uses it when calculating waiting times.

## 7. What happens if a consultation takes longer than the average duration?

If an active consultation exceeds the doctor's average consultation duration, MediFlow assumes a minimum remaining time of 5 minutes for its queue calculation instead of reducing the estimate to zero.

## 8. What happens when a patient checks in late?

Patients who check in after their scheduled slot start time are placed behind patients who are already waiting. Late check-ins are ordered according to their check-in timestamps.

## 9. Does MediFlow automatically update queue information?

The queue tracking interface refreshes queue information automatically every 15 seconds, allowing patients to see updated queue positions and estimates.

## 10. Are estimated waiting times guaranteed?

No. Waiting times are estimates, not guarantees. They may change as consultations progress, appointments are cancelled or patients are marked as no-show.

## 11. Does the estimated waiting time include travel time to the hospital?

No. The estimate represents the expected waiting time at the clinic. It does not calculate travel time or the time required to reach the hospital.

## 12. Does MediFlow consider appointments from previous days?

The queue calculation ignores stale BOOKED and CHECKED_IN appointments from earlier days so they do not inflate the current day's estimates. An active consultation is handled separately.

## 13. What happens when a doctor has no active consultation?

When there is no active consultation, the projected queue starts from the current time. Each waiting appointment is still scheduled no earlier than its own slot start time.

## 14. What information does the queue endpoint return?

The queue endpoint returns:
- Doctor ID
- Queue generation timestamp
- Average consultation duration
- Active consultation information, if present
- Waiting patient count
- Queue position for each waiting appointment
- Estimated waiting time
- Estimated start time
- An estimate disclaimer

## 15. Does MediFlow use GPS to calculate the queue?

No. The current queue implementation does not use GPS or patient location. It calculates waiting estimates using appointment slots and consultation durations.

## 16. How often are waiting-time estimates recalculated?

The backend recalculates estimates whenever the queue endpoint is requested. The frontend refreshes queue information every 15 seconds.

## 17. Does MediFlow guarantee that patients will be seen in the exact estimated order?

No. The queue provides a calculated projection based on current appointment states. Actual consultation progress can change the projected waiting times and positions.