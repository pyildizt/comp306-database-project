# Imports for ui
import customtkinter
from tkinter import *
from tkinter import ttk

# Import for database
import mysql.connector
import csv

# Appearance and style of ui - not really important
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")

# Main application 
main_app = customtkinter.CTk()
main_app.title("Intellectual Property Firm System")
main_app.geometry("1200x700")

### A Tabview
tabview = customtkinter.CTkTabview(master=main_app)
tabview.pack(pady=20, padx=20, fill="both", expand=True)

# Adding tabs
tabs = ["Lawyers", "Clients", "Lawsuits"]

for i in tabs:
    tabview.add(i)

tabview.set("Lawyers") # set as default tab
lawyers_tab = tabview.tab("Lawyers")

# Add label to Tab2
label2 = customtkinter.CTkLabel(master=tabview.tab("Clients"), text="This is the Clients tab.")
label2.pack(pady=10, padx=10)

### A Label
label = customtkinter.CTkLabel(master=lawyers_tab, text="Lawyers in the Firm")
label.pack(pady=10, padx=10)


### A Treeview
# Used to view tables

# Basic table with column names and info to show you how treeview works
table_columns = ("id","fname","lname","sex","fee","email","phone_number")

tree = ttk.Treeview(master=lawyers_tab, columns=table_columns, show="headings", selectmode="browse",height=20) 
# selectmode="browse" means the user can only select one row at a time
tree.pack() # makes ui look good i guess, DO NOT ERASE

# this is used to make the heading names look better

tree.heading("id",text="ID")
tree.heading("fname",text="Name")
tree.heading("lname",text="Surname")
tree.heading("sex",text="Sex")
tree.heading("fee",text="Fee")
tree.heading("email",text="Email")
tree.heading("phone_number",text="Phone No")
for i in range(5):
    tree.column(i,width=80, stretch=NO)


# Database connection
db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql201468", 
  auth_plugin='mysql_native_password'
)
db_cursor = db_connection.cursor(buffered=True)

db_cursor.execute("DROP DATABASE IF EXISTS test_for_ip") # might be necessary for testing

db_cursor.execute("CREATE DATABASE IF NOT EXISTS test_for_ip")
db_cursor.execute("USE test_for_ip")

def populate_table(db_connection, db_cursor, insert_query, file_path):
    with open(file_path, mode='r') as csv_data:
        reader = csv.reader(csv_data, delimiter=',')
        csv_data_list = list(reader)
        for row in csv_data_list[1:]:
            row = tuple(map(lambda x: None if x == "" else x, row))
            db_cursor.execute(insert_query, row)
    db_connection.commit()

# Create basic table
db_cursor.execute("""CREATE TABLE IF NOT EXISTS LAWYERS (id INT NOT NULL,
                                                         fname VARCHAR(50),
                                                         lname VARCHAR(50),
                                                         sex VARCHAR(6), 
                                                         fee INT, 
                                                         email VARCHAR(50), 
                                                         phone_number VARCHAR(30))""")

insert_lawyers = (
    "INSERT INTO LAWYERS(id, fname,lname, sex, fee, email, phone_number)"
    "VALUES (%s, %s, %s, %s, %s, %s, %s)")

# Insert some values
populate_table(db_connection, db_cursor, insert_lawyers, "lawyers.csv")

# Get all values from table
db_cursor.execute("""SELECT * FROM LAWYERS""")

# Insert values into Treeview
rows = db_cursor.fetchall()

for i in rows:
    tree.insert("", END, values=i)

# Example 2
def removeFromDatabase():
    if tree.selection() != None: # this is the row selected by user

        # This is how you get the values from selected item, just copy paste it
        selectedItemValues = tree.item(tree.focus()).get('values')

        db_cursor.execute("""DELETE FROM LAWYERS 
                            WHERE id = """ + str(selectedItemValues[0]))
        db_connection.commit()

        # also delete from treeview
        tree.delete(tree.selection())


remove_button = customtkinter.CTkButton(master=lawyers_tab, text="Remove Lawyer", command=removeFromDatabase)
remove_button.pack(pady=20)

# Start the ui
main_app.mainloop()
