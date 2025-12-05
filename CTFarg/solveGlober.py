import sys
import math
import os
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.qpy import load
from qiskit.circuit.library import MCXGate

# 1. Cargar el oráculo
try:
    with open(os.path.join(os.path.dirname(__file__), 'oracle.qpy'), 'rb') as f:
        circ = load(f)[0]
except FileNotFoundError:
    print("Error: 'oracle.qpy' not found.")
    sys.exit(1)

n = circ.num_qubits
N = 2**n

print(f"[*] Número de qubits (n): {n}")
print(f"[*] Espacio de búsqueda (N): {N}")

# 2. Construir el circuito de Grover (Tal cual venía en el challenge)
# Usamos el oráculo para ver qué estado marca.
# Nota: Para encontrar el secreto, a veces basta con correrlo pocas veces 
# o inspeccionar el circuito, pero usaremos la simulación provista.
circ_decomposed = transpile(circ, basis_gates=['u', 'cx', 'id'])
oracle_gate = circ_decomposed.to_gate(label='Oracle')

qc = QuantumCircuit(n, n)
qc.h(list(range(n)))

# Ejecutamos Grover. Con 1 iteración suele bastar para ver el pico en el simulador
iterations_run = 1 
for _ in range(iterations_run):
    qc.append(oracle_gate, list(range(n)))
    qc.h(list(range(n)))
    qc.x(list(range(n)))
    qc.h(n - 1)
    mcx_gate = MCXGate(n - 1)
    qc.append(mcx_gate, list(range(n)))
    qc.h(n - 1)
    qc.x(list(range(n)))
    qc.h(list(range(n)))

qc.measure(list(range(n)), list(range(n)))

# 3. Simular para encontrar el 'secret'
backend = Aer.get_backend('qasm_simulator')
qc_transpiled = transpile(qc, backend)
job = backend.run(qc_transpiled, shots=4096)
result = job.result()
counts = result.get_counts()

# El 'secret' es el estado con mayor número de conteos (el pico de probabilidad)
# max(counts, key=counts.get) nos da el string binario (ej: '1010')
binary_secret = max(counts, key=counts.get)
secret_int = int(binary_secret, 2)

print(f"[*] Estado más probable (binario): {binary_secret}")
print(f"[*] Secreto (int): {secret_int}")

# 4. Calcular las iteraciones óptimas teóricas
# Fórmula: (pi / 4) * sqrt(N)
optimal_iterations = (math.pi / 4) * math.sqrt(N)
optimal_iterations_floor = math.floor(optimal_iterations)

print(f"[*] Iteraciones óptimas calculadas: {optimal_iterations}")
print(f"[*] Parte entera de iteraciones óptimas: {optimal_iterations_floor}")

# 5. Calcular la Flag
# Flag = UNLP{secret * floor(optimal_iterations)}
flag_number = secret_int * optimal_iterations_floor
flag = f"UNLP{{{flag_number}}}"

print(f"\n>>> LA FLAG ES: {flag}")