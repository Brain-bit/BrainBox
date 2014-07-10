from Tkinter import *
from ttk import *
import ttk
import threading
import time
import BrainBoxWizard
import Server
import NXTrobot
#import MobileApp
import sys
import MySQLdb as mdb

con = mdb.connect('brain-bit.com', 'ssmapcom_bb', 'q2564', 'ssmapcom_bb');
def updateval(username,sliderlist):
    global con
    cur = con.cursor()
    query= "UPDATE expressive SET raise=%f,lb=%f,rb=%f,blink=%f,lrb=%f,fur=%f,smile=%f,clench=%f,laugh=%f,rs=%f,ls=%f WHERE userid=%s"
    cur.execute(query, (sliderlist[0],sliderlist[1],sliderlist[2],sliderlist[3],sliderlist[4],sliderlist[5],sliderlist[6],sliderlist[7],sliderlist[8],sliderlist[9],sliderlist[10],username))

# A Function for creating an input text field and its label
def fieldandlabel(tab,ltext,val,col1,row1,col2,rw2,setter):
    label=ttk.Label(tab, text=ltext).grid(column=col1, row=row1, sticky=W,padx=5,pady=5)
    field = ttk.Entry(tab, width=7,textvariable=val)
    field.grid(column=col2,row=row2, sticky=(W, E),padx=5,pady=5)


# A Function for creating the Overview tab
def overview(tab,brainconfig,N, W, E, S):
    startserver=ttk.Button(tab, text='Start Serfer ya toto', command=brainconfig.destroy)
    startserver.grid(column=1, row=10, sticky=W,padx=5,pady=5)
    startserver=ttk.Button(tab, text='Stop Server', command=brainconfig.destroy)
    startserver.grid(column=2, row=10, sticky=W,padx=5,pady=5)

    userlabel=ttk.Label(tab, text="Username: ").grid(column=1, row=1, sticky=W,padx=5,pady=5)
    username=ttk.Label(tab, text="USERNAME FROM DATA FILE").grid(column=2, row=1, sticky=W,padx=5,pady=5)
    username=ttk.Label(tab, text="STATUS").grid(column=1, row=2, sticky=W,padx=5,pady=5)


# A Function for creating the Overview tab
def settings(tab,brainconfig,N, W, E, S):
    #brainconfig.fieldandlabel(tab,"Server Port: ", "1101", 1, 2, 2, 2,"port")
    label=ttk.Label(tab, text="Server Port: ").grid(column=1, row=2, sticky=W,padx=5,pady=5)
    field = ttk.Entry(tab, width=7,textvariable="1101")
    field.grid(column=2,row=2, sticky=(W, E),padx=5,pady=5)

    #brainconfig.fieldandlabel(tab,"Bluetooth Port: ", "1101", 1, 4, 2, 4,"port")
    label=ttk.Label(tab, text="Bluetooth Port: ").grid(column=1, row=4, sticky=W,padx=5,pady=5)
    field = ttk.Entry(tab, width=7,textvariable="1101")
    field.grid(column=2,row=4, sticky=(W, E),padx=5,pady=5)

    #brainconfig.fieldandlabel(tab,"Address ", "127.0.0.1", 1, 6, 2, 6,"127.0.0.1")
    label=ttk.Label(tab, text="Address: ").grid(column=1, row=6, sticky=W,padx=5,pady=5)
    field = ttk.Entry(tab, width=7,textvariable="127.0.0.1")
    field.grid(column=2,row=6, sticky=(W, E),padx=5,pady=5)

# A Function for creating the Expression tab
def expression(setter,name,col,row,col1,row1,col2,row2,tab,N, W, E, S):
        exp1 = Tkinter.StringVar()
        exp2 = Tkinter.StringVar()  
        rgettt= Tkinter.DoubleVar()
        ttk.Label(tab, text=name).grid(column=col, row=row, sticky=W)
        exp_slide = ttk.Scale(tab, orient=Tkinter.HORIZONTAL, length=200, from_=-50, to=50,variable=rgettt)
        exp_slide.grid(column=col1, row=row1, sticky=(W, E))

        exp_entry = ttk.Entry(tab, width=7,textvariable=rgettt)
        exp_entry.grid(column=col2, row=row2, sticky=(W, E))
        exp_slide.set(setter)
        return exp_slide

