from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from task3 import compiler
from numpy import pi

q = QuantumRegister(4)
c = ClassicalRegister(1)
qc = QuantumCircuit(q,c)
qc.draw()
qc.id(q[0])
qc.h(q[0])
qc.cx(q[0],q[3])
qc.rx(pi,q[2])
qc.y(q[0])
qc.measure(q[0], c[0])
qc.draw()
new_circuit = compiler(qc)
print(new_circuit.depth())
print(new_circuit.size())
print(new_circuit.draw())

