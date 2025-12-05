import sys
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.qpy import load
from qiskit.circuit.library import MCXGate

try:
  with open('oracle.qpy', 'rb') as f:
    circ = load(f)[0]
except FileNotFoundError:
  print("Error: 'oracle.qpy' not found.")
  sys.exit(1)

n = circ.num_qubits

circ_decomposed = transpile(circ, basis_gates=['u', 'cx', 'id'])
oracle_gate = circ_decomposed.to_gate(label='Oracle')

qc = QuantumCircuit(n, n)
qc.h(list(range(n)))

iterations = 1

for _ in range(iterations):

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

backend = Aer.get_backend('qasm_simulator')
qc_transpiled = transpile(qc, backend)
job = backend.run(qc_transpiled, shots=2048)
result = job.result()
counts = result.get_counts()
print(counts)
