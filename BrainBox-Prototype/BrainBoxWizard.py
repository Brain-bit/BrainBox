import ttk
import Tkinter
import globalslidersend
import os
import tkMessageBox
#import BrainBoxGUI2
#global variables
#global slidersend

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
        
    def openother(self):
        os.system("python Brainconfig.py 1")  
        
    def _wizard_buttons(self):
#        global variables
        """Place wizard buttons in the pages."""
        #print self._children.iteritems()
        for indx, child in self._children.iteritems():
            btnframe = ttk.Frame(child)
            btnframe.pack(side='bottom', fill='x', padx=6, pady=12)
#            nextbtn = ttk.Button(btnframe, text="Next", command=self.next_page(self))            
            
            if indx == 0:#welcome page
                nextbtn = ttk.Button(btnframe, text="Sign up", command=self.next_page)
                nextbtn.pack(side='right', anchor='e', padx=6)
                prevbtn = ttk.Button(btnframe, text="Sign in",command=self.sign_up)
                prevbtn.pack(side='right', anchor='e', padx=6)

            elif indx == 3:#sign in page
                nextbtn = ttk.Button(btnframe, text="Sign in", command=self.check_username)
                nextbtn.pack(side='right', anchor='e', padx=6)
                prevbtn = ttk.Button(btnframe, text="Previous",command=self.sign_upprev)
                prevbtn.pack(side='right', anchor='e', padx=6)
                
            else:
                if indx ==1 :#registeriation page
                    nextbtn = ttk.Button(btnframe, text="Next", command=self.next_page)
                    nextbtn.pack(side='right', anchor='e', padx=6)
<<<<<<< HEAD
                elif indx == 2:#Finish registeriation page
                    nextbtn = ttk.Button(btnframe, text="Finish", command=self.close)
=======
                elif indx == 2:
                    nextbtn = ttk.Button(btnframe, text="Finish", command=self.openother)
>>>>>>> origin/master
                    nextbtn.pack(side='right', anchor='e', padx=6)
            
                prevbtn = ttk.Button(btnframe, text="Previous",command=self.prev_page)
                prevbtn.pack(side='right', anchor='e', padx=6)

    #def openother(self):
        

    def next_page(self):#,variable):
        #print self.current
        if self.current == 1:
            variableslist = []
            #Name,email,location,user,password,device
            #user,password,Name,email,location,device
            #print "Page 2" , self.NewAccountVariable
            for variable in self.NewAccountVariable:
                variableslist.append(variable.get())
            print globalslidersend.usernamepassword.keys()
            if variableslist[3] in globalslidersend.usernamepassword.keys():
                tkMessageBox.showinfo("Invalid User", "Please, Enter New User.")
            elif '' in variableslist:
                tkMessageBox.showinfo("Invalid Input", "Please, Fill all textboxes.")
            else:
                userdatafile = open("UserLogin.txt",'a')
                userdatafile.write('\n'+variableslist[3]+','+variableslist[4]+','+variableslist[0]+','+variableslist[1]+','+variableslist[2]+','+variableslist[5])
                #userdatafile.writelines(globalslidersend.userdata)
                userdatafile.close()
                
                userdatafile = open("UserData.txt",'a')
                userdatafile.write('\n'+"%s,0,0,0,0,0,0,0,0,0,0,0"%variableslist[3])
                #globalslidersend.userlist.append(variableslist[3])
                globalslidersend.usernamepassword[variableslist[3]] = variableslist[4]
                #globalslidersend.indexuser = userlist.index(variableslist[3])
                globalslidersend.slidersend = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0 ]
                userdatafile.close()
  
                self.current += 1
        else:self.current += 1

    def prev_page(self):
        self.current -= 1

    def check_username(self):
        #print "Page 1" , self.CurAccountVariable
        inputlist = []
        for i in self.CurAccountVariable:
            inputlist.append(i.get())
        if inputlist[0] in globalslidersend.usernamepassword.keys() and globalslidersend.usernamepassword[inputlist[0]] == inputlist[1]:
            print 'right user'
            self.master.destroy()
            os.system("python Brainconfig.py 1")  
    
        else :
            tkMessageBox.showinfo("Invalid Input", "Please, Enter your useername and password again")
           
        

    def sign_up(self):
        self.current = 3

    def sign_upprev(self):
        self.current = 0

    def close(self):
        self.master.destroy()
        #execfile("Brainconfig.py")
        #os.system('python Brainconfig.py')
        #BrainBoxGUI2.BrainBoxExpressiv()

    def add_empty_page(self):
        child = ttk.Frame(self)
        self._children[len(self._children)] = child
        self.add(child)

    def add_page_body(self, body):
        body.pack(side='top', fill='both', padx=6, pady=12)
        
    def firstpage(self, body):#welcome page
        body.pack(side='top', fill='both', padx=6, pady=12)
        img =Tkinter.PhotoImage(file="bbimtrans.gif")
        bImg = Tkinter.Label(body, image=img)
        bImg.img = img
        bImg.pack(pady=20)
        desc=ttk.Label(body, text='Welcome to the BrainBox Wizard. Please follow the wizard in order to register\nyour device and callibrate the BCI headset with your appplications.\nPlease connect the headset into the USB port.').pack(pady = 20)

    def secondpage(self, body):#Registration page 
        variables = []
        desc=ttk.Label(body, text='Please fill in the registration form below to set up your account with the\nBrainPrint service, and to setup BrainBox.\nPlease make sure you have a proper Internet Connection!').pack(pady = 20)
        seperator = ttk.Frame(height=2)
        seperator.pack()
        body.pack(side='top', fill='both', padx=6, pady=12)
        name=ttk.Label(body, text='Name').pack(pady=0)
        nameentry= ttk.Entry(body)
        nameentry.pack()
        #nameentry.insert(0,'Enter your name :')
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
        
    def thirdpage(self, body):#Finish registeriation page
        body.pack(side='top', fill='both', padx=6, pady=12)
        img =Tkinter.PhotoImage(file="brainboxwizcor.gif")
        bImg = Tkinter.Label(body, image=img)
        bImg.img = img
        bImg.pack(pady=20)
        desc=ttk.Label(body, text='Your are now registered, you may know begin\nusing BrainBox! Have a nice day!').pack(pady = 20)

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

    def page_container(self, page_num):
        if page_num in self._children:
            return self._children[page_num]
        else:
            raise KeyError("Invalid page: %s" % page_num)

    def _get_current(self):
        return self._current
   
    def _set_current(self, curr):
        if curr not in self._children:
            raise KeyError("Invalid page: %s" % curr)

        self._current = curr
        self.select(self._children[self._current])

    current = property(_get_current, _set_current)


def demo():
    globalslidersend.init()
    #variables = 0
    
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
