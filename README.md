Project Description: HappenChain


HappenChain is a comprehensive Event Management System designed for educational institutions, handling hierarchies from Colleges to Departments and Students. It allows for the creation, management, and participation in various academic and extra-curricular events.

Tech Stack


Backend Framework: Python (Django 6.0.1)

Database: MySQL (django.db.backends.mysql)

Frontend: Standard Django Templates (HTML/CSS/JS)

Dependencies: asgiref, pymysql, sqlparse, tzdata


Core Modules & Features


User Roles & Authentication (authapp, appuser):

Roles: System Admin, College Admin, Department Admin, and Student (AppUser).

Profiles: Students have profiles with ID photos, verification status, and academic details (College, Dept, Course).

Social: Built-in Friend Request system allows students to connect, facilitating team formations.

Administrative Structure (college_admin, department_admin):

Hierarchy: Colleges manage Departments; Departments manage Courses and Degrees.

Verification: Colleges and Students go through a verification process (Pending/Accepted/Rejected).


Event Management:

Events: Organized by Departments, categorized by Event Type.

Sub-Events: Specific competitions or activities within an Event. Can be Individual or Team-based.

Team Logic: Students can form teams with their confirmed friends. The system enforces team size limits (min/max).


Registration & Finance:


Registration: Workflow for students to register for sub-events.

Payments: Tracks transaction IDs and payment statuses for registrations.

Utilities:

Complaints: Students can lodge complaints against specific entities/issues.

Notifications: System-wide alerts for users.
