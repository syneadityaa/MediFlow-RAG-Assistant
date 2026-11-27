# MediFlow Doctor Search FAQ

## 1. How can I search for doctors on MediFlow?

Patients can browse the available doctors through the doctor search section. MediFlow provides doctor information including the doctor's name, specialty and rating.

## 2. Can I search doctors by specialty?

Yes. MediFlow supports filtering doctors by specialty. The specialty filter uses case-insensitive matching.

## 3. What information about doctors is displayed?

The doctor listing API returns:
- Doctor ID
- Doctor name
- Specialty
- Average consultation duration
- Rating

## 4. Can I sort doctors by rating?

Yes. The doctor listing API supports sorting by rating in ascending or descending order. It also supports sorting by doctor ID.

## 5. Does MediFlow support pagination in doctor search?

Yes. Doctor search supports pagination.

The default page is 1 and the default page size is 10. The maximum allowed page size is 50.

## 6. Can I view all available doctors?

The doctor listing endpoint returns doctors according to the requested page and page size. Users can navigate through the available pages.

## 7. Can I check a doctor's available appointment slots?

Yes. Patients can select a doctor and retrieve their future available appointment slots.

## 8. What happens if a doctor does not exist?

MediFlow returns a doctor-not-found response when an invalid or nonexistent doctor ID is requested for slot retrieval.

## 9. Can I view a doctor's queue?

Yes. MediFlow provides a queue endpoint for a specific doctor. It returns queue information and estimated waiting times.

## 10. Does MediFlow support searching doctors by location?

Location-based doctor search is not documented as an implemented feature. The current doctor listing implementation supports specialty filtering.