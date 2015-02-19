# Eliminate the need to prefix everything with "tkinter."
from tkinter import *
from math import floor,cos,sin,sqrt
from mat import make_newton_poly,func
class polynomial:
    def __init__(self,coef):
        self.coef=coef
    def __call__(self,x):
        res=0;
        p_x=1
        for i in self.coef:
            res+=p_x*i
            p_x*=x
        return res
class plotlet:
    def __init__(self,f,color,width):
        self.f=f
        self.color=color
        self.width=width
class plotter:
    def __init__(self,canv=None,dx=1,zoom=1,x0=0,y0=0,delta=1,plotlets=None):
        self.canv=canv;
        self.dx=dx
        self.x0=x0
        self.y0=y0
        self.delta=delta
        self.zoom=zoom
        if plotlets:
            self.plotlets=plotlets
        else:
            self.plotlets=[]
        if canv:
            self.canv.bind('<Button-1>',self.__lock_mouse)
            self.canv.bind('<B1-Motion>',self.__move_handler)
            if plotlets:
                self.plot()
    def draw_orts(self):
        self.canv.create_line(3,self.canv["height"],3,1,width=2,arrow=LAST)
        self.canv.create_line(0,int(self.canv["height"]),self.canv["width"],int(self.canv["height"]),width=2,arrow=LAST)
        min_=floor(-self.x0/self.zoom/self.delta)+1
        max_=floor((int(self.canv["width"])-self.x0)/self.zoom/self.delta)
        while min_<=max_:
            self.canv.create_line(self.x0+min_*self.delta*self.zoom,
                                  self.canv["height"],
                                  self.x0+min_*self.delta*self.zoom,
                                  int(self.canv["height"])-5,width=2)
            canv.create_text(self.x0+min_*self.zoom*self.delta,int(self.canv["height"])-8,
                             anchor='s',text=str(min_*self.delta),
                             font="Verdana 7",justify=CENTER,fill='black')
            min_+=1
        min_=floor(-self.y0/self.zoom/self.delta)
        max_=floor((int(self.canv["height"])-self.y0)/self.zoom/self.delta)+1
        while max_>=min_:
            self.canv.create_line(3,
                                  int(self.canv["height"])-self.y0-max_*self.delta*self.zoom,
                                  8,
                                  int(self.canv["height"])-self.y0-max_*self.zoom*self.delta,
                                  width=2)
            canv.create_text(11,int(self.canv["height"])-self.y0-max_*self.delta*self.zoom,
                             anchor='w',text=str(max_*self.delta),
                             font="Verdana 7",justify=CENTER,fill='black')
            max_-=1
    def plot(self):
        self.canv.delete('all')
        maxx,maxy=int(self.canv["width"]),int(self.canv["height"])
        for plt in self.plotlets:
            if plt.f:
                x=-self.x0/self.zoom;y=plt.f(x)
                while x<maxx/self.zoom:
                    x2=x+self.dx;y2=plt.f(x2)
                    canv.create_line(self.x0+self.zoom*x, #x begin
                                     maxy-self.zoom*y-self.y0, #y begin
                                     self.x0+self.zoom*x2, #x end
                                     maxy-self.zoom*y2-self.y0, #y end
                                     width=plt.width,fill=plt.color)
                    x,y=x2,y2
        self.draw_orts()
    def __lock_mouse(self,event):
        self._lock_x,self._lock_y=event.x-self.x0,int(self.canv["height"])-event.y-self.y0
    def __move_handler(self,event):
        self.x0=event.x-self._lock_x
        self.y0=int(self.canv["height"])-event.y-self._lock_y
        
        self.plot()

def add_click(event):
    try:
        float(addl.get())
    except:
        pass
    else:
        lb.insert(END,addl.get())
def del_click(event):
    x=lb.curselection()
    while x:
        lb.delete(x[0])
        x=lb.curselection()
def run_click(event):
    global poly
    x=[float(i) for i in lb.get(0, END)]
    y=[func(i) for i in x]
    print(1)
    coeff=make_newton_poly(x,y)
    poly=polynomial(coeff)
    print(2)
    pl.plotlets.append(plotlet(poly,"red",3))
    pl.plot()
    print(3)
def zoom_move(event):
    pl.zoom=sclzoom.get()
    pl.plot()
root=Tk()
canv=Canvas(root,width=500,height=500,bg="white")

def det_move(event):
    try:
        pl.dx=1/scldet.get()
    except:
        pass
    else:
        pl.plot()

def delta_enter(event):
    try:
        pl.delta=float(ec.get())
    except:
        pass
    else:
        pl.plot()

def check(event):
    try:
        x=float(e1.get())
    except:
        exit()
    f1.set(str(func(x)));
    try:
        f2.set(str(poly(x)))
    except:
        pass
frm1=Frame(root,width=150,height=350)
delb=Button(frm1,text="Удалить")
delb.bind("<Button-1>",del_click)
lb = Listbox(frm1,selectmode=EXTENDED)
scr = Scrollbar(frm1,command=lb.yview)
lb.configure(yscrollcommand=scr.set)

addl=Entry(frm1,width=20)

addb=Button(frm1,text='+')
addb.bind("<Button-1>",add_click)
addl.bind("<Return>",add_click)
runb=Button(frm1,text="Посчитать")
runb.bind('<Button-1>',run_click)
frm1.grid(row=0,column=0)
delb.grid(row=0,column=0,columnspan=2)

lb.grid(row=1,column=0)
scr.grid(row=1,column=1,sticky=N+S)
addl.grid(row=3,column=0)
addb.grid(row=3,column=1)
runb.grid(row=4,column=0,columnspan=2)
canv.grid(row=0,column=1)

frm2=Frame(root,width=150,height=350)
lz=Label(frm2,text="Масштаб:")
sclzoom=Scale(frm2,from_=1,to=500,orient=HORIZONTAL)
sclzoom.set(30)
ld=Label(frm2,text="Детализация:")
scldet=Scale(frm2,from_=1,to=100,orient=HORIZONTAL)
scldet.set(10)
lc=Label(frm2,text="Цена деления:")
ec=Entry(frm2)
l1=Label(frm2,text="Проверка точки:")
e1=Entry(frm2,width=20)
f1,f2=StringVar(),StringVar()
l2=Label(frm2,text="Значение интерполируемой функции:")
e2=Entry(frm2,width=20,textvariable=f1)
l3=Label(frm2,text="Значение интерполирующей функции:")
e3=Entry(frm2,width=20,textvariable=f2)
b2=Button(frm2,text="Посчитать")

sclzoom.bind("<B1-Motion>",zoom_move)
scldet.bind("<B1-Motion>",det_move)
ec.bind("<Return>",delta_enter)
b2.bind("<Button-1>",check)
lz.grid(row=0,column=0)
sclzoom.grid(row=0,column=1)
ld.grid(row=1,column=0)
scldet.grid(row=1,column=1)
lc.grid(row=2,column=0)
ec.grid(row=2,column=1)
l1.grid(row=4,column=0)
e1.grid(row=5,column=0)
b2.grid(row=3,column=1,rowspan=4)
l2.grid(row=3,column=2)
e2.grid(row=4,column=2)
l3.grid(row=5,column=2)
e3.grid(row=6,column=2)
frm2.grid(row=1,column=0,columnspan=2)
mainfunc=plotlet(func,"blue",3)
pl=plotter(canv,0.1,30,plotlets=[mainfunc])
pl.plot()
root.mainloop()

