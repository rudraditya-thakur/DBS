import sqlite3

def add_user(nameofUser, username, password, job_role):
    conn = sqlite3.connect('user_db.sqlite')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO users (nameofUser, username, password, job_role)
                          VALUES (?, ?, ?, ?)''', (nameofUser, username, password, job_role))
        conn.commit()
        print("User added successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists! Please choose a different username.")
    finally:
        conn.close()

# Example usage
add_user("John Doe", "john", "password123", "customer")

def get_user_by_username(username):
    conn = sqlite3.connect('user_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE username=?''', (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

# Example usage
user_data = get_user_by_username('john')
print(user_data)  # (nameofUser, username, password, job_role) or None if user not found

def update_user_password(username, new_password):
    conn = sqlite3.connect('user_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''UPDATE users SET password=? WHERE username=?''', (new_password, username))
    conn.commit()
    conn.close()
    print("Password updated successfully!")

# Example usage
# update_user_password("john", "new_password123")

def delete_user(username):
    conn = sqlite3.connect('user_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM users WHERE username=?''', (username,))
    conn.commit()
    conn.close()
    print("User deleted successfully!")

# Example usage
# delete_user("john")