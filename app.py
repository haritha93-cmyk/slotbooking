from flask import Flask, render_template, request, redirect
from db_config import get_connection

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM slots")
    slots = cursor.fetchall()

    conn.close()
    return render_template('index.html', slots=slots)


@app.route('/book', methods=['POST'])
def book():
    slot_id = request.form['slot_id']
    user_name = request.form['user_name']

    conn = get_connection()
    cursor = conn.cursor()

    # Check if already booked
    cursor.execute("SELECT is_booked FROM slots WHERE id=%s", (slot_id,))
    result = cursor.fetchone()

    if result[0]:
        return "Slot already booked!"

    cursor.execute(
        "UPDATE slots SET is_booked=TRUE, user_name=%s WHERE id=%s",
        (user_name, slot_id)
    )
    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/booked')
def booked():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM slots WHERE is_booked=TRUE")
    slots = cursor.fetchall()

    conn.close()
    return render_template('booked.html', slots=slots)


if __name__ == '__main__':
    app.run(debug=True)