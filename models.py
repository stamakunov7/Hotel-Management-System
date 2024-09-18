import mysql.connector
from mysql.connector import Error

# Connection to MySQL database
def create_connection():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            port = '3306',
            user='tim',
            password='Timik303',
            database='hotel_management'
        )
        if conn.is_connected():
            print("Successfully connected to the database")
    except Error as e:
        print(f"Error: '{e}'")
    return conn

# Add a new room to the database
def add_room(connection, number, room_type, status):
    cursor = connection.cursor() # cursor is used to perform SQL queries
    query = "INSERT INTO rooms (number, type, status) VALUES (%s, %s, %s)" # %s is a placeholder for the values we want to insert into the query
    cursor.execute(query, (number, room_type, status)) 
    connection.commit() # save the changes to the database
    cursor.close() 

# Make a reservation for a room
def make_reservation(room_number, start_date, end_date):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Select the room ID based on the provided room number
            cursor.execute("SELECT id FROM rooms WHERE number = %s", (room_number,))
            room_result = cursor.fetchone()

            if room_result:
                room_id = room_result[0]
                # Check if the room is available
                cursor.execute("""
                SELECT COUNT(*) FROM reservations
                WHERE room_id = %s AND (
                    (start_date BETWEEN %s AND %s) OR 
                    (end_date BETWEEN %s AND %s) OR
                    (%s BETWEEN start_date AND end_date) OR
                    (%s BETWEEN start_date AND end_date)
                )
                """, (room_id, start_date, end_date, start_date, end_date, start_date, end_date))
                
                availability_count = cursor.fetchone()[0]
                if availability_count == 0:
                    # Room is available, proceed to insert the reservation
                    insert_query = """
                    INSERT INTO reservations (room_id, start_date, end_date) 
                    VALUES (%s, %s, %s)
                    """
                    cursor.execute(insert_query, (room_id, start_date, end_date))
                    conn.commit()
                    return True, "Reservation successfully made."
                else:
                    return False, "The room is not available for the selected dates."
            else:
                return False, "No room with that number exists."
        except Error as e:
            return False, f"Error: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    return False, "Could not connect to the database."

# Get all rooms from the database
def get_all_rooms():
    conn = create_connection()
    rooms = [] # creating an empty list to store the fetched rooms
    if conn is not None: # checking the connection
        try:
            cursor = conn.cursor()
            # Adjust the query to join with the reservations table and fetch the required fields
            query = """
            SELECT r.number, r.type, r.status, res.start_date, res.end_date
            FROM rooms r
            LEFT JOIN reservations res ON r.id = res.room_id 
            """ # I added the LEFT JOIN clause to join the rooms and reservations tables based on the room ID, and r. is an alias for the rooms table (like a shortcut to avoid typing the full table name every time) same for res. and reservations table
            cursor.execute(query)
            column_names = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            rooms = [dict(zip(column_names, row)) for row in rows]
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            cursor.close()
            conn.close()
    return rooms
