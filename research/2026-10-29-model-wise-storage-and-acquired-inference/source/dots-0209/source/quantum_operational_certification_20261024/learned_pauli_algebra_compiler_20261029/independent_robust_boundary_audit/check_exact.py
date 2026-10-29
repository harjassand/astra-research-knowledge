"""Independent exact rational mass checks, plus dense operational fidelity fixtures."""
from fractions import Fraction as F
from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from compiled_frame_api_v2 import compile_frame,logical_label
from algebra_compiler_v1 import unitary,pauli

def parity(x):return x.bit_count()%2

def subs(n):
    allsubs={frozenset([0])}; frontier=list(allsubs)
    while frontier:
        T=frontier.pop()
        for z in range(1<<n):
            if z not in T:
                U=T|frozenset(x^z for x in T)
                if U not in allsubs:allsubs.add(U);frontier.append(U)
    return allsubs

def bits(z,n):return [(z>>i)&1 for i in range(n)]

records=[];tests=0;maxerr=0.;fixtures=0
for n in range(1,5):
    SS=subs(n)
    for s in range(1<<(n-1)):
        a=s|(1<<(n-1));S={z for z in range(1<<n) if not parity(a&z)}
        for eta in [F(0),F(1,10),F(1,4),F(1,2)]:
            c=1-2*eta
            p={z:(1+c*(-1)**parity(a&z))/(1<<n) for z in range(1<<n)}
            assert sum(p.values())==1 and min(p.values())>=0
            for T in SS:
                annihilates=all(not parity(a&t) for t in T)
                assert sum(p[z] for z in T)==F(len(T),1<<n)*(1+c*annihilates)
                if len(T)<(1<<n):
                    for shift in range(1<<n):
                        A={z^shift for z in T};mass=sum(p[z] for z in A)
                        tests+=1
                        if mass>F(1,2):assert T==S and A==S
            if n<=3:
                rows=[[0]*n+bits(z,n) for z in S if z]
                frame=compile_frame(rows,n,1)
                assert frame['status']=='compiled'
                recovered={z for z in range(1<<n) if not any(logical_label([0]*n+bits(z,n),frame))}
                assert recovered==S
                normal=[v for v in range(1,1<<n) if all(not parity(v&z) for z in recovered)]
                assert normal==[a]
                U=np.eye(1<<n,dtype=complex)
                for g in frame['decoder_gates']:U=unitary(g,n)@U
                # Logical last qubit, gauge first n-1. Kraus operators indexed by
                # input/output gauge basis; mixed gauge contributes 1/sqrt(Dg).
                dg=1<<(n-1);fe=0.
                for z,weight in p.items():
                    P=U@pauli([0]*n+bits(z,n),n)@U.conj().T
                    for i in range(dg):
                        for j in range(dg):
                            K=P[2*i:2*i+2,2*j:2*j+2]/np.sqrt(dg)
                            fe+=float(weight)*abs(np.trace(K))**2/4
                maxerr=max(maxerr,abs(fe-float(1-eta)));assert abs(fe-float(1-eta))<1e-12
                fixtures+=1
    records.append(dict(n=n,subspaces=len(SS)))
source_files=['ROBUST_SELECTION_BOUNDARY_v1.md','compiled_frame_api_v2.py','algebra_compiler_v1.py']
out=dict(status='PASS',exact_affine_mass_checks=tests,dense_fidelity_fixtures=fixtures,max_dense_fidelity_error=maxerr,subspace_counts=records,source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in source_files})
print(json.dumps(out,indent=2))
