from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

connect = sqlite3.connect('inventory.db')
connect.execute('CREATE TABLE IF NOT EXISTS INVENTORY (name TEXT,description TEXT, \
                 quantity INTEGER, price REAL)')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        with sqlite3.connect('inventory.db') as items:
            cursor = items.cursor()
            cursor.execute('INSERT INTO INVENTORY (name, description, quantity, price) \
                           VALUES (?, ?, ?, ?)', (name, description, quantity, price))
            items.commit()
        return render_template('index.html')
    else:
        return render_template('add.html')

@app.route('/inventory')
def inventory():
    connect = sqlite3.connect('inventory.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM INVENTORY')
    data = cursor.fetchall()
    return render_template('inventory.html', data=data)

if __name__ == '__main__':
    app.run(debug=False)
