from threading import Thread, Lock, Condition
import random
import time

class GasStation:
    def __init__(self, num_pumps):
        self.num_pumps = num_pumps
        self.pumps = [Pump(i+1) for i in range(num_pumps)]
        self.queue = []

    def get_free_pump(self):
        free_pumps = [pump for pump in self.pumps if not pump.busy]
        if free_pumps:
            return min(free_pumps, key=lambda pump: pump.num_cars)
        else:
            return None

    def add_to_queue(self, car):
        self.queue.append(car)

    def remove_from_queue(self, car):
        self.queue.remove(car)

class Car:
    def __init__(self, gas_station):
        self.gas_station = gas_station
        self.pump = None

    def choose_pump(self):
        return self.gas_station.get_free_pump()

    def fill_tank(self):
        fill_time = random.randint(5, 10)
        time.sleep(fill_time)

    def pay(self):
        pay_time = 3
        time.sleep(pay_time)

    def run(self):
        self.pump = self.choose_pump()
        while not self.pump:
            time.sleep(1)
            self.pump = self.choose_pump()

        self.pump.add_car(self)
        self.fill_tank()

        if self.gas_station.queue:
            self.gas_station.remove_from_queue(self)

        if self.pump:
            self.pump.remove_car(self)

        self.pay()

class Pump:
    def __init__(self, num):
        self.num = num
        self.busy = False
        self.num_cars = 0
        self.cars = []
        self.lock = Lock()
        self.condition = Condition()

    def add_car(self, car):
        with self.lock:
            self.busy = True
            self.num_cars += 1
            self.cars.append(car)

    def remove_car(self, car):
        with self.lock:
            self.num_cars -= 1
            self.cars.remove(car)
            if not self.cars:
                self.busy = False

    def get_num_cars(self):
        with self.lock:
            return self.num_cars

    def get_cars(self):
        with self.lock:
            return self.cars

class Producer(Thread):
    def __init__(self, gas_station, max_arrival_time):
        super().__init__()
        self.gas_station = gas_station
        self.max_arrival_time = max_arrival_time

    def run(self):
        while True:
            car = Car(self.gas_station)
            self.gas_station.add_to_queue(car)
            car_thread = Thread(target=car.run)
            car_thread.start()
            time.sleep(random.randint(1, self.max_arrival_time))

class Consumer(Thread):
    def __init__(self, gas_station):
        super().__init__()
        self.gas_station = gas_station

    def run(self):
        while True:
            pumps = self.gas_station.pumps.copy()
            random.shuffle(pumps)
            for pump in pumps:
                cars = pump.get_cars()
                for car in cars:
                    car_thread = Thread(target=car.run)
                    car_thread.start()
            time.sleep(1)
if __name__ == '__main__':
    gas_station = GasStation(num_pumps=4)

    producer = Producer(gas_station, max_arrival_time=15)
    producer.start()

    consumer = Consumer(gas_station)
    consumer.start()

    time.sleep(600)

    producer.join()

    consumer.join()

    print('Done')
