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


def init_database():
    with sqlite3.connect('inventory.db') as connection:
        with open('inventory_schema.sql') as f:
            connection.executescript(f.read())


def convert_to_binary(filename):
    with open(filename, 'rb') as f:
        blob_data = f.read()
    return blob_data

@app.route('/xml-export')
def inventory_to_xml(output_file='inventory.xml'):
    connnection = sqlite3.connect('inventory.db')
    cursor = connnection.cursor()
    cursor.execute('SELECT name, image, description, quantity, price FROM inventory')
    rows = cursor.fetchall()
    connnection.close()
    root = ET.Element('inventory')
    for row in rows:
        item_elmt = ET.SubElement(root, 'item')
        name_elmt = ET.SubElement(item_elmt, 'name')
        name_elmt.text = row[0]
        image_elmt = ET.SubElement(item_elmt, 'image')
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
    xml_bytes = io.BytesIO()
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    xml_bytes.seek(0)

    return send_file(xml_bytes, mimetype='application/xml', as_attachment=True, download_name='inventory.xml')



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
    cursor.execute('SELECT name, description, image, quantity, price FROM inventory')
    rows = cursor.fetchall()

    data = []
    for row in rows:
        name, description, image_blob, quantity, price = row
        if image_blob:
            image_base64 = base64.b64encode(image_blob).decode('utf-8')
            image_uri = f"data:image/jpeg;base64,{image_base64}"
        else:
            image_uri = None  # or a default placeholder image path

        data.append((name, description, image_uri, quantity, price))

    return render_template('inventory.html', data=data)

if __name__ == '__main__':
    init_database()
    app.run(debug=True)
