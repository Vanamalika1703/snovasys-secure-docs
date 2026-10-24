# Snovasys Secure Document Management System

## Project Overview

A web-based document management system built using Django. It allows authenticated users to create, view, edit, and delete their documents, with server-side permission checks and audit logging.

## Features

- User authentication using Django.
- Create, view, edit, and delete documents.
- Document ownership and access control.
- Staff access to documents, according to the implemented permission checks.
- Audit logs for document actions and unauthorized access attempts.
- Automated tests for document functionality, permissions, and audit logging.
- Django templates for the user interface.

## Technology Stack

- Python
- Django
- SQLite for local development
- HTML and CSS
- Django automated testing framework

## Prerequisites

- Python installed
- Git installed
- A terminal such as PowerShell or the VS Code terminal

## Run Locally

### 1. Clone the repository

Replace the URL below if your repository URL is different.

```bash
git clone https://github.com/Vanamalika1703/snovasys-secure-docs.git
cd snovasys-secure-docs
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

If the project includes `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

If that file does not exist yet, install Django using the version required by your project.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrator account

```bash
python manage.py createsuperuser
```

Follow the prompts to create your account.

### 7. Start the development server

```bash
python manage.py runserver
```

Open the local URL shown in the terminal, usually:

http://127.0.0.1:8000/

## Run Tests

Run the document app's tests with:

```bash
python manage.py test documents
```

Check that the tests pass before submitting the project.

## Security Notes

- Authentication is required for protected document views.
- Document permissions are checked on the server.
- Unauthorized access attempts are logged.
- CSRF protection should be retained on POST forms.
- Production deployments should use environment variables for secrets and database credentials.
- Production deployments should disable Django debug mode and configure allowed hosts appropriately.

## Deployment

Live application URL: To be added after deployment.

Deployment configuration, production database setup, and static-file serving should be documented once they are configured and tested.

## Known Limitations

Document the features that remain incomplete after final testing, such as additional role management, improved validation, or an audit-log interface.

## AI Assistance

AI tools were used for development assistance, including code guidance, debugging, and documentation. All generated code and suggested fixes should be reviewed and tested before submission.

## Repository

https://github.com/Vanamalika1703/snovasys-secure-docs
