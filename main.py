# Imports for ui
import customtkinter
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import scrolledtext
from tkinter import ttk


# Imports for showing details in UI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plts

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
db_cursor.execute("""CREATE TABLE Staff (
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
db_cursor.execute("""CREATE TABLE Administrator (
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
db_cursor.execute("""CREATE TABLE Department (
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
db_cursor.execute("""CREATE TABLE Lawyer (
                    lawyer_id CHAR(6),
                    department_id CHAR(6),
                    winning_rate INT,
                    PRIMARY KEY (lawyer_id),
                    FOREIGN KEY (lawyer_id) REFERENCES Staff(id) ON DELETE CASCADE, 
                    FOREIGN KEY (department_id) REFERENCES Department(department_id))""")
                    
insert_lawyers = (
    "INSERT INTO Lawyer(lawyer_id, department_id, winning_rate) "
    "VALUES (%s, %s, %s)"
)

populate_table(db_connection, db_cursor, insert_lawyers, "./data/Lawyer.csv")


# Create Client table
db_cursor.execute("""CREATE TABLE Client (
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
db_cursor.execute("""CREATE TABLE Lawsuit (
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
db_cursor.execute("""CREATE TABLE Represents (
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
db_cursor.execute("""CREATE TABLE Counsels (
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


# Create Triggers
# Enforce %55 women lawyers
db_cursor.execute("""   CREATE TRIGGER before_delete_staff
                        BEFORE DELETE ON staff
                        FOR EACH ROW
                        BEGIN
                            IF OLD.sex = 'F' THEN
                                SIGNAL SQLSTATE '55000'
                                SET MESSAGE_TEXT = 'Cannot delete women staff from the database';
                            END IF;
                        END; """)

# Enforce %45 men lawyers
db_cursor.execute("""   CREATE TRIGGER before_insert_staff
                        BEFORE INSERT ON staff
                        FOR EACH ROW
                        BEGIN
                            IF NEW.sex = 'M' THEN
                                SIGNAL SQLSTATE '45000'
                                SET MESSAGE_TEXT = 'Cannot add men staff to the database';
                            END IF;
                        END; """)


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
    
    db_cursor.execute("""SELECT admin_id FROM Administrator""")
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

        db_cursor.execute("""SELECT password FROM Administrator WHERE Administrator.admin_id = %s""", (username,))
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
tabs = ["Lawyers", "Clients", "Lawsuits", "Departments", "Counseling Appointments"]
for i in tabs:
    tabview.add(i)
tabview.set("Lawyers") # set as default tab


##### LAWYERS TAB
label = customtkinter.CTkLabel(
    master=tabview.tab("Lawyers"),
    text="LAWYERS",
    font=("Courier", 30, "bold")
)
label.pack(pady=10, padx=10)

### A Treeview
table_columns = ("name","surname","id_no")

#lawyers treeview
lawyers_tree = ttk.Treeview(master=tabview.tab("Lawyers"), columns=table_columns, show="headings", selectmode="browse") # selectmode="browse" means the user can only select one row at a time
lawyers_tree.pack(padx=10, pady=10) # makes ui look good i guess, DO NOT ERASE

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

        try:
            db_cursor.execute("DELETE FROM Staff WHERE id = \"" + str(selectedItemValues[2]) + "\"") 
            db_connection.commit()
        except (mysql.connector.errors.DatabaseError) as e:
            messagebox.showwarning("Database Error", "Cannot delete women staff from database.")
            return

        # also delete from treeview
        lawyers_tree.delete(lawyers_tree.selection())

remove_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Remove Lawyer", command=removeLawyerFromDatabase)
remove_button.place(x=900,y=90)

def sort_lawyers_by_name():
    print("sort lawyers by fname")
    db_cursor.execute("SELECT S.fname, S.lname, S.id FROM  Lawyer L JOIN Staff S ON L.lawyer_id = S.id  ORDER BY fname ASC")
    sorted_lawyer = db_cursor.fetchall()

    #Delete old items
    old_items = lawyers_tree.get_children()
    for item in old_items:
        lawyers_tree.delete(item)

    #Insert sorted items from query
    for i in sorted_lawyer:
        lawyers_tree.insert("", END, values=i)

sorted_lawyer_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Sort by Name", command=sort_lawyers_by_name)
sorted_lawyer_button.place(x=900, y=140)

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
        details_window = customtkinter.CTkToplevel(main_app)
        details_window.geometry("400x200+400+100")
        details_window.title(f"Info for Lawyer ID {lawyer_id}")

        if lawyer_details:
            details_label = Label(details_window, text= f"Lawyer ID:\t\t{lawyer_details[0]}\n"
                                                        f"Department ID:\t{lawyer_details[1]}\n"
                                                        f"Winning Rate:\t{lawyer_details[2]}\n"
                                                        f"First Name:\t\t{lawyer_details[3]}\n"
                                                        f"Last Name:\t\t{lawyer_details[4]}\n"
                                                        f"Sex:\t\t{lawyer_details[5]}\n"
                                                        f"Phone Number:\t{lawyer_details[6]}\n"
                                                        f"Email:\t\t{lawyer_details[7]}\n"
                                                        f"Salary:\t\t{lawyer_details[8]}", justify="left")
            details_label.pack(pady=20, padx=20)
        else:
            no_details_label = Label(details_window, text=f"No info found for Lawyer ID {lawyer_id}")
            no_details_label.pack(pady=20, padx=20)

show_details_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Show Info", command=show_lawyer_info)
show_details_button.place(x=900, y=190)

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
show_details_button.place(x=900, y=240)


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
search_button.place(x=900, y=10)
search_entry = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="Enter lawyer's name")
search_entry.place(x=750, y=10)


def show_best_lawyers():
    best_lawyers_window = Toplevel(main_app)
    best_lawyers_window.title("Firm's Best Lawyers")
    best_lawyers_window.geometry("350x200+400+150")

    best_lawyers_exp = customtkinter.CTkLabel(best_lawyers_window, text= "Lawyers with No Failed Lawsuit", font=("Helvetica", 16, "bold"))
    best_lawyers_exp.pack(padx=30, pady=5, anchor="w")

    db_cursor.execute("""SELECT DISTINCT S.fname, S.lname, COUNT(*)
                        FROM Lawyer L JOIN Staff S ON L.lawyer_id = S.id JOIN Represents R ON L.lawyer_id = R.lawyer_id
                        WHERE NOT EXISTS (
                            SELECT R.lawyer_id
                            FROM Represents R
                            JOIN Lawsuit LWS ON R.lawsuit_id = LWS.lawsuit_id
                            WHERE L.lawyer_id = R.lawyer_id
                            AND LWS.verdict = 'Guilty'
                            )
                        GROUP BY S.fname, S.lname
                        """)

    successful_lawyers = db_cursor.fetchall()
    successful_lawyers_txt = "\n".join([f"{fname} {lname}\t- Lawsuit Number: {lawsuit} " for fname, lname, lawsuit in successful_lawyers])
    print(successful_lawyers_txt)

    successful_lawyers_label = customtkinter.CTkLabel(best_lawyers_window, text=successful_lawyers_txt, anchor="w")
    successful_lawyers_label.pack(padx=10, pady=5, anchor="w")


    

    print()

show_best_lawyers_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Best Lawyers", command=show_best_lawyers,width=160)
show_best_lawyers_button.place(x=10, y=100)

#CLIENT Lawyers ACCORDING TO THE Salary
def salary_greater():
    salary = filter_salary_input.get()

    salary_filter_window = customtkinter.CTkToplevel(main_app)
    salary_filter_window.title("Lawyers' Salaries")
    salary_filter_window.geometry("450x250+400+150")
        
    #Department Lawyers Title
    header_label = customtkinter.CTkLabel(salary_filter_window, text= "Lawyers with Salaries Greater Than " + salary, font=("Courier", 16, "bold"))
    header_label.pack(padx=10, pady=5, anchor="w")

    #Salary filter query
    db_cursor.execute("""SELECT CONCAT(S.fname, " ", S.lname), S.salary
                        FROM Lawyer L JOIN Staff S ON L.lawyer_id = S.id
                        WHERE S.salary > %s 
                        """, (salary, ))


    salary_and_lawyers = db_cursor.fetchall()
    salary_and_lawyers_txt = "\n".join([f"{name}: {salary} " for name, salary in salary_and_lawyers])

    scrolled_text = scrolledtext.ScrolledText(salary_filter_window, wrap=tkinter.WORD, width=60, height=10, font=("Courier", 12))
    scrolled_text.pack(padx=15, pady=5, anchor="w")
    scrolled_text.insert(tkinter.END, salary_and_lawyers_txt)
    scrolled_text.configure(state="disabled")

    db_cursor.execute("""SELECT COUNT(*)
                        FROM Lawyer L JOIN Staff S ON L.lawyer_id = S.id
                        WHERE S.salary > %s 
                        """, (salary, ))

    lawyer_count = db_cursor.fetchall()

    lawyer_count_label = customtkinter.CTkLabel(salary_filter_window, text= "Lawyers Count: " + str(lawyer_count[0][0]), font=("Courier", 14, "bold"))
    lawyer_count_label.pack(padx=10, pady=5, anchor="w")



def salary_less():
    salary = filter_salary_input.get()

    salary_filter_window = customtkinter.CTkToplevel(main_app)
    salary_filter_window.title("Lawyers Salaries")
    salary_filter_window.geometry("450x250+400+150")
        
    #Department Lawyers Title
    header_label = customtkinter.CTkLabel(salary_filter_window, text= "Lawyers with Salaries Less Than " + salary, font=("Courier", 16, "bold"))
    header_label.pack(padx=10, pady=5, anchor="w")

    #Salary filter query
    db_cursor.execute("""SELECT CONCAT(S.fname, " ", S.lname), S.salary
                        FROM Lawyer L JOIN Staff S ON L.lawyer_id = S.id
                        WHERE S.salary < %s 
                        """, (salary, ))


    salary_and_lawyers = db_cursor.fetchall()
    salary_and_lawyers_txt = "\n".join([f"{name}: {salary} " for name, salary in salary_and_lawyers])

    scrolled_text = scrolledtext.ScrolledText(salary_filter_window, wrap=tkinter.WORD, width=60, height=10, font=("Courier", 12))
    scrolled_text.pack(padx=15, pady=5, anchor="w")
    scrolled_text.insert(tkinter.END, salary_and_lawyers_txt)
    scrolled_text.configure(state="disabled")


    db_cursor.execute("""SELECT COUNT(*)
                        FROM Lawyer L JOIN Staff S ON L.lawyer_id = S.id
                        WHERE S.salary < %s 
                        """, (salary, ))

    lawyer_count = db_cursor.fetchall()

    lawyer_count_label = customtkinter.CTkLabel(salary_filter_window, text= "Lawyers Count: " + str(lawyer_count[0][0]), font=("Courier", 14, "bold"))
    lawyer_count_label.pack(padx=10, pady=5, anchor="w")


filter_lawyer_salary_label = customtkinter.CTkLabel(tabview.tab("Lawyers"), text="Show Lawyers Salary", font=("Courier", 20, "bold"))
filter_lawyer_salary_label.place(x = 10, y = 160)

filter_salary_input = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="Enter Salary", width = 200)
filter_salary_input.place(x=10, y=190)

salary_greater_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"),text='Greater Than',command=salary_greater) 
salary_greater_button.place(x= 10, y = 230)

salary_less_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"),text='Less Than',command=salary_less) 
salary_less_button.place(x= 10, y = 265)



##### yeni eklediğimi silemiyorum ? ##########

def addLawyer():
    lawyer_id = lawyer_id_input.get()
    lawyer_fname = lawyer_fname_input.get()
    lawyer_lname = lawyer_lname_input.get()
    lawyer_sex = lawyer_sex_input.get()
    lawyer_salary = lawyer_salary_input.get()
    lawyer_phone = lawyer_phone_input.get()
    lawyer_email = lawyer_email_input.get()
    lawyer_winning_rate = lawyer_winning_rate_input.get()
    lawyer_department = lawyer_department_combobox.get()

    if not (all([lawyer_id, lawyer_fname, lawyer_lname, lawyer_sex, lawyer_salary, lawyer_phone, lawyer_email, lawyer_winning_rate, lawyer_department])
            and bool(re.match(r'^DEP\d{3}$', lawyer_department))):
        messagebox.showwarning("Validation Error", "Please fill in all the fields.")
        return

    if not (bool(re.match(r'^LAW\d{3}$', lawyer_id))):
        messagebox.showwarning("Validation Error", "Invalid Lawyer ID format.")
        return

    if not (bool(re.match(r'^(F|M)$', lawyer_sex))):
        messagebox.showwarning("Validation Error", "Invalid Lawyer Sex format.")
        return

    if not (bool(re.match(r'^\d+$', lawyer_salary))):
        messagebox.showwarning("Validation Error", "Invalid Lawyer Salary format.")
        return

    if not (bool(re.match(r'^\d+$', lawyer_winning_rate))):
        messagebox.showwarning("Validation Error", "Invalid Lawyer Winning Rate format.")
        return
    
    if not (bool(re.match(r'^\d{10}$', lawyer_phone))):
        messagebox.showwarning("Validation Error", "Invalid Lawyer Phone Number format.")
        return

    if not (bool(re.match(r'^.+@email\.com$', lawyer_email))):
        messagebox.showwarning("Validation Error", "Invalid Lawyer Email format.")
        return


    
    lawyer_id_query = db_cursor.execute("""SELECT lawyer_id FROM Lawyer""")
    lawyer_ids = db_cursor.fetchall() 
    lawyer_ids_list = [i[0] for i in lawyer_ids]

    if (lawyer_id in lawyer_ids_list):
        messagebox.showwarning("Validation Error", "Lawyer ID already exists in Lawyer table.")
        return

    try:
        db_cursor.execute("INSERT INTO Staff(id,fname,lname,sex,phone_number,email,salary) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                      (lawyer_id, lawyer_fname, lawyer_lname, lawyer_sex, lawyer_phone, lawyer_email, lawyer_salary))
        db_connection.commit()

        db_cursor.execute("INSERT INTO Lawyer(lawyer_id,department_id,winning_rate) VALUES (%s, %s, %s)",
                      (lawyer_id, lawyer_department, lawyer_winning_rate))
        db_connection.commit()
    except (mysql.connector.errors.IntegrityError) as e1:
        messagebox.showwarning("Integrity Error",  str(e1.msg))
        return
    except (mysql.connector.errors.DatabaseError) as e2:
        messagebox.showwarning("Database Error", "Cannot add men staff to database.")
        return

    lawyers_tree.insert("", END, values=(lawyer_fname, lawyer_lname, lawyer_id))

    # Clear the entry widgets
    lawyer_id_input.delete(0, END)
    lawyer_fname_input.delete(0, END)
    lawyer_lname_input.delete(0, END)
    lawyer_sex_input.delete(0, END)
    lawyer_salary_input.delete(0, END)
    lawyer_phone_input.delete(0, END)
    lawyer_email_input.delete(0, END)
    lawyer_winning_rate_input.delete(0, END)

# Entry widgets for adding a new lawyer
lawyer_id_input = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="LAWXXX", width=100)
lawyer_id_input.place(x=270, y=330)
lawyer_id_label = customtkinter.CTkLabel(master=tabview.tab("Lawyers"), text="Lawyer ID:").place(x=270, y=300)

# Label and Entry for First Name
lawyer_fname_input = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="", width=100)
lawyer_fname_input.place(x=420, y=330)
lawyer_fname_label = customtkinter.CTkLabel(master=tabview.tab("Lawyers"), text="Name:").place(x=420, y=300)

# Label and Entry for Last Name
lawyer_lname_input = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="", width=100)
lawyer_lname_input.place(x=570, y=330)
lawyer_lname_label = customtkinter.CTkLabel(master=tabview.tab("Lawyers"), text="Surname:").place(x=570, y=300)

# Label and Entry for Sex
lawyer_sex_input = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="F or M", width=100)
lawyer_sex_input.place(x=720, y=330)
lawyer_sex_label = customtkinter.CTkLabel(master=tabview.tab("Lawyers"), text="Sex:").place(x=720, y=300)

# Label and Entry for Age
lawyer_salary_input = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="0", width=100)
lawyer_salary_input.place(x=870, y=330)
lawyer_salary_label = customtkinter.CTkLabel(master=tabview.tab("Lawyers"), text="Salary:").place(x=870, y=300)

# Label and Entry for Phone Number
lawyer_phone_input = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="xxxxxxxxxxx", width=100)
lawyer_phone_input.place(x=270, y=410)
lawyer_phone_label = customtkinter.CTkLabel(master=tabview.tab("Lawyers"), text="Phone Number:").place(x=270, y=380)

# Label and Entry for Email
lawyer_email_input = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="_@email.com", width=100)
lawyer_email_input.place(x=420, y=410)
lawyer_email_label = customtkinter.CTkLabel(master=tabview.tab("Lawyers"), text="Email:").place(x=420, y=380)

# Winning rate
lawyer_winning_rate_input = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="0", width=100)
lawyer_winning_rate_input.place(x=570, y=410)
lawyer_winning_rate_label = customtkinter.CTkLabel(master=tabview.tab("Lawyers"), text="Winning Rate:").place(x=570, y=380)

# Add Lawyer button
insert_lawyer_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Add Lawyer", width=100, command=addLawyer)
insert_lawyer_button.place(x=570, y=470)

# Department combobox
db_cursor.execute("SELECT department_id FROM Department")
department_ids = db_cursor.fetchall()
department_ids_list = [id[0] for id in department_ids]

lawyer_department_label = customtkinter.CTkLabel(master=tabview.tab("Lawyers"), text="Department:").place(x=720, y=380)
lawyer_department_combobox = ttk.Combobox(master=tabview.tab("Lawyers"), values=department_ids_list, state="readonly")
lawyer_department_combobox.place(x=720, y=410)
lawyer_department_combobox.set("Department ID")

insert_lawyer_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Add Lawyer", width=100, command=addLawyer).place(x=570, y=470)



def get_clients_status_by_lawyer():

    clients_status_window = customtkinter.CTkToplevel(main_app)
    clients_status_window.title("Client States by Lawyer Statistics")
    clients_status_window.geometry("1000x600")

    db_cursor.execute("""
        SELECT L.lawyer_id,
               SUM(C.state = 'Accused') AS accused_clients,
               SUM(C.state = 'Suspect') AS suspect_clients,
               SUM(C.state = 'Defendant') AS defendant_clients
        FROM Lawyer L
        LEFT JOIN Counsels CL ON L.lawyer_id = CL.lawyer_id
        LEFT JOIN Client C ON CL.client_id = C.client_id
        GROUP BY L.lawyer_id
        ORDER BY L.lawyer_id
    """)

    clients_status = db_cursor.fetchall()

    lawyer_ids = [row[0] for row in clients_status]
    accused_clients = [row[1] for row in clients_status]
    suspect_clients = [row[2] for row in clients_status]
    defendant_clients = [row[3] for row in clients_status]

    # Create a bar chart
    fig = plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(lawyer_ids))

    plt.bar(index, accused_clients, bar_width, label='Accused Clients', color='green')
    plt.bar(index, suspect_clients, bar_width, label='Suspect Clients', color='red', bottom=accused_clients)
    plt.bar(index, defendant_clients, bar_width, label='Defendant Clients', color='blue', bottom=suspect_clients)
    
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Lawyer ID')
    plt.ylabel('Number of Clients')
    plt.title('Client States by Lawyer')
    plt.xticks([i for i in index], lawyer_ids)
    plt.legend()
    plt.ylim(0)  

    #plt.show()

    canvas = FigureCanvasTkAgg(fig, master=clients_status_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    def on_close():
        clients_status_window.destroy()

    clients_status_window.protocol("WM_DELETE_WINDOW", on_close)

    # Start the event loop for the new pop-up window
    clients_status_window.mainloop()

get_clients_status_by_lawyer_button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Client States by Lawyer", command=get_clients_status_by_lawyer, width=160)
get_clients_status_by_lawyer_button.place(x=10, y=60) #.place(x=900, y=50)




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
    client_tree.delete(*client_tree.get_children())

    #Insert sorted items from query
    for i in sorted_clients:
        client_tree.insert("", '0', values=i)

sort_clients_by_name_button = customtkinter.CTkButton(master=tabview.tab("Clients"), text="Sort by Name", command=sortClientsByName).place(x=950, y=450)

def sortClientsByState():
    print("sort clients by state")
    db_cursor.execute("SELECT * FROM Client ORDER BY state ASC")
    sorted_clients = db_cursor.fetchall()

    #Delete old items
    client_tree.delete(*client_tree.get_children())

    #Insert sorted items from query
    for i in sorted_clients:
        client_tree.insert("", END, values=i)

sort_clients_by_state_button = customtkinter.CTkButton(master=tabview.tab("Clients"), text="Sort by State", command=sortClientsByState).place(x=950, y=500)

search_client_entry = customtkinter.CTkEntry(master=tabview.tab("Clients"), placeholder_text="Enter client name")
search_client_entry.place(x=750, y=10)

def searchClientByName():
    searched_name = search_client_entry.get().strip().lower()
    print(searched_name)
    client_tree.delete(*client_tree.get_children())

    db_cursor.execute("SELECT * FROM Client WHERE LOWER(CONCAT(' ', fname, lname)) LIKE \"%" + searched_name + "%\"")
    searched_clients = db_cursor.fetchall()

    for i in searched_clients:
        client_tree.insert("", END, values=i)
    
    search_client_entry.delete(0, END)

search_client_button = customtkinter.CTkButton(master=tabview.tab("Clients"), text="Search Client", command=searchClientByName).place(x=900, y=10)


##### LAWSUITS TAB

lawsuitTitle = customtkinter.CTkLabel(master=tabview.tab("Lawsuits"), text="LAWSUITS",font=("Courier", 30, "bold"))
lawsuitTitle.pack(padx=10,pady=10)
lawsuitColumns = ["lawsuit_id","verdict","court_date","judge_name","client_id"]
lawsuitTree = ttk.Treeview(master=tabview.tab("Lawsuits"), columns=lawsuitColumns, show="headings", selectmode="browse")
lawsuitTree.pack(padx=10, pady=10)
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
    selectedLawsuit = lawsuitTree.selection()
    if selectedLawsuit:
        lawsuitAttributes = lawsuitTree.item(selectedLawsuit, 'values')
        clientDetailsWindow = customtkinter.CTkToplevel(main_app)
        clientDetailsWindow.title("Client Details")
        clientDetailsWindow.geometry("400x150+400+150")

        # Department Lawyers Title
        header = customtkinter.CTkLabel(clientDetailsWindow, text=lawsuitAttributes[0]+ " Client Details",font=("Helvetica", 16, "bold"))
        header.pack(padx=10, pady=10, anchor="w")

        clientDetailsQuery = """SELECT C.fname, C.lname, C.sex, C.age, C.email
                                FROM Client C WHERE C.client_id = '{}'""".format(lawsuitAttributes[4])

        db_cursor.execute(clientDetailsQuery)
        clientDetailsList = db_cursor.fetchall()
        clientDetails = "\n".join([f"{fname} {lname} {sex} {age} {email} " for fname, lname, sex, age, email in clientDetailsList])
        department_lawyer_label = customtkinter.CTkLabel(clientDetailsWindow, text=clientDetails)
        department_lawyer_label.pack(padx=10, pady=10, anchor="w")

    return





showLawsuitDetailsButton = customtkinter.CTkButton(master= tabview.tab("Lawsuits"),text="Show Client Details",command=showLawsuitDetails)
showLawsuitDetailsButton.place(x=120,y=300)

def removeLawsuit():
    selectedLawsuit = lawsuitTree.selection()
    if selectedLawsuit:
        selectedLawsuitList = lawsuitTree.item(lawsuitTree.focus(), "values")
        removeLawsuitQuery = """DELETE FROM Lawsuit WHERE lawsuit_id = '{0}'""".format(selectedLawsuitList[0])
        db_cursor.execute(removeLawsuitQuery)
        db_connection.commit()
        lawsuitTree.delete(lawsuitTree.selection())
        return
removeLawsuitButton = customtkinter.CTkButton(master= tabview.tab("Lawsuits"),text="Remove Lawsuit",command=removeLawsuit)
removeLawsuitButton.place(x=350,y=300)

def verdictStatisticsCommand():

    verdictStaticsQuery = """SELECT L.verdict, COUNT(*)
           FROM Lawsuit L, Client C
           WHERE L.client_id = C.client_id""" + \
           (""" AND C.sex = '{}'""".format(clientGenderComboBox.get()[0]) if clientGenderComboBox.get() != "No Choice" else "") + \
           (""" AND L.court_date > '{}'""".format(fromDateEntry.get()) if fromDateEntry.get() != "" else "") + \
           (""" AND L.judge_name LIKE '{}'""".format(whichJudgeComboBox.get()) if whichJudgeComboBox.get() != "No Choice" else "") + \
           """ GROUP BY L.verdict ORDER BY COUNT(*) ASC"""
    print(verdictStaticsQuery)
    db_cursor.execute(verdictStaticsQuery)
    verdictCountList = db_cursor.fetchall()
    verdicts = [i[0] for i in verdictCountList]
    lawsuitSums = [i[1] for i in verdictCountList]

    fig, ax = plt.subplots()
    ax.pie(lawsuitSums, labels=verdicts, colors=["#B0DAFF", "#19A7CE", "#146C94"], autopct='%.2f%%', startangle=90)
    plt.title("Verdict Statistics")
    ax.axis('equal')


    verdictStatisticsWindow = customtkinter.CTkToplevel(main_app)
    verdictStatisticsWindow.title("Verdict Statistics")
    verdictStatisticsWindow.geometry("700x550+300+50")

    canvas = FigureCanvasTkAgg(fig, master=verdictStatisticsWindow)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    def on_close():
        verdictStatisticsWindow.destroy()

    verdictStatisticsWindow.protocol("WM_DELETE_WINDOW", on_close)
    verdictStatisticsWindow.mainloop()

    return

clientGenderComboBox = customtkinter.CTkComboBox(master=tabview.tab("Lawsuits"),values=("No Choice","Male","Female"),state="readonly")
clientGenderComboBox.set("No Choice")
clientGenderLabel = customtkinter.CTkLabel(master=tabview.tab("Lawsuits"),text="Gender:")
fromDateEntry = customtkinter.CTkEntry(master=tabview.tab("Lawsuits"),placeholder_text="YYYY-MM-DD")
fromDateLabel = customtkinter.CTkLabel(master=tabview.tab("Lawsuits"),text="From Which Date:")
db_cursor.execute("SELECT DISTINCT judge_name FROM Lawsuit")
JudgeListDB = db_cursor.fetchall()

JudgeList = []
for jname in JudgeListDB:
    JudgeList.append(jname[0])
JudgeList.insert(0,"No Choice")
whichJudgeComboBox = customtkinter.CTkComboBox(master=tabview.tab("Lawsuits"),values=JudgeList,state="readonly")
whichJudgeComboBox.set("No Choice")
whichJudgeLabel = customtkinter.CTkLabel(master=tabview.tab("Lawsuits"),text="Sort By Judge:")
verdictStatisticsButton = customtkinter.CTkButton(master= tabview.tab("Lawsuits"),text="Verdict Statistics",command=verdictStatisticsCommand)


clientGenderComboBox.place(x=160,y=400)
clientGenderLabel.place(x=20,y=400)
fromDateEntry.place(x=160,y=430)
fromDateLabel.place(x=20,y=430)
whichJudgeComboBox.place(x=160,y=460)
whichJudgeLabel.place(x=20,y=460)
verdictStatisticsButton.place(x=350,y=430)

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

    lawsuitIdQuery = """SELECT lawsuit_id FROM Lawsuit"""
    db_cursor.execute(lawsuitIdQuery)
    lawsuitIds = db_cursor.fetchall()
    lawsuitIdList = [i[0] for i in lawsuitIds]
    if (lawsuitId in lawsuitIdList):
        messagebox.showwarning("Validation Error","Lawsuit ID already exists in Lawsuit table.")
        return

    addLawsuitQuery = """INSERT INTO Lawsuit VALUES ('{0}','{1}','{2}','{3}','{4}')""".format(lawsuitId, verdict, courtDate, judgeName, clientId)
    db_cursor.execute(addLawsuitQuery)
    db_connection.commit()
    lawsuitTree.insert("",END,values=(lawsuitId, verdict, courtDate, judgeName, clientId))


    lawsuitIDEntry.delete(0,END)
    verdictEntry.delete(0,END)
    courtDateEntry.delete(0,END)
    judgeNameEntry.delete(0,END)
    clientIdEntry.delete(0,END)

addLawsuitButton = customtkinter.CTkButton(master= tabview.tab("Lawsuits"), text="Add Lawsuit",command=addLawsuitButtonClick)
addLawsuitButton.place(x=880,y=480)

def filter_lawsuits_verdict(event):
    selected_verdict = lawsuit_combobox.get()
    lawsuitTree.delete(*lawsuitTree.get_children())

    all_lawsuits = db_cursor.execute("""SELECT * FROM Lawsuit""")
    all_lawsuits = db_cursor.fetchall()

    if (selected_verdict == "All"):
        for lawsuit in all_lawsuits:
            lawsuitTree.insert("", END, values=lawsuit)        

    filter_verdict = db_cursor.execute("""SELECT *
                                                 FROM Lawsuit L
                                                 WHERE verdict = %s
                                                """, (selected_verdict,))


    filter_verdict_list = db_cursor.fetchall()
    for lawsuit in filter_verdict_list:
        lawsuitTree.insert("", END, values=lawsuit)

lawsuits_list = ["All","Guilty","Free"]
lawsuit_combobox = ttk.Combobox(master=tabview.tab("Lawsuits"), values=lawsuits_list, state="readonly", width = 30)
lawsuit_combobox.set("Verdict")
lawsuit_combobox.place(x=700, y=20)
lawsuit_combobox.bind("<<ComboboxSelected>>", filter_lawsuits_verdict)

                                            


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
department_tree.pack(padx=10, pady=10)

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
dep_id_label = customtkinter.CTkLabel(tabview.tab("Departments"), text="Department ID:", font=("Courier", 20, "bold"))
dep_name_label = customtkinter.CTkLabel(tabview.tab("Departments"), text="Department Name:", font=("Courier", 20, "bold"))
admin_id_label = customtkinter.CTkLabel(tabview.tab("Departments"), text="Admin ID:", font=("Courier", 20, "bold"))

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
        details_window.geometry("350x200+400+150")
        
        #Department Lawyers Title
        header_label = customtkinter.CTkLabel(details_window, text=details[1] + " Department Lawyers", font=("Helvetica", 16, "bold"))
        header_label.pack(padx=10, pady=5, anchor="w")

        department_lawyers_query = """SELECT S.fname, S.lname
                                                FROM Department D, Staff S, Lawyer L
                                                WHERE D.department_id = %s AND L.department_id = D.department_id AND S.id = L.lawyer_id
                                                """

        db_cursor.execute(department_lawyers_query, (details[0],))
        department_lawyers = db_cursor.fetchall()
        department_lawyers = "\n".join([f"   {fname} {lname} " for fname, lname in department_lawyers])
        print(department_lawyers)

        department_lawyer_label = Label(details_window, text=department_lawyers,  justify="left")
        department_lawyer_label.pack(padx=10, pady=5, anchor="w")

# Button to show details
department_details_button = customtkinter.CTkButton(tabview.tab("Departments"), text="Department Lawyers", command=showDepartmentLawyers, width=160)
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

winning_rate_button = customtkinter.CTkButton(tabview.tab("Departments"), text="Winning Rate Statistics", command=showWinningRate, width=160)
winning_rate_button.place(relx=1, x=-50, rely=0, y=120, anchor="ne")

def bestDepartment():
    best_department_window = customtkinter.CTkToplevel(main_app)
    best_department_window.title("Firm's Best Department")
    best_department_window.geometry("400x150+400+150")

    best_department_exp = customtkinter.CTkLabel(best_department_window, text= "Department with Most Cases Won", font=("Helvetica", 16, "bold"))
    best_department_exp.pack(padx=70, pady=5, anchor="w")

    db_cursor.execute("""SELECT d.department_id, d.department_name, COUNT(l.lawyer_id) as cases_won
                        FROM Department d
                        JOIN Lawyer l ON d.department_id = l.department_id
                        JOIN Represents r ON l.lawyer_id = r.lawyer_id
                        JOIN Lawsuit ls ON r.lawsuit_id = ls.lawsuit_id
                        WHERE ls.verdict = 'Free'
                        GROUP BY d.department_id, d.department_name
                        ORDER BY cases_won DESC
                        LIMIT 1
                        """)

    best_department = db_cursor.fetchall()
    best_department_txt = "".join([f"{department_id}: {department_name} Department has won {cases_won} cases." for department_id, department_name, cases_won in best_department])
    print(best_department_txt)

    best_department_label = customtkinter.CTkLabel(best_department_window, text=best_department_txt)
    best_department_label.pack(padx=10, pady=5, anchor="w")

best_department_button = customtkinter.CTkButton(tabview.tab("Departments"), text="Best Department", command=bestDepartment, width=160)
best_department_button.place(relx=1, x=-50, rely=0, y=170, anchor="ne")

# ****** COUNSELING APPOINTMENTS TAB ***************
counseling_label = customtkinter.CTkLabel(
    master=tabview.tab("Counseling Appointments"),
    text="COUNSELING APPOINTMENTS",
    font=("Courier", 30, "bold")
)
counseling_label.pack(pady=10, padx=10) 

### A Treeview
counseling_table_columns = ("lawyer_id", "lawyer_name", "client_id", "client_name", "fee", "date")

#lawyers treeview
counseling_tree = ttk.Treeview(master=tabview.tab("Counseling Appointments"), columns=counseling_table_columns, show="headings", selectmode="browse") # selectmode="browse" means the user can only select one row at a time
counseling_tree.pack(padx=10, pady=10) # makes ui look good i guess, DO NOT ERASE

# this is used to make the heading names look better
counseling_tree.heading("lawyer_id",text="Lawyer ID")
counseling_tree.heading("lawyer_name",text="Lawyer Name")
counseling_tree.heading("client_id",text="Client ID")
counseling_tree.heading("client_name",text="Client Name")
counseling_tree.heading("fee",text="Fee")
counseling_tree.heading("date",text="Date")

counseling_tree.column(column=0, width = 100, stretch = False)
counseling_tree.column(column=2, width = 100, stretch = False)
counseling_tree.column(column=4, width = 100, stretch = False)



# data from the Lawyer and Staff tables 
db_cursor.execute("""
    SELECT C.lawyer_id, CONCAT(S.fname, " ", S.lname), C.client_id, CONCAT(CL.fname, " ", CL.lname), C.fee, C.date
    FROM Counsels C JOIN Staff S ON C.lawyer_id = S.id JOIN Client CL ON C.client_id = CL.client_id
""")
counseling_data = db_cursor.fetchall()

for counseling in counseling_data:
    counseling_tree.insert("", END, values=counseling)


#Client Total Fee Calculation
client_fee_label = customtkinter.CTkLabel(tabview.tab("Counseling Appointments"), text="Client Total Fee", font=("Courier", 20, "bold"))
client_fee_label.place(x = 130, y = 300)

client_name_search = customtkinter.CTkEntry(master=tabview.tab("Counseling Appointments"), placeholder_text="Client Name", width = 150)
client_name_search.place(x=130, y=330)

db_cursor.execute("""SELECT DISTINCT CONCAT(CL.fname, " ", CL.lname) 
                    FROM Client CL, Counsels CO
                    WHERE CL.client_id = CO.client_id
                    """)

all_clients = db_cursor.fetchall()
client_names_list = [client[0] for client in all_clients]

#Dropdown Client box
client_fee_combobox = ttk.Combobox(tabview.tab("Counseling Appointments"), values=client_names_list, state="readonly", width = 20)
client_fee_combobox.set("Client")
client_fee_combobox.place(x=130, y=365)

#Client search button for filtering clients
def client_name_search_func():
    requested_client_name = client_name_search.get()
    db_cursor.execute("""SELECT DISTINCT CONCAT(CL.fname, " ", CL.lname) 
                        FROM Client CL JOIN Counsels CO on CL.client_id = CO.client_id
                        WHERE CONCAT(CL.fname, " ", CL.lname) LIKE %s""", ('%' + requested_client_name + '%',))

    filtered_client_names = db_cursor.fetchall()
    filtered_clients_list = [client[0] for client in filtered_client_names]
    client_fee_combobox['values'] = filtered_clients_list


client_search_button = customtkinter.CTkButton(master=tabview.tab("Counseling Appointments"),text='Search',command=client_name_search_func) 
client_search_button.place(x= 290, y = 330)


#Total Fee Calculation
def calculate_total_fee():
    selected_client_name = client_fee_combobox.get()
    db_cursor.execute("""SELECT SUM(CO.fee)
                         FROM Client CL JOIN Counsels CO on CL.client_id = CO.client_id
                         WHERE CONCAT(CL.fname, " ", CL.lname) = %s
                         GROUP BY CO.client_id
                         """, (selected_client_name,)
                         )
    fee = db_cursor.fetchall()
    print(fee)
    fee = fee[0][0]
    calculated_fee_label.configure(text="Total Fee: " + str(fee))
                

fee_calculate_button = customtkinter.CTkButton(master=tabview.tab("Counseling Appointments"),text='Calculate Fee',command=calculate_total_fee) 
fee_calculate_button.place(x= 130, y = 395)

style = ttk.Style()
style.configure("Red.TLabel", foreground="red")
calculated_fee_label = ttk.Label(tabview.tab("Counseling Appointments"), text="TOTAL FEE", font=("Courier", 16, "bold"), style="Red.TLabel")
calculated_fee_label.place(x = 135, y = 430)


# INSERT COUNSELING APPOINTMENT
insert_appointment_label = customtkinter.CTkLabel(tabview.tab("Counseling Appointments"), text="Insert Appointment", font=("Courier", 20, "bold"))
insert_appointment_label.place(x = 520, y = 300)

#lawyer ids
db_cursor.execute("""SELECT lawyer_id FROM Lawyer ORDER BY lawyer_id ASC""")
lawyer_ids = db_cursor.fetchall()
lawyer_id_list = [id[0] for id in lawyer_ids]


#client ids
db_cursor.execute("""SELECT client_id FROM Client""")
client_ids = db_cursor.fetchall()
client_id_list = [id[0] for id in client_ids]

#lawyer id dropdown list
lawyer_id_combobox = ttk.Combobox(tabview.tab("Counseling Appointments"), values=lawyer_id_list, state="readonly", width = 30)
lawyer_id_combobox.set("Lawyer ID")
lawyer_id_combobox.place(x=520, y=330)

#client id drop
client_id_combobox = ttk.Combobox(tabview.tab("Counseling Appointments"), values=client_id_list, state="readonly", width = 30)
client_id_combobox.set("Client ID")
client_id_combobox.place(x=520, y=360)

#client fee input
client_fee_input = customtkinter.CTkEntry(master=tabview.tab("Counseling Appointments"), placeholder_text="Fee", width = 250)
client_fee_input.place(x=520, y=390)

#appointment date input
appointment_date_input = customtkinter.CTkEntry(master=tabview.tab("Counseling Appointments"), placeholder_text="yyyy-mm-dd", width = 250)
appointment_date_input.place(x=520, y=425)

def insert_appointment():
    lawyer_id = lawyer_id_combobox.get()
    client_id = client_id_combobox.get()
    client_fee = client_fee_input.get()
    appointment_date = appointment_date_input.get()

    if not all([lawyer_id, client_id, client_fee, appointment_date]):
        messagebox.showwarning("Validation Error", "Please fill in all the fields.")
        return

    if not client_fee.isdigit():
        messagebox.showwarning("Validation Error", "Client fee should be digit.")
        return

    date_pattern = re.compile(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$')
    if not date_pattern.match(appointment_date):
        messagebox.showwarning("Validation Error", "Appointment date is not valid.")
        return
    
    db_cursor.execute("""SELECT CONCAT(S.fname, " ", S.lname) 
                            FROM Lawyer L JOIN Staff S ON L.lawyer_id = S.id
                            WHERE lawyer_id = %s""", (lawyer_id,))
    lawyer_name = db_cursor.fetchall()
    lawyer_name = lawyer_name[0][0]

    db_cursor.execute("""SELECT CONCAT(fname, " ", lname) FROM Client WHERE client_id = %s""", (client_id,))
    client_name = db_cursor.fetchall()
    client_name = client_name[0][0]

    counseling_tree.insert("", '0', values=(lawyer_id, lawyer_name, client_id, client_name, client_fee, appointment_date))
    db_cursor.execute("INSERT INTO Counsels (lawyer_id, client_id, fee, date) VALUES (%s, %s, %s, %s)",
                      (lawyer_id, client_id, client_fee, appointment_date))
    db_connection.commit()

    lawyer_id_combobox.set("Lawyer ID")
    client_id_combobox.set("Client ID")
    client_fee_input.delete(0, END)
    appointment_date_input.delete(0, END)


insert_appointment_button = customtkinter.CTkButton(master=tabview.tab("Counseling Appointments"),text='Add Appointment',command=insert_appointment) 
insert_appointment_button.place(x= 520, y = 460)

#Remove appointment
def removeAppointment():
    if counseling_tree.selection() != None: # this is the row selected by user
        selectedItemValues = counseling_tree.item(counseling_tree.focus()).get('values')

        db_cursor.execute("DELETE FROM Counsels WHERE lawyer_id = %s AND client_id = %s", (selectedItemValues[0], selectedItemValues[2], ))
        db_connection.commit()

        # also delete from treeview
        counseling_tree.delete(counseling_tree.selection())


remove_appointment_button = customtkinter.CTkButton(master=tabview.tab("Counseling Appointments"), text="Remove", command=removeAppointment)
remove_appointment_button.place(x=880,y=280)


# Start the ui
loginWindow()
main_app.mainloop()
