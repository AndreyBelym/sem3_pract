#!/usr/bin/env python3
from tkinter import *
from math import floor,cos,sin,sqrt
from mat3 import approx_func,func,make_approx_poly


class approx_poly:
    def __init__(self,coef):
        self.coef=coef
    def __call__(self,x):
        res=0;
        for i in range(0,len(self.coef)):
            res+=approx_func(i,x)*self.coef[i]
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
        self.canv.create_line(0,int(self.canv["height"]),
                                self.canv["width"],
                                int(self.canv["height"]),
                                width=2,arrow=LAST)
        min_=floor(-self.x0/self.zoom/self.delta)+1
        max_=floor((int(self.canv["width"])-self.x0)/self.zoom/self.delta)
        while min_<=max_:
            self.canv.create_line(self.x0+min_*self.delta*self.zoom,
                                  self.canv["height"],
                                  self.x0+min_*self.delta*self.zoom,
                                  int(self.canv["height"])-5,width=2)
            canv.create_text(self.x0+min_*self.zoom*self.delta,
                             int(self.canv["height"])-8,
                             anchor='s',text=str(min_*self.delta),
                             font="Verdana 7",justify=CENTER,fill='black')
            min_+=1
        min_=floor(-self.y0/self.zoom/self.delta)
        max_=floor((int(self.canv["height"])-self.y0)/self.zoom/self.delta)+1
        while max_>=min_:
            self.canv.create_line(3,
                                  int(self.canv["height"])-self.y0-
                                        max_*self.delta*self.zoom,
                                  8,
                                  int(self.canv["height"])-self.y0-
                                        max_*self.zoom*self.delta,
                                  width=2)
            canv.create_text(11,int(self.canv["height"])-self.y0-
                                        max_*self.delta*self.zoom,
                             anchor='w',text=str(max_*self.delta),
                             font="Verdana 7",justify=CENTER,fill='black')
            max_-=1
    def clear(self):
        self.canv.delete('all')
        self.plot()
        self.draw_orts()
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
        self._lock_x,self._lock_y=(event.x-self.x0,
                                        int(self.canv["height"])-event.y-self.y0)
    def __move_handler(self,event):
        self.x0=event.x-self._lock_x
        self.y0=int(self.canv["height"])-event.y-self._lock_y
        
        self.plot()

def add_click(event):
    try:
        x=float(addl.get())
    except:
        pass
    else:
        lb.insert(END,x)
        y=addly.get()
        try:
            if y=='':
                y=func(float(addl.get()))
            else:
                y=float(addly.get())
        except:
            pass
        else:
            lbY.insert(END,y)

def del_click(event):
    x=lb.curselection()
    while x:
        lb.delete(x[0])
        lbY.delete(x[0])
        x=lb.curselection()
        
    x=lbY.curselection()
    while x:
        lb.delete(x[0])
        lbY.delete(x[0])
        x=lbY.curselection()
def print_approx_func(n):
    if n%2:
        return 'sin({}x)'.format(round(n//2+1,4))
    else:
        return 'cos({}x)'.format(round(n//2,4))        
def print_poly(poly):
    s=''
    if len(poly)>1:    
        for i in range(len(poly)-1,0,-1):
            if poly[i]>0:
                s+='+{}{}'.format(round(poly[i],4),print_approx_func(i))
            elif poly[i]<0:
                s+='{}{}'.format(round(poly[i],4),print_approx_func(i))
    if poly[0]>0:
        s+='+{}'.format(round(poly[i],4))
    elif poly[0]<0:
        s+='{}'.format(round(poly[i],4))
    return s
            
def run_click(event):
    global poly
    x=[float(i) for i in lb.get(0, END)]
    y=[float(i) for i in lbY.get(0,END)]
    try:
        e=float(enEps.get())
        n=int(enN.get())
        if n<0:
            raise ValueError
    except:
        pass
    else:
        coeff=make_approx_poly(x,y,n,e)
        lbcoef.config(text=print_poly(coeff))
        poly=approx_poly(coeff)
        pl.plotlets=[pl.plotlets[0]]
        pl.plotlets.append(plotlet(poly,"red",3))
        pl.plot()
    
def zoom_move(event):
    pl.zoom=sclzoom.get()
    pl.plot()


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
        pass
    else:
        f1.set(str(func(x)));
        try:
            f2.set(str(poly(x)))
        except:
            pass

def yview(*args):
    lb.yview(*args)
    lbY.yview(*args)
    
def scr_set(*args):
    scr.set(*args)
    lb.yview('moveto',args[0])
    lbY.yview('moveto',args[0])
root=Tk()
root.title("Вычислительный практикум №3")

    
frm1=Frame(root,height=350)
delb=Button(frm1,text="Удалить")
delb.bind("<Button-1>",del_click)
lb = Listbox(frm1,selectmode=EXTENDED,width=5)
lbY= Listbox(frm1,selectmode=EXTENDED,width=5)
scr = Scrollbar(frm1,command=yview)
lb.configure(yscrollcommand=scr_set)
lbY.configure(yscrollcommand=scr_set)

addl=Entry(frm1,width=5)
addly=Entry(frm1,width=5)

lbEps=Label(frm1,text="Точность\nрешения\nСЛАУ:")
enEps=Entry(frm1,width=8)
lbN=Label(frm1,text="Степень\nаппрокс.\nфункции:")
enN=Entry(frm1,width=8)

addb=Button(frm1,text='+')
addb.bind("<Button-1>",add_click)
addl.bind("<Return>",add_click)
addly.bind("<Return>",add_click)
runb=Button(frm1,text="Посчитать")
runb.bind('<Button-1>',run_click)

frm1.grid(row=0,column=0)

delb.grid(row=0,column=0,columnspan=2)
lb.grid(row=1,column=0)
lbY.grid(row=1,column=1)
scr.grid(row=1,column=2,sticky=N+S+W)
addl.grid(row=3,column=0)
addly.grid(row=3,column=1)
addb.grid(row=3,column=2)
lbEps.grid(row=4,column=0,columnspan=2)
enEps.grid(row=5,column=0,columnspan=2)
lbN.grid(row=6,column=0,columnspan=2)
enN.grid(row=7,column=0,columnspan=2)
runb.grid(row=8,column=0,columnspan=2)

canv=Canvas(root,width=500,height=500,bg="white")
canv.grid(row=0,column=1)

frm2=Frame(root,height=350)
lz=Label(frm2,text="Масштаб:")
sclzoom=Scale(frm2,from_=1,to=500,orient=HORIZONTAL)
sclzoom.set(30)
ld=Label(frm2,text="Детализация:")
scldet=Scale(frm2,from_=1,to=100,orient=HORIZONTAL)
scldet.set(10)
lbcoef=Label(frm2)
lc=Label(frm2,text="Цена деления:")
ec=Entry(frm2)
l1=Label(frm2,text="Проверка точки:")
e1=Entry(frm2,width=20)
f1,f2=StringVar(),StringVar()
l2=Label(frm2,text="Значение аппроксимируемой функции:")
e2=Entry(frm2,width=20,textvariable=f1)
l3=Label(frm2,text="Значение аппроксимирующей функции:")
e3=Entry(frm2,width=20,textvariable=f2)
b2=Button(frm2,text="Посчитать")

sclzoom.bind("<B1-Motion>",zoom_move)
scldet.bind("<B1-Motion>",det_move)
ec.bind("<Return>",delta_enter)
b2.bind("<Button-1>",check)
lbcoef.grid(row=0,column=2,rowspan=2)
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

