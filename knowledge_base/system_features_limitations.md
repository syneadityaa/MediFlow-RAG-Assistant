# MediFlow System Features and Limitations

## 1. Does MediFlow provide medical diagnosis?

No. MediFlow is an appointment booking and queue management application. It is not a medical diagnosis or treatment platform.

## 2. Does MediFlow recommend medicines?

No. Medicine recommendations and treatment advice are not features of MediFlow.

## 3. Does MediFlow send email notifications?

No. Email notifications are not currently implemented.

## 4. Does MediFlow send SMS notifications?

No. SMS notifications are not currently implemented.

## 5. Does MediFlow provide an admin dashboard?

No. A dedicated admin dashboard is not currently available.

## 6. Does MediFlow use GPS tracking?

No. The current application does not use GPS tracking to calculate patient travel time or queue position.

## 7. Are queue waiting times guaranteed?

No. Queue waiting times are calculated estimates based on scheduled appointment slots and average consultation durations. Actual waiting times may vary.

## 8. Does MediFlow automatically release cancelled appointment slots?

No. In the current implementation, cancelling an appointment does not release its associated slot. Cancelled and no-show slots cannot automatically be booked again.

## 9. Does MediFlow learn consultation durations from historical patient data?

No. The current implementation uses a fixed average consultation duration configured for each doctor. It does not automatically learn or update this value from completed consultations.

## 10. Does MediFlow provide real-time travel directions?

No. Travel directions and travel-time calculations are not part of the current system.

## 11. Does MediFlow support live queue tracking?

Yes. MediFlow provides queue positions and estimated waiting times through its queue endpoint. The frontend refreshes this information periodically. This is not GPS-based tracking.

## 12. Can MediFlow guarantee that a patient will never experience a waiting delay?

No. MediFlow aims to improve waiting-time visibility and appointment management, but it cannot guarantee zero waiting time.

## 13. Does MediFlow provide personalized medical advice?

No. MediFlow focuses on appointment management and queue tracking rather than personalized medical advice.

## 14. What is the main purpose of MediFlow?

MediFlow aims to improve clinic appointment management and reduce uncertainty during hospital visits by allowing patients to book appointments, check in and monitor their queue position and estimated waiting time.