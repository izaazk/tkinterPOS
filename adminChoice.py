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
    

def goToPOS():
    root.destroy()
    import main
    main.root
    
def goToAdmin():
    root.destroy()
    import AdminPanel
    AdminPanel.root


def buildFrame():
    
    root = Tk()
    root.geometry("800x600")
    
    root.resizable(False, False)
    root.title("POS - Administration")
    
    bg_img = PhotoImage(file="./img/regbg.png")

    lbl1 = Label(root, image=bg_img)
    lbl1.image = bg_img
    lbl1.place(x=0, y=0, relwidth=1, relheight=1)   

    
    img = PhotoImage(file="./img/logo.png")

    
    lbl = Label(root, image=img)
    lbl.image = img
    lbl.pack(fill = X, pady=10);
    
    lbl = Label(root, text = "Administrator, Choose an Option Below: ", font=("Helvetica", 26))
    lbl.pack(fill = X, pady = 10);
    frame2 = Frame(root)
    frame2.pack(fill = Y, expand=FALSE, padx=20, pady=10)

    frame3 = Frame(root)
    frame3.pack(side = TOP, expand=TRUE)
    
    
    pos_image = PhotoImage(file="./img/posLogo.png")
    pos_button = Button(frame3, image=pos_image, command = goToPOS)
    pos_button.grid();
    pos_button.image = pos_image    
    
    frame4 = Frame(root)
    frame4.pack(side = BOTTOM, expand=TRUE)
    #inventory button
    usermgt_image = PhotoImage(file="./img/userAdmin.png")
    inventoryL = Button(frame4, image=usermgt_image, command = goToAdmin)
    inventoryL.grid();
    inventoryL.image = usermgt_image        
    
    
    
    
    return root


root = buildFrame()
root.mainloop()



