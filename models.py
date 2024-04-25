import sqlite3

# Connect to SQLite database (create it if not exists)
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Create a table to store inventory information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
''')

dummy_data = [
    ('Laptop', 10, 800.00),
    ('Monitor', 20, 200.00),
    ('Keyboard', 50, 20.00),
    ('Mouse', 75, 10.00),
    ('Headphones', 30, 30.00),
    ('Webcam', 15, 50.00),
    ('Docking Station', 5, 150.00),
    ('HDMI Cable', 100, 5.00),
    ('Ethernet Cable', 75, 3.00),
    ('Power Strip', 25, 15.00),
]

cursor.executemany('''
    INSERT INTO inventory (item_name, quantity, price) VALUES (?, ?, ?)
''', dummy_data)


# Commit changes and close connection
conn.commit()
conn.close()


# Connect to SQLite database
conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

# Create the "orders" table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        item_name TEXT NOT NULL,
        price REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending'
    )
''')


# Commit the changes and close the connection
conn.commit()
conn.close()

conn = sqlite3.connect('menu.db')
cursor = conn.cursor()

# Create menu table
cursor.execute('''CREATE TABLE IF NOT EXISTS menu (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT NOT NULL,
                    description TEXT,
                    category TEXT,
                    price REAL NOT NULL
                )''')

menu_items = [
    ('Pizza', 'Delicious pizza with cheese and toppings', 'Main Course', 10.99),
    ('Burger', 'Classic burger with beef patty and vegetables', 'Main Course', 8.99),
    ('Pasta', 'Pasta with tomato sauce and cheese', 'Main Course', 12.99),
    ('Salad', 'Fresh salad with mixed greens and vegetables', 'Appetizer', 6.99),
    ('Soup', 'Hearty soup of the day', 'Appetizer', 4.99),
    ('Chicken Wings', 'Spicy chicken wings with blue cheese dip', 'Appetizer', 8.99),
    ('Fish and Chips', 'Fried fish with crispy fries', 'Main Course', 14.99),
    ('Steak', 'Grilled steak with mashed potatoes and vegetables', 'Main Course', 19.99),
    ('Ribs', 'BBQ ribs with coleslaw and fries', 'Main Course', 16.99),
    ('Chicken Alfredo', 'Chicken pasta with creamy Alfredo sauce', 'Main Course', 13.99),
    ('Vegetable Stir Fry', 'Stir-fried vegetables with rice', 'Main Course', 11.99),
    ('Cheesecake', 'Rich and creamy cheesecake with fruit topping', 'Dessert', 6.99),
    ('Ice Cream', 'Vanilla ice cream with chocolate sauce', 'Dessert', 4.99),
    ('Apple Pie', 'Warm apple pie with vanilla ice cream', 'Dessert', 7.99),
    ('Brownie', 'Fudgy chocolate brownie with whipped cream', 'Dessert', 5.99),
]

cursor.executemany('INSERT INTO menu (item_name, description, category, price) VALUES (?, ?, ?, ?)', menu_items)


# Commit changes and close connection
conn.commit()
conn.close()

# Connect to SQLite database (create it if not exists)
conn = sqlite3.connect('user.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

CREATE_USER_TABLE = '''
CREATE TABLE IF NOT EXISTS users (
nameofUser TEXT NOT NULL,
username TEXT PRIMARY KEY NOT NULL,
password TEXT NOT NULL,
job_role TEXT NOT NULL
)'''

# Create a table to store user information
cursor.execute(CREATE_USER_TABLE)

users = {
    'john': {'password': 'password123', 'role': 'customer'},
    'emma': {'password': 'abc123', 'role': 'supplier'},
    'alice': {'password': 'qwerty', 'role': 'manager'},
    'bob': {'password': 'pass', 'role': 'chef'},
    'charlie': {'password': 'admin123', 'role': 'waiter'}
}

for username, user_info in users.items():
    cursor.execute('''
    INSERT INTO users (nameofUser, username, password, job_role)
    VALUES (?, ?, ?, ?)
    ''', (username, username, user_info['password'], user_info['role']))


# Commit changes and close connection
conn.commit()
conn.close()
