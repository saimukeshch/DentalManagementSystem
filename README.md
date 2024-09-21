# Dental Management System

Welcome to the Dental Management System! This Django-based web application is designed manage clinics, doctors, patients, and appointments.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.8 or newer
- pip 

### Installation

Follow these steps to set up your environment:

1. **Clone the repository:**
   
   git clone https://github.com/saimukeshch/DentalManagementSystem.git
   cd dental-management-system

2. **Set up a Python virtual environment (Optional):**
    
    python -m venv myenv
    source myenv/bin/activate  ( On Windows use `myenv\Scripts\activate`)

3. **Install the required packages:**
    
    pip install -r requirements.txt

4. **Run the following commands to set up the database (make sure your database settings in settings.py are configured for your local environment):**

    python manage.py makemigrations Users
    python manage.py makemigrations Clinics
    python manage.py makemigrations Doctors
    python manage.py makemigrations Patients
    
    python manage.py migrate 

    Note: To insert doctor specialties, run 'SampleData.sql' provided in the directory (DO NOT FORGET to change the username to the username used in the settings.py).

5. **Run the development server: Start the Django development server:**

    python manage.py runserver


=> The server will start running on http://127.0.0.1:8000/



**Usage**
After setting up the project, you can access it through your web browser at http://127.0.0.1:8000/. 

**Here’s how to use the key features:**


Dashboard has Sign up/ sign in button and 3 tabs( Clinics, Patients and Doctors)

When you hit 'Sign up/ Sign in' button it will take you to sign in page. If you are a new user hit 'Sign up' and register as a new user. Then log in with your credentials.

Login to the system to view list of Clinics, Patients and Doctors

Clinic Management:
Add a new clinic and manage clinic details including their addresses and contact info.

Doctor Management: 
Add a new doctor and manage details about doctors including their specializations and schedules.

Patient Management: 
Add and manage patient information and track their appointment histories.

Appointment Scheduling: 
Schedule and manage appointments through patient details page.


**Key Features & API Usage**

General Navigation:

Dashboard - http://127.0.0.1:8000/

User Management:

Login - http://127.0.0.1:8000/login/
Logout - http://127.0.0.1:8000/logout/
Register - http://127.0.0.1:8000/register/

Clinic Management:

View Clinics - http://127.0.0.1:8000/clinics/
    => You can edit clinic details, view/edit/delete affiliated doctors and add doctor affiliation
Add Clinic - http://127.0.0.1:8000/add_clinic/

Doctor Management:

View Doctors - http://127.0.0.1:8000/doctors/
    => You can edit doctor details, view affiliations with Clinics and affiliated patients
Add Doctor - http://127.0.0.1:8000/add_doctor/


Patient Management:

View Patients - http://127.0.0.1:8000/patients/
     => You can edit patient details, schedule new appointment, view patient visit history and upcoming appointments
Add Patient - http://127.0.0.1:8000/add_patient/




