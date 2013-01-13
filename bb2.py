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
FILE="levels.txt"
w=None
colors=[]
NIVELL_ACTUAL=1
def llegirFitxer(level):
    global w,bubbles,colors,M
    f=open(FILE,'r')
    f.seek((level-1)*(MAXF*MAXC+2))
    l=f.readline().strip()
    cont=0
    for i in range(len(M)):
        for j in range(len(M[i])):
            if l[cont]=="0":
                color="white"
                M[i][j]=0
            if l[cont]=="1":
                color="red"
                M[i][j]=1
            elif l[cont]=="2":
                color="green"
                M[i][j]=2
            elif l[cont]=="3":
                color="yellow"
                M[i][j]=3
            elif l[cont]=="4":
                color="blue"
                M[i][j]=4
            w.itemconfig(cont+1,fill=color)
            bubbles[cont+1]=color
            cont+=1
    f.close()
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
        
def tira(event):
    global w,bubbles,movs,puntuacio,explotats,NIVELL_ACTUAL
    id=event.widget.find_closest(event.x, event.y)[0]
    cont=0
    fi=False
    for i in range(MAXF):
        for j in range(MAXC):
            cont+=1
            if cont==id:
                movs.append([i,j,"C"])
                while len(movs)!=0:
                    actualitzarMoviments()
                explotats=0
                fi=True
                break
        if fi:
            break
    agafaM()
    if solved():
        print "NIVELL",NIVELL_ACTUAL,"SOLUCIONAT"
        NIVELL_ACTUAL+=1
        llegirFitxer(NIVELL_ACTUAL)
def agafaM():
    global M,w,bubbles
    cont=0
    for i in range(len(M)):
        for j in range(len(M[i])):
            cont+=1
            color="white"
            if M[i][j]==1:
                color="red"
            elif M[i][j]==2:
                color="green"
            elif M[i][j]==3:
                color="yellow"
            elif M[i][j]==4:
                color="blue"
            w.itemconfig(cont,fill=color)
            bubbles[cont]=color
       
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

def main():
    global MAXF, MAXC,bubbles,bubblesC,w,movs,puntuacio,NIVELL_ACTUAL
    movs=[]
    puntuacio=0
    d=41
    root=Tk()
    balls=[]
    root.title("BB2 Solver")
    w = Canvas(root, width=200, height=250, bg="white",relief=GROOVE, borderwidth=5)
    w.pack(expand=1)
    for i in range(MAXF):
        for j in range(MAXC):
            balls.append(w.create_oval(d*j+5,d*i+5,d*j+d,d*i+d,width=0,fill="white"))
            w.tag_bind(balls[-1], '<Button-1>', tira)
    llegirFitxer(NIVELL_ACTUAL)
    root.mainloop()
main()
