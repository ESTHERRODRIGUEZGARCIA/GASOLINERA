#simulación de una gasolinera en la que:
#hay n surtidores
#se generan 50 coches que son threads
#a la gasolinera llgan coches de forma aleatoria de hasta 15 minutos
#cuando un coche se pone en el surtidor, se baja el conductor, elige el combistible y elige la cantidad y llena el depósito entre 5 y 10 minutos
#luego paga en una caja única y se va
#en pagar se tarda 3 minutos
#al irse, queda el surtidor libre

#importo las librerías necesarias
import random
import threading
import time
from queue import Queue
from threading import Semaphore

coches = Queue(50)
surtidores = Semaphore(1)
tiempo_llegada = 900 #15 minutos

#creo las funciones
def coche(id):
    global coches
    global surtidores
    global tiempo_llegada

    while True:
        coches.put()
        surtidores.acquire()
        print("El coche", id, "se pone en el surtidor\n")
        coches.task_done()
        #tiempo de llegada de los coches
        time.sleep(random.randint(0,tiempo_llegada))
        #se baja el conductor
        print("El conductor baja del coche\n")
        #se elige el combustible
        combustible = random.randint(0,1)
        if combustible == 0:
            print("El conductor elige gasolina\n")
        else:
            print("El conductor elige diesel\n")
        #el conductor llena el depósito
        cantidad = random.randint(5,10)
        print("El conductor elige una cantidad de", cantidad, "litros\n")
        print("El conductor llena el depósito\n")
        time.sleep(0.1)
        #se paga en la caja única
        print("El conductor paga en la caja única\n")
        time.sleep(0.1)
        #se va
        print("El conductor se va\n")
        coches.get()


def main():
    global coches
    global surtidores
    global tiempo_llegada
    #creo los threads
    for i in range(50):
        coches.put(i)
    for i in range(50):
        threading.Thread(target=coche).start()


if __name__ == "__main__":
    main()
