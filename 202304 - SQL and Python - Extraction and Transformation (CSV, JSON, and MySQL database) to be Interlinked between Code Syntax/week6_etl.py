!pip install mysql-connector-python
import pandas as pd
import json
import mysql.connector
from mysql.connector import Error

# Extract data from CSV file
def extract_csv(file_path):
    data = pd.read_csv(file_path)
    return data

# Extract data from JSON file
def extract_json(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    data = pd.DataFrame(json_data)
    return data

# Extract data from MySQL database
def extract_sql(query, connection_config):
    try:
        conn = mysql.connector.connect(**connection_config)
        data = pd.read_sql_query(query, conn)
    finally:
        if conn.is_connected():
            conn.close()
    return data

# Transform the products data
def transform_products(data):
    data['product_name'] = data['product_name'].str.capitalize()
    data['category'] = data['category'].str.capitalize()
    return data

# Transform the orders data
def transform_orders(data, products_data):
    data['quantity'] = data['quantity'].abs().astype(int)
    data = data.merge(products_data[['product_id', 'price']], on='product_id')
    data['total_value'] = data['quantity'] * data['price']
    data.drop(columns=['price'], inplace=True)
    return data

# Transform the customers data
def transform_customers(data):
    data['email'] = data['email'].str.lower()
    return data

# Transform and aggregate the orders data by customer
def transform_aggregate_orders(data):
    aggregated_data = data.groupby('customer_id').agg(
        total_orders=('order_id', 'count'),
        total_value=('total_value', 'sum')
    ).reset_index()
    aggregated_data['average_order_value'] = aggregated_data['total_value'] / aggregated_data['total_orders']
    return aggregated_data

# Load the data into a MySQL database
def load(data, table_name, connection_config):
    try:
        conn = mysql.connector.connect(**connection_config)
        data.to_sql(table_name, conn, if_exists='replace', index=False)
    finally:
        if conn.is_connected():
            conn.close()

# Execute ETL process
def main():
    connection_config = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'your_database'
    }
    ##############################
    # Extract
    ##############################
    products_csv_data = extract_csv('D:/UNPAR/Semester 8/Kapita Selekta Statistika/Tugas/Tugas 1/Tugas_1/products.csv')
    orders_json_data = extract_json('D:/UNPAR/Semester 8/Kapita Selekta Statistika/Tugas/Tugas 1/Tugas_1/orders.json')
    customers_sql_data = extract_sql('SELECT * FROM customers', connection_config)

    ##############################
    # Transform
    ##############################
    products_csv_transformed = transform_products(products_csv_data)
    orders_json_transformed = transform_orders(orders_json_data, products_csv_transformed)
    customers_sql_transformed = transform_customers(customers_sql_data)

    customer_metrics = transform_aggregate_orders(orders_json_transformed)

    ##############################
    # Load
    ##############################
    load(products_csv_transformed, 'products', connection_config)
    load(orders_json_transformed, 'orders', connection_config)
    load(customers_sql_transformed, 'customers', connection_config)
    load(customer_metrics, 'customer_metrics', connection_config)

if __name__ == '__main__':
    main()
