## Final Year Project Management System

### Project Description
This project is a web-based system developed to facilitate the management of final year projects (FYP) for students, supervisors, panel members, and the FYP committee. The system aims to streamline the process of project allocation, supervision, and evaluation, reducing the time and effort required while enhancing communication and collaboration among all parties involved.

### Features

#### User Management
- **Roles**: FYP Committee, Project Supervisors, Panel Members, Students
- **Account Creation**: Each user must have a user account
- **Role Assignment**: The FYP Committee can assign roles and manage users

#### Interfaces
1. **FYP Committee Interface**
   - Manage users and roles
   - View registered students, groups, and project details
   - Monitor supervisor workload and redistribute projects if necessary
   - Send notifications to supervisors
   - Create evaluation panels
   - Generate reports (Missing Evaluation Report, FYPs Supervised by Faculty Report, Grades Report)
   - Assign deadlines for submissions and evaluations

2. **Panel Members Interface**
   - View FYPs assigned to their panel
   - Fill out evaluation forms
   - Identify and complete missing evaluations

3. **Project Supervisors Interface**
   - View supervised FYPs and their details
   - Read comments and suggestions from panel members
   - View assessment deadlines
   - Identify and complete missing reviews

4. **Students Interface**
   - View group members, project title, and supervisor
   - See assigned panels and read reviews/suggestions (anonymized)
   - View deadlines for presentations and submissions
   - View finalized grades

#### Security and Audit
- **Authentication**: Login and password protection for user access
- **Audit Trail**: Log every action performed by users, including operation details, user identity, and timestamps
- **Triggers**: Generate triggers to detect and log direct database modifications for security

### Technologies Used
- **Backend**: Python, SQLAlchemy (ORM)
- **Frontend**: HTML, CSS
- **Design Pattern**: MVC (Model-View-Controller)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/final-year-project-management-system.git
   cd final-year-project-management-system
   ```

2. **Create a virtual environment and activate it**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup the database**
   ```bash
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
   ```

5. **Run the application**
   ```bash
   python manage.py runserver
   ```

### Project Structure

```
final-year-project-management-system/
│
├── controllers/
│   ├── base_controller.py
│   ├── faculty_controller.py
│   ├── fypCommittee_controller.py
│   ├── login_controller.py
│   ├── register_for_fyp_controller.py
│   ├── signup_controller.py
│   ├── students_controller.py
│   └── user_controller.py
│
├── database/
│   └── site.db
│
├── migrations/
│
├── models/
│   └── models.py
│
├── services/
│   ├── fypCommittee_service.py
│   ├── students_service.py
│   └── user_service.py
│
├── views/
│
├── LICENSE
│
└── app.py
```

### Usage

1. **Register Users**
   - FYP Committee registers students, supervisors, and panel members.
2. **Create Groups**
   - Students are grouped and assigned projects.
3. **Allocate Supervisors and Panels**
   - FYP Committee assigns supervisors and panels.
4. **Evaluation**
   - Panel members fill out evaluation forms during project presentations.
5. **Review and Grade**
   - Supervisors and panel members provide reviews and grades.

### Contribution Guidelines

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
