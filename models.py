import sqlite3
import os
from datetime import datetime

# Database file path
DB_FILE = 'hotel_management.db'

# Connection to SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # This allows column access by name
        # Initialize database tables if they don't exist
        init_database(conn)
        print("Successfully connected to the database")
    except Exception as e:
        print(f"Error: '{e}'")
    return conn

# Initialize database - create tables if they don't exist
def init_database(conn):
    cursor = conn.cursor()
    
    # Create rooms table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    
    # Create reservations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
    """)
    
    conn.commit()
    cursor.close()

# Add a new room to the database
def add_room(connection, number, room_type, status):
    cursor = connection.cursor()
    query = "INSERT INTO rooms (number, type, status) VALUES (?, ?, ?)"
    cursor.execute(query, (number, room_type, status))
    connection.commit()
    cursor.close()

# Make a reservation for a room
def make_reservation(room_number, start_date, end_date):
    conn = create_connection()
    if conn is not None:
        cursor = None
        try:
            cursor = conn.cursor()
            # Select the room ID based on the provided room number
            cursor.execute("SELECT id FROM rooms WHERE number = ?", (room_number,))
            room_result = cursor.fetchone()

            if room_result:
                room_id = room_result[0]
                # Check if the room is available
                cursor.execute("""
                SELECT COUNT(*) FROM reservations
                WHERE room_id = ? AND (
                    (start_date BETWEEN ? AND ?) OR 
                    (end_date BETWEEN ? AND ?) OR
                    (? BETWEEN start_date AND end_date) OR
                    (? BETWEEN start_date AND end_date)
                )
                """, (room_id, start_date, end_date, start_date, end_date, start_date, end_date))
                
                availability_count = cursor.fetchone()[0]
                if availability_count == 0:
                    # Room is available, proceed to insert the reservation
                    insert_query = """
                    INSERT INTO reservations (room_id, start_date, end_date) 
                    VALUES (?, ?, ?)
                    """
                    cursor.execute(insert_query, (room_id, start_date, end_date))
                    # Update room status to reserved when reservation is made
                    update_status_query = "UPDATE rooms SET status = ? WHERE id = ?"
                    cursor.execute(update_status_query, ('reserved', room_id))
                    conn.commit()
                    return True, "Reservation successfully made."
                else:
                    return False, "The room is not available for the selected dates."
            else:
                return False, "No room with that number exists."
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    return False, "Could not connect to the database."

# Get all rooms from the database
def get_all_rooms():
    conn = create_connection()
    rooms = [] # creating an empty list to store the fetched rooms
    if conn is not None: # checking the connection
        cursor = None
        try:
            cursor = conn.cursor()
            # Adjust the query to join with the reservations table and fetch the required fields
            query = """
            SELECT r.number, r.type, r.status, res.start_date, res.end_date
            FROM rooms r
            LEFT JOIN reservations res ON r.id = res.room_id 
            ORDER BY r.number
            """ # I added the LEFT JOIN clause to join the rooms and reservations tables based on the room ID, and r. is an alias for the rooms table (like a shortcut to avoid typing the full table name every time) same for res. and reservations table
            cursor.execute(query)
            rows = cursor.fetchall()
            # Convert rows to dictionaries
            for row in rows:
                rooms.append({
                    'number': row[0],
                    'type': row[1],
                    'status': row[2],
                    'start_date': row[3],
                    'end_date': row[4]
                })
        except Exception as e:
            print(f"Error: '{e}'")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    return rooms

# Delete a room from the database
def delete_room(room_number):
    conn = create_connection()
    if conn is not None:
        cursor = None
        try:
            cursor = conn.cursor()
            # First, delete all reservations for this room
            cursor.execute("SELECT id FROM rooms WHERE number = ?", (room_number,))
            room_result = cursor.fetchone()
            
            if room_result:
                room_id = room_result[0]
                # Delete reservations first (due to foreign key constraint)
                cursor.execute("DELETE FROM reservations WHERE room_id = ?", (room_id,))
                # Then delete the room
                cursor.execute("DELETE FROM rooms WHERE number = ?", (room_number,))
                conn.commit()
                return True, "Room deleted successfully."
            else:
                return False, "Room not found."
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    return False, "Could not connect to the database."
