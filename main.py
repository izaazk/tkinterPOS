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
import sqlite3
from sqlite3 import Error
from sqlite3 import Cursor
from tkinter import simpledialog
import os
import hashlib



def buildFrame () :
    
    global tree, inputSKU, skuEntry, subAmount, taxAmount,totalAmount, trans_counter, rights1
    global userID, rights, emp_name, pcButton, qtyButton, lineVoid, lineVoid, pcOverride,transVoid, btm_frame2, total_button, goButton
    global timestamp
    locale.setlocale( locale.LC_ALL, '' )
    timestamp = datetime.datetime.now()

    global popup, user_id, user_pw
   
    initial=0
    root = Tk()
    root.geometry("1000x800")
    
    root.resizable(False, False)
    root.title("POS - Main Screen")
    
    #root.protocol("WM_DELETE_WINDOW", disable_event)
    
    root.state('zoomed')
    
    global rights, employeeID
    subAmount = StringVar()
    taxAmount = StringVar()
    totalAmount = StringVar()
    trans_counter = StringVar()
    emp_name = StringVar()   
    
    try:
        temp = open('./database/active_user','r').read().split('\n')
    
    
        employeeID = temp[0]
        name = temp[1]
        rights = temp[2]
    
    
        os.remove("./database/active_user")
    except FileNotFoundError:
        root.destroy()
        import Login_screenn
        Login_screenn.root
    #userID.set(employeeID)
    
    rights1 = int(rights)
    
    if (rights1 == 1):
        position = "Cashier"
    if (rights1 == 2):
        position = "Manager"

    emp_name.set(name.title() + " - " + position)
    
    if (initial is 0):
        subAmount.set(0)
        taxAmount.set(0)
        totalAmount.set(0)
        trans_counter.set("0")
        initial = initial + 1
    
    # create all of the main containers
    top_frame = Frame(root, width=400, height=40, pady=10, padx=10)
    center = Frame(root, width=400, height=200, padx=3, pady=3)
    btm_frame = Frame(root, width=400, height=80, pady=3)
    btm_frame2 = Frame(root, width=400, height=40, pady=3)
    btm_frame3 = Frame(root,  width=400, height=45, pady=3)

    
    
    # layout all of the main containers
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    top_frame.grid(row=0, sticky = "")
    center.grid(row=1, sticky="")
    btm_frame.grid(row=3, sticky="e", padx = 320)
    btm_frame2.grid(row=4, sticky="")
    btm_frame3.grid(row=5, sticky="ew")
    
    #the actual widgets on the top part of screen
    
    logo = PhotoImage(file="./img/logo.png")
    lbl = Label(top_frame, image=logo)
    lbl.image = logo
    lbl.grid(padx = 130, sticky = 'nsew');
    
    # layout the widgets in the top frame
    #company_label.grid(row=1, column = 0, sticky=N+S+E+W)
    #item sku entry:
    
    #skuLabel = Label(center, text='Click Here to Enter a SKU: ')
    #skuLabel.grid(row = 1,sticky = 'w', ipadx = 60)
    
    inputSKU = StringVar()
    
    skuEntry = Entry(center, textvariable = inputSKU, width = 100)
    skuEntry.grid(row = 1, ipadx = 100, ipady=20, sticky='w')  
    skuEntry.insert(0, "Click Here to Enter a SKU")   
    skuEntry.bind("<Button-1>", clear_search) 
    
    goButton = Button(center,text="Enter",bg="white", height = 1, width = 5, command = fetchData)
    goButton.grid(row = 1, ipadx = 40, ipady = 20, column = 2);

    

    
    #actual item loader
    from tkinter import ttk  
    tree = ttk.Treeview(center,show="headings", height = 20)

    tree["columns"]=("one","two","three","four")
    tree.column("one", width=125 )
    tree.column("two", width=600 )
    tree.column("three", width=150)
    tree.column("four", width=100)
    tree.heading("one",text="SKU")
    tree.heading("two", text="Description")
    tree.heading("three", text="Price")
    tree.heading("four", text="Quantity")
    
    vsb = ttk.Scrollbar(orient="vertical", command=tree.yview)
    vsb.grid(column=5, row=2, sticky='ns', in_=center)
    tree.configure(yscrollcommand=vsb.set)
    #tree.insert("" , 0, values=("91919","Monster Energy Drink 12oZ","2.99", "1"))

    tree.grid(sticky = E+W+N+S, row = 2,columnspan = 4)
    tree.bind('<Button-1>', handle_click)
    
    subTotal_label = Label(btm_frame, text='Active Customer: ')
    subTotal_label.grid(sticky = 'e', row = 0, ipadx = 40, ipady=10, pady = 5)
    
    
    #total rows
    subTotal_label = Label(btm_frame, text='Subtotal: $')
    subTotal_label.grid(sticky = 'w', row = 0, ipadx = 40, ipady=10, pady = 5)
    subTotal_field = Entry(btm_frame, textvariable=subAmount, justify = LEFT,state = 'readonly')
    subTotal_field.grid( row = 0, column = 2,ipadx = 20, ipady=5, pady = 5)
    
    tax_label = Label(btm_frame, text='Tax:        $')
    tax_label.grid(sticky = 'w', row = 1, ipadx = 40, ipady=10)
    tax_field = Entry(btm_frame, textvariable=taxAmount, justify = LEFT,state = 'disabled')
    tax_field.grid( row = 1, column = 2,ipadx = 20, ipady=5)
    
    total_label = Label(btm_frame, text='Total Due: $', bg="yellow")
    total_label.grid(sticky = 'w', row = 2, ipadx = 40, ipady=10,pady = 5)
    total_field = Entry(btm_frame, textvariable=totalAmount, justify = LEFT, readonlybackground="yellow",state = 'readonly')
    total_field.grid( row = 2, column = 2,ipadx = 20, ipady=10, pady = 5)

    
    
    
    
    #register function buttons
    pcButton = Button(btm_frame2,text="Price Check",bg="cyan", height = 1, width = 5, command = priceCheck)
    pcButton.grid(row = 1, ipadx = 40, ipady = 20, padx = 17);
    
    qtyButton = Button(btm_frame2,text="Quantity",bg="magenta", height = 1, width = 5, command = qtyModify)
    qtyButton.grid(row = 1, column = 2,ipadx = 40, ipady = 20, padx = 17);
    
    lineVoid = Button(btm_frame2,text="Line Void",bg="red", height = 1, width = 5, command = lnVoid)
    lineVoid.grid(row = 1, column = 3,ipadx = 40, ipady = 20, padx = 17);
    
    
    pcOverride = Button(btm_frame2,text="Price Override",bg="yellow", height = 1, width = 5, command = popupmsg, state='normal')
    pcOverride.grid(row = 1, column = 4,ipadx = 40, ipady = 20, padx = 17);
    


    transVoid = Button(btm_frame2,text="Trans Void",bg="white", height = 1, width = 5, command = delButton)
    transVoid.grid(row = 1, column = 6,ipadx = 40, ipady = 20, padx = 17);
    
    #totalButton = Button(btm_frame2,text="Tender",bg="green", height = 1, width = 5, command = tenderFunc)
    #totalButton.grid(row = 1, column = 6,ipadx = 40, ipady = 20, padx = 30);

    total_image = PhotoImage(file="./img/tenders/mainbtn.png")
    total_button = Button(btm_frame2, image=total_image, command = tenderFunc, state='disabled')
    total_button.grid(row = 1, column = 8, padx = 70);
    total_button.image = total_image
    
    #bottom of program
        
    user_label = Label(btm_frame3, text='Current User: ')

    active_user = Entry(btm_frame3, textvariable=emp_name, state = 'readonly')
    user_label.grid(sticky = 'w', row = 0, ipadx = 0)
    active_user.grid(sticky = 'n', row = 0, ipadx = 40, column = 1, padx = 0)
    
    spacer = Label(btm_frame3, text='')
    spacer.grid(row = 0, column = 4 ,padx = 200, ipadx = 0)
    
    trans_qty = Label(btm_frame3, text='Total Number of Items: ')
    trans_qty.grid(row = 0, column = 5 ,padx = 0, ipadx = 0)
    
    
    transcounter = Entry(btm_frame3, textvariable=trans_counter, state = 'readonly')
    transcounter.grid(sticky = 'n', row = 0, ipadx = 0, column = 6, padx = 0)
    return root

