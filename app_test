import unittest
import sqlite3
import app as app
import os
import filecmp

app.init_database()


def add_inventory_item(name, description, quantity, price, image_path=None):
    image_blob = None
    if image_path and os.path.exists(image_path):
        image_blob = app.convert_to_binary(image_path)
    with sqlite3.connect('inventory.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO INVENTORY (name, image, description, quantity, price)
                          VALUES (?, ?, ?, ?, ?)''',
                       (name, image_blob, description, quantity, price))
        conn.commit()

def update_inventory_item_quantity(name, new_quantity):
    with sqlite3.connect('inventory.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE INVENTORY SET quantity = ? WHERE name = ?''', (new_quantity, name))
        conn.commit()


class MyTestCase(unittest.TestCase):
    def test_1(self):
        add_inventory_item("Water", "Bottled", 5, 1)
        self.assertTrue(filecmp.cmp('inventory.db', 'inventoryCheck1.db', shallow=False))


    def test_2(self):
        add_inventory_item("Apples", "By the pound", 10, 2, "apples.png")
        self.assertTrue(filecmp.cmp('inventory.db', 'inventoryCheck2.db', shallow=False))


    def test_3(self):
        add_inventory_item("Coca Cola", "Normal Flavor, 12oz, Canned", 60, 0.5)
        self.assertTrue(filecmp.cmp('inventory.db', 'inventoryCheck3.db', shallow=False))


    def test_4(self):
        update_inventory_item_quantity("Water", 100)
        self.assertTrue(filecmp.cmp('inventory.db', 'inventoryCheck4.db', shallow=False))


if __name__ == '__main__':
    unittest.main()
