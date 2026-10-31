"""Constructive real-control Clifford+T compiler and algebra diagnostics.

No gate following or hardware calibration is inferred by these matrix checks.
All original gates are compiled into reflections F_beta and two-site CZ.
"""
from pathlib import Path
import json
import numpy as np


I = np.eye(2)
H = np.array([[1,1],[1,-1]])/np.sqrt(2)
T = np.diag([1,np.exp(1j*np.pi/4)])
J = np.array([[0.,-1.],[1.,0.]])
CZ = np.diag([1.,1.,1.,-1.])
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],float)


def F(beta):
    u=np.array([np.cos(beta),np.sin(beta)])
    return I-2*np.outer(u,u)


def Ry(alpha):
    c,s=np.cos(alpha/2),np.sin(alpha/2)
    return np.array([[c,-s],[s,c]])


def embed(M,sites,n):
    """Embed a k-site matrix, sites listed in its tensor order."""
    sites=tuple(sites)
    k=len(sites)
    U=np.zeros((2**n,2**n),dtype=M.dtype)
    for col in range(2**n):
        bits=[(col>>(n-1-j))&1 for j in range(n)]
        subcol=sum(bits[q]<<(k-1-j) for j,q in enumerate(sites))
        for subrow in range(2**k):
            rb=bits.copy()
            for j,q in enumerate(sites):rb[q]=(subrow>>(k-1-j))&1
            row=sum(b<<(n-1-j) for j,b in enumerate(rb))
            U[row,col]=M[subrow,subcol]
    return U


def compile_h(q):
    return [('F',q,5*np.pi/8)]


def compile_ry(q,alpha):
    return [('F',q,0.),('F',q,alpha/4)]


def compile_cnot(c,t):
    return compile_h(t)+[('CZ',c,t)]+compile_h(t)


def compile_t(q,r,sign=1):
    # Chronological order: Ry(theta/2), CNOT, Ry(-theta/2), CNOT.
    theta=sign*np.pi/2
    return (compile_ry(r,theta/2)+compile_cnot(q,r)
            +compile_ry(r,-theta/2)+compile_cnot(q,r))


def apply_primitives(primitives,psi,n):
    for op in primitives:
        if op[0]=='F':
            psi=embed(F(op[2]),[op[1]],n)@psi
        else:
            psi=embed(CZ,[op[1],op[2]],n)@psi
    return psi


def main():
    reflection_h_error=np.linalg.norm(F(5*np.pi/8)-H,2)
    reflection_ry_error=max(np.linalg.norm(F(a/4)@F(0)-Ry(a),2)
                            for a in [-np.pi/4,np.pi/4,np.pi/2,.37])
    cnot_error=np.linalg.norm(np.kron(I,H)@CZ@np.kron(I,H)-CNOT,2)
    t_real=np.kron(T.real,I)+np.kron(T.imag,J)
    t_compiled=np.column_stack([apply_primitives(compile_t(0,1),I4,2)
                               for I4 in np.eye(4)])
    t_error=np.linalg.norm(t_compiled-t_real,2)
    minus_i=np.array([1.,-1j])/np.sqrt(2)
    rng=np.random.default_rng(20261031)
    x=rng.normal(size=2)+1j*rng.normal(size=2);x/=np.linalg.norm(x)
    catalytic_error=np.linalg.norm(t_real@np.kron(x,minus_i)-np.kron(T@x,minus_i))

    # Random, nontrivial 3-qubit circuit with 120 operations and one phase rebit.
    n=3;r=n
    psi=np.zeros(2**n,complex);psi[0]=1.
    psi_r=np.zeros(2**(n+1));psi_r[0]=1.
    counts={'H':0,'T':0,'Tdag':0,'CNOT':0,'primitive_loops':0}
    worst_error=0.
    for _ in range(120):
        typ=rng.choice(['H','T','Tdag','CNOT'])
        q=int(rng.integers(n))
        if typ=='H':
            psi=embed(H,[q],n)@psi
            primitives=compile_h(q)
        elif typ in ['T','Tdag']:
            sign=1 if typ=='T' else -1
            psi=embed(T if sign==1 else T.conj(),[q],n)@psi
            primitives=compile_t(q,r,sign)
        else:
            other=[j for j in range(n) if j!=q]
            t=int(rng.choice(other))
            psi=embed(CNOT,[q,t],n)@psi
            primitives=compile_cnot(q,t)
        counts[typ]+=1
        counts['primitive_loops']+=len(primitives)
        psi_r=apply_primitives(primitives,psi_r,n+1)
        encoded=np.stack([psi.real,psi.imag],axis=1).ravel()
        worst_error=max(worst_error,np.linalg.norm(psi_r-encoded))
    probabilities=np.sum(psi_r.reshape(-1,2)**2,axis=1)
    output_error=np.max(np.abs(probabilities-np.abs(psi)**2))
    expected=(counts['H']+10*(counts['T']+counts['Tdag'])+3*counts['CNOT'])
    assert counts['primitive_loops']==expected
    results={
        'reflection_h_error':float(reflection_h_error),
        'reflection_ry_error':float(reflection_ry_error),
        'cnot_decomposition_error':float(cnot_error),
        't_realification_decomposition_error':float(t_error),
        'catalytic_minus_i_identity_error':float(catalytic_error),
        'random_circuit_max_state_error':float(worst_error),
        'random_circuit_output_probability_error':float(output_error),
        'random_circuit_gate_counts':counts,
        'extra_rebits':1,
        'scope':'Ideal matrix compiler; finite-time gate, routing, loading and readout costs remain separate.'
    }
    for key,val in results.items():
        if key.endswith('error'):assert val<1e-10,(key,val)
    Path(__file__).with_name('rebit_compiler_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__':main()
