# Imports for ui
import customtkinter
from tkinter import *
from tkinter import ttk

# Import for database
import mysql.connector

# Appearance and style of ui - not really important
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")

# Main application 
main_app = customtkinter.CTk()
main_app.title("Intellectual Property Firm System")
main_app.geometry("1200x700")

### A Frame
#frame = customtkinter.CTkFrame(master=main_app)
#frame.pack(pady=20, padx=20, fill="both", expand=True)


### A Tabview
tabview = customtkinter.CTkTabview(master=main_app)
tabview.pack(pady=20, padx=20, fill="both", expand=True)

# Adding tabs
tabs = ["Tab1", "Tab2", "Tab3"]

for i in tabs:
    tabview.add(i)

tabview.set("Tab1") # set as default tab

# Add label to Tab2
label2 = customtkinter.CTkLabel(master=tabview.tab("Tab2"), text="This is tab2!")
label2.pack(pady=10, padx=10)


frame = tabview.tab("Tab1") # So i do not have to change all the code,
# Basically master=frame or master=tabview.tab("Tab1") is where the components are put into


### A Label
label = customtkinter.CTkLabel(master=frame, text="Hello World")
label.pack(pady=10, padx=10)
# note: Anything with a CTk before it like CTkFrame is from customtkinter library and lets you use .pack(pady=?, padx=?)
# But other things like Treeview is from tkinter library so you have to use .place(x=?, y=?)
# If pack() is hard to use just use place() instead


### An Entry
# Like a TextBox, lets the user enter string inside
entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Enter something here.")
entry1.pack(pady=10, padx=10)


### A Button
# You create a function without any arguments and then use command=function_name to call it with button press
# In this example, the function prints "Button is pressed" to the console
def test():
    print("Button is pressed")

button = customtkinter.CTkButton(master=frame, text="Test Button", command=test)
button.pack(pady=10, padx=10)


### A Treeview
# Used to view tables

# Basic table with column names and info to show you how treeview works
table_columns = ("name","surname","id_no")
info = (("Ali","Aman",5),("Fatma","Tekin",7),("Öykü","Dolu",11))

tree = ttk.Treeview(master=frame, columns=table_columns, show="headings", selectmode="browse") # selectmode="browse" means the user can only select one row at a time
tree.pack() # makes ui look good i guess, DO NOT ERASE

# this is used to make the heading names look better
tree.heading("name",text="Name")
tree.heading("surname",text="Surname")
tree.heading("id_no",text="ID No")

# Insert info into treeview
for i in info:
    tree.insert("", END, values=i)


# Example
def removeFromTree():
    if tree.selection() != None: # this is the row selected by user
        print(tree.selection())
        tree.delete(tree.selection())

remove_button = customtkinter.CTkButton(master=frame, text="Remove Item From Tree", command=removeFromTree)
remove_button.place(x=700,y=500)



### A Treeview with Info From Database

# Database connection
db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql201468", 
  auth_plugin='mysql_native_password'
)
db_cursor = db_connection.cursor(buffered=True)

db_cursor.execute("DROP DATABASE test_for_ip") # might be necessary for testing

db_cursor.execute("CREATE DATABASE IF NOT EXISTS test_for_ip")
db_cursor.execute("USE test_for_ip")

# Create basic table
db_cursor.execute("""CREATE TABLE IF NOT EXISTS PEOPLE (name VARCHAR(50),
                                                         surname VARCHAR(50),
                                                         id_no INT NOT NULL)""")

# Insert some values
db_cursor.execute("""INSERT INTO PEOPLE(name, surname, id_no)
                    VALUES ("Ekin", "Doğru", 2)""")
db_cursor.execute("""INSERT INTO PEOPLE(name, surname, id_no)
                    VALUES ("Turgut", "Yılmaz", 8)""")

db_connection.commit() # otherwise it does not actually update your local mysql database

# Get all values from table
db_cursor.execute("""SELECT * FROM PEOPLE""")

# Insert values into Treeview
rows = db_cursor.fetchall()

for i in rows:
    tree.insert("", END, values=i)


# Example 2
def removeFromDatabase():
    if tree.selection() != None: # this is the row selected by user

        ### IMPORTANT BIT ###
        # This is how you get the values from selected item, just copy paste it
        selectedItemValues = tree.item(tree.focus()).get('values')
        #####################

        print(selectedItemValues)

        db_cursor.execute("""DELETE FROM PEOPLE 
                            WHERE id_no = """ + str(selectedItemValues[2]))
        db_connection.commit()

        # also delete from treeview
        tree.delete(tree.selection())


remove_button = customtkinter.CTkButton(master=frame, text="Remove Item From Database", command=removeFromDatabase)
remove_button.place(x=200,y=500)

# Start the ui
main_app.mainloop()
