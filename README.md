# Invoice Generator

A Django-based invoice management and PDF generation web application for creating, managing, and downloading professional invoices.

## Overview

This project is a full-stack web application built with **Python and Django**.

The application allows users to create invoices, manage invoice information, and generate invoices as downloadable PDF files.

The project was built to practice building a practical Django application with database-backed functionality, document generation, and email configuration.

## Technologies

* Python
* Django
* HTML
* CSS
* JavaScript
* SQLite
* Git
* GitHub
* PDF generation

## Features

* Create invoices
* Manage invoice information
* Generate invoices as PDF files
* Download generated PDF invoices
* Store invoice data in the database
* Manage invoice items
* Calculate invoice totals
* Customer information management
* Django forms
* Form validation
* CRUD operations
* Email functionality
* Web-based invoice management

## How It Works

The application provides a web interface for creating and managing invoices.

A typical workflow is:

```text id="e8h4qs"
Create Invoice
      ↓
Add Customer Information
      ↓
Add Invoice Items
      ↓
Calculate Total
      ↓
Generate PDF
      ↓
Download Invoice
```

Users can create an invoice, provide the required information, add products or services, and generate a PDF version of the invoice.

The generated PDF can then be downloaded for use outside the application.

## PDF Generation

One of the main features of the project is the ability to generate invoices as **PDF documents**.

After creating an invoice, the application generates a corresponding PDF that can be downloaded by the user.

This demonstrates the integration of document generation into a Django web application rather than simply displaying invoice information in an HTML page.

## Email Configuration

The project includes email-related functionality that requires environment variables.

The original development environment contained private email credentials, so those credentials are **not included in this repository**.

You must provide your own email configuration if you want to use the email functionality.

### Environment Variables

Create a `.env` file according to the variables expected by the project.

For example:

```env id="q6w1sr"
EMAIL_BACKEND=
EMAIL_HOST=
EMAIL_PORT=
EMAIL_USE_TLS=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

The exact variables required may depend on the current project configuration.

### Important

**Never add real passwords, API keys, or other private credentials to GitHub.**

Use your own development credentials and keep the `.env` file private.

A `.env.example` file can be used as a template without containing actual credentials.

## Installation

### 1. Clone the Repository

```bash id="p3k7hx"
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd InvoiceGenerator
```

### 2. Create a Virtual Environment

```bash id="r8n2mv"
python -m venv venv
```

Activate it:

**macOS / Linux**

```bash id="c4d9ya"
source venv/bin/activate
```

**Windows**

```bash id="j7x5qw"
venv\Scripts\activate
```

### 3. Install Dependencies

```bash id="a6f1ze"
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create your `.env` file and add the required email configuration.

Do not use the credentials from the original development environment.

### 5. Apply Database Migrations

```bash id="n9v3pk"
python manage.py migrate
```

### 6. Create a Superuser

```bash id="w4c8sd"
python manage.py createsuperuser
```

Follow the prompts to create your administrator account.

### 7. Start the Development Server

```bash id="h2m6vx"
python manage.py runserver
```

Open the application:

```text id="k5r1qt"
http://127.0.0.1:8000/
```

## Testing the Application

After starting the application, you can test the main invoice workflow:

1. Create or access a user account.
2. Create an invoice.
3. Enter customer information.
4. Add invoice items.
5. Review the calculated invoice total.
6. Generate the invoice.
7. Download the generated PDF.
8. Test the email functionality if your email environment has been configured.

## Project Structure

The project follows a standard Django architecture.

```text id="n3q8vf"
InvoiceGenerator/
├── manage.py
├── requirements.txt
├── .env.example
├── project/
├── application/
├── templates/
├── static/
└── ...
```

> The exact application and directory names may vary depending on the current repository structure.

## What I Built

This project gave me practical experience building a complete Django application around a real-world business use case.

I worked with:

* Django project architecture
* Django applications
* Database models
* Database relationships
* CRUD operations
* Forms
* Views
* Templates
* Form validation
* Invoice calculations
* PDF generation
* File handling
* Email configuration
* Environment variables
* Git and GitHub

## Project Status

**Completed educational/backend project.**

The project is provided as source code and requires local environment configuration for email-related functionality.

## Security

Private credentials are intentionally excluded from the repository.

Never commit:

* Email passwords
* API keys
* Django secret keys
* Database credentials
* Private environment variables

Use `.env` for local configuration and keep it excluded from Git.

## Running the Project

Quick setup:

```bash id="s8k3nd"
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd InvoiceGenerator

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Create and configure your .env file

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

For Windows:

```bash id="u2f6rm"
venv\Scripts\activate
```

instead of the macOS/Linux activation command.

## License

This project is available for educational and portfolio purposes.
