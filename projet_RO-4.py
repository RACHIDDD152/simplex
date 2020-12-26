# -*- coding: utf-8 -*-
"""Created on Sun Oct 20 01:09:20 2019 @author: JABRANE"""
import tkinter
import math

from tkinter import ttk  # la bibliotheque 
from tkinter import *   
from tkinter.ttk import * 
from fractions import Fraction

firstW=tkinter.Tk() #premier fenetre pour lire les nombre de contraints et nombre de variable de decision 
firstW.title("Méthode du Simplexe")
prinW=tkinter.Tk() #fenetre pour lire   (les entrees)
prinW.title("Méthode du Simplexe") # 
prinW.withdraw() 
secoW=tkinter.Tk()#kl;
secoW.title("Méthode du Simplexe")
secoW.withdraw()  # pour masquer la fenetre secoW
s = ttk.Style() #pour configurer le style
s.configure('my.TButton', font=('Helvetica', 14))

nbrVar=0  #de decision 
nbrCon=0   #de contrainte
nbrVarArt=0  #artificielle 
nbrVarEct=0 #  d'ecart
inCo=0     # indice de colonne pivot 
inLi=0 #  indice ligne pivot
pv=0     # valeur pivot 
tst=0    #test 
tstUn=0   #garder l'ordre chronologique de fonction de phase 1
FnOb=[]   # fonction objectif
testcorrA=0  # pour tester si la correction est fait ou non 
testModifier=0  #pour tester si la modification est faite 
testchange=0  #pour passer a la phase 2
VAR=[]   # pour stocker les entrer 
inVare=[] # les coefficiet des var ecart 
inVara=[] #les coeficient des var artificielle
Tab=[] # tableau de simplex
ra=[] #pour afficher tableaux tab
boutond=""#bouton d solution direct
boutonc=""#bouton  pour afficher chaque etape

nbrVarLab=ttk.Label(text="Combien de variables de décision ?",font=("Helvetica", 14))
nbrVarLab.grid(row=0,column=0) #option d'affichage 
nbrVarEn=ttk.Entry(firstW,width=13)#champ pour entrer le nombre de variables de decision
nbrVarEn.grid(row=0,column=1,pady=5) #espace entre les boutons (pady)
nbrConLab=ttk.Label(text="Combien de contraintes?",font=("Helvetica", 14))
nbrConLab.grid(row=1,column=0)
nbrConEn=ttk.Entry(firstW,width=13)#champ pour entrer le nombre de contraintes
nbrConEn.grid(row=1,column=1,pady=5)