def delButton():
    
    if messagebox.askokcancel("Void Transaction", "Are you SURE you want to void the entire transaction?"):
        
    
        global subAmount
        orig_subtotal = subAmount.get()
        conv_subtotal = float (orig_subtotal)
        conv_subtotal = 0
    
        sub_update = str("%.2f" % conv_subtotal)
        subAmount.set(sub_update)
    
       
    
        global taxAmount
        orig_tax = taxAmount.get()
        conv_tax = float (orig_tax)
        conv_tax = 0
    
        tax_update = str("%.2f" % conv_tax)
    
        taxAmount.set(tax_update)
    
    
    
        global totalAmount
        
        orig_total = totalAmount.get()
        orig_total = float(orig_total)
        
        update = 0
        final_update = str("%.2f" % update)
    
        totalAmount.set(final_update)
        
       
        trans_counter.set(str(0))
        
            #clear the cartlist
        x = tree.get_children()
        
        for item in x:
            tree.delete(item)
        
        if not tree.get_children():
            total_button.config(state = 'disabled')
        

        
        
def disable_event():
    pass

def qtyModify():
    
    
    sell_price = tree.item(tree.selection())['values'][2]
    orig_qty =  tree.item(tree.selection())['values'][3]
    
    orig_qty = int(orig_qty)
    sell_price = float(sell_price)
    
    answer = simpledialog.askinteger("Quantity Edit", "Enter Quantity:",
                                parent=root)
    
    if (answer == ""):
        showerror("NO ENTRY", "You did not enter anything...?")
    
    if answer is not None and answer is not "":
        
        tree.set(tree.selection(), 3, answer)
        
        original_sell = orig_qty * sell_price
        
        sel_price2 = sell_price * answer
        
        global subAmount
        orig_subtotal = subAmount.get()
        conv_subtotal = float (orig_subtotal)
        
        conv_subtotal = conv_subtotal - original_sell
        conv_subtotal = conv_subtotal + sel_price2
    
        sub_update = str("%.2f" % conv_subtotal)
    
        subAmount.set(sub_update)
    
        sales_taxes = conv_subtotal * 0.0925
    
        global taxAmount
        
        taxAmount.set("0")
    
        tax_update = str("%.2f" % sales_taxes)
    
        taxAmount.set(tax_update)
    
    
    
        global totalAmount
        
        orig_total = totalAmount.get()
        orig_total = float(orig_total)
        
        final_update = str("%.2f" % (conv_subtotal + sales_taxes))
    
        totalAmount.set(final_update)
    
        global trans_counter
        origqty = int( trans_counter.get())
        origqty = origqty + answer

