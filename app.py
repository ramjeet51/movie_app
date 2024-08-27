import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

# Function to hash passwords for secure storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to handle user registration
def register():
    username = register_username_entry.get()
    password = register_password_entry.get()
    confirm_password = register_confirm_password_entry.get()
    
    if password != confirm_password:
        messagebox.showerror("Registration Error", "Passwords do not match")
        return
    
    if username and password:
        if not user_exists(username):
            add_user(username, password)
            messagebox.showinfo("Registration Successful", "User registered successfully")
            register_window.destroy()
            root.deiconify()
        else:
            messagebox.showerror("Registration Error", "Username already exists")
    else:
        messagebox.showwarning("Input Error", "Username and password cannot be empty")

# Function to check if a user already exists
def user_exists(username):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Function to add a new user to the database
def add_user(username, password):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hash_password(password)))
    conn.commit()
    conn.close()

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()
    if authenticate(username, password):
        root.withdraw()
        show_movie_screen()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to authenticate user
def authenticate(username, password):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Function to display the movie screen
def show_movie_screen():
    movie_screen = tk.Toplevel(root)
    movie_screen.title("Movie Management")

    # Add movie section
    tk.Label(movie_screen, text="Add Movie").pack(pady=10)
    tk.Label(movie_screen, text="Movie Name:").pack()
    movie_name_entry = tk.Entry(movie_screen)
    movie_name_entry.pack()

    def add_movie():
        movie_name = movie_name_entry.get()
        if movie_name:
            add_movie_to_db(movie_name)
            movie_name_entry.delete(0, tk.END)
            update_movie_list()
        else:
            messagebox.showwarning("Input Error", "Movie name cannot be empty")

    tk.Button(movie_screen, text="Add Movie", command=add_movie).pack(pady=5)

    # Movie list section
    tk.Label(movie_screen, text="Movies List").pack(pady=10)
    global movie_listbox
    movie_listbox = tk.Listbox(movie_screen)
    movie_listbox.pack(padx=10, pady=10)

    def update_movie_list():
        movie_listbox.delete(0, tk.END)
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM movies')
        movies = cursor.fetchall()
        conn.close()
        for movie in movies:
            movie_listbox.insert(tk.END, movie[0])

    update_movie_list()

# Function to add movie to the database
def add_movie_to_db(movie_name):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO movies (name) VALUES (?)', (movie_name,))
    conn.commit()
    conn.close()

# Function to initialize the login screen
def initialize_login_screen():
    global root, username_entry, password_entry
    root = tk.Tk()
    root.title("Login")

    tk.Label(root, text="Username").pack(pady=10)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password").pack(pady=10)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    tk.Button(root, text="Login", command=login).pack(pady=10)
    tk.Button(root, text="Register", command=show_registration_window).pack(pady=5)

    root.mainloop()

# Function to display the registration window
def show_registration_window():
    global register_window, register_username_entry, register_password_entry, register_confirm_password_entry

    root.withdraw()
    register_window = tk.Toplevel()
    register_window.title("Register")

    tk.Label(register_window, text="Username").pack(pady=10)
    register_username_entry = tk.Entry(register_window)
    register_username_entry.pack(pady=5)

    tk.Label(register_window, text="Password").pack(pady=10)
    register_password_entry = tk.Entry(register_window, show="*")
    register_password_entry.pack(pady=5)

    tk.Label(register_window, text="Confirm Password").pack(pady=10)
    register_confirm_password_entry = tk.Entry(register_window, show="*")
    register_confirm_password_entry.pack(pady=5)

    tk.Button(register_window, text="Register", command=register).pack(pady=10)
    tk.Button(register_window, text="Back to Login", command=back_to_login).pack(pady=5)

# Function to switch back to the login window
def back_to_login():
    register_window.destroy()
    root.deiconify()

# Function to initialize the database and tables if they don't exist
def initialize_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')
    conn.close()

if __name__ == "__main__":
    initialize_db()
    initialize_login_screen()
