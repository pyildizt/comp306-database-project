# Imports for ui
import customtkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Import for database
import mysql.connector
import csv
import pandas as pd

#CREATE DATABASE:
db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="123678zulal", 
  auth_plugin='mysql_native_password'
)
db_cursor = db_connection.cursor(buffered=True)


def populate_table(db_connection, db_cursor, insert_query, file_path):

    with open(file_path, mode='r') as csv_data:
        reader = csv.reader(csv_data, delimiter=';')
        csv_data_list = list(reader)
        for row in csv_data_list[1:]:
            row = tuple(map(lambda x: None if x == "" else x, row[0].split(',')))
            db_cursor.execute(insert_query, row)
        
    db_connection.commit()

db_cursor.execute("DROP DATABASE IF EXISTS law_firm")
db_cursor.execute("CREATE DATABASE IF NOT EXISTS law_firm")
db_cursor.execute("USE law_firm")


# Create Staff table
db_cursor.execute("""CREATE TABLE IF NOT EXISTS Staff (
                    id CHAR(6),
                    fname VARCHAR(30),
                    lname VARCHAR(30),
                    sex CHAR(1),
                    phone_number CHAR(11),
                    email VARCHAR(50),
                    salary INT,
                    PRIMARY KEY (id))""")

insert_staff = (
    "INSERT INTO Staff(id, fname, lname, sex, phone_number, email, salary) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
)

populate_table(db_connection, db_cursor, insert_staff, "./data/Staff.csv")


#Create Administrator table
db_cursor.execute("""CREATE TABLE IF NOT EXISTS Administrator (
                    admin_id CHAR(6),
                    password INT,
                    PRIMARY KEY (admin_id),
                    FOREIGN KEY (admin_id) REFERENCES Staff(id))""")

insert_administrators = (
    "INSERT INTO Administrator(admin_id,password) "
    "VALUES (%s,%s)"
)

populate_table(db_connection, db_cursor, insert_administrators, "./data/Administrator.csv")


# Create Department table
db_cursor.execute("""CREATE TABLE IF NOT EXISTS Department (
                    department_id CHAR(6),
                    department_name VARCHAR(50),
                    admin_id CHAR(6),
                    PRIMARY KEY (department_id),
                    FOREIGN KEY (admin_id) REFERENCES Administrator(admin_id)
                )""")

insert_departments = (
    "INSERT INTO Department(department_id, department_name, admin_id) "
    "VALUES (%s, %s, %s)"
)

populate_table(db_connection, db_cursor, insert_departments, "./data/Department.csv")


# Create Lawyer table
db_cursor.execute("""CREATE TABLE IF NOT EXISTS Lawyer (
                    lawyer_id CHAR(6),
                    department_id CHAR(6),
                    winning_rate INT,
                    PRIMARY KEY (lawyer_id),
                    FOREIGN KEY (lawyer_id) REFERENCES Staff(id), 
                    FOREIGN KEY (department_id) REFERENCES Department(department_id))""")
                    
insert_lawyers = (
    "INSERT INTO Lawyer(lawyer_id, department_id, winning_rate) "
    "VALUES (%s, %s, %s)"
)

populate_table(db_connection, db_cursor, insert_lawyers, "./data/Lawyer.csv")


# Create Client table
db_cursor.execute("""CREATE TABLE IF NOT EXISTS Client (
                    client_id CHAR(6),
                    fname VARCHAR(30),
                    lname VARCHAR(30),
                    sex CHAR(1),
                    age INT,
                    phone_number CHAR(12),
                    email VARCHAR(50),
                    address VARCHAR(50),
                    bdate DATE,
                    state VARCHAR(50),
                    PRIMARY KEY (client_id))""")

insert_clients = (
    "INSERT INTO Client(client_id, fname, lname, sex, age, phone_number, email, address, bdate, state) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
)

populate_table(db_connection, db_cursor, insert_clients, "./data/Client.csv")

