from Tkinter import *
from ttk import *
import ttk
import globalslidersend 
import threading

root = Tk()
root.title("BrainBox | Configuration")
globalslidersend.init()
note = Notebook(root,  padding="3 3 12 12")
note.grid(column=0, row=0, sticky=(N, W, E, S))

def fieldandlabel(tab,ltext,val,col1,row1,col2,row2,setter):
	label=ttk.Label(tab, text=ltext).grid(column=col1, row=row1, sticky=W)
        field = ttk.Entry(tab, width=7,textvariable=val)
	field.grid(column=col2,row=row2, sticky=(W, E))

def overview(tab):
	startserver=ttk.Button(tab, text='Start Serfer ya toto', command=root.destroy)
	startserver.grid(column=1, row=10, sticky=W)
	startserver=ttk.Button(tab, text='Stop Server', command=root.destroy)
	startserver.grid(column=2, row=10, sticky=W)

	userlabel=ttk.Label(tab, text="Username: ").grid(column=1, row=1, sticky=W)
	username=ttk.Label(tab, text="USERNAME FROM DATA FILE").grid(column=2, row=1, sticky=W)
	username=ttk.Label(tab, text="STATUS").grid(column=1, row=2, sticky=W)

def settings(tab):
	fieldandlabel(tab,"Server Port: ", "1101", 1, 2, 2, 2,"port")
	fieldandlabel(tab,"Bluetooth Port: ", "1101", 1, 4, 2, 4,"port")
	fieldandlabel(tab,"Address ", "127.0.0.1", 1, 6, 2, 6,"127.0.0.1")
	
def expression(setter,name,col,row,col1,row1,col2,row2):
        exp1 = StringVar()
        exp2 = StringVar()	
        rgettt= DoubleVar()
        ttk.Label(tab2, text=name).grid(column=col, row=row, sticky=W)
        exp_slide = ttk.Scale(tab2, orient=HORIZONTAL, length=200, from_=-50, to=50,variable=rgettt)
        exp_slide.grid(column=col1, row=row1, sticky=(W, E))

        exp_entry = ttk.Entry(tab2, width=7,textvariable=rgettt)
        exp_entry.grid(column=col2, row=row2, sticky=(W, E))
        exp_slide.set(setter)
        return exp_slide

def slidersender(*args):
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
	userdatafile = open("UserData.txt",'w')
	
	globalslidersend.userdata[globalslidersend.indexuser]  = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"%(globalslidersend.username,float(raise_slide.get()),float(lb_slide.get()),float(rb_slide.get()),float(blink_slide.get()),float(lrb_slide.get()),float(fur_slide.get()),float(smile_slide.get()),float(clench_slide.get()),float(laugh_slide.get()),float(rs_slide.get()),float(ls_slide.get()))
	
	userdatafile.writelines(globalslidersend.userdata)
	userdatafile.close()
	print globalslidersend.slidersend  #writelines
	return globalslidersend.slidersend
    
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
overview(tab1)
settings(tab5)
#Expressive
raise_slide = expression(0,"Raise Eyebrows:",1,3,2,3,3,3)
lb_slide = expression(0,"Left Brow:",1,4,2,4,3,4)
rb_slide = expression(0,"Right Brow:",1,5,2,5,3,5)
blink_slide = expression(0,"Blink:",1,6,2,6,3,6)
lrb_slide = expression(0,"Smile:",1,7,2,7,3,7)
fur_slide = expression(0,"Furrowborrow:",1,8,2,8,3,8)
smile_slide = expression(0,"Smile:",1,9,2,9,3,9)
clench_slide = expression(0,"Clench:",1,10,2,10,3,10)
laugh_slide = expression(0,"Laugh:",1,11,2,11,3,11)
rs_slide = expression(0,"Right Smirk:",1,12,2,12,3,12)
ls_slide = expression(0,"Left Smirk:",1,13,2,13,3,13)

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

for child in tab2.winfo_children(): child.grid_configure(padx=5, pady=5)
ttk.Button(tab2, text="Apply", command=slidersender).grid(column=10, row=12, sticky=W)
ttk.Button(tab2, text="Update BrainPrint", command=slidersender).grid(column=10, row=11, sticky=W)
root.bind('<Return>', slidersender)

note.pack()
root.mainloop()
exit()
