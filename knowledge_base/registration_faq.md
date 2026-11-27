# MediFlow Registration FAQ

## 1. How can I register on MediFlow?

Patients can create an account through the MediFlow registration page. They need to provide their full name, email address and password. After successful registration, they are redirected to the login page to sign in.

## 2. What information is required during registration?

The patient registration form requires three fields:
- Full name
- Email address
- Password (minimum 8 characters)

All three fields are mandatory.

## 3. Can doctors register themselves on MediFlow?

No. The public registration page is designed exclusively for patients. Doctor accounts are created and managed directly by the clinic. Doctors should contact their clinic administrator to obtain their login credentials.

## 4. Do I need an account to book an appointment?

Yes. Patients must register and log in before booking appointments. Appointment booking is a protected feature available to authenticated patient accounts.

## 5. What happens after successful registration?

After creating an account successfully, MediFlow displays a confirmation message and redirects the patient to the login page. The patient can then sign in using their registered email address and password.

## 6. Can I register using an existing email address?

Each MediFlow user account must have a unique email address. The system enforces email uniqueness, so an email address already associated with an account cannot be used to create another account.

## 7. Are passwords stored securely?

Yes. MediFlow uses password hashing with bcryptjs rather than storing passwords as plain text. Authentication is handled using JWT-based authentication.

## 8. What types of accounts are available in MediFlow?

MediFlow supports two primary user workflows:

- **Patient:** Can search for doctors, view available slots, book and manage appointments, check in and track queue status.
- **Doctor:** Can access a doctor dashboard, view daily appointments, manage consultations and mark appointment statuses.

Doctor accounts are provisioned by the clinic rather than through public registration.

## 9. Can I access MediFlow immediately after registration?

After successful registration, patients must sign in through the login page. Once authenticated, they can access patient features such as doctor search, appointment booking and their dashboard.

## 10. What should I do if registration fails?

Check that all required fields are filled in correctly, that your email address is valid and that your password contains at least 8 characters. If the problem persists, try again with a valid email address that is not already registered.