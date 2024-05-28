OJT Management System

Welcome to the OJT Management System project! This Django-based system helps manage on-the-job training activities for students and organizations.

Features:
- User Authentication: Secure user login and registration functionality.
- Admin Panel: Admin interface for managing users, permissions, and system settings.
- Student Dashboard: Dashboard for students to view their time logs, announcement, upload requirements, progress report, and manage their profiles.
- Time Logging: Recording of time in and time out activities, with image upload support.
- Profile Management: Ability for students to update their profile information.

Installation:

Prerequisites:
- Python 3.x
- Poetry
- PostgreSQL

Steps:
1. Clone the Repository:
   git clone https://github.com/chrstncleofas/OMS.git
   cd OMS

2. Install Dependencies:
   poetry install

3. Set Up Database:
   - Create a PostgreSQL database for the project.
   - Update the database settings in backend_side/settings.py.

4. Run Migrations:
   poetry run python manage.py migrate app and students

5. Create Superuser:
   poetry run python manage.py createsuperuser

6. Run the Development Server:
   poetry run python manage.py runserver

7. Access the Application:
   Open your web browser and go to http://localhost:8000 to access the application.

Usage:
- Admin Panel: Access the admin panel at http://localhost:8000/adminSite to manage users, permissions, and system settings.
- Student Dashboard: Students can log in to view their time logs, upload images, and manage their profiles.
