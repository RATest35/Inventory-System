from flask import Flask, render_template, request, send_file
import sqlite3
import os
import base64
import xml.etree.ElementTree as ET
import io

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


# Function to connect the database
def init_database():
    with sqlite3.connect('inventory.db') as connection:
        with open('inventory_schema.sql') as f:
            connection.executescript(f.read())


# Converts a file to binary
def convert_to_binary(filename):
    with open(filename, 'rb') as f:
        blob_data = f.read()
    return blob_data


# Takes the database table and downloads a xml file to the users computer
@app.route('/xml-export')
def inventory_to_xml():
    connection = sqlite3.connect('inventory.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name, image, description, quantity, price FROM inventory')
    # Stores all the rows of the database
    rows = cursor.fetchall()
    connection.close()

    '''
    Creates a tree and creates a child node (item) for each item and then adds a child node (characteristics [name,
    image, quantity, etc.]) for each column in a row. The value of the characteristic is stored in the
    corresponding node
    '''
    root = ET.Element('inventory')
    for row in rows:
        item_elmt = ET.SubElement(root, 'item')
        name_elmt = ET.SubElement(item_elmt, 'name')
        name_elmt.text = row[0]
        image_elmt = ET.SubElement(item_elmt, 'image')
        '''
        Have to check if an image is stored, for this item.
        If an image is stored then have to convert from binary back into base64 
        '''
        if row[1]:
            image_base64 = base64.b64encode(row[1]).decode('utf-8')
            image_elmt.text = image_base64
        else:
            image_elmt.text = ''
        description_elmt = ET.SubElement(item_elmt, 'description')
        description_elmt.text = row[2]
        quantity_elmt = ET.SubElement(item_elmt, 'quantity')
        quantity_elmt.text = str(row[3])
        price_elmt = ET.SubElement(item_elmt, 'price')
        price_elmt.text = f'{row[4]:.2f}'

    # Sets up output file
    output_xml = io.BytesIO()
    tree = ET.ElementTree(root)
    tree.write(output_xml, encoding='utf-8', xml_declaration=True)
    output_xml.seek(0)

    return send_file(output_xml, mimetype='application/xml', as_attachment=True, download_name='inventory.xml')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        image_file = request.files.get('image')
        description = request.form['description']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        #
        image_blob = None
        if image_file and image_file.filename != '':
            # Temporarily save the file to read it as binary
            temp_folder = 'temp'
            os.makedirs(temp_folder, exist_ok=True)

            temp_path = os.path.join(temp_folder, image_file.filename)
            image_file.save(temp_path)
            image_blob = convert_to_binary(temp_path)
            os.remove(temp_path)

        with sqlite3.connect('inventory.db') as items:
            cursor = items.cursor()
            cursor.execute('INSERT INTO INVENTORY (name, image, description, quantity, price) \
                           VALUES (?, ?, ?, ?, ?)', (name, image_blob, description, quantity, price))
            items.commit()
        return render_template('index.html')
    else:
        return render_template('add.html')


@app.route('/inventory')
def inventory():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, image, description, quantity, price FROM inventory')
    rows = cursor.fetchall()

    data = []
    for row in rows:
        name, image_blob, description, quantity, price = row
        if image_blob:
            image_base64 = base64.b64encode(image_blob).decode('utf-8')
            image_uri = f"data:image/jpeg;base64,{image_base64}"
        else:
            image_uri = None  # or a default placeholder image path

        data.append((name, image_uri, description, quantity, price))

    return render_template('inventory.html', data=data)


if __name__ == '__main__':
    init_database()
    app.run(debug=True)
