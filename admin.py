import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk  

def delete_entry():
    
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showinfo("Error", "Please select an entry to delete.")
        return

    
    selected_id = tree.item(selected_item, "values")[0]

    
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    
    cursor.execute('DELETE FROM login WHERE id = ?', (selected_id,))

    
    conn.commit()
    conn.close()

    
    tree.delete(selected_item)

    messagebox.showinfo("Success", "Entry deleted successfully.")


conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()


cursor.execute('SELECT * FROM login')
records = cursor.fetchall()


conn.close()


admin_window = Tk()
admin_window.title("Admin Dashboard")


tree = ttk.Treeview(admin_window)


tree["columns"] = ("ID", "Password", "Name", "Phone Number")


tree.column("#0", width=0, stretch=NO)
tree.column("ID", anchor=CENTER, width=100)
tree.column("Password", anchor=CENTER, width=100)
tree.column("Name", anchor=CENTER, width=100)
tree.column("Phone Number", anchor=CENTER, width=100)


tree.heading("#0", text="", anchor=W)
tree.heading("ID", text="ID", anchor=CENTER)
tree.heading("Password", text="Password", anchor=CENTER)
tree.heading("Name", text="Name", anchor=CENTER)
tree.heading("Phone Number", text="Phone Number", anchor=CENTER)


for record in records:
    tree.insert("", END, values=record)


tree.pack(expand=YES, fill=BOTH)


delete_button = Button(admin_window, text='Delete Entry', command=delete_entry)
delete_button.pack()

admin_window.mainloop()
