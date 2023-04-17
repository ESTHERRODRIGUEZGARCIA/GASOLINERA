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
