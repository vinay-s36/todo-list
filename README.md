# Todo List

This is a simple Todo application built with Django that helps users manage their tasks efficiently. The application allows users to add, edit, delete, and mark tasks as completed.

## Setup Instructions

### Prerequisites

- Python (>=3.8)
- pip (>=20.x)
- virtualenv (optional but recommended)

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/vinay-s36/todo-list.git
   cd todo-list
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Environment Variables

To configure the environment variables, follow these steps:

1. Copy the `.env.example` file to `.env`:

   ```sh
   cp .env.example .env
   ```

2. Open the `.env` file and add your database and email credentials:
   ```env
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=your_db_port
   EMAIL_HOST_USER=email_user
   EMAIL_HOST_PASSWORD=email_pass
   ```

Make sure to replace `your_db_name`, `your_db_user`, `your_db_password`, `your_db_host`, `your_db_port` with your actual database credentials and `EMAIL_HOST_USER`, `EMAL_HOST_PASSWORD` with your actual email credentials.

### Running the Application

1. Apply migrations:

   ```sh
   python manage.py migrate
   ```

2. Start the development server:

   ```sh
   python manage.py runserver
   ```

3. Open your browser and navigate to `http://localhost:8000`.

## Happy coding! 🚀
