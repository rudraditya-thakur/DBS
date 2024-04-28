from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from plyer import notification

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('inventory.db')

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    # Fetch the user from the database
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    print(user)

    # Close the database connection
    conn.close()

    if username in user and user[2] == password and user[3] == "customer":
        session['username'] = username
        return redirect(url_for('menu_page'))
    if username in user and user[2] == password and user[3] == "supplier":
        session['username'] = username
        return redirect(url_for('inventory'))
    if username in user and user[2] == password and user[3] == "chef":
        session['username'] = username
        return redirect(url_for('chef_orders'))
    if username in user and user[2] == password and user[3] == "waiter":
        session['username'] = username
        return redirect(url_for('waiter_orders'))
    if username in user and user[2] == password and user[3] == "manager":
        session['username'] = username
        return redirect(url_for('manager_dashboard'))
    else:
        return render_template('login.html', error='Invalid username or password')

menu_data = []

cart_items = []

@app.route('/menu')
def menu_page():
    global menu_data
    if 'username' not in session:
        return redirect(url_for('login_page'))

    # Connect to the database
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()

    # Fetch menu items from the database
    cursor.execute('SELECT * FROM menu')
    menu = cursor.fetchall()

    # Close the database connection
    conn.close()
    menu_data = [{'id': row[0], 'item_name': row[1], 'description': row[2], 'category': row[3], 'price': row[4]} for row in menu]

    # Pass menu items to the menu.html template
    return render_template('menu.html', menu=menu_data)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    item_id = int(request.form['item_id'])
    print(item_id)
    cart_items.append(item_id)
    return redirect(url_for('menu_page'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    item_id = int(request.form['item_id'])
    cart_items.remove(item_id)
    return redirect(url_for('menu_page'))

items = []

@app.route('/view_cart')
def view_cart():
    global cart_items, items
    items.clear()
    if 'username' not in session:
        return redirect(url_for('login_page'))
    print(cart_items)
    for item_id in cart_items:
        item = next((x for x in menu_data if x['id'] == item_id), None)
        if item:
            items.append(item)
        print(items)
    return render_template('cart.html', cart_items=items)

def connect_db_orders():
    return sqlite3.connect('orders.db')

@app.route('/place_order', methods=['POST'])
def place_order():
    global menu_data
    if 'username' not in session:
        return redirect(url_for('login_page'))
    conn = connect_db_orders()
    cursor = conn.cursor()
    for item_id in cart_items:
        item = next((x for x in menu_data if x['id'] == item_id), None)
        if item:
            print(item)
            cursor.execute('INSERT INTO orders (customer_name, item_name, price, status) VALUES (?,?,?,?)',
                           (session['username'], item['item_name'], item['price'], 'pending'))
    conn.commit()
    conn.close()

    return redirect(url_for('order_confirmation'))

@app.route('/order_confirmation')
def order_confirmation():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('order_confirmation.html')

@app.route('/inventory')
def inventory():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    inventory_items = cursor.fetchall()
    conn.close()

    return render_template('inventory.html', inventory_items=inventory_items)

# Route to add an item to the inventory
@app.route('/add_item', methods=['POST'])
def add_item():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    item_name = request.form['item_name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO inventory (item_name, quantity, price) VALUES (?, ?, ?)',
                   (item_name, quantity, price))
    conn.commit()
    conn.close()

    return redirect(url_for('inventory'))

# Route to delete an item from the inventory
@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if 'username' not in session:
        return redirect(url_for('login_page'))

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('inventory'))

@app.route('/update_item/<int:item_id>', methods=['POST'])
def update_item(item_id):
    if 'username' not in session:
        return redirect(url_for('login_page'))

    quantity = int(request.form['quantity'])
    price = float(request.form['price'])

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE inventory SET quantity = ?, price = ? WHERE id = ?',
                   (quantity, price, item_id))
    conn.commit()
    conn.close()

    return redirect(url_for('inventory'))

# Route for the chef's page to view and update orders
@app.route('/chef_orders')
def chef_orders():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    # Connect to the database
    conn = connect_db_orders()
    cursor = conn.cursor()

    # Fetch all pending orders from the database
    cursor.execute('SELECT * FROM orders WHERE status = "pending"')
    pending_orders = cursor.fetchall()

    # Close the database connection
    conn.close()

    return render_template('chef_orders.html', pending_orders=pending_orders)

# Route to update the status of orders to complete
@app.route('/complete_order/<int:order_id>')
def complete_order(order_id):
    if 'username' not in session:
        return redirect(url_for('login_page'))

    # Connect to the database
    conn = connect_db_orders()
    cursor = conn.cursor()

    # Update the status of the order to complete in the database
    cursor.execute('UPDATE orders SET status = "complete" WHERE id = ?', (order_id,))
    conn.commit()
    # notification.notify(
    #     title= "Order Completed: {}".format(order_id),
    #     message="The Customer can pickup there order",
    #     app_icon=None,
    #     timeout=5
    # )

    # Close the database connection
    conn.close()

    return redirect(url_for('chef_orders'))


# Route for the waiter's page to view and manage completed orders
@app.route('/waiter_orders')
def waiter_orders():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    # Connect to the database
    conn = connect_db_orders()
    cursor = conn.cursor()

    # Fetch all pending orders from the database
    cursor.execute('SELECT * FROM orders WHERE status = "complete"')
    completed_orders = cursor.fetchall()
    orders = [{'id': row[0], 'customer_name': row[1], 'item_name': row[2], 'price': row[3], 'status': row[4]} for row in completed_orders]
    # Close the database connection
    conn.close()

    return render_template('waiter_orders.html', completed_orders=orders)

# Route to mark an order as delivered or picked up by the customer
@app.route('/mark_delivered/<int:order_id>')
def mark_delivered(order_id):
    if 'username' not in session :
        return redirect(url_for('login_page'))

    # Connect to the database
    conn = connect_db_orders()
    cursor = conn.cursor()

    # Update the status of the order to delivered in the database
    cursor.execute('UPDATE orders SET status = "delivered" WHERE id = ?', (order_id,))
    conn.commit()

    # Close the database connection
    conn.close()

    return redirect(url_for('waiter_orders'))

# Manager dashboard route
@app.route('/manager_dashboard')
def manager_dashboard():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    # Fetch statistics and earnings from the database
    conn = connect_db_orders()
    cursor = conn.cursor()

    # Fetch number of orders pending, completed, and delivered
    cursor.execute('SELECT COUNT(*) FROM orders WHERE status = "pending"')
    pending_orders = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM orders WHERE status = "complete"')
    completed_orders = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM orders WHERE status = "delivered"')
    delivered_orders = cursor.fetchone()[0]

    # Calculate total earnings
    cursor.execute('SELECT SUM(price) FROM orders')
    total_earnings = cursor.fetchone()[0]
    if total_earnings == None:
        total_earnings = 0

    # Close the database connection
    conn.close()

    return render_template('manager_dashboard.html', pending_orders=pending_orders, completed_orders=completed_orders,
                           delivered_orders=delivered_orders, total_earnings=total_earnings)

# Route to add new users
@app.route('/add_user', methods=['POST'])
def add_user():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    # Get user details from the form
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    # Check if the user already exists
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return render_template('error.html', message="User already exists")

    # Add the new user to the database
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (nameofUser, username, password, job_role) VALUES (?, ?, ?, ?)', (username, username, password, role))
    conn.commit()
    conn.close()

    return redirect(url_for('manager_dashboard'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
