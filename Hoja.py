import simpy
import random
import matplotlib.pyplot as plt

# Parámetros de la simulación
RANDOM_SEED = 42
MEMORY_CAPACITY = 100  # Capacidad total de RAM
CPU_CAPACITY = 2  # Número de CPUs disponibles
INSTRUCTIONS_PER_CYCLE = 3  # Instrucciones ejecutadas por ciclo

# Lista de configuraciones a probar
PROCESS_COUNTS = [25, 50, 100]  # Cantidad de procesos
ARRIVAL_INTERVALS = [10, 5, 1]  # Intervalos de llegada


class Process:
    
    def _init_(self, env, name, ram, cpu, completion_times):
        self.env = env
        self.name = name
        self.ram = ram
        self.cpu = cpu
        self.memory_needed = random.randint(1, 10)
        self.instructions = random.randint(1, 10)
        self.completion_times = completion_times
        env.process(self.run())

    def run(self):
        """Simula la ejecución de un proceso."""
        yield self.ram.get(self.memory_needed)  
        with self.cpu.request() as req:
            yield req  
            while self.instructions > 0:
                yield self.env.timeout(1) 
                self.instructions -= min(INSTRUCTIONS_PER_CYCLE, self.instructions)
        self.ram.put(self.memory_needed) 
        self.completion_times.append(self.env.now) 


class SimulationSystem:

    def _init_(self, num_processes, arrival_interval):
        self.num_processes = num_processes
        self.arrival_interval = arrival_interval
        self.env = simpy.Environment()
        self.ram = simpy.Container(self.env, init=MEMORY_CAPACITY, capacity=MEMORY_CAPACITY)
        self.cpu = simpy.Resource(self.env, capacity=CPU_CAPACITY)
        self.completion_times = []

    def generate_processes(self):
        for i in range(self.num_processes):
            Process(self.env, f'P{i}', self.ram, self.cpu, self.completion_times)
            yield self.env.timeout(random.expovariate(1.0 / self.arrival_interval))