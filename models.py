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
            cursor.execute("SELECT id FROM rooms WHERE number = %s", (room_number,)) # '%s' is a placeholder for the room number we want to insert into the query
            room_result = cursor.fetchone()

            if room_result: # if the room is found in the database then perform the following actions
                room_id = room_result[0]
                # Insert the new reservation with the fetched room ID
                insert_query = """
                INSERT INTO reservations (room_id, start_date, end_date) 
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query, (room_id, start_date, end_date))
                conn.commit()
            else:
                print("No room with that number exists.") # I tried to print this message if the room is not found, but it doesn't work. It just will take me to the index page without any message
        except Error as e:
            print(f"Error: '{e}'") # And this is just a general error message
        finally:
            cursor.close()
            conn.close()

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
