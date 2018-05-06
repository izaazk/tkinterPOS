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

def buildFrame () :
    
    global name_input, pass_input, ssn_input, tkvar
    
    root = Tk()
    root.geometry("1000x600")
    
    root.resizable(False, False)
    root.title("POS - Administration")
    
    #root.protocol("WM_DELETE_WINDOW", disable_event)
    
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
    
    logo = PhotoImage(file="./img/logo.png")
    lbl = Label(top_frame, image=logo)
    lbl.image = logo
    lbl.grid(padx = 130, sticky = 'nsew');
    
    usermgt_label = Label(center, text='User Management Functions:')
    usermgt_label.grid(sticky = 'n', row = 0, ipadx = 40, ipady=10,pady = 5)  
    
    addUserBtn_image = PhotoImage(file="./img/user/addUser.png")
    addUserBtn = Button(center, image=addUserBtn_image, command = addUser)
    addUserBtn.grid(row = 1);
    addUserBtn.image = addUserBtn_image
    
    
    return root



def addUser():
    root.destroy()
    import addEmp
    addEmp.root
    




root = buildFrame()
root.mainloop()




    
    
    
    
    
    