# A Function for getting the slider values, as well as the username, and saving them to UserData.txt
def slidersender():
    global username
    global raise_slide
    global lb_slide
    global lrb_slide
    global rb_slide
    global blink_slide
    global fur_slide
    global smile_slide,clench_slide,laugh_slide,rs_slide,ls_slide

    globalslidersend.slidersend = []
    globalslidersend.slidersend.append(float(raise_slide.get()))
    globalslidersend.slidersend.append(float(lb_slide.get()))
    globalslidersend.slidersend.append(float(rb_slide.get()))
    globalslidersend.slidersend.append(float(blink_slide.get()))
    globalslidersend.slidersend.append(float(lrb_slide.get()))
    globalslidersend.slidersend.append(float(fur_slide.get()))
    globalslidersend.slidersend.append(float(smile_slide.get()))
    globalslidersend.slidersend.append(float(clench_slide.get()))
    globalslidersend.slidersend.append(float(laugh_slide.get()))
    globalslidersend.slidersend.append(float(rs_slide.get()))
    globalslidersend.slidersend.append(float(ls_slide.get()))
    sliderlist= globalslidersend.slidersend    
    userdatafile = open("UserData.txt",'r')
    userdata = userdatafile.readlines()
    userdatafile.close()
    userdatafile = open("UserData.txt",'w')
    userlist,userdatalist = [],[]
    for x in range(len(userdata)):
        if userdata[x] != '\n' or userdata[x] != '':
                userdatalist.append([])
                userdalist = userdata[x].strip().split(',')
                userlist.append(userdalist[0])
    indexuser = userlist.index(username)
    userdata[indexuser]  = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"%(username,float(raise_slide.get()),float(lb_slide.get()),float(rb_slide.get()),float(blink_slide.get()),float(lrb_slide.get()),float(fur_slide.get()),float(smile_slide.get()),float(clench_slide.get()),float(laugh_slide.get()),float(rs_slide.get()),float(ls_slide.get()))    
    for x in userdata:
        userdatafile.write(x+'\n')
    userdatafile.close()


# Code to start server

threadserver = threading.Thread(target=Server.main)
threadserver.start()
time.sleep(1)
print 'server is begining to work'
threadexp = threading.Thread(target=ExpressivSuite.main)
threadexp.start()
time.sleep(3)

threadrobot = threading.Thread(target=NXTrobot.main)
threadrobot.start()

username = globalslidersend.slidersend[-1]

# Code to initiate the GUI
brainconfig = Tk()
brainconfig.title("BrainBox | Configuration")
note = Notebook(brainconfig,  padding="3 3 12 12")
note.grid(column=0, row=0, sticky=(N, W, E, S))
tab1 = Frame(note)
tab2 = Frame(note)
tab3 = Frame(note)
tab4 = Frame(note)
tab5 = Frame(note)

note.add(tab1, text = "Overview")
note.add(tab2, text = "Expressive")
note.add(tab3, text = "Cognitive")
note.add(tab4, text = "Applications")
note.add(tab5, text = "Settings")

#Overview
overview(tab1,brainconfig,N, W, E, S)
settings(tab5,brainconfig,N, W, E, S)
#Expressive Elements to exist
raise_slide = expression(0,"Raise Eyebrows:",1,3,2,3,3,3,tab2,N, W, E, S)
lb_slide = expression(0,"Left Brow:",1,4,2,4,3,4,tab2,N, W, E, S)
rb_slide = expression(0,"Right Brow:",1,5,2,5,3,5,tab2,N, W, E, S)
blink_slide = expression(0,"Blink:",1,6,2,6,3,6,tab2,N, W, E, S)
lrb_slide = expression(0,"Smile:",1,7,2,7,3,7,tab2,N, W, E, S)
fur_slide = expression(0,"Furrowborrow:",1,8,2,8,3,8,tab2,N, W, E, S)
smile_slide = expression(0,"Smile:",1,9,2,9,3,9,tab2,N, W, E, S)
clench_slide = expression(0,"Clench:",1,10,2,10,3,10,tab2,N, W, E, S)
laugh_slide = expression(0,"Laugh:",1,11,2,11,3,11,tab2,N, W, E, S)
rs_slide = expression(0,"Right Smirk:",1,12,2,12,3,12,tab2,N, W, E, S)
ls_slide = expression(0,"Left Smirk:",1,13,2,13,3,13,tab2,N, W, E, S)
raise_slide.set(globalslidersend.slidersend[0])
lb_slide.set(globalslidersend.slidersend[1])
rb_slide.set(globalslidersend.slidersend[2])
blink_slide.set(globalslidersend.slidersend[3])
lrb_slide.set(globalslidersend.slidersend[4])
fur_slide.set(globalslidersend.slidersend[5])
smile_slide.set(globalslidersend.slidersend[6])
clench_slide.set(globalslidersend.slidersend[7])
laugh_slide.set(globalslidersend.slidersend[8])
rs_slide.set(globalslidersend.slidersend[9])
ls_slide.set(globalslidersend.slidersend[10])

t = Text(tab2,width=40, height=10)
t.grid(column=2,row=14, sticky=(W, E))
for child in tab2.winfo_children():
    child.grid_configure(padx=5, pady=5)
sliderlist = slidersender()
ttk.Button(tab2, text="Update BrainPrint", command=updateval(username,sliderlist)).grid(column=10, row=11, sticky=W)
brainconfig.bind('<Return>', slidersender)

note.pack()
brainconfig.mainloop()

