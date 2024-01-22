# Imports for ui
import customtkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Import for database
import mysql.connector
import csv
import pandas as pd

#CREATE DATABASE:
db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="z1x?1zKucs",
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
                    PRIMARY KEY (admin_id),
                    FOREIGN KEY (admin_id) REFERENCES Staff(id))""")

insert_administrators = (
    "INSERT INTO Administrator(admin_id) "
    "VALUES (%s)"
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
main_app.geometry("1200x700")

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
label = customtkinter.CTkLabel(master=tabview.tab("Lawyers"), text="Lawyers")
# Basically master=frame or master=tabview.tab("Tab1") is where the components are put into
label.pack(pady=10, padx=10)
# note: Anything with a CTk before it like CTkFrame is from customtkinter library and lets you use .pack(pady=?, padx=?)
# But other things like Treeview is from tkinter library so you have to use .place(x=?, y=?)
# If pack() is hard to use just use place() instead


### An Entry
# Like a TextBox, lets the user enter string inside
entry1 = customtkinter.CTkEntry(master=tabview.tab("Lawyers"), placeholder_text="Enter something here.")
entry1.pack(pady=10, padx=10)

### A Button
# You create a function without any arguments and then use command=function_name to call it with button press
# In this example, the function prints "Button is pressed" to the console
def test():
    print("Button is pressed")

button = customtkinter.CTkButton(master=tabview.tab("Lawyers"), text="Test Button", command=test)
button.pack(pady=10, padx=10)


### A Treeview
#df = pd.read_csv('./data/Lawyer.csv')
#lawyers_columns = list(df.columns)


#db_cursor.execute("SELECT * FROM Lawyer")
#lawyers = db_cursor.fetchall()

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
info = (("Ali","Aman",5),("Fatma","Tekin",7),("Öykü","Dolu",11))
for i in info:
    lawyers_tree.insert("", END, values=i)


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



##### CLIENTS TAB



##### LAWSUITS TAB
lawsuitTitle = customtkinter.CTkLabel(master=tabview.tab("Lawsuits"), text="Lawsuits")
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

showLawsuitDetailsButton = customtkinter.CTkButton(master= tabview.tab("Lawsuits"),text="Show Details")
showLawsuitDetailsButton.place(x=180,y=300)

lawsuitIDEntry = customtkinter.CTkEntry(master=tabview.tab("Lawsuits"), placeholder_text="Lawsuit ID")
lawsuitIDEntry.place(x=880,y=300)

verdictEntry = customtkinter.CTkEntry(master=tabview.tab("Lawsuits"), placeholder_text="Verdict")
verdictEntry.place(x=880,y=330)

courtDateEntry = customtkinter.CTkEntry(master= tabview.tab("Lawsuits"),placeholder_text="Court Date")
courtDateEntry.place(x=880,y=360)

judgeNameEntry = customtkinter.CTkEntry(master= tabview.tab("Lawsuits"),placeholder_text="Judge Name")
judgeNameEntry.place(x=880,y=390)

clientIdEntry = customtkinter.CTkEntry(master= tabview.tab("Lawsuits"),placeholder_text="Client ID")
clientIdEntry.place(x=880,y=420)

def addLawsuitButtonClick():
    lawsuitId = lawsuitIDEntry.get()
    verdict = verdictEntry.get()
    courtDate = courtDateEntry.get()
    judgeName = judgeNameEntry.get()
    clientId = clientIdEntry.get()
    try:
        addLawsuitQuery = """INSERT INTO Lawsuit VALUES ('{0}','{1}','{2}','{3}','{4}')""".format(lawsuitId, verdict, courtDate, judgeName, clientId)
        print(addLawsuitQuery)
        db_cursor.execute(addLawsuitQuery)
        lawsuitTree.insert("",END,values=(lawsuitId, verdict, courtDate, judgeName, clientId))
    except:
        messagebox.showwarning("Format Error!","The input format is wrong.")

addLawsuitButton = customtkinter.CTkButton(master= tabview.tab("Lawsuits"), text="Add Lawsuit",command=addLawsuitButtonClick)
addLawsuitButton.place(x=880,y=480)







##### DEPARTMENTS TAB



# Start the ui
main_app.mainloop()
