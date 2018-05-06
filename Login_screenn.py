'''
@author: Izaaz Kothawala
@date: 03/26/2018
@class: ITMD 413
@Lab: 08



'''
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
from _ctypes import alignment
from tkinter import simpledialog
import sys





def buildFrame () :
    
    global user_input, pass_input, root, username_entry
    
    root = Tk()
    root.geometry("1000x500")
    
    frame1 = Frame(root)
    frame1.pack()
    
    
    root.resizable(False, False)
    root.title("POS Login Screen")
    root.option_add('*font', 'Helvetica -20')
    
    img = PhotoImage(file="./img/logo.png")
    bg_img = PhotoImage(file="./img/bg.png")

    lbl1 = Label(root, image=bg_img)
    lbl1.image = bg_img
    lbl1.place(x=0, y=0, relwidth=1, relheight=1)   
    
    lbl = Label(root, image=img)
    lbl.image = img
    lbl.pack(fill = X, pady=15);
    
    frame2 = Frame(root)
    frame2.pack(side = LEFT, expand=FALSE, padx=20, pady=5)
    
    #username label
    username_label = Label(frame2, text="Username:", font=("Helvetica", 24))
    username_label.grid(row=1, column=0, sticky=W, padx = 20, pady = 20)
    
    #password label
    password_label = Label(frame2, text="Password:", font=("Helvetica", 24))
    password_label.grid(row=2, column=0, sticky=W, padx = 15)
    
    #input for username
    user_input = StringVar()
    
    username_entry = Entry(frame2, textvariable=user_input, font="Helvetica 20")
    username_entry.grid(row=1, column=1, sticky=W, padx = 10, ipadx=70, ipady=10)
    
    #input for password
    pass_input = StringVar()
    
    password_entry = Entry(frame2, textvariable=pass_input, show="*", font="Helvetica 20")
    password_entry.grid(row=2, column=1, sticky=W, padx = 10, pady = 10,ipadx=70, ipady=10)
    
    #submit button
    login_image = PhotoImage(file="./img/login.png")
    submit_button = Button(frame2, image=login_image, command = fetchRecord)
    submit_button.grid(row = 3, column = 1);
    submit_button.image = login_image
   
    #clear button
    clear_image = PhotoImage(file="./img/clear.png")
    clear_button = Button(frame2, image=clear_image, command = clearFields)
    clear_button.grid(row = 3, padx=10, pady=10 );
    clear_button.image = clear_image    
    
    
    frame3 = Frame(root)
    frame3.pack(side = TOP, expand=TRUE)
    
    #pricecheck button
    pricecheck = PhotoImage(file="./img/pricecheck.png")
    pc_button = Button(frame3, image=pricecheck, command = priceCheck)
    pc_button.grid();
    pc_button.image = pricecheck    
    
    frame4 = Frame(root)
    frame4.pack(side = BOTTOM, expand=TRUE)
    #inventory button
    inventoryLookup = PhotoImage(file="./img/inventory.png")
    inventoryL = Button(frame4, image=inventoryLookup, command = inventoryCheck)
    inventoryL.grid();
    inventoryL.image = inventoryLookup        
    
    return root

def clearFields():
    user_input.set("")
    pass_input.set("")
    username_entry.focus()

def fetchRecord():
    userID = user_input.get()
    try:
        cont = sqlite3.connect('./database/users.db')
        with cont:
            global database_entry
            c = cont.cursor()
            c.execute('''SELECT emp_pass FROM employee WHERE employee_id=?''', (userID,))
            database_entry = c.fetchone()
            resultString = str(database_entry)
            resultString=resultString.replace("(","")
            resultString=resultString.replace(")","")
            resultString=resultString.replace("\'","")
            resultString=resultString.replace(",","")
            

            user_entry = pass_input.get()
            user_entry = user_entry.encode(encoding='utf_8')
            secure (user_entry, resultString)
            
        cont.close()
    except Error as e:
       # if (userID == "adminIIT") and (pass_input == "IITadmin"):
         #   showinfo("OFFLINE ACCOUNT", "LOCAL ACCOUNT LOGGED IN SUCCESSFULLY")
        print (e)
        
