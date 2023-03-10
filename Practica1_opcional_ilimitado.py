#Practica 1 de programación paralela
#Irma Alonso Sánchez

#Parte opcional, segunda version con un array para cada productor con capacidad limitada, pero cada productor puede producir un número de elementos mayor que la capacidad del array


from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import Manager
from random import random, randint
import math

N=11
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

def minimo(values,ind_con,k):#dado el almacen de todos los consumidores y la lista de indices que les toca coger devuelve el indice del productor, el indice de la posición dentpo de almacen de ese productor y el menor
    values_aux=[]
    for i in range(len(values)):
        values_aux.append(values[i][ind_con[i]%k])
    ind,men=minimo_val(values_aux)
    print("el menor es {}".format(men))
    print("del productor {}".format(ind))
    print("en la posicion {}".format(ind_con[ind]%k))
    return ind_con[ind],ind,men

def producer(val,k,index_con,index_prod,aux,sem,sem2,sem_k,N,p):
    
    for i in range(N):
       
        print("Va a producir {}".format(p))
        print("vuelta {}".format(i))
        
        aux.value=aux.value+randint(0,10)
        val[index_prod%k]=aux.value
        index_prod=index_prod+1
        print("Ha producido el numero {}".format(aux.value))
        sem.release()
        sem_k.acquire()
        if index_prod==index_con%k:
            sem2.acquire()
       
    print("el productor {} ha producido todos".format(p))
    val[index_prod%k]=-1
    sem.release()

def fin(values,ind_con,k): #devuelve True si todas las posiciones donde le toca al consumidor coger el elemento tienen un -1
    for i in range(len(values)):
        if values[i][ind_con[i]%k]!=-1:
                return False
    return True
    
def consumer(values,k,ind_con,sem,sem2,sem_k,N,salida):

    for j in range(len(values)):
        sem[j].acquire()
    print("Todos han producido al menos el primero")
    
    while(not fin(values,ind_con,k)):
        
        t=0
        for i in values:
            print("almacen del productor {}".format(t))
            t +=1
            for j in i:
                print(j)
                
        print("buscamos el minimo")
        
        ind,pro,m=minimo(values,ind_con,k)
        
        print("el menor es {}".format(m))
       
        salida.append(m)
        values[pro][ind%k]=-2
        ind_con[pro]=ind_con[pro]+1
        print("ha consumido")
        
        sem_k[pro].release()
        if values[pro][ind_con[pro]%k]==-2:
            sem2[pro].release()
            sem[pro].acquire()
        
        
    print("la lista final queda:" )
    print(salida)
    



def main():
    semprod=[]
    semcon=[]
    semklst=[]
    
    k=5 #capacidad del array de cada productor
    #inicializamos las listas con los semáforos para cada productor
    for i in range(NPROD):
        semprod.append(Semaphore(0))
        semcon.append(Semaphore(0))
        semklst.append(Semaphore(k-1))
        
    salida=Manager().list() #lista en la que guardamos la lista final ordenada
    
    
    values =  [Array('i',k) for _ in range(NPROD)] #almacen donde se van guardando los almacenes de los productores
    aux=[Value('i',0) for _ in range(NPROD)] #variables auxiliares para poder generar los números de forma creciente en cada productor
    ind_con = Array('i',NPROD) #lista con los índices con la posición donde tiene que coger el consumir el elemento que le toca
    ind_prod= Array('i',NPROD)#lista con los índices con la posición donde tiene que coger el productor el elemento que le toca
    #inicializamos los valores en 0 para los índices y en -2 para el almacén
    for i in range(NPROD):
        ind_con[i]=0
        ind_prod[i]=0
        for j in range(k):
            values[i][j]=-2
     
 
    prodlst=[Process(target=producer, args=(values[i],k,ind_con[i],ind_prod[i],aux[i],semprod[i],semcon[i],semklst[i],N,i)) for i in range(NPROD)]
    
    
    cons= Process(target=consumer, args=(values,k,ind_con,semprod,semcon,semklst,N,salida))
    
    for p in prodlst:
        p.start()
    cons.start()
    
    for p in prodlst:
        p.join()
    cons.join()
    
if __name__ == '__main__':
    main()
                
