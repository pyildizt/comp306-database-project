# Imports for ui
import customtkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Imports for showing details in UI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Import for checking inputs in UI (regular expressions)
import re

# Imports for database
import mysql.connector
import csv
import pandas as pd

#CREATE DATABASE:
db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql201468",
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
                        FOREIGN KEY (client_id) REFERENCES Client(client_id) ON DELETE CASCADE
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
                        FOREIGN KEY (lawyer_id) REFERENCES Lawyer(lawyer_id) ON DELETE CASCADE,
                        FOREIGN KEY (lawsuit_id) REFERENCES Lawsuit(lawsuit_id) ON DELETE CASCADE
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
                        FOREIGN KEY(lawyer_id) REFERENCES Lawyer(lawyer_id) ON DELETE CASCADE,
                        FOREIGN KEY(client_id) REFERENCES Client(client_id) ON DELETE CASCADE
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
main_app.geometry("1200x700+70+0")
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
    
    admin_id_query = db_cursor.execute("""SELECT admin_id FROM Administrator""")
    admin_ids = db_cursor.fetchall() 
    admin_ids_list = [i[0] for i in admin_ids]

    admin_id_combobox = ttk.Combobox(master=frame, values=admin_ids_list, state="readonly", width = 30)
    admin_id_combobox.set("Admin ID")
    admin_id_combobox.pack(pady=12, padx=120)

    user_pass= customtkinter.CTkEntry(master=frame,placeholder_text="Password",show="*", width=180) 
    user_pass.pack(pady=12,padx=10)


    def login():
        username = admin_id_combobox.get()  # Use the selected admin ID as the username
        password = user_pass.get()

        adm_password = db_cursor.execute("""SELECT password FROM Administrator WHERE Administrator.admin_id = %s""", (username,))
        adm_password = db_cursor.fetchall()
        adm_password = str(adm_password[0][0])

        if password == adm_password: 
            main_app.deiconify()
            login_window.destroy()

        elif password == "":
            messagebox.showwarning("Password Error", "Admin password is null!")

        else:
            messagebox.showwarning("Password Error", "Admin password is wrong!")
            return
            

    button = customtkinter.CTkButton(master=frame,text='Login',command=login) 
    button.pack(pady=12,padx=10) 



### Tabview
tabview = customtkinter.CTkTabview(master=main_app)
tabview.pack(pady=20, padx=20, fill="both", expand=True)

# Adding tabs
tabs = ["Lawyers", "Clients", "Lawsuits", "Departments"]
for i in tabs:
    tabview.add(i)
tabview.set("Lawyers") # set as default tab


##### LAWYERS TAB
label = customtkinter.CTkLabel(
    master=tabview.tab("Lawyers"),
    text="LAWYERS",
    font=("Courier", 30, "bold")
)
label.pack(pady=60, padx=10)

### A Treeview
table_columns = ("name","surname","id_no")

#lawyers treeview
lawyers_tree = ttk.Treeview(master=tabview.tab("Lawyers"), columns=table_columns, show="headings", selectmode="browse") # selectmode="browse" means the user can only select one row at a time
lawyers_tree.pack() # makes ui look good i guess, DO NOT ERASE

# this is used to make the heading names look better
lawyers_tree.heading("name",text="Name")
lawyers_tree.heading("surname",text="Surname")
lawyers_tree.heading("id_no",text="ID No")

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
        selectedItemValues = lawyers_tree.item(lawyers_tree.focus()).get('values')

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
clients_label = customtkinter.CTkLabel(master=tabview.tab("Clients"), text="CLIENTS", font=("Courier", 30, "bold")).pack(pady=10, padx=10)

#Client Headers
df = pd.read_csv('./data/Client.csv')
client_columns = tuple(df.columns)

#Client Columns
db_cursor.execute("SELECT * FROM Client")
clients_from_database = db_cursor.fetchall()

#Client Tree View
client_tree = ttk.Treeview(master=tabview.tab("Clients"), columns=client_columns, show="headings", selectmode="browse") 
client_tree.pack(padx=10, pady=10)

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
    

## Entry widgets for adding a new client
# Label and Entry for Client ID
client_id_label = customtkinter.CTkLabel(master=tabview.tab("Clients"), text="Client ID:").place(x=120, y=300)
client_id_input = customtkinter.CTkEntry(master=tabview.tab("Clients"), placeholder_text="CLIXX", width=100)
client_id_input.place(x=120, y=330)

# Label and Entry for First Name
client_fname_label = customtkinter.CTkLabel(master=tabview.tab("Clients"), text="Name:").place(x=270, y=300)
client_fname_input = customtkinter.CTkEntry(master=tabview.tab("Clients"), placeholder_text="", width=100)
client_fname_input.place(x=270, y=330)

