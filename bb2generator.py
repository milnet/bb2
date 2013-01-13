# -*- coding: cp1252 -*-
import os,copy
from itertools import combinations_with_replacement, product
from Tkinter import *
import tkMessageBox
M=[[2,0,1,1,2],
   [0,4,2,4,1],
   [3,2,1,1,3],
   [1,4,1,4,1],
   [3,2,4,4,2],
   [3,1,3,4,1]]
M_TOTAL=[]
movs=[]
Maux=[]
MAXF=6
MAXC=5
bubbles={}
puntuacio=0
INC_PUNT=10
def guarda(w,t):
    global bubbles
    total=""
    for i in bubbles.keys():
        if bubbles[i]=="white":
            total+="0"
        elif bubbles[i]=="red":
            total+="1"
            bubbles[i]="white"
        elif bubbles[i]=="green":
            total+="2"
            bubbles[i]="white"
        elif bubbles[i]=="yellow":
            total+="3"
            bubbles[i]="white"
        elif bubbles[i]=="blue":
            total+="4"
            bubbles[i]="white"
        w.itemconfig(i,fil="white")
    f=open("levels.txt","a")
    f.write("\n"+total)
    f.close()
def changeColor(event):
    global bubbles
    id=event.widget.find_closest(event.x, event.y)[0]
    if bubbles[id]=="white":
        event.widget.itemconfig(id,fill="red")
        bubbles[id]="red"
    elif bubbles[id]=="red":
        event.widget.itemconfig(id,fill="green")
        bubbles[id]="green"
    elif bubbles[id]=="green":
        event.widget.itemconfig(id,fill="yellow")
        bubbles[id]="yellow"
    elif bubbles[id]=="yellow":
        event.widget.itemconfig(id,fill="blue")
        bubbles[id]="blue"
    elif bubbles[id]=="blue":
        event.widget.itemconfig(id,fill="white")
        bubbles[id]="white"
        
def deleteBubble(event):
    global bubbles
    id=event.widget.find_closest(event.x, event.y)[0]
    event.widget.itemconfig(id,fill="white")
    bubbles[id]="white"
bubblesC={}    
def main():
    global MAXF, MAXC,bubbles,bubblesC
    d=41
    root=Tk()
    balls=[]
    root.title("BB2 Solver")
    w = Canvas(root, width=200, height=250, bg="white",relief=GROOVE, borderwidth=5)
    w.pack(expand=1)
    for i in range(MAXF):
        for j in range(MAXC):
            balls.append(w.create_oval(d*j+5,d*i+5,d*j+d,d*i+d,width=0,fill="white"))
            bubbles[balls[-1]]="white"
            bubblesC[balls[-1]]=[d*j+d/2,d*i+d/2]
            w.tag_bind(balls[-1], '<Button-1>', changeColor)
            w.tag_bind(balls[-1], '<B3-Motion>', deleteBubble)
            w.tag_bind(balls[-1], '<Button-3>', deleteBubble)
    f=Frame(root)
    f.pack()
    l=Label(f,text="Tocs: ").pack(side="left")
    e=Entry(f,width=3,justify="center")
    e.pack(side="right")
    b=Button(root,text="Guarda",command=lambda:guarda(w,e.get()),cursor="hand2")
    b.pack(pady=4)
    root.mainloop()
main()
##print jocAuto(3)
'''
printM()
print "\n"
intents=int(raw_input("Tocs: "))
jocAuto(intents)
os.system("pause")'''