def valider():# affichage du tableau d'insertion 
    global firstW 
    global nbrVar
    global nbrCon
    global VAR
    prinW.update() #pour afficher la fenetre prinW 
    prinW.deiconify()
    firstW.resizable(0,100) 
    f=0 
    k=0  
    nbrVar=int(nbrVarEn.get())# lire le nombre de variable de decision 
    nbrCon=int(nbrConEn.get()) #lire le nbr de contraint 
    VAR=[0]*(nbrCon+1)*(nbrVar+2) # tableau remplie par les zero 
    firstW.destroy()  
    for k in range(1,nbrVar+3):  #pour afficher l'entete du tableau 
        m=2*k
        a='x'+str(k)
        if k==nbrVar+2:
            a="B"
            lab1=ttk.Label(prinW,text=a,font=("Helvetica", 11))
            lab1.grid(row=0,column=m)
        elif k==nbrVar+1:
            a="OP"
            lab1=ttk.Label(prinW,text=a,font=("Helvetica", 11))
            lab1.grid(row=0,column=m)
        else:
            lab1=ttk.Label(prinW,text=a,font=("Helvetica", 11))
            lab1.grid(row=0,column=m)
       
    for i in range(nbrCon+1): # pour afficher les entrees
        for j in range(1,nbrVar+3): #Columns1
            if j==nbrVar+1:
                if i==nbrCon:
                    VAR[f]=ttk.Combobox(prinW,state="readonly",width=3)
                    VAR[f].grid(row=i+2,column=j*2)
                    VAR[f].config(value=('='))
                    VAR[f].current(0)
                else:
                    VAR[f]=ttk.Combobox(prinW,state="readonly",width=3)
                    VAR[f].grid(row=i+1,column=j*2)
                    VAR[f].config(value=('<=','>=','='))
                    VAR[f].current(0)
                    lab1=ttk.Label(prinW,text="   ")
                    s=j*2+1
                    lab1.grid(row=i+2,column=s)
                    
            elif i==nbrCon and j==nbrVar+2:
                VAR[f]=ttk.Combobox(prinW,state="readonly",width=7)
                VAR[f].grid(row=i+2,column=j*2)
                VAR[f].config(value=('MAX Z','MIN Z'))
                VAR[f].current(0)
            else:
                k=i
                if i==nbrCon:
                    k=i+1
                    lab1=ttk.Label(prinW,text="Fonction Objectif:",font=("Helvetica", 12))
                    lab1.grid(row=i+1,column=0)             
                VAR[f]=ttk.Entry(prinW,justify='center',width=15)
                
                VAR[f].grid(row=k+1,column=j*2,pady=5)
                if j<nbrVar:
                    if i==nbrCon:
                        lab1=ttk.Label(prinW,text="+")
                        s=j*2+1
                        lab1.grid(row=i+2,column=s)
                    else:
                        lab1=ttk.Label(prinW,text="+")
                        s=j*2+1
                        lab1.grid(row=i+1,column=s) 
                else:
                    lab1=ttk.Label(prinW,text="   ")
                    s=j*2+1
                    lab1.grid(row=i+2,column=s)
            f+=1
    boutonA=ttk.Button(prinW,text="valider",command=afficher)
    boutonA.grid(row=nbrCon+6,column=nbrVar*4)
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
def ajout():   #pour remplir le tableau de 2 dimention  
    f=0
    L=[[ 0 for i in range(nbrVar+2)]for i in range(nbrCon+1)]
    for i in range(nbrCon+1):
        for j in range(nbrVar+2):
            if j==nbrVar or (i==nbrCon and j==nbrVar+1):
                L[i][j]=VAR[f].get()
            else:
                L[i][j]=Fraction(VAR[f].get())
            f=f+1
    return L
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------""" 
def traiter():  # fnc qui calcule le nbr de variable artificielle et d' ecart ainsi que remplir le le premiere tableau de simplex 
    global Tab
    global nbrVarArt
    global nbrVarEct
    global inVare
    global inVara
    global nbr
    k=[]
    L=ajout()
    X="X"
    E="e"
    A="a"
    for i in range(nbrCon):#  traiter les cas de b <=0 et calculer le nbre de variable artificielle et decision 
        if L[i][nbrVar+1]==0 and L[i][nbrVar]=='>=':
            L[i][nbrVar]='<='
            for j in range(nbrVar+2):
                if type(L[i][j])!=type("x"):
                    L[i][j]=-L[i][j]
        if L[i][nbrVar+1]<0:
            for j in range(nbrVar+2):
                if j==nbrVar and L[i][j]=='<=':
                    L[i][j]='>='
                elif j==nbrVar and L[i][j]=='>=':
                    L[i][j]='<='
                elif j==nbrVar and L[i][j]=='=':
                    pass
                else:
                    L[i][j]=-L[i][j]  
        if L[i][nbrVar]=='<=':
            nbrVarEct+=1
            inVare.append(1)
            inVara.append(0)
        if  L[i][nbrVar]=='>=':
            nbrVarArt+=1
            nbrVarEct+=1
            inVare.append(1)
            inVara.append(1)
        if nbrVar and L[i][nbrVar]=='=':
            nbrVarArt+=1
            inVare.append(0)
            inVara.append(1)
    nbr=nbrVarArt
    if L[len(L)-1][nbrVar+1]=='MAX Z':# transformer le probleme max au probleme de min  
        L[len(L)-1][nbrVar+1]='MIN Z'
        for m in range(nbrVar):
            L[len(L)-1][m]=-L[len(L)-1][m]
    Tab=[[ 0 for i in range(nbrVar+nbrVarEct+nbrVarArt+3)]for i in range(nbrCon+2)] # initialiser le tableau 1 par des zero
    Tab[0][0]="" 
    q=0
    p=0
    for j in range(1,nbrVar+nbrVarEct+nbrVarArt+3):# remplir l'entet aussi inserer les coeficient des var artificielle et d'ecart 
        if j < nbrVar+1:
            Tab[0][j]=X+str(j)
        elif j<nbrVar+nbrVarEct+1:
            i=0
            while p<len(inVare):
                if inVare[p]==1:
                    Tab[0][j]=E+str(p+1)
                    Tab[p+1][j]=1
                    if inVara[p]==1:
                        Tab[p+1][j]=-1
                    p+=1 
                    break
                p+=1
        elif j<nbrVar+nbrVarEct+nbrVarArt+1:
            while q<len(inVare):
                if inVara[q]==1:
                    Tab[0][j]=A+str(q+1)
                    Tab[q+1][j]=1
                    q+=1
                    break
                q+=1
        elif j==nbrVar+nbrVarEct+nbrVarArt+1:
            Tab[0][j]="B"
        elif j==nbrVar+nbrVarEct+nbrVarArt+2:
             Tab[0][j]="Ratio"
    for i in range (1,nbrCon+2):# remplir la colonne de var de base 
        if i==nbrCon+1:
            Tab[i][0]="Cj"
        elif inVara[i-1]==1:
            Tab[i][0]=A+str(i)
        else:
            Tab[i][0]=E+str(i)
    for i in range(nbrCon+1): # les valeur de coeficient de var de decision et les valeur de B
        for j in range(nbrVar):
            Tab[i+1][j+1]=L[i][j]#pour variable de decision
            if i==nbrCon and j==nbrVar-1: 
                Tab[i+1][nbrVar+nbrVarEct+nbrVarArt+1]=0
            else:
                Tab[i+1][nbrVar+1+nbrVarEct+nbrVarArt]=L[i][nbrVar+1]#pour les valeur de b
    global FnOb
    for j in range(len(Tab[0])): #obtenir une copie de la fonction objectif 
        FnOb.append(Tab[nbrCon+1][j])
    return Tab
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
def afficher():# affichage du tableau initial
    global boutond
    global boutonc
    A=traiter() # traiter renvoie tableau entree et le stock dans A 
    prinW.destroy()
    global secoW
    secoW.update()
    secoW.deiconify()
    for i in range(nbrCon+2):
        for j in range(nbrVar+nbrVarEct+nbrVarArt+3):
            az=str(A[i][j])
            l=ttk.Label(secoW,anchor="center",width=15,relief='solid',text=az)
            l.grid(row=i+nbrCon+3,column=j+1)
    boutonc=ttk.Button(secoW,text="continuer",command=main)
    boutonc.grid(row=100,column=nbrVar+nbrVarEct+nbrVarArt+3)
    boutond=ttk.Button(secoW,text="Solution directe",command=solutuindirect)
    boutond.grid(row=100,column=1)
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
def indiceC(): #trouver l'indice colonne du pivot 
    global Tab
    global inCo
    global secoW
    mini=0
    inCo=""
    for j in range(1,nbrVar+nbrVarEct+nbrVarArt+1):
        if mini>Tab[nbrCon+1][j]:
            mini=Tab[nbrCon+1][j]
            inCo=j        
    if mini==0:
        if nbrVarArt!=0:#CAS DE PHASE 1
            pass#afficherEtapeInfo(1)
        else:#CAS DE PHASE 2
            afficherEtapeInfo(2)#pour afficher la solution finale 
        return False
    return inCo
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
def indiceL(): # trouver indice de ligne pivet 
    global Tab
    global inLi
    inLi=""
    minP=math.inf
    testDg=False
    for i in range(1,nbrCon+1):
        if (minP>Tab[i][nbrVar+nbrVarEct+nbrVarArt+2]) and (Tab[i][nbrVar+nbrVarEct+nbrVarArt+2]!=0):
            minP=Tab[i][nbrVar+nbrVarEct+nbrVarArt+2]
            inLi=i
        if Tab[i][nbrVar+nbrVarEct+nbrVarArt+2]==0:
            testDg=True
    if minP==math.inf and testDg!=True :
        afficherEtapeInfo(3)#Modele non borne
        return False
    elif testDg==True and minP==math.inf :
        afficherEtapeInfo(4)#solutions degenerees
        return False
    return inLi
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
def affinf():# coloration 
    global inLi
    global inCo
    inCo=indiceC()
    K=[]
    if inCo!=False:
        for i in range(1,nbrCon+1): # calculer ratio 
            if Tab[i][inCo]<=0:
                Tab[i][nbrVar+nbrVarEct+nbrVarArt+2]=math.inf
            else:
                Tab[i][nbrVar+nbrVarEct+nbrVarArt+2]=(Tab[i][nbrVar+nbrVarEct+nbrVarArt+1])/(Tab[i][inCo])
        inLi=indiceL()
        for i in range(nbrCon+2):
            for j in range(nbrVar+nbrVarEct+nbrVarArt+3):
                az=str(Tab[i][j])
                if (j==inCo and inLi!=False) or (i==inLi and inLi!=False):
                    ra=ttk.Label(secoW,background='yellow',anchor="center",width=15,relief='solid',text=az)
                    ra.grid(row=i+nbrCon+3,column=j+1)
                else:
                    ra=ttk.Label(secoW,anchor="center",width=15,relief='solid',text=az)
                    ra.grid(row=i+nbrCon+3,column=j+1)
        return True
    else:
        return False   
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
def calculerL(): # construire les nouveaux tab 
    global pv
    global Tab
    global inCo
    global inLi
    global nbr
    Tab[inLi][0]=Tab[0][inCo]
    pv=Tab[inLi][inCo]
    for i in range(1,nbrCon+2): #calculer toute les cases sauf ligne et colonne de pivot 
        for j in range(1,nbrVar+nbrVarEct+nbrVarArt+2):
            if i!=inLi and j!=inCo:
                Tab[i][j]=Fraction(Tab[i][j])-Fraction((Tab[i][inCo]*Tab[inLi][j]),pv)

    for j in range(1,nbrVar+nbrVarEct+nbrVarArt+2):#calculer ligne pivot
        Tab[inLi][j]=Fraction(Tab[inLi][j],pv)

    for i in range(1,nbrCon+2):#calculer colone de pivot 
        if i!=inLi:
            Tab[i][inCo]=0
    #affichage
    for i in range(nbrCon+2):
        for j in range(nbrVar+nbrVarEct+nbrVarArt+3):
            az=str(Tab[i][j])
            ra=ttk.Label(secoW,anchor="center",width=15,relief='solid',text=az)
            ra.grid(row=i+nbrCon+3,column=j+1)
    return True
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
def modifierCj():  # construire la nouvelle fonction objectif en fonction de var artificielle 
    global Tab
    global testModifier
    a="a"
    for j in range(1,nbrVar+nbrVarEct+nbrVarArt+2):
        if a in Tab[0][j]:
            Tab[nbrCon+1][j]=1
        else:
            Tab[nbrCon+1][j]=0
    testModifier=1   
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
def corrA(): #la correction de la fonction objectif 
    global Tab
    global testcorrA
    k=[]
    for i in range(nbrCon+2):
        k.append(Tab[i][0])
    for inCoVarBa in range(1,nbrVar+nbrVarEct+nbrVarArt+1):
        case=Tab[nbrCon+1][inCoVarBa]
        if Tab[0][inCoVarBa] in k and Tab[nbrCon+1][inCoVarBa]!=0:
            for j in range(1,nbrVar+nbrVarEct+nbrVarArt+2):
                Tab[nbrCon+1][j]=Fraction(Tab[nbrCon+1][j])-Fraction((case*Tab[k.index(Tab[0][inCoVarBa])][j]))
    #affichage            
    for i in range(nbrCon+2):
        for j in range(nbrVar+nbrVarEct+nbrVarArt+3):
            az=str(Tab[i][j])
            if i==nbrCon+1:
                ra=ttk.Label(secoW,background='yellow',anchor="center",width=15,relief='solid',text=az)
                ra.grid(row=i+nbrCon+3,column=j+1)
            else:
                ra=ttk.Label(secoW,anchor="center",width=15,relief='solid',text=az)
                ra.grid(row=i+nbrCon+3,column=j+1)
    testcorrA=1
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
def changeTable(): #enlever les var artificielle et recuperer la fonction objectif initaile pour lancer le phase 2
    global FnOb
    global nbrVarArt
    global nbr
    global testchange
    global boutonc
    Tab[nbrCon+1]=FnOb # la fonction objectif initiale
    for i in range(nbrCon+2):  
        Tab[i]=Tab[i][:nbrVar+nbrVarEct+1]+Tab[i][nbrVar+nbrVarEct+nbrVarArt+1:]#enlever les var artificielle
    nbrVarArt=0
    nbr=0 
    testchange=1
    for c in secoW.winfo_children():#supprimer les elemenets de seconW
            c.destroy()
            
    for i in range(nbrCon+2):#affichage du 1er tableau de phase 2
        for j in range(nbrVar+nbrVarEct+nbrVarArt+3):
            az=str(Tab[i][j])
            if i==nbrCon+1:
                ra=ttk.Label(secoW,background='yellow',anchor="center",width=15,relief='solid',text=az)
                ra.grid(row=i+nbrCon+3,column=j+1)
            else:
                ra=ttk.Label(secoW,anchor="center",width=15,relief='solid',text=az)
                ra.grid(row=i+nbrCon+3,column=j+1)
    boutonc=ttk.Button(secoW,text="continuer",command=main)#
    boutonc.grid(row=100,column=nbrVar+nbrVarEct+nbrVarArt+3)
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
info1=False
def phasU(): #phase 1
    global tstUn
    global Tab
    global info1
    if tstUn==0:
       if testModifier==0: 
           modifierCj()
       if testcorrA==0:
           corrA()
       else:
           testAffich=affinf()
           if testAffich==True:
               tstUn=1 
           if Tab[nbrCon+1][nbrVar+nbrVarEct+nbrVarArt+1]==0:
               if info1==True:
                   changeTable()
               else:
                   info1=afficherEtapeInfo(1) #fin de phase1
           elif testAffich==False:
               afficherEtapeInfo(5)#pas de solution realisable
    else:
        calculerL()
        tstUn=0
"""---------------------------------------------------------------------------------------------------------------"""
def phasD():# phase 2
    global tst
    global inLi
    global inCo
    global pv
    global Tab
    global testchange
    if testchange==1:
        corrA()
        testchange=0   
    else:
        if tst==0:#
            affinf()
            tst=1
        else:
            pv=Tab[inLi][inCo]
            calculerL()
            tst=0
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
def afficherEtapeInfo(info): # afficher des information en fonction des resultat
    global Tab
    global boutonc
    if info==1:
        info1=ttk.Label(secoW,text="fin de phase 1:Il y a une solution de base réalisable au problème, nous pouvons donc passer à la Phase II pour le calcul.",font=("Helvetica", 12))
        info1.grid(row=203,column=1,columnspan=11)
        return True
    elif info==2:#for c in secoW.winfo_children():c.destroy()
        boutonc.destroy()   
        if Solutions_infinies():
            Z="Il y a une infinité des valeurs de Xi pour cette solution , Une d'elles est:"
            info1=ttk.Label(secoW,text=Z,font=("Helvetica", 12))
            info1.grid(row=200,column=1,columnspan=6)
        z="La solution  optimale  est : z ="
        z+=str(abs(Tab[len(Tab)-1][nbrVar+nbrVarEct+1]))
        info1=ttk.Label(secoW,text=z,font=("Helvetica", 12))
        info1.grid(row=199,column=1,columnspan=3)
        for i in range(len(Tab)):
            if "X" in Tab[i][0]:
                a=Tab[i][0]
                a+=str(" = ")
                a+=str(Tab[i][nbrVar+nbrVarEct+1])
                lab1=ttk.Label(secoW,text=a,font=("Helvetica", 12))
                lab1.grid(row=i+200,column=2)
    elif info==3:
        boutonc.destroy()
        info1=ttk.Label(secoW,text=" Modèle non borné",font=("Helvetica", 12))
        info1.grid(row=202,column=1,columnspan=2)
    elif info==4:
        boutonc.destroy()
        info1=ttk.Label(secoW,text=" Solutions dégénérées",font=("Helvetica", 12))
        info1.grid(row=202,column=1,columnspan=2)
    elif info==5:
        boutonc.destroy()
        info1=ttk.Label(secoW,text=" Z!=0,alors il n’existe aucune solution réalisable.",font=("Helvetica", 12))
        info1.grid(row=202,column=1,columnspan=4)
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
def Solutions_infinies():  #tester si il y a une autre solution obtimale 
    global Tab
    K=[]
    for i in range(1,len(Tab)-1):
        K.append(Tab[i][0])
    for j in range(len(Tab[0])-2):
        if Tab[0][j] not in K and Tab[len(Tab)-1][j]==0:
            return True
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
def solutuindirect():# pour touver la solution directement 
    global Tab
    while indiceC() or Tab[nbrCon+1][nbrVar+nbrVarEct+nbrVarArt+1]==0:
        main()
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
def main():
    global boutond
    boutond.destroy()
    global nbr #nombre de var artificielle 
    global Tab  # tableau de simplex 
    if nbr!=0:
        phasU()
    else:
        phasD()    
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
boutonV=ttk.Button(firstW,text="valider",style='my.TButton',command=valider)
boutonV.grid(row=4,column=1)
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
firstW.mainloop()
