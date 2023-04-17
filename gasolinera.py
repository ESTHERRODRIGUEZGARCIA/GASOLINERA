#simulación de una gasolinera en la que:
#hay n surtidores
#se generan 50 coches que son threads
#a la gasolinera llgan coches de forma aleatoria de hasta 15 minutos
#cuando un coche se pone en el surtidor, se baja el conductor, elige el combistible y elige la cantidad y llena el depósito entre 5 y 10 minutos
#luego paga en una caja única y se va
#en pagar se tarda 3 minutos
#al irse, queda el surtidor libre

import random
import threading
import time

#número de surtidores
surtidores = 1
#número de coches
coches = 50
#tiempo de llegada de los coches
tiempo_llegada = 900 #15 minutos
gas = threading.Semaphore(surtidores)

def coche():
    global coches
    global surtidores
    global tiempo_llegada

    while coches > 0:
        #tiempo de llegada de los coches
        time.sleep(random.randint(0,tiempo_llegada))
        #se baja el conductor
        print("El conductor baja del coche\n")
        #se elige el combustible
        combustible = random.randint(0,1)
        if combustible == 0:
            print("El conductor elige gasolina")
        else:
            print("El conductor elige diesel")
        #el conductor llena el depósito
        cantidad = random.randint(5,10)
        print("El conductor elige una cantidad de", cantidad, "litros")
        print("El conductor llena el depósito")
        time.sleep(0.1)
        #se paga en la caja única
        print("El conductor paga en la caja única")
        time.sleep(0.1)
        #se va
        print("El conductor se va")
        coches -= 1

def tiempo_medio():
    global coches
    global surtidores
    global tiempo_llegada
    #tiempo medio de llegada de los coches
    tiempo_medio_llegada = tiempo_llegada / 2
    #tiempo medio de llenado del depósito
    tiempo_medio_llenado = 5
    #tiempo medio de pago
    tiempo_medio_pago = 3
    #tiempo medio de salida
    tiempo_medio_salida = tiempo_medio_llegada + tiempo_medio_llenado + tiempo_medio_pago
    #tiempo medio de espera
    tiempo_medio_espera = tiempo_medio_salida / surtidores
    #tiempo medio de estancia
    tiempo_medio_estancia = tiempo_medio_espera + tiempo_medio_salida
    #tiempo medio de los coches
    tiempo_medio_coches = tiempo_medio_estancia * coches
    print("El tiempo medio de los coches es", tiempo_medio_coches, "segundos")

def main():
    #se crea el thread
    t = threading.Thread(target=coche)
    #se inicia el thread
    t.start()
    #se espera a que termine el thread
    t.join()
    #se calcula el tiempo medio
    tiempo_medio()


if __name__ == "__main__":
    main()
