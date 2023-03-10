#Practica 1 de programación paralela
#Irma Alonso Sánchez

#Parte opcional, primera version con un array para cada productor, pero con la condición de que el número de elementos que produce cada productor sea menor que el tamaño del array k menos 1

from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import Manager
from random import random, randint
import math

N=8
NPROD = 5
NCONS = 1


def minimo_val(values): #función que dado el almacen values devuelve la posición y el valor del menor (sin tener en cuenta los -1)
    aux=[]
    for i in range(len(values)):
    	if values[i]!=-1:
    		aux.append(values[i])
    men=min(aux)
    for i in range(len(values)):
    	if values[i]==men:
    		ind=i
    return ind,values[ind]

def minimo(values,ind_con):
    values_aux=[]
    for i in range(len(values)):
        if ind_con[i]<len(values[i]):
            values_aux.append(values[i][ind_con[i]])
    ind,men=minimo_val(values_aux)
    print("el menor es {}".format(men))
    print("del productor {}".format(ind))
    print("en la posicion {}".format(ind_con[ind]))
    return ind_con[ind],ind,men

def producer(val,k,index_con,index_prod,aux,sem,sem2,N,p):
    
    for i in range(N):
       
        print("Va a producir {}".format(p))
        print("vuelta {}".format(i))
        
        aux.value=aux.value+randint(0,10)
        val[index_prod]=aux.value
        index_prod=index_prod+1
        print("Ha producido {}".format(val[i%k]))
        sem.release()
        if index_prod==index_con:
            sem2.acquire()
    
    print("el productor {} ha producido todos".format(p))
    val[index_prod]=-1
    sem.release()



def fin(values,ind_con,k): #devuelve True si todas las posiciones donde le toca al consumidor coger el elemento tienen un -1
    for i in range(len(values)):
        if values[i][ind_con[i]%k]!=-1:
                return False
    return True
    
def consumer(values,k,ind_con,sem,sem2,N,salida):

    for j in range(NPROD):
        sem[j].acquire()
        
    print("Todos han producido al menos el primero")
    
    while(not fin(values,ind_con,k)):
         
        t=0
        for i in values:
            print("almacen del productor {}".format(t))
            t +=1
            for j in i:
                print(j)
                
        print("buscamos minimo")
        
        ind,pro,m=minimo(values,ind_con)
        
        print("el menor es {}".format(m))
       
        
        salida.append(m)
        values[pro][ind]=-2
        ind_con[pro]=ind_con[pro]+1
        print("ha consumido")

        if values[pro][ind_con[pro]]==-2:
            sem2[pro].release()
            sem[pro].acquire()
        
    print("la lista final queda:" )
    print(salida)
    



def main():
    semprod=[]
    semcon=[]
    
    for i in range(NPROD):
        semprod.append(Semaphore(0))
        semcon.append(Semaphore(0))
        
    salida=Manager().list() #lista en la que guardamos la lista final ordenada
    
    k=10 #tamaño del almacen de cada productor
    values =  [Array('i',k) for _ in range(NPROD)] #almacen donde se van guardando los almacenes de los productores
    aux=[Value('i',0) for _ in range(NPROD)]
    ind_con = Array('i',NPROD)#lista con los índices con la posición donde tiene que coger el consumir el elemento que le toca
    ind_prod= Array('i',NPROD)#lista con los índices con la posición donde tiene que coger el productor el elemento que le toca
    #inicializamos los valores en 0 para los índices y en -2 para el almacén
    for i in range(NPROD):
        ind_con[i]=0
        ind_prod[i]=0
        for j in range(k):
            values[i][j]=-2
            
   

    prodlst=[Process(target=producer, args=(values[i],k,ind_con[i],ind_prod[i],aux[i],semprod[i],semcon[i],N,i)) for i in range(NPROD)]
    
    
    cons= Process(target=consumer, args=(values,k,ind_con,semprod,semcon,N,salida))
    
    for p in prodlst:
        p.start()
    cons.start()
    
    for p in prodlst:
        p.join()
    cons.join()
    
if __name__ == '__main__':
    main()
                