# Label and Entry for Last Name
client_lname_label = customtkinter.CTkLabel(master=tabview.tab("Clients"), text="Surname:").place(x=420, y=300)
client_lname_input = customtkinter.CTkEntry(master=tabview.tab("Clients"), placeholder_text="", width=100)
client_lname_input.place(x=420, y=330)

# Label and Entry for Sex
client_sex_label = customtkinter.CTkLabel(master=tabview.tab("Clients"), text="Sex:").place(x=570, y=300)
client_sex_input = customtkinter.CTkEntry(master=tabview.tab("Clients"), placeholder_text="F or M", width=100)
client_sex_input.place(x=570, y=330)

# Label and Entry for Age
client_age_label = customtkinter.CTkLabel(master=tabview.tab("Clients"), text="Age:").place(x=720, y=300)
client_age_input = customtkinter.CTkEntry(master=tabview.tab("Clients"), placeholder_text="", width=100)
client_age_input.place(x=720, y=330)

# Label and Entry for Phone Number
client_phone_label = customtkinter.CTkLabel(master=tabview.tab("Clients"), text="Phone Number:").place(x=120, y=380)
client_phone_input = customtkinter.CTkEntry(master=tabview.tab("Clients"), placeholder_text="___-___-____", width=100)
client_phone_input.place(x=120, y=410)

# Label and Entry for Email
client_email_label = customtkinter.CTkLabel(master=tabview.tab("Clients"), text="Email:").place(x=270, y=380)
client_email_input = customtkinter.CTkEntry(master=tabview.tab("Clients"), placeholder_text="_@email.com", width=100)
client_email_input.place(x=270, y=410)

# Label and Entry for Address
client_address_label = customtkinter.CTkLabel(master=tabview.tab("Clients"), text="Address:").place(x=420, y=380)
client_address_input = customtkinter.CTkEntry(master=tabview.tab("Clients"), placeholder_text="", width=100)
client_address_input.place(x=420, y=410)

# Label and Entry for Birthdate
client_bdate_label = customtkinter.CTkLabel(master=tabview.tab("Clients"), text="Birthdate:").place(x=570, y=380)
client_bdate_input = customtkinter.CTkEntry(master=tabview.tab("Clients"), placeholder_text="yyyy-mm-dd", width=100)
client_bdate_input.place(x=570, y=410)

# Label and Entry for State
client_state_label = customtkinter.CTkLabel(master=tabview.tab("Clients"), text="State:").place(x=720, y=380)
client_state_input = customtkinter.CTkEntry(master=tabview.tab("Clients"), placeholder_text="", width=100)
client_state_input.place(x=720, y=410)

