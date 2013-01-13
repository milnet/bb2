
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
def printM():
    global M
    for i in M:
        print i
def solved():
    global M
    add=0
    for i in M:
        add+=sum(i)
    if add==0:
        return True
    return False

def crearMoviments(r,c):
    moves=[]
    if r>0:
        moves.append([r-1,c,"N"])
    if r<5:
        moves.append([r+1,c,"S"])
    if c>0:
        moves.append([r,c-1,"O"])
    if c<4:
        moves.append([r,c+1,"E"])
    return moves

def eliminarMovimentsDuplicats():
    global movs,M
    aux=copy.deepcopy(movs)
    esborrar=[]
    
    for i in range(len(movs)):
        for j in range(i+1,len(movs)):
            if movs[i][0]==movs[j][0] and movs[i][1]==movs[j][1] and M[movs[i][0]][movs[i][1]]==1:
                esborrar.append(movs[j])
    for i in esborrar:
        try:
            del movs[movs.index(i)]
        except:
            pass
explotats=0                               
def actualitzarMoviments():
    global movs,M,puntuacio,INC_PUNT,explotats
    eliminarMovimentsDuplicats()
    nousMovs=[]
    for i in range(len(movs)):
        if M[movs[i][0]][movs[i][1]]==1:
            M[movs[i][0]][movs[i][1]]-=1
            for j in crearMoviments(movs[i][0],movs[i][1]):
                nousMovs.append(j)
            puntuacio+=INC_PUNT+explotats       
            explotats+=1
        elif M[movs[i][0]][movs[i][1]]>1:
            M[movs[i][0]][movs[i][1]]-=1
        elif movs[i][2]!="C":
            if movs[i][2]=="N" and movs[i][0]>0:
                movs[i][0]-=1
                nousMovs.append(movs[i])
            elif movs[i][2]=="S" and movs[i][0]<5:
                movs[i][0]+=1
                nousMovs.append(movs[i])
            elif movs[i][2]=="E" and movs[i][1]<4:
                movs[i][1]+=1
                nousMovs.append(movs[i])
            elif movs[i][2]=="O" and movs[i][1]>0:
                movs[i][1]-=1
                nousMovs.append(movs[i])
    movs=[]
    for j in nousMovs:
        movs.append(j)
        
def generarSolucions(intents):
    global M
    l=[]
    for i in range(len(M)):
        for j in range(len(M[i])):
            l.append([i,j])

    pos=combinations_with_replacement(l, intents)
    return pos

def joc():
    global M,movs
    printM()
    while not solved():
        row=int(raw_input("Fila: "))
        column=int(raw_input("Columna: "))
        movs.append([row,column,"C"])
        while len(movs)!=0:
            actualitzarMoviments()
        printM()
        
def jocAuto(intents):
    global M,movs,Maux,puntuacio,explotats,M_TOTAL
    Maux=copy.deepcopy(M)
    parcial=[]
    movs=[]
    solucions=generarSolucions(intents)
    for i in solucions:
        puntuacio=0
        for j in i:
            puntuacio=0
            explotats=0
            if M[j[0]][j[1]]!=0:
                parcial.append([j[0],j[1]])
                movs.append([j[0],j[1],"C"])
                while len(movs)!=0:
                    actualitzarMoviments()
                explotats=0
                if solved():
##                    M_TOTAL.append([copy.deepcopy(Maux),parcial[:]])
                    return parcial          

        M=copy.deepcopy(Maux)
        movs=[]
        parcial=[]
    return "ERROR"
def calcula(master,inte):
    global bubbles, bubblesC, MAXF, MAXC,puntuacio,M_TOTAL
    correct=True
    try:
        intents=int(inte)
    except:
        tkMessageBox.showwarning("Error","Escriu un número d'intents compatible")
        correct=False
    d=40
    id=1
    if correct:
        carregaM()
        resultat=jocAuto(intents)
        cont=1
        color="black"
        if resultat=="ERROR":
            tkMessageBox.showwarning("Error","Impossible resoldre amb aquest número d'intents")
        else:
            print "Resultat:",resultat
            print "Puntuacio:",puntuacio
            l=Toplevel(master)
            l.transient(master)
            l.title("Resultat")
            w = Canvas(l, width=200, height=250, bg="white",bd=5,relief=GROOVE)
            w.pack(expand=1,fill="both",side="left")
            for i in range(MAXF):
                for j in range(MAXC):
                    w.create_oval(d*j+5,d*i+5,d*j+d,d*i+d,width=0,fill=bubbles[id])
                    if [i,j] in resultat:
                        w.create_text(bubblesC[id][0],bubblesC[id][1],text=str(cont),font="arial 15",fill=color)
                        color="black"
                        cont+=1
                    id+=1
            f=Frame(l)
            f.pack(side="right", expand="yes")
            L=Label(f,text="Tocs: %d/%d\n"%(len(resultat),intents)).pack()
            for i in resultat:
                L=Label(f,text="%d-%d"%(i[0]+1,i[1]+1)).pack()
            L=Label(f,text="\n").pack()
            L=Label(f,text="Puntuació:\n").pack()
            L=Label(f,text="%d"%puntuacio).pack()
##        print M_TOTAL
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
        
def carregaM():
    global M,bubbles,MAXF,MAXC
    M=[]
    id=1
    parcial=[]
    for i in range(MAXF):
        for j in range(MAXC):
            c=bubbles[id]
            if c=="white":
                parcial.append(0)
            if c=="red":
                parcial.append(1)
            if c=="green":
                parcial.append(2)
            if c=="yellow":
                parcial.append(3)
            if c=="blue":
                parcial.append(4)
            id+=1 
        M.append(parcial)
        parcial=[] 
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
    b=Button(root,text="Calcula",command=lambda:calcula(root,e.get()),cursor="hand2")
    b.pack(pady=4)
    root.mainloop()
main()
##print jocAuto(3)
