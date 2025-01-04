import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                quantity INTEGER,
                price REAL)''')

# Add a new product
def add_product():
    id = int(input("Enter Product ID: "))
    name = input("Enter Product Name: ")
    quantity = int(input("Enter Quantity: "))
    price = float(input("Enter Price: "))
    c.execute("INSERT INTO Products VALUES (?, ?, ?, ?)", (id, name, quantity, price))
    conn.commit()
    print("Product added successfully!")

# View all products
def view_products():
    c.execute("SELECT * FROM Products")
    products = c.fetchall()
    for product in products:
        print(product)

# Update stock
def update_stock():
    id = int(input("Enter Product ID: "))
    new_quantity = int(input("Enter New Quantity: "))
    c.execute("UPDATE Products SET quantity = ? WHERE id = ?", (new_quantity, id))
    conn.commit()
    print("Stock updated successfully!")

# Process sale
def process_sale():
    id = int(input("Enter Product ID: "))
    quantity_sold = int(input("Enter Quantity Sold: "))
    c.execute("SELECT quantity, price FROM Products WHERE id = ?", (id,))
    result = c.fetchone()
    if result:
        quantity, price = result
        if quantity >= quantity_sold:
            new_quantity = quantity - quantity_sold
            c.execute("UPDATE Products SET quantity = ? WHERE id = ?", (new_quantity, id))
            conn.commit()
            print(f"Sale processed successfully! Total: ${price * quantity_sold}")
        else:
            print("Insufficient stock!")
    else:
        print("Product not found!")

# Main menu
def main():
    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Stock")
        print("4. Process Sale")
        print("5. Exit")
        choice = int(input("Choose an option: "))

        if choice == 1:
            add_product()
        elif choice == 2:
            view_products()
        elif choice == 3:
            update_stock()
        elif choice == 4:
            process_sale()
        elif choice == 5:
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()

conn.close()
