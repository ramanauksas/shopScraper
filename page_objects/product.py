from page_objects.db import DB
from datetime import datetime


class Product:

    def __init__(self, driver) :
        self.db = DB()
        self.driver = driver
        self.title = ""
        self.brand = ""
        self.property = ""
        self.size = ""
        self.unit = ""
        self.price = ""
        self.category = []
        self.store = ""
        self.link = ""
        self.product_id = ""

    def save_category(self, category_list):
        # Check if the category exists, if not, insert it and get its ID
        query = "SELECT id FROM `categories` WHERE `category1` = %s AND `category2` = %s AND `category3`= %s AND `store`= %s"
        cursor = self.db.conn.cursor()
        if len(category_list) < 3:
            if len(category_list) == 2:
                category_list.append(category_list[1])
            else:
                print("uncategorized product. Not saving it.")
                cursor.close()
                return
        print("save_category from save_category", category_list)
        cursor.execute(query, (*category_list, self.store))
        self.category = cursor.fetchone()[0]
        print("cursor fetch all", cursor.fetchall())
        cursor.close()


        # if result:
        #     # Category exists, get the ID
        #     self.category = result[0]
        # else:
        #     # Category does not exist, insert it
        #     query = "INSERT INTO `categories` (`category1`, `category2`, `category3`, `store`) VALUES (%s, %s, %s, %s)"
        #     cursor.execute(query, (*self.category, self.store))
        #     self.db.conn.commit()
        #     # Get the newly inserted category ID
        #     self.category = cursor.lastrowid

    def save(self):
        # Check if the product already exists
        check_query = """
            SELECT `id`, `price` 
            FROM `product` 
            WHERE `link` = %s
        """
        cursor = self.db.conn.cursor()
        cursor.execute(check_query, (self.link,))
        existing_product = cursor.fetchone()
        print("existing product", existing_product)

        if existing_product:
            print("product already exists; checking price change")
            # If the product exists, check if the price has changed
            product_id = existing_product[0]
            existing_price = existing_product[1]

            if float(existing_price) != float(self.price):
                print("existing_price", existing_price, type(existing_price))
                print("self.price", self.price, type(self.price))
                # If the price is different, update the product
                update_query = """
                    UPDATE `product`
                    SET `price` = %s
                    WHERE `id` = %s
                """
                cursor.execute(update_query, (self.price, product_id))
                self.db.conn.commit()
                self.product_id = product_id
                self.save_price_history()
                print(f"Updated product with ID {product_id} and logged price change")
            else:
                print(f"No update needed for product with ID {product_id}.")
        else:
            # If the product doesn't exist, insert a new one
            insert_query = """
                INSERT INTO `product`(`title`, `brand`, `price`, `size`, `unit`, `property`, `category`, `link`, `store`) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            print(self.title, self.brand, self.price, self.size, self.unit, self.property, self.category, self.link, self.store)
            cursor.execute(insert_query, (
            self.title, self.brand, self.price, self.size, self.unit, self.property, self.category, self.link, self.store))
            self.db.conn.commit()
            self.product_id = cursor.lastrowid
            self.save_price_history()
            print(f"Inserted new product with ID {self.product_id} and logged price")

        cursor.close()


    def save_price_history(self):
        query = "INSERT INTO `prices`(`product`, `price`, `date`) VALUES (%s, %s, %s)"
        date = datetime.now()
        self.db.conn.cursor().execute(query, (self.product_id, self.price, date))
        self.db.conn.commit()


    def __str__(self):
        return f"{self.title}, {self.brand}, {self.property}, {self.size}, {self.unit}, {self.price}, {self.category}"

