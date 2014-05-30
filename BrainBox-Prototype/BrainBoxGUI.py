from Tkinter import *
import ttk
import globalslidersend 
import threading
import Expressivedetection1


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
    print globalslidersend.slidersend
    return globalslidersend.slidersend
        
root = Tk()
root.title("BrainBox | Configuration")

globalslidersend.init()

threadexp = threading.Thread(target=Expressivedetection1.main)
threadexp.start()




mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

##Raise Eyebrows Slider
raise1 = StringVar()
raise2 = StringVar()
rgettt= DoubleVar()
ttk.Label(mainframe, text="Raise Eyebrows:").grid(column=1, row=1, sticky=W)
raise_slide = ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=-50, to=50,variable=rgettt)
raise_slide.grid(column=2, row=1, sticky=(W, E))

raise_entry = ttk.Entry(mainframe, width=7,textvariable=rgettt)
raise_entry.grid(column=3, row=1, sticky=(W, E))
raise_slide.set(0)
###
##Left Brow Slider
l1 = StringVar()
l2 = StringVar()
lgettt= DoubleVar()
ttk.Label(mainframe, text="Left Wink:").grid(column=1, row=2, sticky=W)
lb_slide = ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=-50, to=50,variable=lgettt)
lb_slide.grid(column=2, row=2, sticky=(W, E))

lb_entry = ttk.Entry(mainframe, width=7,textvariable=lgettt)
lb_entry.grid(column=3, row=2, sticky=(W, E))
lb_slide.set(0)
###
##rIGHT Brow Slider
r1 = StringVar()
r2 = StringVar()
rigettt= DoubleVar()
ttk.Label(mainframe, text="Right Wink:").grid(column=1, row=3, sticky=W)
rb_slide = ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=-50, to=50,variable=rigettt)
rb_slide.grid(column=2, row=3, sticky=(W, E))

rb_entry = ttk.Entry(mainframe, width=7,textvariable=rigettt)
rb_entry.grid(column=3, row=3, sticky=(W, E))
rb_slide.set(0)
###
##Blink Slider
blink1 = StringVar()
blink2 = StringVar()
blinkgettt= DoubleVar()
ttk.Label(mainframe, text="Blink:").grid(column=1, row=4, sticky=W)
blink_slide = ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=-50, to=50,variable=blinkgettt)
blink_slide.grid(column=2, row=4, sticky=(W, E))
blink_entry = ttk.Entry(mainframe, width=7,textvariable=blinkgettt)
blink_entry.grid(column=3, row=4, sticky=(W, E))
blink_slide.set(0)
###
##Look Right/Left Slider
lr1 = StringVar()
lr2 = StringVar()
lrgettt= DoubleVar()
ttk.Label(mainframe, text="Look Left/Right:").grid(column=1, row=5, sticky=W)
lrb_slide = ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=-50, to=50,variable=lrgettt)
lrb_slide.grid(column=2, row=5, sticky=(W, E))
lrb_entry = ttk.Entry(mainframe, width=7,textvariable=lrgettt)
lrb_entry.grid(column=3, row=5, sticky=(W, E))
lrb_slide.set(0)
###
##FurrowBrow Slider
fur1 = StringVar()
fur2 = StringVar()
furgettt= DoubleVar()
ttk.Label(mainframe, text="Furrow Brow:").grid(column=1, row=6, sticky=W)
fur_slide = ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=-50, to=50,variable=furgettt)
fur_slide.grid(column=2, row=6, sticky=(W, E))
fur_entry = ttk.Entry(mainframe, width=7,textvariable=furgettt)
fur_entry.grid(column=3, row=6, sticky=(W, E))
fur_slide.set(0)
###
##Smile Slider
smile1 = StringVar()
smile2 = StringVar()
smilegettt= DoubleVar()
ttk.Label(mainframe, text="Smile:").grid(column=1, row=7, sticky=W)
smile_slide = ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=-50, to=50,variable=smilegettt)
smile_slide.grid(column=2, row=7, sticky=(W, E))

smile_entry = ttk.Entry(mainframe, width=7,textvariable=smilegettt)
smile_entry.grid(column=3, row=7, sticky=(W, E))
smile_slide.set(0)
###
##Clench Slider
clench1 = StringVar()
clench2 = StringVar()
clenchgettt= DoubleVar()
ttk.Label(mainframe, text="Clench:").grid(column=1, row=8, sticky=W)
clench_slide = ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=-50, to=50,variable=clenchgettt)
clench_slide.grid(column=2, row=8, sticky=(W, E))
clench_entry = ttk.Entry(mainframe, width=7,textvariable=clenchgettt)
clench_entry.grid(column=3, row=8, sticky=(W, E))
clench_slide.set(0)
###
##laugh Slider
laugh1 = StringVar()
laugh2 = StringVar()
laughgettt= DoubleVar()
ttk.Label(mainframe, text="Laugh:").grid(column=1, row=9, sticky=W)
laugh_slide = ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=-50, to=50,variable=laughgettt)
laugh_slide.grid(column=2, row=9, sticky=(W, E))
laugh_entry = ttk.Entry(mainframe, width=7,textvariable=laughgettt)
laugh_entry.grid(column=3, row=9, sticky=(W, E))
laugh_slide.set(0)
###
##right smirk Slider
rs1 = StringVar()
rs2 = StringVar()
rsgettt= DoubleVar()
ttk.Label(mainframe, text="Right Smirk:").grid(column=1, row=10, sticky=W)
rs_slide = ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=-50, to=50,variable=rsgettt)
rs_slide.grid(column=2, row=10, sticky=(W, E))
rs_entry = ttk.Entry(mainframe, width=7,textvariable=rsgettt)
rs_entry.grid(column=3, row=10, sticky=(W, E))
rs_slide.set(0)
###
##leftsmirk Slider
ls1 = StringVar()
ls2 = StringVar()
lsgettt= DoubleVar()
ttk.Label(mainframe, text="Left Smirk:").grid(column=1, row=11, sticky=W)
ls_slide = ttk.Scale(mainframe, orient=HORIZONTAL, length=200, from_=-50, to=50,variable=lsgettt)
ls_slide.grid(column=2, row=11, sticky=(W, E))
ls_entry = ttk.Entry(mainframe, width=7,textvariable=lsgettt)
ls_entry.grid(column=3, row=11, sticky=(W, E))
ls_slide.set(0)
###
t = Text(mainframe,width=40, height=10)
t.grid(column=2,row=12, sticky=(W, E))

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
ttk.Button(mainframe, text="Apply", command=slidersender).grid(column=10, row=12, sticky=W)
#raise_entry.focus()

root.bind('<Return>', slidersender)

root.mainloop()
