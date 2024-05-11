import sqlite3
from tkinter import *
from tkinter import messagebox, simpledialog
import subprocess
import os

def buttonClick():
    entered_login_id = login_id_entry.get()
    entered_password = password_entry.get()

    if verify_login(entered_login_id, entered_password):
        print("Login successful. Opening display.py...")

        
        script_path = os.path.join("display.py")

        
        subprocess.run(["python", script_path])

        
        root.destroy()
    else:
        print("Login failed. Please check your credentials.")
        
        messagebox.showerror("Login Failed", "Invalid credentials. Please check your login ID and password.")

def open_registration_window():
    
    registration_script_path = os.path.join("registration.py")

    
    subprocess.run(["python", registration_script_path])

def open_admin_login():
    
    entered_password = simpledialog.askstring("Admin Login", "Enter admin password:", show="*")

    
    if entered_password == "1234567890":
        print("Admin login successful. Opening admin.py...")

        
        admin_script_path = os.path.join("admin.py")

        
        subprocess.run(["python", admin_script_path])

    else:
        
        messagebox.showerror("Admin Login Failed", "Incorrect admin password. Please try again.")

def toggle_password_visibility():
    if hide_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

def validate_login_id(P):
    if P == "" or (P.isdigit() and len(P) <= 10):
        return True
    return False

def verify_login(login_id, password):
    conn = sqlite3.connect('mydatabase.db') 
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM login WHERE id = ? AND password = ?', (login_id, password))
    result = cursor.fetchone()

    conn.close()

    if result:
        return True
    return False

root = Tk()
root.geometry("1250x600")
root.title("Rent calculation application")

f = Frame(root, height=40, width=1250)
f.propagate(0)
f.pack()


heading_label = Label(f, text="PY Room Rentals Login", font=("Helvetica", 20, "bold"))
heading_label.grid(row=0, columnspan=3, padx=10, pady=10)


login_id_label = Label(f, text="Login ID:")
login_id_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
validate_login_id_cmd = (root.register(validate_login_id), "%P")
login_id_entry = Entry(f, validate="key", validatecommand=validate_login_id_cmd)
login_id_entry.grid(row=1, column=1, padx=10, pady=10)


password_label = Label(f, text="Password:")
password_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
password_entry = Entry(f, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=10)


hide_password_var = IntVar()
hide_password_checkbox = Checkbutton(f, text="Unhide", variable=hide_password_var, command=toggle_password_visibility)
hide_password_checkbox.grid(row=2, column=2, padx=10, pady=5, sticky="w")


login_button = Button(f, text='Login', fg='blue', activebackground='green', activeforeground='red', command=buttonClick)
login_button.grid(row=3, column=1, padx=10, pady=20)


registration_button = Button(f, text='Register', fg='black', activebackground='blue', activeforeground='red', command=open_registration_window)
registration_button.grid(row=5, column=1, padx=10, pady=20)


admin_login_button = Button(f, text='Admin Login', fg='black', activebackground='orange', activeforeground='white', command=open_admin_login)
admin_login_button.grid(row=6, column=1, padx=10, pady=20)

root.mainloop()
