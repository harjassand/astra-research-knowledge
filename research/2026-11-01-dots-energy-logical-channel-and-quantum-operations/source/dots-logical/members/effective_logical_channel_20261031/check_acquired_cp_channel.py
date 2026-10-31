#!/usr/bin/env python3
"""Independent numerical comparison of exact acquired CP certificate.
Exact CP/TP/factor identities checked by rational algebra, numerical error versus
exponential is diagnostic only; theorem provides the certified error allowance.
"""
import json,sys
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import sympy as sp
from scipy.linalg import expm
sys.set_int_max_str_digits(0)
def decode(a):return sp.Matrix([[sp.Rational(z[0],z[1])+sp.I*sp.Rational(z[2],z[3]) for z in row] for row in a])
def J_of(E):return np.array([[E[(a%2)+2*(b%2),(a//2)+2*(b//2)] for b in range(4)] for a in range(4)])
rows=[]
for name in ['effective_qubit_certificate.json','effective_qubit_certificate_1e4.json','effective_billion_spin_certificate.json']:
 p=Path(__file__).parent/name;a=json.loads(p.read_text());c=a['channel'];J=decode(c['choi']);L=decode(c['ldl_unit_lower']);ds=[sp.Rational(*x) for x in c['ldl_positive_diagonal']]
 assert all(x>0 for x in ds);assert J==J.conjugate().T;assert L*sp.diag(*ds)*L.conjugate().T==J
 assert sp.Matrix(2,2,lambda i,j:sum(J[2*i+k,2*j+k] for k in range(2)))==sp.eye(2)
 # Verify Kraus TP directly without numerical square roots: weighted column Gram.
 K=[sp.Matrix(2,2,lambda a,i:L[2*i+a,j]) for j in range(4)]
 assert sum((ds[j]*(K[j].conjugate().T*K[j]) for j in range(4)),sp.zeros(2))==sp.eye(2)
 D=float(F(*a['coefficient_rational']));X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);I=np.eye(2)
 G=-1j*(np.kron(I,X)-np.kron(X.T,I))+2*D*(np.kron(Z,Z)-np.eye(4))
 Jexactnum=J_of(expm(G));Jnum=np.array(J.evalf(17)).astype(complex)
 diff=Jnum-Jexactnum;err=float(np.abs(np.linalg.eigvalsh((diff+diff.conj().T)/2)).sum())
 budget=float(F(*c['CP_channel_error_upper']));assert err<budget
 maxbits=max(abs(v).bit_length() for row in c['choi'] for entry in row for v in entry)
 rows.append(dict(file=name,exact_CP_TP_Kraus_checks=True,numerical_diamond_upper=err,certified_budget=budget,max_choi_integer_bits=maxbits,Kraus_operators=4,environment_qubits=2))
out=dict(scope=__doc__,rows=rows)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