def tenderFunc():
    
    global cash_button, card_button, escape_button
    
    pcButton.grid_forget()
    lineVoid.grid_forget()
    transVoid.grid_forget()
    qtyButton.grid_forget()
    pcOverride.grid_forget()
    total_button.grid_forget()

    skuEntry.grid_forget()
    goButton.grid_forget()
    
   
    
    cash_image = PhotoImage(file="./img/tenders/cash.png")
    cash_button = Button(btm_frame2, image=cash_image, command = cashPMT)
    cash_button.grid(row = 1, padx = 30);
    cash_button.image = cash_image
    
    card_image = PhotoImage(file="./img/tenders/card.png")
    card_button = Button(btm_frame2, image=card_image, command = cardPMT)
    card_button.grid(row = 1, column = 2,padx = 30);
    card_button.image = card_image
    
    escape_image = PhotoImage(file="./img/tenders/exit.png")
    escape_button = Button(btm_frame2, image=escape_image, command = tenderESC)
    escape_button.grid(row = 1, column = 7,padx = 30);
    escape_button.image = escape_image
    

def tenderESC():
    
    cash_button.grid_forget()
    card_button.grid_forget()
    escape_button.grid_forget()
    
    
    skuEntry.grid(row = 1, ipadx = 100, ipady=20, sticky='w')  
    goButton.grid(row = 1, ipadx = 40, ipady = 20, column = 2);
    
    pcButton.grid(row = 1, ipadx = 40, ipady = 20, padx = 17);
    qtyButton.grid(row = 1, column = 2,ipadx = 40, ipady = 20, padx = 17);
    lineVoid.grid(row = 1, column = 3,ipadx = 40, ipady = 20, padx = 17);
    pcOverride.grid(row = 1, column = 4,ipadx = 40, ipady = 20, padx = 17);
    transVoid.grid(row = 1, column = 6,ipadx = 40, ipady = 20, padx = 17);
    total_button.grid(row = 1, column = 7, padx = 17);
    
