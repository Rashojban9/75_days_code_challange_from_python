import sqlite3

# Connect to the database or create one if it doesn't exist
def connect():
    conn = sqlite3.connect("warehouse.db")
    return conn

# Create tables
def create_tables():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            low_stock_threshold INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add a product
def add_product(name, quantity, price, low_stock_threshold):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Products (name, quantity, price, low_stock_threshold)
        VALUES (?, ?, ?, ?)
    """, (name, quantity, price, low_stock_threshold))
    conn.commit()
    conn.close()
    print("Product added successfully!")

# View all products
def view_products():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    conn.close()

    print("\n--- Product List ---")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Quantity: {product[2]}, Price: ${product[3]}, Low Stock Threshold: {product[4]}")
    if not products:
        print("No products available.")

# Update stock
def update_stock(product_id, new_quantity):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Products
        SET quantity = ?
        WHERE id = ?
    """, (new_quantity, product_id))
    conn.commit()
    if cursor.rowcount > 0:
        print("Stock updated successfully!")
    else:
        print("Product not found.")
    conn.close()

# Delete a product
def delete_product(product_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Products WHERE id = ?", (product_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print("Product deleted successfully!")
    else:
        print("Product not found.")
    conn.close()

# Check low stock
def check_low_stock():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products WHERE quantity < low_stock_threshold")
    products = cursor.fetchall()
    conn.close()

    print("\n--- Low Stock Products ---")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Quantity: {product[2]}, Low Stock Threshold: {product[4]}")
    if not products:
        print("No low stock products.")

# Main menu
def main():
    create_tables()

    while True:
        print("\n--- Warehouse Management System ---")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Stock")
        print("4. Delete Product")
        print("5. Check Low Stock")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter Product Name: ")
            quantity = int(input("Enter Quantity: "))
            price = float(input("Enter Price: "))
            low_stock_threshold = int(input("Enter Low Stock Threshold: "))
            add_product(name, quantity, price, low_stock_threshold)
        elif choice == "2":
            view_products()
        elif choice == "3":
            product_id = int(input("Enter Product ID: "))
            new_quantity = int(input("Enter New Quantity: "))
            update_stock(product_id, new_quantity)
        elif choice == "4":
            product_id = int(input("Enter Product ID: "))
            delete_product(product_id)
        elif choice == "5":
            check_low_stock()
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
