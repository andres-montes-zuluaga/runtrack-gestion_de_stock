import mysql.connector
import csv

class Stock:
    def __init__(self, host, user, password, database):
        try:
            print("Attempting to connect to the database...")
            self.conexion = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                auth_plugin='mysql_native_password'
            )
            if self.conexion.is_connected():
                self.cursor = self.conexion.cursor()
                print("Database connection established.")
            else:
                print("Failed to connect to the database.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def add_product(self, name, description, price, quantity, image_url, id_category):
        try:
            query = "INSERT INTO product (name, description, price, quantity, image_url, id_category) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (name, description, price, quantity, image_url, id_category)
            self.cursor.execute(query, values)
            self.conexion.commit()
            print(f"Product {name} added.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def delete_product(self, product_id):
        try:
            query = "DELETE FROM product WHERE id = %s"
            self.cursor.execute(query, (product_id,))
            self.conexion.commit()
            print(f"Product ID {product_id} deleted.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def modify_product(self, product_id, name=None, description=None, price=None, quantity=None, image_url=None, id_category=None):
        try:
            updates = []
            values = []
            if name:
                updates.append("name = %s")
                values.append(name)
            if description:
                updates.append("description = %s")
                values.append(description)
            if price:
                updates.append("price = %s")
                values.append(price)
            if quantity:
                updates.append("quantity = %s")
                values.append(quantity)
            if image_url:
                updates.append("image_url = %s")
                values.append(image_url)
            if id_category:
                updates.append("id_category = %s")
                values.append(id_category)
            
            query = f"UPDATE product SET {', '.join(updates)} WHERE id = %s"
            values.append(product_id)
            self.cursor.execute(query, values)
            self.conexion.commit()
            print(f"Product ID {product_id} was modified.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def add_category(self, name):
        try:
            query = "INSERT INTO category (name) VALUES (%s)"
            values = (name,)
            self.cursor.execute(query, values)
            self.conexion.commit()
            print("Category added.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def delete_category(self, id_category):
        try:
            query = "DELETE FROM category WHERE id = %s"
            self.cursor.execute(query, (id_category,))
            self.conexion.commit()
            print(f"Category ID {id_category} deleted.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def show_products(self):
        try:
            query = "SELECT * FROM product"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def show_categories(self):
        try:
            query = "SELECT * FROM category"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def show_products_by_category(self, id_category):
        try:
            query = "SELECT * FROM product WHERE id_category = %s"
            self.cursor.execute(query, (id_category,))
            results = self.cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def stock_total_price(self):
        try:
            query = "SELECT SUM(price * quantity) AS total_price FROM product"
            self.cursor.execute(query)
            stock_total_price = self.cursor.fetchone()[0]
            print(f"Stock total price: $ {stock_total_price}.")
            return stock_total_price  # Devolver el valor del stock total
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def fermer_conexion(self):
        try:
            if self.cursor and not self.cursor.close:
                self.cursor.close()
                print("Cursor is closed.")
            if self.conexion and self.conexion.is_connected():
                self.conexion.close()
                print("Disconnected.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise