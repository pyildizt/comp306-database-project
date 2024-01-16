
### NEED TO RUN THIS CODE FROM TERMINAL IN VSCODE USING python deneme.py

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
main_app.title("Intellectual Property Law Firm Management System")
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

### A Label
label = customtkinter.CTkLabel(master=lawyers_tab, text="Lawyers in the Firm")
label.pack(pady=10, padx=10)


### A Treeview
# Used to view tables

# Basic table with column names and info to show you how treeview works
table_columns = ("id","fname","lname","sex","fee","email","phone_number")

lawyers_tree = ttk.Treeview(master=lawyers_tab, columns=table_columns, show="headings", selectmode="browse",height=20) 
# selectmode="browse" means the user can only select one row at a time
lawyers_tree.pack() # makes ui look good i guess, DO NOT ERASE

# this is used to make the heading names look better

lawyers_tree.heading("id",text="ID")
lawyers_tree.heading("fname",text="Name")
lawyers_tree.heading("lname",text="Surname")
lawyers_tree.heading("sex",text="Sex")
lawyers_tree.heading("fee",text="Fee")
lawyers_tree.heading("email",text="Email")
lawyers_tree.heading("phone_number",text="Phone No")
for i in range(5):
    lawyers_tree.column(i,width=80, stretch=NO)


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
    lawyers_tree.insert("", END, values=i)

# Example 2
def removeFromDatabase():
    if lawyers_tree.selection() != None: # this is the row selected by user

        # This is how you get the values from selected item, just copy paste it
        selectedItemValues = lawyers_tree.item(lawyers_tree.focus()).get('values')

        db_cursor.execute("""DELETE FROM LAWYERS 
                            WHERE id = """ + str(selectedItemValues[0]))
        db_connection.commit()

        # also delete from treeview
        lawyers_tree.delete(lawyers_tree.selection())


remove_button = customtkinter.CTkButton(master=lawyers_tab, text="Remove Lawyer", command=removeFromDatabase)
remove_button.pack(pady=20)



####### CLIENTS TAB

clients_tab = tabview.tab("Clients")

### A Label
clients_label = customtkinter.CTkLabel(master=clients_tab, text="Clients of the Firm")
clients_label.pack(pady=10, padx=10)

### A Treeview
table_columns = ("id","fname","lname","sex","fee","email","phone_number")

table_columns2 = ("client_id","fname","lname","sex","age","bdate","state")

clients_tree = ttk.Treeview(master=clients_tab, columns=table_columns2, show="headings", selectmode="browse",height=20) 
clients_tree.pack()

# this is used to make the heading names look better
clients_tree.heading("client_id", text="Client ID")
clients_tree.heading("fname", text="First Name")
clients_tree.heading("lname", text="Last Name")
clients_tree.heading("sex", text="Sex")
clients_tree.heading("age", text="Age")
clients_tree.heading("bdate", text="Birth Date")
clients_tree.heading("state", text="State")
for i in range(7):
    clients_tree.column(i,width=100, stretch=NO)

# Create basic table
db_cursor.execute("""CREATE TABLE IF NOT EXISTS CLIENTS (
    client_id INT NOT NULL,
    fname VARCHAR(50),
    lname VARCHAR(50),
    sex VARCHAR(6),
    age INT,
    bdate DATE,
    state VARCHAR(50),
    PRIMARY KEY (client_id))""")

insert_clients = (
    "INSERT INTO CLIENTS (client_id, fname, lname, sex, age, bdate, state)"
    "VALUES (%s, %s, %s, %s, %s, %s, %s)")

# Insert some values
populate_table(db_connection, db_cursor, insert_clients, "clients.csv")

# Get all values from table
db_cursor.execute("""SELECT * FROM CLIENTS""")

# Insert values into Treeview
rows = db_cursor.fetchall()

for i in rows:
    clients_tree.insert("", END, values=i)

# Example 2
def removeFromDatabase2():
    if clients_tree.selection() != None: # this is the row selected by user

        # This is how you get the values from selected item, just copy paste it
        selectedItemValues = clients_tree.item(clients_tree.focus()).get('values')

        db_cursor.execute("""DELETE FROM CLIENTS 
                            WHERE client_id = """ + str(selectedItemValues[0]))
        db_connection.commit()

        # also delete from treeview
        clients_tree.delete(clients_tree.selection())


remove_button2 = customtkinter.CTkButton(master=clients_tab, text="Remove Client", command=removeFromDatabase2)
remove_button2.pack(pady=20)


# Start the ui
main_app.mainloop()