## create Lawsuit table
db_cursor.execute("""CREATE TABLE IF NOT EXISTS Lawsuit (
                        lawsuit_id CHAR(6),
                        verdict VARCHAR(30),
                        court_date DATE,
                        judge_name VARCHAR(50),
                        client_id CHAR(6),
                        PRIMARY KEY (lawsuit_id),
                        FOREIGN KEY (client_id) REFERENCES Client(client_id)
                    )""")

insert_lawsuits = (
    "INSERT INTO Lawsuit(lawsuit_id, verdict, court_date, judge_name, client_id) "
    "VALUES (%s, %s, %s, %s, %s)"
)

populate_table(db_connection, db_cursor, insert_lawsuits, "./data/Lawsuit.csv")


# create Represents table
db_cursor.execute("""CREATE TABLE IF NOT EXISTS Represents (
                        lawyer_id CHAR(6),
                        lawsuit_id CHAR(6),
                        fee INT,
                        PRIMARY KEY (lawyer_id, lawsuit_id),
                        FOREIGN KEY (lawyer_id) REFERENCES Lawyer(lawyer_id),
                        FOREIGN KEY (lawsuit_id) REFERENCES Lawsuit(lawsuit_id)
                    )""")

insert_represents = (
    "INSERT INTO Represents(lawyer_id, lawsuit_id, fee) "
    "VALUES (%s, %s, %s)"
)

populate_table(db_connection, db_cursor, insert_represents, "./data/Represents.csv")



# Create Counsels table
db_cursor.execute("""CREATE TABLE IF NOT EXISTS Counsels (
                        lawyer_id CHAR(6),
                        client_id CHAR(6),
                        fee INT,
                        date DATE,
                        PRIMARY KEY(lawyer_id, client_id),
                        FOREIGN KEY(lawyer_id) REFERENCES Lawyer(lawyer_id),
                        FOREIGN KEY(client_id) REFERENCES Client(client_id)
                        )""")

# Insert into Counsels table
insert_patents = (
    "INSERT INTO Counsels(lawyer_id, client_id, fee, date) "
    "VALUES (%s, %s, %s, %s)"
)

populate_table(db_connection, db_cursor, insert_patents, "./data/Counsels.csv")



# Appearance and style of ui - not really important
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")

# Main application 
main_app = customtkinter.CTk()
main_app.title("Intellectual Property Firm System")
main_app.geometry("1300x700+70+0")
main_app.resizable(width=None, height=None)

def loginWindow():
    login_window = customtkinter.CTkToplevel(main_app) 
    login_window.title("Login")
    login_window.geometry("500x300+500+300")

    main_app.withdraw() #iconify()

    frame = customtkinter.CTkFrame(master=login_window) 
    frame.pack(pady=20,padx=40,fill='both',expand=True)

    login_label1 = customtkinter.CTkLabel(master=frame, text="")
    login_label1.pack(pady=10, padx=10)
    
    user_entry= customtkinter.CTkEntry(master=frame,placeholder_text="Username") 
    user_entry.pack(pady=12,padx=10) 
    
    user_pass= customtkinter.CTkEntry(master=frame,placeholder_text="Password",show="*") 
    user_pass.pack(pady=12,padx=10)

    login_label2 = customtkinter.CTkLabel(master=frame, text="")

    def login():
        username = "admin"
        password = "1234"
        if user_entry.get() == username and user_pass.get() == password: 
            main_app.deiconify()
            login_window.destroy()
        else:
            login_label2.configure(text="Incorrect password. Try again.")

    button = customtkinter.CTkButton(master=frame,text='Login',command=login) 
    button.pack(pady=12,padx=10) 
    login_label2.pack(pady=10, padx=10) 



### Tabview
tabview = customtkinter.CTkTabview(master=main_app)
tabview.pack(pady=20, padx=20, fill="both", expand=True)

# Adding tabs
tabs = ["Lawyers", "Clients", "Lawsuits", "Departments"]
for i in tabs:
    tabview.add(i)
tabview.set("Lawyers") # set as default tab