def cashPMT():
    amount = simpledialog.askfloat("Amount", "Enter cash amount?",
                                parent=root)
    
    if (amount == ""):
        showerror("NO ENTRY", "You did not enter anything...?")
    skulist = []
    
    for child in tree.get_children():
        
        skulist.append(str(tree.item(child)["values"][0]) )        ## append elem at end
        print (skulist)
    
    uploadSKUs = ','.join(map(str, skulist)) 
    
    if amount is not None and amount is not "":
        dueAMT = float(totalAmount.get())
        givenAMT = float(amount)
        
        if (givenAMT > dueAMT):
            give_change = True
            changeDUE = givenAMT - dueAMT
            
        try:
            cont = sqlite3.connect('./database/trans.db')
            with cont:
                global database_entry
                c = cont.cursor()
                
                c.execute('''INSERT INTO transactions (transactionTimeStamp, employeeID, skuList, total, pmtMethod)
                  VALUES(?,?,?,?, ?)''', (timestamp.strftime("%m-%d-%Y %H:%M"), employeeID,uploadSKUs, totalAmount.get(), 'CASH'))
                cont.commit()
            
            if (give_change):
                showwarning("CHANGE DUE:", "Please return change to customer:\n$" + str(("%.2f" % changeDUE)))
                total_button.config(state = 'disabled')
                
            
            cont.close()
            tree.delete(*tree.get_children())
           
            subAmount.set(0)
            taxAmount.set(0)
            totalAmount.set(0)
            trans_counter.set("0")
            tenderESC()
            
        except Error as e:
            print(e)
        except ValueError:
            showerror("SKU ERROR", "SKU: " + amount + " not found... \nPlease check the sku and try again.")
            
        
            
    else:
        print ("")



    
    
def popupmsg():
    if not tree.selection():
        showerror("ERROR", "NO ITEM SELECTED")
        exit
    
    else:
        global user_input, pass_input
    
        popup = Toplevel(root) 
    #popup = Tk()
    #popup.wm_title("!")
    
        frame2 = Frame()
        frame2.grid()
    
        #username label
        main_label = Label(popup, text="Manager Override:", font=("Helvetica", 24))
        main_label.grid(row=1, column=0, sticky=NSEW, padx = 20, pady = 20)
    
    #username label
        username_label = Label(popup, text="Username:", font=("Helvetica", 18))
        username_label.grid(row=2, column=0, sticky=W, padx = 20, pady = 20)
    
    #password label
        password_label = Label(popup, text="Password:", font=("Helvetica", 18))
        password_label.grid(row=3, column=0, sticky=W, padx = 15)
    
    
    
        user_input = StringVar()
        username_entry = Entry(popup, textvariable=user_input, font="Helvetica 20")
        username_entry.grid(row=2, column=1, sticky=W, padx = 10, ipadx=70, ipady=10)

        pass_input = StringVar()
        password_entry = Entry(popup, textvariable=pass_input, show="*", font="Helvetica 20")
        password_entry.grid(row=3, column=1, sticky=W, padx = 10, pady = 10,ipadx=70, ipady=10)
    

    #submit button
        submit_button = Button(popup, text = "Approve", command = approve_override)
        submit_button.grid(row = 4, column = 1, ipadx = 20, ipady=20);
    
    #submit button
        submit_button = Button(popup, text = "Cancel", command = lambda: popup.destroy())
        submit_button.grid(row = 4, column = 0, ipadx = 20, ipady=20);

    
        popup.mainloop()

