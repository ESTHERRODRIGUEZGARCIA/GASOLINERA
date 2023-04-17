

import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor
from tkinter import *

# Define the MVC components

class Model:
    def __init__(self, n_pumps, max_wait_time, min_filling_time, max_filling_time, pay_time):
        self.n_pumps = n_pumps
        self.max_wait_time = max_wait_time
        self.min_filling_time = min_filling_time
        self.max_filling_time = max_filling_time
        self.pay_time = pay_time
        self.gas_station = GasStation(self.n_pumps, self.min_filling_time, self.max_filling_time, self.pay_time)
        self.executor = ThreadPoolExecutor(max_workers=50)

class GasStation:
    def __init__(self, n_pumps, min_filling_time, max_filling_time, pay_time):
        self.pumps = threading.Semaphore(n_pumps)
        self.checkout = threading.Lock()
        self.min_filling_time = min_filling_time
        self.max_filling_time = max_filling_time
        self.pay_time = pay_time

    def fill_gas(self, car_id):
        fuel_type = random.choice(['Regular', 'Plus', 'Premium'])
        fuel_quantity = random.randint(5, 20)
        filling_time = random.randint(self.min_filling_time, self.max_filling_time)
        print(f"Car {car_id} is filling up with {fuel_quantity} liters of {fuel_type} fuel for {filling_time} seconds...")
        time.sleep(filling_time)

    def pay(self, car_id):
        print(f"Car {car_id} is paying...")
        time.sleep(self.pay_time)

class Controller:
    def __init__(self, model):
        self.model = model
        self.view = View(self)
    
    def start(self):
        self.view.mainloop()

    def car_arrival(self):
        # Acquire a pump
        self.model.gas_station.pumps.acquire()
        print(f"Car {threading.current_thread().getName()} has pulled up to a fuel pump.")

        # Fill up the gas tank
        self.model.gas_station.fill_gas(threading.current_thread().getName())

        # Go to the checkout and pay
        self.model.gas_station.checkout.acquire()
        self.model.gas_station.pumps.release()
        print(f"Car {threading.current_thread().getName()} is at the checkout.")
        self.model.gas_station.pay(threading.current_thread().getName())
        self.model.gas_station.checkout.release()
        print(f"Car {threading.current_thread().getName()} has left the gas station.")
        
class View(Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Gas Station Simulation")
        self.geometry("400x400")
        self.btn_start = Button(self, text="Start", command=self.start_simulation)
        self.btn_start.pack(pady=20)
        self.lbl_status = Label(self, text="Click 'Start' to begin the simulation")
        self.lbl_status.pack(pady=20)

    def start_simulation(self):
        self.lbl_status.config(text="Simulation in progress...")
        self.btn_start.config(state=DISABLED)
        for i in range(50):
            self.controller.model.executor.submit(self.controller.car_arrival)
        self.controller.model.executor.shutdown(wait=True)
        self.lbl_status.config(text="Simulation complete")

# Run the simulation
model = Model(5, 10, 5, 10, 5)
controller = Controller(model)
controller.start()

