"""
 Must have the environment variables set properly prior to running the script
"""
from woocommerce import API
import json
import os
from faker import Faker
import random

fake = Faker()


def create_api_object():
    wcapi = API(
        url=os.environ.get('BASE_URL'),
        consumer_key=os.environ.get('API_KEY'),
        consumer_secret=os.environ.get('API_SECRET'),
        version="wc/v3",
        timeout=15
    )
    return wcapi


store_api = create_api_object()


class Products:
    def __init__(self) -> None:
        self.endpoint = 'products'
        self.products = self.fetch_all_products()

    def create_random_product(self):
        product_data = self.generate_random_product_data()

        try:
            response = store_api.post(self.endpoint, data=product_data)
            if response.ok:
                print("A product has been added successfully")
            else:
                raise Exception(f"Failed to add product. Status code: {response.status_code}")
        except Exception:
            print("Something went wrong while adding a product.")

    @classmethod
    def generate_random_product_data(cls):
        fake_data = {
            "name": fake.word().capitalize() + " " + fake.word().capitalize(),
            "regular_price": "{:.2f}".format(random.uniform(10, 100)),
            "description": fake.text(max_nb_chars=200),
            "short_description": fake.text(max_nb_chars=100)
        }
        return fake_data

    def fetch_all_products(self):
        products = []
        page = 1

        while True:
            response = store_api.get(self.endpoint, params={'page': page, 'per_page': 100}).json()
            if not response:
                break
            products.extend(response)
            page += 1
        return products

    def display_products_details(self):
        for product in self.products:
            product_id = product.get('id')
            name = product.get('name')
            price = product.get('regular_price')
            stock_status = product.get('stock_status')
            stock_quantity = product.get('stock_quantity')
            images = product.get('images')
            has_image = True if images else False

            print('_' * 100)
            text = f"id: {product_id}, name: {name}, price: {price}, stock status: {stock_status}, stock quantity: {stock_quantity}, has image: {has_image}"
            print(text)

    def update_product(self, product_id, data):
        try:
            update_endpoint = f"{self.endpoint}/{product_id}"
            response = store_api.put(update_endpoint, data)
            if response.ok:
                print(f"Product with id: {product_id} has been updated")

                print(response.status_code)
            else:
                raise Exception(
                    f"Failed to update the product. Status code: {response.status_code}, Response: {response.text}")

        except Exception as ex:
            print(f"Something went wrong while updating the product. Message: {ex}")

    def update_products_stock_details(self):
        for product in self.products:
            product_id = str(product.get('id'))
            stock_status = product.get('stock_status')
            images = product.get('images')
            has_image = True if images else False

            # Only update the products that have images
            if has_image and stock_status == 'outofstock':
                data = {
                    'stock_status': 'instock'
                }

                self.update_product(product_id, data)


if __name__ == '__main__':
    products_object = Products()
    # products_object.update_products_stock_details()
    products_object.display_products_details()