def approve_override():
    
    user_id = user_input.get()
    user_pw = pass_input.get()
    
    try:
        cont = sqlite3.connect('./database/users.db')
        with cont:
            global database_entry
            c = cont.cursor()
            print (user_id)
            c.execute('''SELECT emp_pass, rights FROM employee WHERE employee_id=?''', (user_id,))
            database_entry = c.fetchone()
            
            resultString = str(database_entry)
            
            resultString=resultString.replace("(","")
            resultString=resultString.replace(")","")
            resultString=resultString.replace("\'","")
            
            emp_pass1, rights = resultString.split(',', 1)
            rights = rights.replace(" ", "")
            rights = int(rights)
            print ("manager check:" + str(rights))
            #resultString=resultString.replace(",","")
            

            user_entry = user_pw
            user_entry = user_entry.encode(encoding='utf_8')
            
            
            sha = hashlib.sha1(user_entry)
            check1 = sha.hexdigest()
            
            print ("hashed inputted pass: " + check1)
            print ("hashed db pass: "  + emp_pass1)
    
            if (check1 == emp_pass1 and rights == 2):
                original_price = tree.item(tree.selection())['values'][2]
                orig_qty =  tree.item(tree.selection())['values'][3]
    
                orig_qty = int(orig_qty)
                original_price = float(original_price)
    
                new_price = simpledialog.askfloat("New Price", "Enter New Price:",
                                parent=root)
    
                if (new_price == ""):
                    showerror("NO ENTRY", "You did not enter anything...?")
    
    
                if new_price is not None and new_price is not "":
        
                    tree.set(tree.selection(), 2, new_price)
        
                    original_price = original_price * orig_qty
        
                    global subAmount
                    orig_subtotal = subAmount.get()
                    conv_subtotal = float (orig_subtotal)
        
                    conv_subtotal = conv_subtotal - original_price
        
                    new_price = new_price * orig_qty 
                    conv_subtotal = conv_subtotal + new_price
    
                    sub_update = str("%.2f" % conv_subtotal)
    
                    subAmount.set(sub_update)
    
                    sales_taxes = conv_subtotal * 0.0925
    
                    global taxAmount
                    
                    taxAmount.set("0")
    
                    tax_update = str("%.2f" % sales_taxes)
    
                    taxAmount.set(tax_update)
    
    
    
                    global totalAmount
        
                    orig_total = totalAmount.get()
                    orig_total = float(orig_total)
        
                    final_update = str("%.2f" % (conv_subtotal + sales_taxes))
    
                    totalAmount.set(final_update)
                
            else:
                showwarning("Incorrect Credentials", "Please try again.")
                popup.destroy()
            
        cont.close()
    except ValueError:
        showwarning("Incorrect Credentials", "Please try again.")
    

    
        
    
def cardPMT():
    number = simpledialog.askinteger("Card Info", "Enter 16-Digit Card Number: \n --- Without Any Dashes or Spaces ---",
                                parent=root)
    
    if (number == ""):
        showerror("NO ENTRY", "You did not enter anything...?")
    skulist = []
    
    for child in tree.get_children():
        
        skulist.append(str(tree.item(child)["values"][0]) )        ## append elem at end
        print (skulist)
    
    uploadSKUs = ','.join(map(str, skulist)) 
    
    if number is not None and number is not "":
        
       
            
        try:
            cont = sqlite3.connect('./database/trans.db')
            with cont:
                global database_entry
                c = cont.cursor()
                number= str(number)
                submission = hashlib.sha1(number.encode('utf-8')).hexdigest()
                c.execute('''INSERT INTO transactions (transactionTimeStamp, employeeID, skuList, total, pmtMethod, pmtInfo)
                  VALUES(?,?,?,?,?, ?)''', (timestamp.strftime("%m-%d-%Y %H:%M"), employeeID,uploadSKUs, totalAmount.get(), 'CARD', submission))
                cont.commit()

                total_button.config(state = 'disabled')
                
            
            cont.close()
            tree.delete(*tree.get_children())
           
            subAmount.set(0)
            taxAmount.set(0)
            totalAmount.set(0)
            trans_counter.set("0")
            tenderESC()
            
        except Error as e:
            print(e)
        except ValueError:
            showerror("SKU ERROR", "SKU: "  + " not found... \nPlease check the sku and try again.")
            
        
            
    else:
        print ("")

    
    
    
    
