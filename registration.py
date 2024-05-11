import sqlite3
from tkinter import *
from tkinter import messagebox

def create_update_login_table():
    
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login (
            id NUMBER PRIMARY KEY,
            password TEXT,
            name TEXT,
            phone_number TEXT
        )
    ''')

    
    conn.commit()
    conn.close()

def validate_name(name):
    
    return all(c.isalpha() or c == '_' for c in name)

def register_user():
    try:
        
        entered_id = id_entry.get()
        entered_password = password_entry.get()
        entered_name = name_entry.get()
        entered_phone_number = phone_number_entry.get()

        
        if not (entered_id.isdigit() and len(entered_id) <= 10):
            messagebox.showerror("Error", "Invalid ID. Please enter a valid ID.")
            return

        if len(entered_password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
            return

        if not validate_name(entered_name):
            messagebox.showerror("Error", "Invalid name. Please enter name along with underscore('_').")
            return

        if not (entered_phone_number.isdigit() and len(entered_phone_number) == 10):
            messagebox.showerror("Error", "Invalid phone number. Please enter a valid 10-digit phone number.")
            return

        
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()

        
        cursor.execute('SELECT * FROM login WHERE id = ?', (entered_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            
            response = messagebox.askquestion("User Exists", "User with the given ID already exists. Do you want to overwrite?")
            
            if response == 'yes':
                
                cursor.execute('UPDATE login SET password=?, name=?, phone_number=? WHERE id = ?',
                               (entered_password, entered_name, entered_phone_number, entered_id))
                messagebox.showinfo("Success", "User information updated successfully.")
            else:
                
                pass
        else:
            
            cursor.execute('INSERT INTO login (id, password, name, phone_number) VALUES (?, ?, ?, ?)',
                           (entered_id, entered_password, entered_name, entered_phone_number))
            messagebox.showinfo("Success", "User registered successfully.")

        
        conn.commit()
        conn.close()

        
        id_entry.delete(0, END)
        password_entry.delete(0, END)
        name_entry.delete(0, END)
        phone_number_entry.delete(0, END)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def toggle_password_visibility():
    if hide_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


create_update_login_table()


registration_window = Tk()
registration_window.title("User Registration")


id_label = Label(registration_window, text="ID:")
id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
id_entry = Entry(registration_window)
id_entry.grid(row=0, column=1, padx=10, pady=10)


password_label = Label(registration_window, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
password_entry = Entry(registration_window, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)


hide_password_var = IntVar()
hide_password_checkbox = Checkbutton(registration_window, text="Unhide", variable=hide_password_var, command=toggle_password_visibility)
hide_password_checkbox.grid(row=1, column=2, padx=10, pady=5, sticky="w")


name_label = Label(registration_window, text="Name:")
name_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
name_entry = Entry(registration_window)
name_entry.grid(row=2, column=1, padx=10, pady=10)


phone_number_label = Label(registration_window, text="Phone Number:")
phone_number_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
phone_number_entry = Entry(registration_window)
phone_number_entry.grid(row=3, column=1, padx=10, pady=10)


register_button = Button(registration_window, text="Register", command=register_user)
register_button.grid(row=4, column=1, padx=10, pady=20)


cancel_button = Button(registration_window, text="Cancel", command=registration_window.destroy)
cancel_button.grid(row=4, column=2, padx=10, pady=20)

registration_window.mainloop()