##### LAWYERS TAB

### A Label
#label = customtkinter.CTkLabel(master=tabview.tab("Lawyers"), text="Lawyers")

label = customtkinter.CTkLabel(
    master=tabview.tab("Lawyers"),
    text="LAWYERS",
    font=("Courier", 30, "bold")
)



# Basically master=frame or master=tabview.tab("Tab1") is where the components are put into
label.pack(pady=60, padx=10)
# note: Anything with a CTk before it like CTkFrame is from customtkinter library and lets you use .pack(pady=?, padx=?)
# But other things like Treeview is from tkinter library so you have to use .place(x=?, y=?)
# If pack() is hard to use just use place() instead


### An Entry
# Like a TextBox, lets the user enter string inside
#entry1 = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), #placeholder_text="Enter something here.")
#entry1.pack(pady=10, padx=10)

### A Button
# You create a function without any arguments and then use command=function_name to call it with button press
# In this example, the function prints "Button is pressed" to the console
#def test():
#    print("Button is pressed")

#button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Test Button", command=test)
#button.pack(pady=10, padx=10)


### A Treeview


# for now i just wrote it insetad of taking from database
table_columns = ("name","surname","id_no")

#lawyers treeview
lawyers_tree = ttk.Treeview(master=tabview.tab("Lawyers"), columns=table_columns, show="headings", selectmode="browse") # selectmode="browse" means the user can only select one row at a time
lawyers_tree.pack() # makes ui look good i guess, DO NOT ERASE

# this is used to make the heading names look better
lawyers_tree.heading("name",text="Name")
lawyers_tree.heading("surname",text="Surname")
lawyers_tree.heading("id_no",text="ID No")

# Insert info into treeview (NORMALLY info SHOULD BE TAKEN FROM DATABASE)
#info = (("Fatma","Tekin","LAW007"),("Ali","Aman","LAW005"),("Öykü","Dolu","LAW0011"))
#for i in info:
#    lawyers_tree.insert("", END, values=i)


# data from the Lawyer and Staff tables 
db_cursor.execute("""
    SELECT s.fname, s.lname,s.id, s.sex, s.phone_number, s.email, s.salary
    FROM Staff s
    JOIN Lawyer l ON s.id = l.lawyer_id
""")
lawyers_data = db_cursor.fetchall()

for lawyer in lawyers_data:
    lawyers_tree.insert("", END, values=lawyer)




def removeLawyerFromDatabase():
    if lawyers_tree.selection() != None: # this is the row selected by user

        ### IMPORTANT BIT ###
        # This is how you get the values from selected item, just copy paste it
        selectedItemValues = lawyers_tree.item(lawyers_tree.focus()).get('values')
        # This returns a list like ["Ali", "Aman", 5], then you can do selectedItemValues[0] to get "Ali" or whatever
        #####################

        print(selectedItemValues)

        db_cursor.execute("""DELETE FROM Lawyers
                            WHERE id_no = """ + str(selectedItemValues[2]))  #PROBABLY WONT WORK RIGHT NOW
        db_connection.commit()

        # also delete from treeview
        lawyers_tree.delete(lawyers_tree.selection())

remove_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Remove Item From Tree", command=removeLawyerFromDatabase)
remove_button.place(x=700,y=500)


def sort_lawyers_by_name():
    valid_items = [item for item in lawyers_tree.get_children() if lawyers_tree.item(item, 'values')]
    sorted_items = sorted(valid_items, key=lambda x: lawyers_tree.item(x, 'values')[0])

    for index, item in enumerate(sorted_items):
        lawyers_tree.move(item, "", index)

sort_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Sort by Name", command=sort_lawyers_by_name)
sort_button.place(x=900, y=200)

