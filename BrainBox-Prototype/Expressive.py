from Tkinter import *
import ttk
import globalslidersend 
import threading
#import Expressivedetection1

def expression(setter,name,col,row,col1,row1,col2,row2):
        exp1 = StringVar()
        exp2 = StringVar()
        rgettt= DoubleVar()
        ttk.Label(mainframe, text=name).grid(column=col, row=row, sticky=W)
        exp_slide = ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=-50, to=50,variable=rgettt)
        exp_slide.grid(column=col1, row=row1, sticky=(W, E))

        exp_entry = ttk.Entry(mainframe, width=7,textvariable=rgettt)
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
        
root = Tk()
root.title("BrainBox | Configuration")

globalslidersend.init()

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
var = StringVar()
var.set("a")
###let it read profile names from here hossam VVVVVVVVV
d=ttk.OptionMenu(root, var, "asdasdas","bssasd","cadasdasd")
d.grid(column=1, row=2, sticky=(N, W))

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


t = Text(mainframe,width=40, height=10)
t.grid(column=2,row=13, sticky=(W, E))

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
ttk.Button(mainframe, text="Apply", command=slidersender).grid(column=10, row=12, sticky=W)
ttk.Button(mainframe, text="Update BrainPrint", command=slidersender).grid(column=10, row=11, sticky=W)
#raise_entry.focus()

root.bind('<Return>', slidersender)

root.mainloop()


