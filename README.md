def run_simulation(self):
        random.seed(RANDOM_SEED)
        self.env.process(self.generate_processes())
        self.env.run()
        return sum(self.completion_times) / len(self.completion_times) if self.completion_times else 0


# Ejecutar simulaciones y almacenar resultados
results = {interval: [] for interval in ARRIVAL_INTERVALS}
for interval in ARRIVAL_INTERVALS:
    for num_processes in PROCESS_COUNTS:
        sim = SimulationSystem(num_processes, interval)
        avg_time = sim.run_simulation()
        results[interval].append((num_processes, avg_time))

# Graficar resultados
plt.figure(figsize=(8, 5))
colors = ['b', 'g', 'r']  # Colores para cada curva
for i, (interval, data) in enumerate(results.items()):
    x, y = zip(*data)
    plt.plot(x, y, marker='o', linestyle='-', color=colors[i], label=f'Intervalo {interval}')

plt.xlabel('Número de procesos')
plt.ylabel('Tiempo promedio')
plt.title('Simulación de procesos con SimPy')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("simulacion_procesos_clases.png")
plt.show()

print("Gráfica guardada")