def show_lawyer_info():
    selected_item = lawyers_tree.selection()
    if selected_item:
        item_values = lawyers_tree.item(selected_item, "values")
        lawyer_id = item_values[2]

        db_cursor.execute(f"SELECT L.*, S.fname, S.lname, S.sex, S.phone_number, S.email, S.salary "
                          f"FROM Lawyer L JOIN Staff S ON L.lawyer_id = S.id "
                          f"WHERE L.lawyer_id = '{lawyer_id}'")
        lawyer_details = db_cursor.fetchone()

        # yeni window oluşturup gösteriyor - başka nasıl gösterebiliriz?
        details_window = Toplevel(main_app)
        details_window.title(f"Info for Lawyer ID {lawyer_id}")

        if lawyer_details:
            details_label = Label(details_window, text=f"Lawyer ID: {lawyer_details[0]}\n"
                                                        f"Department ID: {lawyer_details[1]}\n"
                                                       f"Winning Rate: {lawyer_details[2]}\n"
                                                       f"First Name: {lawyer_details[3]}\n"
                                                        f"Last Name: {lawyer_details[4]}\n"
                                                       f"Sex: {lawyer_details[5]}\n"
                                                       f"Phone Number: {lawyer_details[6]}\n"
                                                       f"Email: {lawyer_details[7]}\n"
                                                      f"Salary: {lawyer_details[8]}")
            details_label.pack(pady=20, padx=20)
        else:
            no_details_label = Label(details_window, text=f"No info found for Lawyer ID {lawyer_id}")
            no_details_label.pack(pady=20, padx=20)

show_details_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Show Info", command=show_lawyer_info)
show_details_button.place(x=900, y=250)

#info ile aynı mantık ama clientları da var ekstradan
def show_lawyer_details():
    selected_item = lawyers_tree.selection()
    if selected_item:
        item_values = lawyers_tree.item(selected_item, "values")
        lawyer_id = item_values[2]

        db_cursor.execute(f"SELECT * FROM Lawyer WHERE lawyer_id = '{lawyer_id}'")
        lawyer_details = db_cursor.fetchone()

        db_cursor.execute(f"""
            SELECT c.client_id, c.fname, c.lname, c.sex, c.age, c.phone_number, c.email, c.address, c.bdate, c.state
            FROM Counsels cl
            JOIN Client c ON cl.client_id = c.client_id
            WHERE cl.lawyer_id = '{lawyer_id}'
        """)
        client_details = db_cursor.fetchall()

        details_window = Toplevel(main_app)
        details_window.title(f"Details for Lawyer ID {lawyer_id}")

        if lawyer_details:
            details_label = Label(details_window, text=f"Lawyer ID: {lawyer_details[0]}")
            details_label.pack(pady=20, padx=20)
        else:
            no_details_label = Label(details_window, text=f"No details found for Lawyer ID {lawyer_id}")
            no_details_label.pack(pady=20, padx=20)

        if client_details:
            client_label = Label(details_window, text="Client Details:")
            client_label.pack(pady=10, padx=20)

            for client in client_details:
                client_info_label = Label(
                    details_window,
                    text=f"Client ID: {client[0]}, Name: {client[1]} {client[2]}, Sex: {client[3]}, Age: {client[4]}, Phone: {client[5]}, Email: {client[6]}, Address: {client[7]}, Birthdate: {client[8]}, State: {client[9]}"
                )
                client_info_label.pack(pady=5, padx=20)

show_details_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Show Details", command=show_lawyer_details)
show_details_button.place(x=900, y=300)


def search_lawyers():
    search_name = search_entry.get().strip().lower()

    lawyers_tree.delete(*lawyers_tree.get_children())
        
    db_cursor.execute(f"""
        SELECT s.fname, s.lname,s.id,  s.sex, s.phone_number, s.email, s.salary, l.*
        FROM Staff s
        JOIN Lawyer l ON s.id = l.lawyer_id
        WHERE LOWER(CONCAT(' ', s.fname, s.lname)) LIKE '%{search_name}%'
    """)
    searched_lawyers = db_cursor.fetchall()

    for lawyer in searched_lawyers:
        lawyers_tree.insert("", END, values=lawyer)

