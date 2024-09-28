# Hotel Management System

This is a simple hotel management system built with Flask and MySQL. It allows users to manage rooms and make reservations.

## Features

- Add new rooms
- Make reservations
- View all rooms

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- MySQL

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hotel-management-system.git
   cd hotel-management-system
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your MySQL database using the schema provided in `database_schema.txt`.

4. Create a `.env` file in the project root and add your database credentials:
   ```bash
   DB_HOST=your_host
   DB_PORT=your_port
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=your_database_name
   ```

## Usage

To run the application:

```
python main.py
```

Then, navigate to `http://localhost:5000` in your web browser.

## Project Structure

- `main.py`: The main Flask application
- `models.py`: Database models and operations
- `templates/`: HTML templates for the web pages
- `database_schema.txt`: SQL schema for the database