def lnVoid():
    selection = tree.selection() ## get selected item

    sel_sku = tree.item(tree.selection())['values'][0]
    sel_desc = tree.item(tree.selection())['values'][1]
    sel_price = tree.item(tree.selection())['values'][2]
    sel_qty = tree.item(tree.selection())['values'][3]
    
    if messagebox.askokcancel("Void Line", "Confirm Void Entry: \nSKU:" + str(sel_sku) + "\nItem: " + sel_desc + "\nPrice: " + str(sel_price)):
        conv_sel = float(sel_price)
        conv_qty = int(sel_qty)
        
        conv_sel = conv_sel * conv_qty
    
        global subAmount
        orig_subtotal = subAmount.get()
        conv_subtotal = float (orig_subtotal)
        conv_subtotal = conv_subtotal - conv_sel
    
        sub_update = str("%.2f" % conv_subtotal)
    
        subAmount.set(sub_update)
    
        sel_taxes = conv_sel * 0.0925
    
        global taxAmount
        orig_tax = taxAmount.get()
        conv_tax = float (orig_tax)
        conv_tax = conv_tax - sel_taxes
    
        tax_update = str("%.2f" % conv_tax)
    
        taxAmount.set(tax_update)
    
    
    
        global totalAmount
        sel_total = conv_sel+sel_taxes
        orig_total = totalAmount.get()
        orig_total = float(orig_total)
        
        update = orig_total - sel_total
        final_update = str("%.2f" % update)
    
        totalAmount.set(final_update)
    
        global trans_counter
        origqty = int( trans_counter.get())
        origqty = origqty - conv_qty
        
       
        trans_counter.set(str(origqty))
        
        tree.delete(selection)
        
        if not tree.get_children():
            total_button.config(state = 'disabled')

def clear_search(event): 
    skuEntry.delete(0, END) 
    
def handle_click(event):
    if tree.identify_region(event.x, event.y) == "separator":
        return "break"




def edit():
    x = tree.get_children()
    for item in x: ## Changing all children from root item
        tree.item(item, text="blub", values=("foo", "bar"))



def fetchData():
    
    tree.focus_set()
    

    if inputSKU.get() is not None and inputSKU.get() is not "":
                
        try:
            cont = sqlite3.connect('./database/SKU.db')
            with cont:
                global database_entry
                c = cont.cursor()
                c.execute('''SELECT Description, Price FROM skus WHERE SKU=?''', (inputSKU.get(),))
                database_entry = c.fetchone()
                resultString = str(database_entry)
                resultString=resultString.replace("(","")
                resultString=resultString.replace(")","")
                resultString=resultString.replace("\'","")
                #resultString=resultString.replace(",","")
            
                description, price = resultString.split(',', 1)
                
                price = float(price)
                
                global subAmount
                
                subAmount1 = float(subAmount.get())
                subAmount1 = subAmount1 + price
                subAmount2 = str("%.2f" % subAmount1)
                subAmount.set((subAmount2))
                
                global taxAmount
                taxAmount0 = float(taxAmount.get())
                taxAmount1 = (price * 0.0925) 
                
                taxAmount2 = taxAmount0 + taxAmount1
                taxAmount3 = str(("%.2f" % taxAmount2))
                
                taxAmount.set(taxAmount3)
                
                global totalAmount
                
                totalAmount0 = float(totalAmount.get())
                totalAmount1 = totalAmount0 + price + taxAmount1
                
                totalAmount.set(("%.2f" % totalAmount1))
                
                
            
                tree.insert('', 'end', text = inputSKU.get(), values=(inputSKU.get(),description,price,'1'))
                
                global trans_counter
                trans_counter0 = trans_counter.get()
                trans_counter1 = int(trans_counter0)
                
                trans_counter1 = trans_counter1 + 1
                trans_counter2 = str(trans_counter1)
                
                trans_counter.set(trans_counter2)
                skuEntry.delete(0, END)
                skuEntry.insert(0, "Click Here to Enter a SKU")   
                total_button.config(state = 'normal')
            cont.close()
        except Error as e:
            print(e)
        except ValueError:
            showerror("SKU ERROR", "SKU not found... \nPlease check the sku and try again.")
            skuEntry.delete(0, END)
            skuEntry.insert(0, "Click Here to Enter a SKU")   
    else:
        skuEntry.delete(0, END)
        skuEntry.insert(0, "Click Here to Enter a SKU")   
        
    

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
        
        


root = buildFrame()
root.mainloop()



