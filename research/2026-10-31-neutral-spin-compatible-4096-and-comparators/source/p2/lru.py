"""A supplied teleportation leakage-reduction circuit.

The finite qutrit model tests the essential logic of an arbitrary leaked
input. The physical gate's stronger full-Fock-space property is checked
separately in run_checks.py. This is the established teleportation LRU,
not a new fault-tolerance protocol.
"""
import numpy as np
from native import kron, norm


def elementary():
    h=np.eye(3,dtype=complex)
    h[:2,:2]=np.array([[1,1],[1,-1]])/np.sqrt(2)
    x=np.eye(3,dtype=complex); x[:2,:2]=[[0,1],[1,0]]
    z=np.diag([1.,-1.,1.]).astype(complex)
    # The charge parity of a leaked state can be either sign. Choose the
    # odd sign, which can disturb a valid neighbor without leaking it.
    q=np.diag([1.,-1.,-1.])
    odd=(np.eye(3)-q)/2
    cz=np.eye(9)-2*np.kron(odd,odd)
    cnot=np.kron(np.eye(3),h)@cz@np.kron(np.eye(3),h)
    return h,x,z,cz,cnot


def branch_maps():
    """Return maps input A -> spent A,B + output C for every fine record.

    Both computational measurements have a harmless, arbitrary extension
    to leakage: a leakage result is assigned bit 1. The spent systems are
    retained, not silently traced away before checking the reference map.
    """
    h,x,z,cz,cnot=elementary()
    zero=np.array([[1.],[0.],[0.]],complex)
    bc=np.kron(zero,zero)
    bc=cnot@np.kron(h,np.eye(3))@bc
    v=np.kron(np.eye(3),bc)
    v=np.kron(cnot,np.eye(3))@v
    v=kron(h,np.eye(3),np.eye(3))@v
    maps=[]
    for a in range(3):
        for b in range(3):
            ra=int(a!=0); rb=int(b!=0)
            proj_a=np.zeros((3,3)); proj_a[a,a]=1
            proj_b=np.zeros((3,3)); proj_b[b,b]=1
            correction=np.linalg.matrix_power(z,ra)@np.linalg.matrix_power(x,rb)
            w=kron(proj_a,proj_b,correction)@v
            maps.append(((a,b),w))
    return maps


def check_lru():
    p=np.diag([1.,1.,0.]); pc=kron(np.eye(3),np.eye(3),p)
    completeness=np.zeros((3,3),complex)
    max_valid=0.; max_leakage=0.
    for (a,b),w in branch_maps():
        completeness+=w.conj().T@w
        max_leakage=max(max_leakage,norm((np.eye(27)-pc)@w))
        expected=np.zeros((27,2),complex)
        if a<2 and b<2:
            for j in range(2): expected[(a*3+b)*3+j,j]=.5
        # Some Bell branches can differ by an irrelevant scalar phase.
        actual=w[:,:2]
        ov=np.vdot(expected,actual)
        phase=ov/abs(ov) if abs(ov)>1e-14 else 1
        max_valid=max(max_valid,norm(actual-phase*expected))
    return dict(valid_reference_map_error=max_valid,
                arbitrary_input_output_leakage=max_leakage,
                completeness_error=norm(completeness-np.eye(3)),
                elementary_locations=10,
                maximum_lru_gate_locations=21)