search_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Search Lawyers", command=search_lawyers)
search_button.place(x=900, y=100)
search_entry = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="Enter lawyer's name")
search_entry.place(x=750, y=100)


##### yeni eklediğimi silemiyorum ? ##########

def addLawyer():
    fname = fname_input.get()
    lname = lname_input.get()
    lawyer_id = lawyer_id_input.get()

    if not all([fname, lname, lawyer_id]):
        messagebox.showwarning("Validation Error", "Please fill in all the fields.")
        return

    if not (lawyer_id.startswith("LAW") and len(lawyer_id) == 6):
        messagebox.showwarning("Validation Error", "Invalid input format or length.")
        return

    lawyers_tree.insert("", END, values=(fname, lname, lawyer_id))
    db_cursor.execute("INSERT INTO LAWYER (fname, lname, lawyer_id) VALUES (%s, %s, %s)",
                      (fname, lname, lawyer_id))
    db_connection.commit()

    fname_input.delete(0, END)
    lname_input.delete(0, END)
    lawyer_id_input.delete(0, END)

fname_input = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="First Name")
fname_input.place(x=500, y=400)

lname_input = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="Last Name")
lname_input.place(x=500, y=450)

lawyer_id_input = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="LAWXXX")
lawyer_id_input.place(x=500, y=500)


insert_button1 = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Add Lawyer", command=addLawyer)
insert_button1.place(x=500, y=550)


##### CLIENTS TAB
clients_label = customtkinter.CTkLabel(master=tabview.tab("Clients"), text="Clients")
clients_label.pack(pady=10, padx=10)

#Client Headers
df = pd.read_csv('./data/Client.csv')
client_columns = tuple(df.columns)
print(client_columns)

#Client Columns
db_cursor.execute("SELECT * FROM Client")
clients_from_database = db_cursor.fetchall()

#Client Tree View
client_tree = ttk.Treeview(master=tabview.tab("Clients"), columns=client_columns, show="headings", selectmode="browse") 
client_tree.pack()

client_tree.heading(client_columns[0], text="Client ID")
client_tree.heading(client_columns[1], text="Name")
client_tree.heading(client_columns[2], text="Surname")
client_tree.heading(client_columns[3], text="Sex")
client_tree.heading(client_columns[4], text="Age")
client_tree.heading(client_columns[5], text="Phone No")
client_tree.heading(client_columns[6], text="Email")
client_tree.heading(client_columns[7], text="Address")
client_tree.heading(client_columns[8], text="Birthdate")
client_tree.heading(client_columns[9], text="State")

for i in range(10):
    if i == 0 or i == 3 or i == 4:
        client_tree.column(column=i,width=60,stretch=False)
    elif i == 5:
        client_tree.column(column=i,width=115,stretch=False)
    elif i == 6:
        client_tree.column(column=i,width=200,stretch=False)
    else:
        client_tree.column(column=i,width=105,stretch=False)

for i in clients_from_database:
    client_tree.insert("", END, values=i)
    





##### LAWSUITS TAB




##### DEPARTMENTS TAB
department_label = customtkinter.CTkLabel(master=tabview.tab("Departments"), text="Departments")
department_label.pack(pady=10, padx=10)

#Department Headers
df = pd.read_csv('./data/Department.csv')
department_columns = tuple(df.columns)
print(department_columns)

#Department Columns
db_cursor.execute("SELECT * FROM Department")
departments = db_cursor.fetchall()

#Department Tree View
department_tree = ttk.Treeview(master=tabview.tab("Departments"), columns=department_columns, show="headings", selectmode="browse") 
department_tree.pack()

department_tree.heading(department_columns[0], text="Department ID")
department_tree.heading(department_columns[1], text="Department Name")
department_tree.heading(department_columns[2], text="Admin ID")
department_tree.column(department_columns[1], minwidth=0, width=300)

for i in departments:
    department_tree.insert("", END, values=i)
    

