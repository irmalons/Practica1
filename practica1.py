#Practica 1 de programación paralela
#Irma Alonso Sánchez

from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import Manager
from random import random, randint
import math

N=5
NPROD = 5
NCONS = 1


def minimo_val(values): #función que dado el almacen values devuelve la posición y el valor del menor (sin tener en cuenta los -1)
    aux=[]
    for i in range(len(values)):
    	if values[i].value!=-1:
    		aux.append(values[i].value)
    men=min(aux)
    for i in range(len(values)):
    	if values[i].value==men:
    		ind=i
    return ind,values[ind]

#val es el valor en el almacen
#aux es una variable auxiliar de cada productor para producir los elementos de manera creciente
#sem y sem2 son los semáforos de cada productor
#N es el numero de elementos que produce cada uno y p el numero de productor
def producer(val,aux,sem,sem2,N,p):
    
    for i in range(N):
       
        print("Va a producir {}".format(p))
        print("vuelta {}".format(i))
        aux.value=aux.value+randint(0,10)
        val.value=aux.value
        print("Ha producido {}".format(val.value))
        sem.release()
        sem2.acquire()
    
    print("el productor {} ha producido todos".format(p))
    val.value=-1
    sem.release()


def fin(values): #devuelve True si todas las posiciones de values tienen un -1
    for i in range(len(values)):
        if values[i].value!=-1:
            return False
    return True

#values es la lista del almacen
#sem y sem2 son las listas de los semáforos de los productores
#N es el numero de elementos que produce cada uno 
#salida es la lista en la que guardamos los valores ordenados
def consumer(values,sem,sem2,N,salida):

    for j in range(NPROD):
        sem[j].acquire()
        
    print("Todos han producido el primero")
    
    while(not fin(values)):

        for i in range(len(values)):
            print(values[i].value)
        
        ind,m=minimo_val(values)
        
        print("el menor es {}".format(m.value))
       
        
        salida.append(values[ind].value)
        values[ind].value=-2
        
        sem2[ind].release()
        sem[ind].acquire()
    print("la lista final queda:" )
    print(salida)



def main():
    semprod=[]
    semcon=[]
    
    for i in range(NPROD):
        semprod.append(Semaphore(0))
        semcon.append(Semaphore(0))
        
    salida=Manager().list() #lista en la que guardamos la lista final ordenada
    
    values = [Value('i',0) for _ in range(NPROD)] #almacen donde se van guardando los valores que producen los productores
    aux=[Value('i',0) for _ in range(NPROD)]
    
    prodlst=[Process(target=producer, args=(values[i],aux[i],semprod[i],semcon[i],N,i)) for i in range(NPROD)]
    
    cons= Process(target=consumer, args=(values,semprod,semcon,N,salida))
    
    for p in prodlst:
        p.start()
    cons.start()
    
    for p in prodlst:
        p.join()
    cons.join()
    
if __name__ == '__main__':
    main()
                
    
                     
    
