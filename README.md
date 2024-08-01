# Community Empowerment Portal-Backend

## Description

This project serves as a comprehensive platform that consolidates government schemes, scholarships, job opportunities, and other beneficial programs specifically tailored for minority communities and SC/ST communities. It aims to provide a centralized resource for individuals from these communities to easily access and benefit from various government initiatives.

## Installation and Setup Guide

### Prerequisites

- **Python 3.9 and above:** Make sure Python 3.9 or above is installed on your system.
- **pip:** Python package installer for installing dependencies.
- **Virtualenv:** Helps to create isolated Python environments.
- **PostgreSQL:** A relational database system that you need for database operations.

### Step-by-Step Installation

#### Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### Create and Activate a Virtual Environment

It is recommended to use a virtual environment to manage dependencies. You can create and activate a virtual environment using the following commands:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

Install the necessary dependencies using pip:

```bash
pip install -r requirements.txt
```

### Configure the Database

Update the `DATABASES` setting in `settings.py` to configure your database. If you're using PostgreSQL, make sure you have it installed and configured on your machine.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yourdbname',
        'USER': 'yourdbuser',
        'PASSWORD': 'yourdbpassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

### Set Up Environment Variables

```bash
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://yourdbuser:yourdbpassword@localhost/yourdbname
```

### Run Database Migrations

Apply database migrations to set up your database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a Superuser

Create a superuser account to access the Django admin interface:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your superuser account.

### Run the Development Server

Start the development server to test if everything is set up correctly:

```bash
python manage.py runserver
```

You should be able to access the application at http://127.0.0.1:8000.

### Additional Notes

- **PostgreSQL Installation:** Make sure PostgreSQL is properly installed and running on your machine. You can download and install it from the [official PostgreSQL website](https://www.postgresql.org/download/).

- **Django Admin Panel:** Access the Django admin panel at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) using the superuser account you created.

- **Environment Variables:** Ensure that your `.env` file is correctly configured and included in your `.gitignore` to avoid exposing sensitive information.

## Features

- **Comprehensive Scheme Listings:** Consolidates government schemes for minority and SC/ST communities.
- **Search and Filter:** Allows users to search and filter schemes based on various criteria.
- **Admin Interface:** Manage and update schemes, scholarships, and job opportunities from the Django admin panel.