# Insert Client Button
def insertClientToDatabase():
    client_id = client_id_input.get()
    client_fname = client_fname_input.get()
    client_lname = client_lname_input.get()
    client_sex = client_sex_input.get()
    client_age = client_age_input.get()
    client_phone = client_phone_input.get()
    client_email = client_email_input.get()
    client_address = client_address_input.get()
    client_bdate = client_bdate_input.get()
    client_state = client_state_input.get()

    if not all([client_id, client_fname, client_lname, client_sex, client_age, client_phone, client_email, client_address, client_bdate, client_state]):
        messagebox.showwarning("Validation Error", "Please fill in all the fields.")
        return

    if not(bool(re.match(r'^CLI\d{2}$', client_id)) and 
           bool(re.match(r'^(F|M)$', client_sex)) and 
           bool(re.match(r'^\d+$', client_age)) and 
           bool(re.match(r'^\d{3}-\d{3}-\d{4}$', client_phone)) and 
           bool(re.match(r'^.+@email\.com$', client_email)) and 
           bool(re.match(r'^\d{4}-\d{2}-\d{2}$', client_bdate)) and
           bool(re.match(r'^(Suspect|Defendant|Accused)$', client_state))):
        messagebox.showwarning("Validation Error", "Invalid input format.")
        return
    
    client_id_query = db_cursor.execute("""SELECT client_id FROM Client""")
    client_ids = db_cursor.fetchall() 
    client_ids_list = [i[0] for i in client_ids]

    if (client_id in client_ids_list):
        messagebox.showwarning("Validation Error", "Client ID already exists in Client table.")
        return

    client_tree.insert("", END, values=(client_id, client_fname, client_lname, client_sex, client_age, client_phone, client_email, client_address, client_bdate, client_state))
    db_cursor.execute("INSERT INTO Client (client_id,fname,lname,sex,age,phone_number,email,address,bdate,state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                      (client_id, client_fname, client_lname, client_sex, client_age, client_phone, client_email, client_address, client_bdate, client_state))
    db_connection.commit()

    # Clear the entry widgets
    client_id_input.delete(0, END)
    client_fname_input.delete(0, END)
    client_lname_input.delete(0, END)
    client_sex_input.delete(0, END)
    client_age_input.delete(0, END)
    client_phone_input.delete(0, END)
    client_email_input.delete(0, END)
    client_address_input.delete(0, END)
    client_bdate_input.delete(0, END)
    client_state_input.delete(0, END)

insert_client_button = customtkinter.CTkButton(master=tabview.tab("Clients"), text="Add Client", width=100, command=insertClientToDatabase).place(x=420, y=470)

# Remove Client Button
def removeClientFromDatabase():
    if client_tree.selection() != None: 
        selectedItemValues = client_tree.item(client_tree.focus()).get('values')
        db_cursor.execute("DELETE FROM Client WHERE client_id = \"" + str(selectedItemValues[0]) + "\"")
        db_connection.commit()

        # also delete from treeview
        client_tree.delete(client_tree.selection())

    #else:
    #    messagebox.showwarning("Selection Error", "Please select client to remove.")


remove_client_button = customtkinter.CTkButton(master=tabview.tab("Clients"), text="Remove Client", command=removeClientFromDatabase).place(x=950, y=300)

def showClientStateStatistics():
    print("button pressed")
    db_cursor.execute("""SELECT state, COUNT(client_id)
                        FROM Client
                        GROUP BY state
                        ORDER BY COUNT(client_id) ASC
                        """)
    state_count_query = db_cursor.fetchall()
    states = [i[0] for i in state_count_query]
    state_sums = [i[1] for i in state_count_query]

    fig, ax = plt.subplots()
    ax.pie(state_sums, labels=states, colors=["#B0DAFF", "#19A7CE","#146C94"], autopct='%.2f%%', startangle=90)
    plt.title("Client Status Statistics")
    ax.axis('equal') 
    #plt.show()
    
    client_status_rate_window = customtkinter.CTkToplevel(main_app)
    client_status_rate_window.title("Client Status Statistics")
    client_status_rate_window.geometry("700x550+300+50")

    canvas = FigureCanvasTkAgg(fig, master=client_status_rate_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    def on_close():
        client_status_rate_window.destroy()

    client_status_rate_window.protocol("WM_DELETE_WINDOW", on_close)
    client_status_rate_window.mainloop()

show_client_details_button = customtkinter.CTkButton(master=tabview.tab("Clients"), text="Show State Statistics", command=showClientStateStatistics).place(x=950, y=350)

def sortClientsByID():
    print("sort clients by client_id")
    db_cursor.execute("SELECT * FROM Client ORDER BY client_id ASC")
    sorted_clients = db_cursor.fetchall()

    #Delete old items
    old_items = client_tree.get_children()
    for item in old_items:
        client_tree.delete(item)

    #Insert sorted items from query
    for i in sorted_clients:
        client_tree.insert("", END, values=i)

sort_clients_by_id_button = customtkinter.CTkButton(master=tabview.tab("Clients"), text="Sort by ID", command=sortClientsByID).place(x=950, y=400)

def sortClientsByName():
    print("sort clients by fname")
    db_cursor.execute("SELECT * FROM Client ORDER BY fname ASC")
    sorted_clients = db_cursor.fetchall()

    #Delete old items
    old_items = client_tree.get_children()
    for item in old_items:
        client_tree.delete(item)

    #Insert sorted items from query
    for i in sorted_clients:
        client_tree.insert("", END, values=i)

sort_clients_by_name_button = customtkinter.CTkButton(master=tabview.tab("Clients"), text="Sort by Name", command=sortClientsByName).place(x=950, y=450)

def sortClientsByState():
    print("sort clients by state")
    db_cursor.execute("SELECT * FROM Client ORDER BY state ASC")
    sorted_clients = db_cursor.fetchall()

    #Delete old items
    old_items = client_tree.get_children()
    for item in old_items:
        client_tree.delete(item)

    #Insert sorted items from query
    for i in sorted_clients:
        client_tree.insert("", END, values=i)

sort_clients_by_state_button = customtkinter.CTkButton(master=tabview.tab("Clients"), text="Sort by State", command=sortClientsByState).place(x=950, y=500)


##### LAWSUITS TAB

lawsuitTitle = customtkinter.CTkLabel(master=tabview.tab("Lawsuits"), text="LAWSUITS",font=("Courier", 30, "bold"))
lawsuitTitle.pack(padx=10,pady=10)
lawsuitColumns = ["lawsuit_id","verdict","court_date","judge_name","client_id"]
lawsuitTree = ttk.Treeview(master=tabview.tab("Lawsuits"), columns=lawsuitColumns, show="headings", selectmode="browse")
lawsuitTree.pack()
lawsuitTree.heading("lawsuit_id",text="Lawsuit ID")
lawsuitTree.heading("verdict",text="Verdict")
lawsuitTree.heading("court_date",text="Court Date")
lawsuitTree.heading("judge_name",text="Judge Name")
lawsuitTree.heading("client_id",text="Client ID")

allLawsuitsQuery = """SELECT * FROM Lawsuit"""
db_cursor.execute(allLawsuitsQuery)
allLawsuits = db_cursor.fetchall()
for lawsuit in allLawsuits:
    lawsuitTree.insert("",END,values=lawsuit)

def showLawsuitDetails():
    return

showLawsuitDetailsButton = customtkinter.CTkButton(master= tabview.tab("Lawsuits"),text="Show Details",command=showLawsuitDetails)
showLawsuitDetailsButton.place(x=120,y=300)

def removeLawsuit():
    selectedLawsuit = lawsuitTree.item(lawsuitTree.focus(),"values")
    removeLawsuitQuery = """DELETE FROM Lawsuit WHERE lawsuit_id = '{0}'""".format(selectedLawsuit[0])
    db_cursor.execute(removeLawsuitQuery)
    db_connection.commit()
    lawsuitTree.delete(lawsuitTree.selection())
    return

removeLawsuitButton = customtkinter.CTkButton(master= tabview.tab("Lawsuits"),text="Remove Lawsuit",command=removeLawsuit)
removeLawsuitButton.place(x=350,y=300)



lawsuitIDLabel = customtkinter.CTkLabel(master=tabview.tab("Lawsuits"),text="Lawsuit ID:")
lawsuitIDEntry = customtkinter.CTkEntry(master=tabview.tab("Lawsuits"), placeholder_text="LWSXXX")
lawsuitIDEntry.place(x=880,y=300)
lawsuitIDLabel.place(x=780,y=300)

verdictLabel = customtkinter.CTkLabel(master=tabview.tab("Lawsuits"),text="Verdict:")
verdictEntry = customtkinter.CTkEntry(master=tabview.tab("Lawsuits"), placeholder_text="Guilty/Free")
verdictEntry.place(x=880,y=330)
verdictLabel.place(x=780,y=330)

courtDateLabel = customtkinter.CTkLabel(master=tabview.tab("Lawsuits"),text="Court Date:")
courtDateEntry = customtkinter.CTkEntry(master= tabview.tab("Lawsuits"),placeholder_text="YYYY-MM-DD")
courtDateEntry.place(x=880,y=360)
courtDateLabel.place(x=780,y=360)

judgeNameLabel = customtkinter.CTkLabel(master=tabview.tab("Lawsuits"),text="Judge Name:")
judgeNameEntry = customtkinter.CTkEntry(master= tabview.tab("Lawsuits"),placeholder_text="Judge XXXX")
judgeNameEntry.place(x=880,y=390)
judgeNameLabel.place(x=780,y=390)

clientIdLabel = customtkinter.CTkLabel(master= tabview.tab("Lawsuits"),text="Client ID:")
clientIdEntry = customtkinter.CTkEntry(master= tabview.tab("Lawsuits"),placeholder_text="CLIXX")
clientIdEntry.place(x=880,y=420)
clientIdLabel.place(x=780,y=420)

def addLawsuitButtonClick():
    lawsuitId = lawsuitIDEntry.get()
    verdict = verdictEntry.get()
    courtDate = courtDateEntry.get()
    judgeName = judgeNameEntry.get()
    clientId = clientIdEntry.get()

    if not all([lawsuitId, verdict, courtDate, judgeName, clientId]):
        messagebox.showwarning("Validation Error", "Please fill in all the fields.")
        return

    if not(bool(re.match(r'^LWS\d{3}$', lawsuitId)) and 
           bool(re.match(r'^(Free|Guilty)$', verdict)) and 
           bool(re.match(r'^\d{4}-\d{2}-\d{2}$', courtDate)) and  
           bool(re.match(r'^CLI\d{2}$', clientId))):
        messagebox.showwarning("Validation Error", "Invalid input format.")
        return

    try:
        addLawsuitQuery = """INSERT INTO Lawsuit VALUES ('{0}','{1}','{2}','{3}','{4}')""".format(lawsuitId, verdict, courtDate, judgeName, clientId)
        print(addLawsuitQuery)
        db_cursor.execute(addLawsuitQuery)
        db_connection.commit()
        lawsuitTree.insert("",END,values=(lawsuitId, verdict, courtDate, judgeName, clientId))
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showwarning("Format Error!","The input format is wrong.")

addLawsuitButton = customtkinter.CTkButton(master= tabview.tab("Lawsuits"), text="Add Lawsuit",command=addLawsuitButtonClick)
addLawsuitButton.place(x=880,y=480)







##### DEPARTMENTS TAB
department_label = customtkinter.CTkLabel(master=tabview.tab("Departments"), text="DEPARTMENTS",font=("Courier", 30, "bold"))
department_label.pack(pady=10, padx=10)

#Department Headers
df = pd.read_csv('./data/Department.csv')
department_columns = tuple(df.columns)

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
        messagebox.showwarning("Validation Error", "Invalid input format or length.")
        return

    admin_id_query = db_cursor.execute("""SELECT admin_id FROM Administrator""")
    admin_ids = db_cursor.fetchall() 
    admin_ids_list = [i[0] for i in admin_ids]

    dep_id_query = db_cursor.execute("""SELECT department_id FROM Department""")
    dep_ids = db_cursor.fetchall() 
    dep_ids_list = [i[0] for i in dep_ids]

    if (dep_id in dep_ids_list):
        messagebox.showwarning("Validation Error", "This Department already exists!")
        return

    if (adm_id not in admin_ids_list):
        messagebox.showwarning("Validation Error", "Assign an existing Admin!")
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

        department_lawyers_query = """SELECT S.fname, S.lname
                                                FROM Department D, Staff S, Lawyer L
                                                WHERE D.department_id = %s AND L.department_id = D.department_id AND S.id = L.lawyer_id
                                                """

        db_cursor.execute(department_lawyers_query, (details[0],))
        department_lawyers = db_cursor.fetchall()
        department_lawyers = "\n".join([f"{fname} {lname} " for fname, lname in department_lawyers])
        print(department_lawyers)

        department_lawyer_label = customtkinter.CTkLabel(details_window, text=department_lawyers)
        department_lawyer_label.pack(padx=0, pady=5, anchor="w")

# Button to show details
department_details_button = customtkinter.CTkButton(tabview.tab("Departments"), text="Department Lawyers", command=showDepartmentLawyers)
department_details_button.place(relx=1, x=-50, rely=0, y=70, anchor="ne")

#-----------------------------------------------------------------------
# Canvas for the bar chart
def showWinningRate():

    winning_rate_window = customtkinter.CTkToplevel(main_app)
    winning_rate_window.title("Winning Rate Statistics")
    winning_rate_window.geometry("700x550")

    winning_rate_query = """SELECT D.department_id, AVG(L.winning_rate)
                            FROM Department D, Staff S, Lawyer L
                            WHERE D.department_id = L.department_id AND L.lawyer_id = S.id
                            GROUP BY D.department_id
                            """

    db_cursor.execute(winning_rate_query)
    winning_rates = db_cursor.fetchall()

    dep_ids = [i[0] for i in winning_rates]
    average_rates = [i[1] for i in winning_rates]

    fig = plt.figure(figsize = (4, 0.5))
    plt.bar(dep_ids, average_rates, width = 0.4)
    plt.xlabel("Departments")
    plt.ylabel("Average Winning Rates")
    plt.title("Winning Rate Statistics of Departments")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(np.arange(0, 101, 5), fontsize=10)

    canvas = FigureCanvasTkAgg(fig, master=winning_rate_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    def on_close():
        winning_rate_window.destroy()

    winning_rate_window.protocol("WM_DELETE_WINDOW", on_close)

    # Start the event loop for the new pop-up window
    winning_rate_window.mainloop()

winning_rate_button = customtkinter.CTkButton(tabview.tab("Departments"), text="Winning Rate Statistics", command=showWinningRate)
winning_rate_button.place(relx=1, x=-50, rely=0, y=120, anchor="ne")



#Funny little query
"""SELECT DISTINCT L.lawyer_id
FROM Lawyer L
WHERE NOT EXISTS
(
(SELECT R.lawyer_id
FROM Represents R, Lawsuit LWS
WHERE L.lawyer_id = R.lawyer_id
AND R.lawsuit_id = LWS.lawsuit_id
)
EXCEPT
(SELECT R2.lawyer_id
FROM Represents R2, Lawsuit LWS2
WHERE R2.lawsuit_id = LWS2.lawsuit_id
AND LWS2.verdict = "Guilty")
)"""


# Start the ui
loginWindow()
main_app.mainloop()