def secure(user_entry, resultString):
    sha = hashlib.sha1(user_entry)
    check1 = sha.hexdigest()
    
    if (check1 == resultString):
        #showinfo("Success", "Login verified")
        getUserInfo()
    else:
        showwarning("GANDU", "GANDU")

def getUserInfo():
    userID = user_input.get()
    try:
        cont = sqlite3.connect('./database/users.db')
        with cont:
            global database_entry
            c = cont.cursor()
            c.execute('''SELECT emp_name, rights FROM employee WHERE employee_id=?''', (userID,))
            database_entry = c.fetchone()
            resultString = str(database_entry)
            resultString=resultString.replace("(","")
            resultString=resultString.replace(")","")
            resultString=resultString.replace("\'","")
            #resultString=resultString.replace(",","")
            
            emp_name, rights = resultString.split(',', 1)
            
            rights = rights.replace(" ", "")
            
            fo = open("./database/active_user", "w+")
            fo.writelines([userID+"\n", emp_name+"\n", rights+"\n"])
            fo.close()
            
            root.destroy()
            success = 1
            if (success == 1):
                rights2 = int(rights)
                print (rights2)
                if(rights2 == 2):
                    import adminChoice
                    adminChoice.root
                elif(rights2 == 1):
                    import main
                    main.root
        cont.close()
    except Error as e:
       # if (userID == "adminIIT") and (pass_input == "IITadmin"):
         #   showinfo("OFFLINE ACCOUNT", "LOCAL ACCOUNT LOGGED IN SUCCESSFULLY")
        print (e)
        
    

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
       
def priceCheck():
    answer = simpledialog.askstring("Price Lookup", "What is the SKU of the item?",
                                parent=root)
    
    if (answer == ""):
        showerror("NO ENTRY", "You did not enter anything...?")
    
    if answer is not None and answer is not "":
                
        try:
            cont = sqlite3.connect('./database/SKU.db')
            with cont:
                global database_entry
                c = cont.cursor()
                c.execute('''SELECT Description, Price FROM skus WHERE SKU=?''', (answer,))
                database_entry = c.fetchone()
                resultString = str(database_entry)
                resultString=resultString.replace("(","")
                resultString=resultString.replace(")","")
                resultString=resultString.replace("\'","")
                #resultString=resultString.replace(",","")
            
                description, price = resultString.split(',', 1)
            
            
                showinfo("SKU: " + answer, description + "\nCost: $" + price)
            
            
            cont.close()
        except Error as e:
            print(e)
        except ValueError:
            showerror("SKU ERROR", "SKU: " + answer + " not found... \nPlease check the sku and try again.")
            
    else:
        print ("")
        
        
def inventoryCheck():
    answer = simpledialog.askstring("Inventory Lookup", "What is the SKU of the item?",
                                parent=root)
    
    if (answer == ""):
        showerror("NO ENTRY", "You did not enter anything...?")
    
    if answer is not None and answer is not "":
                
        try:
            cont = sqlite3.connect('./database/SKU.db')
            with cont:
                global database_entry
                c = cont.cursor()
                c.execute('''SELECT Description, Quantity FROM skus WHERE SKU=?''', (answer,))
                database_entry = c.fetchone()
                resultString = str(database_entry)
                resultString=resultString.replace("(","")
                resultString=resultString.replace(")","")
                resultString=resultString.replace("\'","")
                    #resultString=resultString.replace(",","")
            
                description, stock = resultString.split(',', 1)
            
            
                showinfo("SKU: " + answer, description + "\nOn-Hand Quantity: " + stock)
            
            
            cont.close()
        except Error as e:
            print(e)
        except ValueError:
            showerror("SKU ERROR", "SKU: " + answer + " not found... \nPlease check the sku and try again.")
                 
        
    

root = buildFrame()
root.mainloop()



locale.setlocale( locale.LC_ALL, '' )
timestamp = datetime.datetime.now()
print(("\nAuthor: Izaaz Kothawala") + ("\nLab 08") + ("\nTimestamp: ") + timestamp.strftime("%m-%d-%Y %H:%M"))