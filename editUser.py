import datetime
import locale
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import showinfo, showwarning, showerror
import uuid
import hashlib
import sqlite3
from sqlite3 import Error
from sqlite3 import Cursor
import sys


def buildFrame () :
    
    global name_input, pass_input, ssn_input, tkvar
    
    root = Tk()
    root.geometry("800x600")
    
    frame1 = Frame(root)
    frame1.pack()
    
    root.resizable(False, False)
    root.title("POS - Edit Employee")
    
    bg_img = PhotoImage(file="./img/regbg.png")

    lbl1 = Label(root, image=bg_img)
    lbl1.image = bg_img
    lbl1.place(x=0, y=0, relwidth=1, relheight=1)   

    
    img = PhotoImage(file="./img/logo.png")

    
    lbl = Label(root, image=img)
    lbl.image = img
    lbl.pack(fill = X, pady=10);
    
    lbl = Label(root, text = "Please Edit the details below: ", font=("Helvetica", 26))
    lbl.pack(fill = X, pady = 10);
    frame2 = Frame(root)
    frame2.pack(fill = Y, expand=FALSE, padx=20, pady=10)
    
        #username label
    user_search = Label(frame2, text="Search Name:", font=("Helvetica", 24))
    fullname_label.grid(row=1, column=0, sticky=W, padx = 20)
    
    #username label
    fullname_label = Label(frame2, text="Full Name:", font=("Helvetica", 24))
    fullname_label.grid(row=1, column=0, sticky=W, padx = 20)
    
    #password label
    password_label = Label(frame2, text="Password:", font=("Helvetica", 24))
    password_label.grid(row=2, column=0, sticky=W, padx = 20)
    
    rights_label = Label(frame2, text="Employee Type:", font=("Helvetica", 24))
    rights_label.grid(row=3, column=0, sticky=W, padx = 20)
    
    #input for username
    name_input = StringVar()
    
    fullname_entry = Entry(frame2, textvariable=name_input, font="Helvetica 20")
    fullname_entry.grid(row=1, column=1, sticky=W, padx = 10, ipadx=70, ipady=10)
    
    #input for password
    pass_input = StringVar()
    
    password_entry = Entry(frame2, textvariable=pass_input, show="*", font="Helvetica 20")
    password_entry.grid(row=2, column=1, sticky=W, padx = 10, pady = 10,ipadx=70, ipady=10)

# Create a Tkinter variable
    tkvar = StringVar(root)
 
# Dictionary with options
    choices = { 'Cashier','Manager'}
    tkvar.set('Cashier') # set the default option
 
    popupMenu = OptionMenu(frame2, tkvar, *choices)
    popupMenu.grid(row = 3, column = 1, padx = 10, pady = 10, ipadx=70, ipady = 10,sticky = N+S+E+W)
    popupMenu.configure(font=('Helvetica', 20))
# on change dropdown value

 
# link function to change dropdown
    #submit button
    login_image = PhotoImage(file="./img/register_submit.png")
    submit_button = Button(frame2, image=login_image, command = edit_record)
    submit_button.grid(column = 1, pady = 10);
    submit_button.image = login_image
    
    
    return root

    
def edit_record():
    rights = 0
    name = name_input.get()
    pw = pass_input.get()
    if (tkvar.get() == "Cashier"):
        rights = 1
    if (tkvar.get() == "Manager"):
        rights = 2
    submission = hashlib.sha1(pw.encode('utf-8')).hexdigest()
    
    if (name == "") or (pw == ""):
        showerror("ERROR", "You cannot have a blank name or pin!")
        root.destroy()
    else:
        
        try:
            cont = sqlite3.connect('./database/users.db')
            with cont:
                
                c = cont.cursor()
                c.execute('''INSERT INTO employee (emp_name, emp_pass, rights)
                  VALUES(?,?, ?)''', (name,submission, rights))
                
                c.execute("""UPDATE employee SET emp_name = ? ,emp_pass = ?,rights = ? WHERE employee_id= ? """,
                               (name,submission,rights,emp_id))
                cont.commit()
            
                showinfo("New Employee Added","Added successfully! \n\nEmployee Name: " + name + "\nEmployee ID:" + str(c.lastrowid))
                root.destroy()
                success = 1
                print (success)
                if (success == 1):
                    import adminChoice
                    adminChoice.root
            
            cont.close()
        
        
        
        except Error as e:
            print(e)


    
    
    
root = buildFrame()
root.mainloop()