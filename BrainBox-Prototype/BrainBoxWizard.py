# Importing important libraries
import ttk
import Tkinter
import globalslidersend
import os
import tkMessageBox
import sys
import ExpressivSuite
from ttk import *
#import ttk
import threading
import time

# A Class that creates the Wizard GUI
class Wizard(object, ttk.Notebook):
    NewAccountVariable = 0
    CurAccountVariable = 0
    
    def __init__(self, master=None, **kw):
        npages = kw.pop('npages', 3)
        kw['style'] = 'Wizard.TNotebook'
        ttk.Style(master).layout('Wizard.TNotebook.Tab', '')
        ttk.Notebook.__init__(self, master, **kw)
        self._children = {}
        for page in range(npages):
            self.add_empty_page()
        self.current = 0
        self._wizard_buttons()
    # A method for placing the wizard buttons in the pages
    def _wizard_buttons(self):
        
        for indx, child in self._children.iteritems():
            btnframe = ttk.Frame(child)
            btnframe.pack(side='bottom', fill='x', padx=6, pady=12)

            # Welcome page
            if indx == 0:
                nextbtn = ttk.Button(btnframe, text="Sign up", command=self.next_page)
                nextbtn.pack(side='right', anchor='e', padx=6)
                prevbtn = ttk.Button(btnframe, text="Sign in",command=self.sign_up)
                prevbtn.pack(side='right', anchor='e', padx=6)
                
            # Sign in page
            elif indx == 3:
                nextbtn = ttk.Button(btnframe, text="Sign in", command=self.check_username)
                nextbtn.pack(side='right', anchor='e', padx=6)
                prevbtn = ttk.Button(btnframe, text="Previous",command=self.sign_upprev)
                prevbtn.pack(side='right', anchor='e', padx=6)
                
            else:
                # Registeriation page
                if indx ==1 :
                    nextbtn = ttk.Button(btnframe, text="Next", command=self.next_page)
                    nextbtn.pack(side='right', anchor='e', padx=6)
                # Finish registeriation page
                elif indx == 2:
                    nextbtn = ttk.Button(btnframe, text="Finish", command=self.close)
                    nextbtn.pack(side='right', anchor='e', padx=6)
            
                prevbtn = ttk.Button(btnframe, text="Previous",command=self.prev_page)
                prevbtn.pack(side='right', anchor='e', padx=6)

        
    # A method calling the next page in the wizard
    def next_page(self):
        
        if self.current == 1:
            variableslist = []
            for variable in self.NewAccountVariable:
                variableslist.append(variable.get())

            if variableslist[3] in globalslidersend.usernamepassword.keys():
                tkMessageBox.showinfo("Invalid User", "Please, Enter New User.")

            elif '' in variableslist:
                tkMessageBox.showinfo("Invalid Input", "Please, Fill all textboxes.")

            else:
                
                userdatafile = open("UserLogin.txt",'a')
                userdatafile.write('\n'+variableslist[3]+','+variableslist[4]+','+variableslist[0]+','+variableslist[1]+','+variableslist[2]+','+variableslist[5])
                userdatafile.close()
                userdatafile = open("UserData.txt",'a')
                userdatafile.write('\n'+"%s,0,0,0,0,0,0,0,0,0,0,0"%variableslist[3])
                globalslidersend.usernamepassword[variableslist[3]] = variableslist[4]
                globalslidersend.slidersend = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0 ]
                globalslidersend.slidersend.append(variableslist[3])
                userdatafile.close()
                self.current += 1
                
        else:
            self.current += 1

    # A method for calling the previous page in the wizard
    def prev_page(self):
        self.current -= 1

    # A method for checking the username inserted
    def check_username(self):
        inputlist = []
        for i in self.CurAccountVariable:
            inputlist.append(i.get())
        if inputlist[0] in globalslidersend.usernamepassword.keys() and globalslidersend.usernamepassword[inputlist[0]] == inputlist[1]:
            for i in range(len(globalslidersend.userdatalist)):
                if len(globalslidersend.userdatalist[i]) != 0:
                    if globalslidersend.userdatalist[i][0] == inputlist[0]:
                        for x in range(1,len(globalslidersend.userdatalist[i])):
                              globalslidersend.slidersend.append(float(globalslidersend.userdatalist[i][x]))
                        globalslidersend.slidersend.append(inputlist[0])
            self.master.destroy()                 
            execfile("Brainconfig.py")
        else :
            tkMessageBox.showinfo("Invalid Input", "Please, Enter your useername and password again")
           
        
    # A method for numbering the sign_up
    def sign_up(self):
        self.current = 3
        
    # A method for reversing the sign up
    def sign_upprev(self):
        self.current = 0

    # A method for closing and opening the configuration window
    def close(self):
        self.master.destroy()
        execfile("Brainconfig.py")

    # A method for adding empty wizard steps
    def add_empty_page(self):
        child = ttk.Frame(self)
        self._children[len(self._children)] = child
        self.add(child)

    # A method for adding page bodies
    def add_page_body(self, body):
        body.pack(side='top', fill='both', padx=6, pady=12)

    # A metho for the Welcome page   
    def firstpage(self, body):
        body.pack(side='top', fill='both', padx=6, pady=12)
        img =Tkinter.PhotoImage(file="bbimtrans.gif")
        bImg = Tkinter.Label(body, image=img)
        bImg.img = img
        bImg.pack(pady=20)
        desc=ttk.Label(body, text='Welcome to the BrainBox Wizard. Please follow the wizard in order to register\nyour device and callibrate the BCI headset with your appplications.\nPlease connect the headset into the USB port.').pack(pady = 20)

    # A method for calling the registration page
    def secondpage(self, body):#Registration page 
        variables = []
        desc=ttk.Label(body, text='Please fill in the registration form below to set up your account with the\nBrainPrint service, and to setup BrainBox.\nPlease make sure you have a proper Internet Connection!').pack(pady = 20)
        seperator = ttk.Frame(height=2)
        seperator.pack()
        body.pack(side='top', fill='both', padx=6, pady=12)
        name=ttk.Label(body, text='Name').pack(pady=0)
        nameentry= ttk.Entry(body)
        nameentry.pack()
        variables.append(nameentry)
        
        email=ttk.Label(body, text='Email').pack(pady=10)
        emailentry= ttk.Entry(body)
        emailentry.pack()
        variables.append(emailentry)
        
        loation=ttk.Label(body, text='Location').pack(pady=10)
        locationentry= ttk.Entry(body)
        locationentry.pack()
        variables.append(locationentry)

        user=ttk.Label(body, text='User').pack(pady=5)
        userentry= ttk.Entry(body)
        userentry.pack()
        variables.append(userentry)
        
        password=ttk.Label(body, text='Password').pack(pady=10)
        passentry= ttk.Entry(body)
        passentry.pack()
        variables.append(passentry)
        
        device=ttk.Label(body, text='Device').pack(pady=10)
        deviceentry= ttk.Entry(body)
        deviceentry.pack()
        variables.append(deviceentry)
        return variables
    
    # A method for registration page finish
    def thirdpage(self, body):#Finish registeriation page
        body.pack(side='top', fill='both', padx=6, pady=12)
        img =Tkinter.PhotoImage(file="brainboxwizcor.gif")
        bImg = Tkinter.Label(body, image=img)
        bImg.img = img
        bImg.pack(pady=20)
        desc=ttk.Label(body, text='Your are now registered, you may know begin\nusing BrainBox! Have a nice day!').pack(pady = 20)

    # A method for sign in registration page
    def signin(self, body):#sign in 
        variables = []
        body.pack(side='top', fill='both', padx=6, pady=12)
        img =Tkinter.PhotoImage(file="braincloud2.gif")
        bImg = Tkinter.Label(body, image=img)
        bImg.img = img
        bImg.pack(pady=20)
        desc=ttk.Label(body, text='Sign in using your login credentials to load your BrainCloud').pack(pady = 20)
        user=ttk.Label(body, text='User').pack(pady=5)
        userentry= ttk.Entry(body)
        userentry.pack()
        variables.append(userentry)

        password=ttk.Label(body, text='Password').pack(pady=10)
        passentry= ttk.Entry(body)
        passentry.pack()
        variables.append(passentry)
        return variables

    # A method for the page contrainer
    def page_container(self, page_num):
        if page_num in self._children:
            return self._children[page_num]
        else:
            raise KeyError("Invalid page: %s" % page_num)

    # A method for getting current page
    def _get_current(self):
        return self._current
    # A method for....  
    def _set_current(self, curr):
        if curr not in self._children:
            raise KeyError("Invalid page: %s" % curr)

        self._current = curr
        self.select(self._children[self._current])

    current = property(_get_current, _set_current)

# A Function initiating the wizard
def demo():
    globalslidersend.init()
    root = Tkinter.Tk()
    wizard = Wizard(npages=4)
    wizard.master.minsize(400, 350)
    page0 = ttk.Label(wizard.page_container(0))
    page1 = ttk.Label(wizard.page_container(1))
    page2 = ttk.Label(wizard.page_container(2))
    page3 = ttk.Label(wizard.page_container(3))


    wizard.firstpage(page0)
    wizard.NewAccountVariable = wizard.secondpage(page1)
    wizard.thirdpage(page2)
    wizard.CurAccountVariable = wizard.signin(page3)

    wizard.pack(fill='both', expand=True)
    root.mainloop()

if __name__ == "__main__":
    demo()
