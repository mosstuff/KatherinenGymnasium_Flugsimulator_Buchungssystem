from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import sqlite3
import os
import datetime

app = Flask(__name__)

# Function to initialize the database
def initialize_database():
    with sqlite3.connect('booking.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS bookings
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, ph_desc TEXT, activity TEXT, timeslot TEXT, qr_code TEXT, status TEXT)''')
        conn.commit()

# Check if the database file exists, if not, create the database
if not os.path.exists('booking.db'):
    initialize_database()

def get_next_10_minute_range():
    current_time = datetime.datetime.now().time()
    next_10_minutes = (current_time.minute // 10 + 1) * 10
    if next_10_minutes == 60:
        next_10_minutes = 0
        current_hour = current_time.hour + 1
    else:
        current_hour = current_time.hour
    next_time10 = current_time.replace(hour=current_hour, minute=next_10_minutes, second=0, microsecond=0)

    next_20_minutes = (current_time.minute // 10 + 1) * 10 + 10
    if next_20_minutes >= 60:
        next_20_minutes -= 60
        current_hour += 1
    next_time20 = current_time.replace(hour=current_hour, minute=next_20_minutes, second=0, microsecond=0)

    final_time = next_time10.strftime("%H:%M") + " - " + next_time20.strftime("%H:%M")

    return final_time


def get_current_10_minute_range():
    current_time = datetime.datetime.now().time()
    current_10_minutes = (current_time.minute // 10) * 10
    current_time10 = current_time.replace(minute=current_10_minutes, second=0, microsecond=0)

    # Check if adding 10 minutes would exceed 59 minutes
    if current_10_minutes == 50:
        current_time20 = current_time.replace(hour=current_time.hour + 1, minute=0, second=0, microsecond=0)
    else:
        current_time20 = current_time.replace(minute=current_10_minutes + 10, second=0, microsecond=0)

    final_time = current_time10.strftime("%H:%M") + " - " + current_time20.strftime("%H:%M")

    return final_time

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logo.png')
def logo():
    return send_file('./templates/airk.png')

@app.route('/instructor')
def inst():
    return render_template('instructor.html')

@app.route('/instructor/kampfjet')
def instkj():
    return render_template('instructor_kj.html')

@app.route('/instructor/propeller')
def instpp():
    return render_template('instructor_pp.html')

@app.route('/get_next_time_slot')
def get_next_time_slot():
    activity = str(request.args.get('activity'))
    print(activity)

    next_time = get_current_10_minute_range()
    print(next_time)
    # Get the next available time slot for the selected activity
    with sqlite3.connect('booking.db') as conn:
        c = conn.cursor()
        c.execute("SELECT name, status, ph_desc  FROM bookings WHERE activity = ? AND timeslot = ?", (activity, next_time))
        row = c.fetchone()
        if row:
            return jsonify({'name': row[0], 'status': row[1], 'ph_desc': row[2]})
        else:
            return jsonify('None')

@app.route('/get_next_next_time_slot')
def get_next_next_time_slot():
    activity = str(request.args.get('activity'))
    print(activity)

    next_time = get_next_10_minute_range()
    print(next_time)
    # Get the next available time slot for the selected activity
    with sqlite3.connect('booking.db') as conn:
        c = conn.cursor()
        c.execute("SELECT name, status, ph_desc  FROM bookings WHERE activity = ? AND timeslot = ?", (activity, next_time))
        row = c.fetchone()
        if row:
            return jsonify({'name': row[0], 'status': row[1], 'ph_desc': row[2]})
        else:
            return jsonify('None')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        with sqlite3.connect('booking.db') as conn:
            name = request.form['name']
            ph_desc = request.form['ph_desc']
            activity = request.form['activity']
            timeslot = request.form['timeslot']
            qr_code = request.form['qr_code']
            status = "Booked"

            c = conn.cursor()
            c.execute("INSERT INTO bookings (name, ph_desc, activity, timeslot, qr_code, status) VALUES (?, ?, ?, ?, ?, ?)",
                      (name, ph_desc, activity, timeslot, qr_code, status))
            conn.commit()

        return redirect(url_for('booking'))
    else:
        return render_template('booking.html')

@app.route('/get_booked_timeslots')
def get_booked_timeslots():
    activity = request.args.get('activity')
    with sqlite3.connect('booking.db') as conn:
        c = conn.cursor()
        c.execute("SELECT timeslot FROM bookings WHERE activity = ? AND status IN ('Booked', 'Arrived')", (activity,))
        booked_timeslots = [row[0] for row in c.fetchall()]
        return jsonify(booked_timeslots)

@app.route('/get_next_timeslot')
def get_timeslots():
    timeslots = {
        "Kampfjet": ["17:00 - 17:10", "17:10 - 17:20", "17:20 - 17:30", "17:30 - 17:40", "17:40 - 17:50", "17:50 - 18:00", "18:00 - 18:10", "18:10 - 18:20", "18:20 - 18:30", "18:30 - 18:40", "18:40 - 18:50", "18:50 - 19:00", "19:00 - 19:10", "19:10 - 19:20", "19:20 - 19:30", "19:30 - 19:40", "19:40 - 19:50", "19:50 - 20:00"],
        "Propeller": ["17:00 - 17:10", "17:10 - 17:20", "17:20 - 17:30", "17:30 - 17:40", "17:40 - 17:50", "17:50 - 18:00", "18:00 - 18:10", "18:10 - 18:20", "18:20 - 18:30", "18:30 - 18:40", "18:40 - 18:50", "18:50 - 19:00", "19:00 - 19:10", "19:10 - 19:20", "19:20 - 19:30", "19:30 - 19:40", "19:40 - 19:50", "19:50 - 20:00"]
        # Add more activities and their corresponding timeslots as needed
    }

    with sqlite3.connect('booking.db') as conn:
        c = conn.cursor()
        c.execute("SELECT activity, timeslot, status FROM bookings WHERE status IN ('Booked', 'Arrived')")
        booked_timeslots = {activity: set() for activity in timeslots.keys()}
        for row in c.fetchall():
            activity = row[0]
            timeslot = row[1]
            booked_timeslots[activity].add(timeslot)

    # Filter out booked timeslots for each activity
    for activity in timeslots.keys():
        timeslots[activity] = [timeslot for timeslot in timeslots[activity] if timeslot not in booked_timeslots[activity]]

    return jsonify(timeslots)



@app.route('/get_bookings')
def get_bookings():
    with sqlite3.connect('booking.db') as conn:
        c = conn.cursor()
        c.execute("SELECT name, ph_desc, activity, timeslot, status FROM bookings ORDER BY timeslot ASC")
        bookings = [{'name': row[0], 'ph_desc': row[1], 'activity': row[2], 'timeslot': row[3], 'status': row[4]} for row in c.fetchall()]
        return jsonify(bookings)

@app.route('/remove_booking', methods=['DELETE'])
def remove_booking():
    booking_name = request.args.get('name')
    with sqlite3.connect('booking.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM bookings WHERE name = ?", (booking_name,))
        conn.commit()
        return '', 204  # No content response for successful deletion


@app.route('/instascan.min.js')
def instascan():
    return send_file('./templates/instascan.min.js')

@app.route('/qr.png')
def qrpng():
    return send_file('./templates/qr.png')

@app.route('/check.png')
def checkpng():
    return send_file('./templates/check.png')

@app.route('/clock.png')
def clockpng():
    return send_file('./templates/clock.png')

@app.route('/cross.png')
def crosspng():
    return send_file('./templates/cross.png')

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method == 'POST':
        qr_code = request.form['qr_code']
        current_time = datetime.datetime.now().strftime("%H:%M")

        with sqlite3.connect('booking.db') as conn:
            c = conn.cursor()
            c.execute("SELECT timeslot FROM bookings WHERE qr_code = ? AND status = 'Booked'", (qr_code,))
            row = c.fetchone()

            if row:
                timeslot = row[0]
                timeslot_start = timeslot.split('-')[0].strip()
                timeslot_end = timeslot.split('-')[1].strip()

                if timeslot_start <= current_time <= timeslot_end:
                    c.execute("UPDATE bookings SET status = 'Arrived' WHERE qr_code = ?", (qr_code,))
                    conn.commit()
                    return render_template('checkin_ok.html')
                else:
                    return render_template('checkin_wait.html')
            else:
                return render_template('checkin_error.html')
    else:
        return render_template('checkin.html')


@app.route('/info')
def info():
    #current_time = datetime.datetime.now().strftime("%H:%M")
#
 #   with sqlite3.connect('booking.db') as conn:
  #      c = conn.cursor()
   #     c.execute("SELECT timeslot FROM bookings WHERE status = 'Booked' AND timeslot >= ? ORDER BY timeslot ASC LIMIT 4", (current_time,))
    #    next_timeslots = [row[0] for row in c.fetchall()]
#
 #       c.execute("SELECT timeslot FROM bookings WHERE status != 'Booked' AND timeslot >= ? ORDER BY timeslot ASC LIMIT 4", (current_time,))
  #      future_timeslots = [row[0] for row in c.fetchall()]
#
    return render_template('info.html')
    #return 'ToDo'
if __name__ == '__main__':
    app.run(debug=True,host="192.168.178.79",ssl_context='adhoc')