#Insert Button for Department
def insertDepartmentToDatabase():
    dep_id = dep_id_input.get()
    dep_name = dep_name_input.get()
    adm_id = admin_id_input.get()

    if not all([dep_id, dep_name, adm_id]):
        messagebox.showwarning("Validation Error", "Please fill in all the fields.")
        return

    if not (dep_id.startswith("DEP") and len(dep_id) == 6 and adm_id.startswith("ADM") and len(adm_id) == 6):
        print(dep_id.startswith("DEP"))
        print(len(dep_id) == 6)
        print(adm_id.startswith("ADM"))
        print(len(adm_id) == 6)

        messagebox.showwarning("Validation Error", "Invalid input format or length.")
        return

    department_tree.insert("", END, values=(dep_id, dep_name, adm_id))
    db_cursor.execute("INSERT INTO Department (department_id, department_name, admin_id) VALUES (%s, %s, %s)",
                      (dep_id, dep_name, adm_id))
    db_connection.commit()

    # Clear the entry widgets
    dep_id_input.delete(0, END)
    dep_name_input.delete(0, END)
    admin_id_input.delete(0, END)


# Entry widgets for adding a new department
dep_id_label = customtkinter.CTkLabel(tabview.tab("Departments"), text="Department ID:")
dep_name_label = customtkinter.CTkLabel(tabview.tab("Departments"), text="Department Name:")
admin_id_label = customtkinter.CTkLabel(tabview.tab("Departments"), text="Admin ID:")

dep_id_label.pack(side="top",padx=5, pady=9)
dep_id_input = customtkinter.CTkEntry(tabview.tab("Departments"), placeholder_text="DEPXXX")
dep_id_input.pack(padx=5, pady=5)

dep_name_label.pack(padx=5, pady=4)
dep_name_input = customtkinter.CTkEntry(tabview.tab("Departments"), placeholder_text="Department Name")
dep_name_input.pack(padx=5, pady=5)

admin_id_label.pack(padx=5, pady=4)
admin_id_input = customtkinter.CTkEntry(tabview.tab("Departments"), placeholder_text= "ADMXXX")
admin_id_input.pack(padx=5, pady=5)

# Insert Button for Department
insert_button = customtkinter.CTkButton(master=tabview.tab("Departments"), text="Add Department", command=insertDepartmentToDatabase)
insert_button.pack(pady=10)

#Show Department Details
def showDepartmentLawyers():
    selected_item = department_tree.selection()
    if selected_item:
        details = department_tree.item(selected_item, 'values')

        details_window = customtkinter.CTkToplevel(main_app)
        details_window.title("Details")
        details_window.geometry("400x150+400+150")
        
        #Department Lawyers Title
        header_label = customtkinter.CTkLabel(details_window, text=details[1] + " Department Lawyers", font=("Helvetica", 16, "bold"))
        header_label.pack(padx=0, pady=5, anchor="w")

        department_lawyers_query = db_cursor.execute("""SELECT S.fname, S.lname
                                                FROM Department D, Staff S, Lawyer L
                                                WHERE D.department_id = %s AND L.department_id = D.department_id AND S.id = L.lawyer_id
                                                """, (details[0],))

        db_cursor.execute(department_lawyers_query)
        department_lawyers = db_cursor.fetchall()
        department_lawyers = "\n".join([f"{fname} {lname} " for fname, lname in department_lawyers])

        department_lawyer_label = customtkinter.CTkLabel(details_window, text=department_lawyers)
        department_lawyer_label.pack(padx=0, pady=5, anchor="w")

# Button to show details
department_details_button = customtkinter.CTkButton(tabview.tab("Departments"), text="Department Lawyers", command=showDepartmentLawyers)
department_details_button.place(relx=1, x=-50, rely=0, y=70, anchor="ne")

#-----------------------------------------------------------------------
# Canvas for the bar chart
department_details_button = customtkinter.CTkButton(tabview.tab("Departments"), text="Winning Rate Statistics", command=showDepartmentLawyers)
department_details_button.place(relx=1, x=-50, rely=0, y=120, anchor="ne")




# Start the ui
loginWindow()
main_app.mainloop()
