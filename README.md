# Hotel Management System

A modern, user-friendly hotel management system built with Flask and SQLite. This application allows you to manage hotel rooms, create reservations, and track room availability with an intuitive web interface.

## Features

- 🏨 **Room Management**
  - Add new rooms with type (Single, Double, Suite, VIP) and status
  - View all rooms with their current status and reservations
  - Delete rooms (automatically removes associated reservations)
  
- 📅 **Reservation System**
  - Create reservations for available rooms
  - Automatic status update (room status changes to "reserved" when booked)
  - Date conflict checking to prevent double bookings
  - View reservation details for each room

- 🎨 **Modern UI**
  - Beautiful gradient design with smooth animations
  - Responsive layout for mobile and desktop
  - Color-coded status badges (Available, Reserved, Occupied, Maintenance)
  - Flash messages for user feedback

## Prerequisites

- Python 3.7 or higher
- No database server required (uses SQLite)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Hotel-Management-System
   ```

2. Install the required packages:
   ```bash
   pip install flask
   ```
   
   Or if using a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install flask
   ```

3. The database will be created automatically on first run. No additional setup required!

## Usage

1. Run the application:
   ```bash
   python3 main.py
   ```
   
   Or if using packages from virtual environment:
   ```bash
   PYTHONPATH=env/Lib/site-packages:$PYTHONPATH python3 main.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5001
   ```

3. The application will automatically create the SQLite database (`hotel_management.db`) and necessary tables on first run.

## Application Routes

- `/` - Home page with navigation
- `/add_room` - Add a new room to the system
- `/make_reservation` - Create a new reservation and view available rooms
- `/rooms` - View all rooms and their details

## Database

The application uses SQLite, which means:
- ✅ No database server installation required
- ✅ Database file (`hotel_management.db`) is created automatically
- ✅ All data is stored locally in a single file
- ✅ Tables are created automatically on first connection

### Database Schema

- **rooms**: Stores room information (id, number, type, status)
- **reservations**: Stores reservation details (id, room_id, start_date, end_date)

## Project Structure

```
Hotel-Management-System/
├── main.py                 # Flask application and routes
├── models.py               # Database models and operations (SQLite)
├── hotel_management.db      # SQLite database (auto-created)
├── static/
│   └── static.css          # Modern CSS styling
├── templates/
│   ├── index.html          # Home page
│   ├── add_room.html       # Add room form
│   ├── make_reservation.html # Reservation page
│   └── rooms.html          # Rooms list page
└── README.md               # This file
```

## Features in Detail

### Room Status
- **Available**: Room is free and ready for booking
- **Reserved**: Room has an active reservation
- **Occupied**: Room is currently in use
- **Maintenance**: Room is under maintenance

### Reservation System
- Automatically checks for date conflicts
- Updates room status to "reserved" when booking is made
- Prevents double-booking of the same room for overlapping dates

## Troubleshooting

### Port Already in Use
If port 5001 is already in use, you can:
1. Stop the process using the port:
   ```bash
   lsof -ti :5001 | xargs kill
   ```
2. Or change the port in `main.py`:
   ```python
   app.run(debug=True, port=5002)  # Change to any available port
   ```

### Database Issues
If you encounter database errors:
- Delete `hotel_management.db` and restart the application (it will be recreated)
- Make sure you have write permissions in the project directory

## Technologies Used

- **Flask**: Web framework
- **SQLite**: Database (no server required)
- **HTML/CSS**: Frontend with modern design
- **Python 3**: Backend language
