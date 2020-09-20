#!/usr/bin/env python
# coding: utf-8


from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
from numpy import pi, random, array
from math import cos, sin, e
from typing import Optional
from qiskit.circuit.library.standard_gates.rx import RXGate
from qiskit.circuit.library.standard_gates.rz import RZGate
from qiskit.circuit.library.standard_gates.z import CZGate
from qiskit.circuit.measure import Measure


def convert_angle_to_float(angle):
    """
    Convert pi to 3.14159
    angle: string type
    """
    if angle == 'pi':
        return 3.14159
    if '*' in angle:
        return float(angle[:angle.find('*')])*3.14159/float(angle[angle.find('/')+1:])
    else:
        return float(angle[:angle.find('pi')])*3.14159/float(angle[angle.find('/')+1:])




list_gate = ['id','h','x','y','z','rx','ry','rz','cx','cz']
def decompose_gate(gate):
    """
    decompose gate in the list_gate to composition of Rx, Rz, Cz
    input: gate (string type)
    output: quantum gate
    """
    if gate == 'id':
        return (RXGate(0),)
    if gate == 'h':
        return (RZGate(pi/2),RXGate(pi/2),RZGate(pi/2)) 
    if gate == 'x':
        return (RXGate(pi),)
    if gate == 'y':
        return (RZGate(pi),RXGate(pi))
    if gate == 'z':
        return (RZGate(pi),)
    if gate == 'cx':
        return RZGate(pi/2),RXGate(pi/2),RZGate(pi/2), CZGate(), RZGate(pi/2),RXGate(pi/2),RZGate(pi/2) 
    if gate == 'cz':
        return (CZGate(),)
    if 'rx' in gate:
        start = gate.find('(')		# find the angle
        end = gate.find(')')
        if 'pi' in gate:
            angle = convert_angle_to_float(gate[start+1: end])
        else:
            angle = float(gate[start+1: end])
        return (RXGate(angle),)
    if 'ry' in gate:
        start = gate.find('(')  		# find the angle
        end = gate.find(')')
        if 'pi' in gate:
            angle = convert_angle_to_float(gate[start+1: end])
        else:
            angle = float(gate[start+1: end])
        return RZGate(-pi/2),RXGate(angle),RZGate(pi/2)
    if 'rz' in gate:
        start = gate.find('(')		# find the angle
        end = gate.find(')')
        if 'pi' in gate:
            angle = convert_angle_to_float(gate[start+1: end])
        else:
            angle = float(gate[start+1: end])
        return (RZGate(angle),)
    if 'measure' in gate:
        return (Measure(),)


def compiler(qc : QuantumCircuit):
    circuit_array = qc.qasm().split('\n')    # put instruction in a list
    q = QuantumRegister(qc.num_qubits)
    c = ClassicalRegister(qc.num_clbits)
    new_circuit = QuantumCircuit(q,c)		# create circuit with the same number of qubits and cbits
    if qc.num_clbits + qc.num_qubits == 0:
        circuit_array = circuit_array[2:]
    if qc.num_clbits == 0 or qc.num_qubits == 0:
        circuit_array = circuit_array[3:]
    else:
        circuit_array = circuit_array[4:]
    for operation in circuit_array:
        if operation == "":
            break
        list_op = operation.split(" ")
        list_of_gate = decompose_gate(list_op[0])
        list_of_qubits = []
        if 'measure' in list_op[0]:		# treat measurement separately
            bits = [list_op[1],list_op[3]]
            start = bits[0].find('[')
            end = bits[0].find(']')
            index_qubit = int(bits[0][start+1:end])
            start = bits[1].find('[')
            end = bits[1].find(']')
            index_cbit = int(bits[1][start+1:end])
            new_circuit.append(list_of_gate[0], [q[index_qubit]], [c[index_cbit]])
            new_circuit.barrier()
            continue
        qubits = list_op[1].split(',')
        for qubit in qubits:
            start = qubit.find('[')
            end = qubit.find(']')
            list_of_qubits.append(q[int(qubit[start+1: end])])
        if len(list_of_qubits) == 1:
            for gate in list_of_gate:
                new_circuit.append(gate,list_of_qubits)
        else:
            for gate in list_of_gate:
                if type(gate) == CZGate:
                    new_circuit.append(gate, list_of_qubits)
                else:
                    new_circuit.append(gate, [list_of_qubits[1]])
        new_circuit.barrier()
    return new_circuit


if __name__ == '__main__':
    print('Testing...')
    q = QuantumRegister(2)
    c = ClassicalRegister(2)
    qc = QuantumCircuit(q,c)
    qc.id(q[0])
    qc.h(q[0])
    qc.cx(q[0],q[1])
    qc.rx(pi,q[0])
    qc.y(q[0])
    qc.measure([q[0],q[1]],[c[0],c[1]])
    new_circuit = compiler(qc)
    print(new_circuit.draw())




