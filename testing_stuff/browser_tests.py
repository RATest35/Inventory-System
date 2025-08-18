import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class BusinessInventoryTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
    
    def test_register(self):
        driver = self.driver
        driver.get('http://34.67.55.188:5000/')
        submit_button = driver.find_element(By.TAG_NAME, 'button')
        submit_button.click()
        self.assertIn("Register account", driver.title)
        register_username_box=driver.find_element(By.NAME, 'username')
        register_password_box=driver.find_element(By.NAME, 'user_password')
        register_store_box=driver.find_element(By.NAME, 'store_name')
        register_username_box.send_keys("testuser")
        register_password_box.send_keys("test")
        register_store_box.send_keys("Test Store")
        register_account=driver.find_element(By.CSS_SELECTOR, '[value="Register"]')
        register_account.click()
        self.assertIn("Register account", driver.title)
        driver.back()
        driver.back()
    
    def test_login(self):
        driver = self.driver
        driver.get('http://34.67.55.188:5000/')
        self.assertIn("Enter your user name and password", driver.title)
        login_username_box=driver.find_element(By.NAME, 'username')
        login_password_box=driver.find_element(By.NAME, 'user_password')
        login_username_box.send_keys("testuser")
        login_password_box.send_keys("test")
        login_button=driver.find_element(By.XPATH, "//form[1]/input[3]")
        login_button.click()
        self.assertIn("Business Inventory Home", driver.title)
        
    def test_add_item(self):
        driver = self.driver
        driver.get('http://34.67.55.188:5000/home')
        self.assertIn("Business Inventory Home", driver.title)
        add_item_box=driver.find_element(By.XPATH, "//div[2]/a[2]")
        add_item_box.click()
        self.assertIn("Add Inventory Item", driver.title)
        item_name_box=driver.find_element(By.NAME, 'name')
        item_description_box=driver.find_element(By.NAME, 'description')
        item_quantity_box=driver.find_element(By.NAME, 'quantity')
        item_price_box=driver.find_element(By.NAME, 'price')
        item_name_box.send_keys("Pear")
        item_description_box.send_keys("Green")
        item_quantity_box.send_keys("4")
        item_price_box.send_keys("0.99")
        submit_item=driver.find_element(By.XPATH, "//form[1]/input[6]")
        submit_item.click()
        self.assertIn("Business Inventory Home", driver.title)

    def test_inventory(self):
        driver = self.driver
        driver.get('http://34.67.55.188:5000/home')
        self.assertIn("Business Inventory Home", driver.title)
        inventory_box=driver.find_element(By.XPATH, "//div[2]/a[1]")
        inventory_box.click()
        self.assertIn("Business Inventory", driver.title)
        items = driver.findElements(By.XPATH, "//table[1]/tr[2]/td")
        self.assertGreater(items.size(), 0)
        
    def test_low_stock(self):
        driver = self.driver
        driver.get('http://34.67.55.188:5000/home')
        self.assertIn("Business Inventory Home", driver.title)
        inventory_box=driver.find_element(By.XPATH, "//div[2]/a[1]")
        inventory_box.click()
        low_stock_box=driver.find_element(By.XPATH, "//button[3]")
        low_stock_box.click()
        self.assertIn("Low and Empty Stock", driver.title)
        low_items = driver.findElements(By.XPATH, "//table[1]/tr[2]/td")
        self.assertGreater(low_items.size(), 0)
    
    def test_delete_item(self):
        driver = self.driver
        driver.get('http://34.67.55.188:5000/home')
        self.assertIn("Business Inventory Home", driver.title)
        inventory_box=driver.find_element(By.XPATH, "//div[2]/a[1]")
        inventory_box.click()
        self.assertIn("Business Inventory", driver.title)
        delete_item_box = driver.find_element(By.XPATH, "//button[4]")
        delete_item_box.click()
        self.assertIn("Delete item", driver.title)
        delete_box=driver.find_element(By.TAG_NAME, "button")
        delete_box.click()
        self.assertIn("Business Inventory", driver.title)
        
    def test_logout(self):
        driver = self.driver
        driver.get('http://34.67.55.188:5000/home')
        self.assertIn("Business Inventory Home", driver.title)
        logout_box=driver.find_element(By.XPATH, "//div[2]/a[3]")
        logout_box.click()
        self.assertIn("Enter your user name and password", driver.title)
        
    def tearDown(self):
        self.driver.close()
        
if __name__ == "__main__":
    unittest.main()
