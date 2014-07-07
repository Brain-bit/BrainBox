import ttk
import Tkinter
global variables
class Wizard(object, ttk.Notebook):
    variables = 0
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

    def _wizard_buttons(self):
#        global variables
        """Place wizard buttons in the pages."""
        for indx, child in self._children.iteritems():
            btnframe = ttk.Frame(child)
            btnframe.pack(side='bottom', fill='x', padx=6, pady=12)
#            nextbtn = ttk.Button(btnframe, text="Next", command=self.next_page(self))            
            nextbtn = ttk.Button(btnframe, text="Next", command=self.next_page)
            nextbtn.pack(side='right', anchor='e', padx=6)
            if indx != 0:
                prevbtn = ttk.Button(btnframe, text="Previous",
                    command=self.prev_page)
                prevbtn.pack(side='right', anchor='e', padx=6)

                if indx == len(self._children) - 1:
                    nextbtn.configure(text="Finish", command=self.close)

    def next_page(self):#,variable):
        print self.current 
        if self.current == 1:
            print "Page 1" , self.variables
        self.current += 1

    def prev_page(self):
        self.current -= 1

    def close(self):
        self.master.destroy()

    def add_empty_page(self):
        child = ttk.Frame(self)
        self._children[len(self._children)] = child
        self.add(child)

    def add_page_body(self, body):
        body.pack(side='top', fill='both', padx=6, pady=12)
        
    def firstpage(self, body):
        body.pack(side='top', fill='both', padx=6, pady=12)
        img =Tkinter.PhotoImage(file="bbimtrans.gif")
        bImg = Tkinter.Label(body, image=img)
        bImg.img = img
        bImg.pack(pady=20)
        desc=ttk.Label(body, text='Welcome to the BrainBox Wizard. Please follow the wizard in order to register\nyour device and callibrate the BCI headset with your appplications.\nPlease connect the headset into the USB port.').pack(pady = 20)

    def secondpage(self, body):
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
        
    def thirdpage(self, body):
        body.pack(side='top', fill='both', padx=6, pady=12)
        img =Tkinter.PhotoImage(file="brainboxwizcor.gif")
        bImg = Tkinter.Label(body, image=img)
        bImg.img = img
        bImg.pack(pady=20)
        desc=ttk.Label(body, text='Your are now registered, you may know begin\nusing BrainBox! Have a nice day!').pack(pady = 20)

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
    variables = 0
    root = Tkinter.Tk()
    wizard = Wizard(npages=3)
    wizard.master.minsize(400, 350)
    page0 = ttk.Label(wizard.page_container(0))
    page1 = ttk.Label(wizard.page_container(1))
    page2 = ttk.Label(wizard.page_container(2))
    wizard.firstpage(page0)
    wizard.secondpage(page1)
    wizard.thirdpage(page2)
    wizard.pack(fill='both', expand=True)
    root.mainloop()

if __name__ == "__main__":
    demo()

