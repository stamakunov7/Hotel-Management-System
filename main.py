from flask import Flask, render_template, g, request, redirect, url_for, flash
import models

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_room', methods=['GET', 'POST']) # GET is used to request data from a specified resource, POST is used to submit data to be processed to a specified resource
def add_room():
    if request.method == 'POST':
        number = request.form['number'] # request.form is just a data that user inputs into an HTML form and sends to the server, and it is stored in a dictionary
        room_type = request.form['type']
        status = request.form['status']
        connection = models.create_connection()
        if connection is not None: # if connection is not None, then add room. If is None, then return to index page
            models.add_room(connection, number, room_type, status)
            connection.close()
        return redirect(url_for('index'))
    return render_template('add_room.html')

# Requests data from the web page and sends it to the server
@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'POST':
        room_number = request.form['number']  
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        success, message = models.make_reservation(room_number, start_date, end_date)
        
        if success:
            flash(message, 'success') # Flash success message
        else:
            flash(message, 'error') # Flash error message
        
        return redirect(url_for('make_reservation'))
    
    rooms = models.get_all_rooms()
    return render_template('make_reservation.html', rooms=rooms)

# This route is used to get all the rooms in the database and display them in the rooms.html file
@app.route('/rooms', methods=['GET'])
def get_rooms():
    connection = models.create_connection()
    rooms = []
    if connection is not None:
        rooms = models.get_all_rooms()
        connection.close()
    return render_template('rooms.html', rooms=rooms)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)


    