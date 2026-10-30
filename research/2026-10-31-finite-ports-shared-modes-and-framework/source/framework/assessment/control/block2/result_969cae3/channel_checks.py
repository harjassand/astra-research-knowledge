"""Finite checks for the analytic barriers; no optimization is a proof.

Uses NumPy only, and analytic native exponentials for the repeated-cycle test.
"""
import json
from math import pi, sqrt, cos, sin, ceil, log
from pathlib import Path
import numpy as np
from exact_degree5 import W5, HANDLES

D=Path(__file__).resolve().parent
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
PA={'I':I,'X':X,'Y':Y,'Z':Z}
def pauli(s):
    r=np.ones((1,1),complex)
    for c in s:r=np.kron(r,PA[c])
    return r
ID=np.eye(8,dtype=complex)
HM=pauli('IIZ')/2
F=pauli('ZXI')
HS={h:pauli(p) for h,p in HANDLES.items()}

def pulse(h,o,drift,d):
    if h=='C':
        return (cos(d/2)*ID-1j*drift*sin(d/2)*2*HM) @ (cos(d)*ID-1j*o*sin(d)*HS[h])
    r=sqrt(1.25)
    return cos(r*d)*ID-1j*sin(r*d)/r*(drift*HM+o*HS[h])

def cycle(d):
    rows=[]; sm=np.zeros((64,64),complex)
    for sa in (-1,1):
        for sb in (-1,1):
            ss={'A':sa,'B':sb,'C':sa*sb}
            u=ID.copy()
            for j,(h,o) in enumerate(W5+W5[::-1]):
                u=pulse(h,o*ss[h],1 if j<46 else -1,d)@u
            rows.append(float(np.linalg.norm(u.conj().T@u-ID,2)))
            sm+=np.kron(u.conj(),u)/4
    return sm,max(rows)

def main():
    moments=[]
    for n in (3,9):
        t=np.eye(n,dtype=complex)
        for j in range(n):
            for k in range(n):
                if j>k:t[j,k]=-1j
                elif j<k:t[j,k]=1j
        v=np.exp(1j*pi*np.arange(n)/n)/sqrt(n)
        ev=1-1/np.tan(pi/(2*n))
        assert np.linalg.norm(t@v-ev*v)<1e-12
        bound=-ev/(n-1)
        moments.append({'moments':n-1,'minimum_eigenvalue':ev,'error_lower_bound':bound})
    e=(sqrt(3)-1)/2
    p=(3-sqrt(3))/6
    zs=[-1,np.exp(-1j*pi/3)]
    m=[p*zs[0]**k+(1-p)*zs[1]**k for k in (1,2)]
    assert all(abs(abs(z+1j)-e)<1e-14 for z in m)
    result={'moment_barriers':moments,'sharp_two_point':{'epsilon':e,'p_at_minus_one':p,'moments':[[z.real,z.imag] for z in m]},'triangular_bath_cycles':[]}
    delta=F/4 # difference of rho_+ and rho_- on D times I_M/2
    vec=delta.reshape(64,order='F')
    for d in (.02,.01,.005,.0025):
        ch,uerr=cycle(d)
        m=ceil(log(1/d)/(33800*d**4))
        n=ceil(pi/(128*d**5))
        evolved=(np.linalg.matrix_power(ch,m)@vec).reshape((8,8),order='F')
        tn=float(np.linalg.svd(evolved,compute_uv=False).sum())
        row={'d':d,'intermediate_cycles':m,'nominal_degree5_gate_cycles':n,
             'joint_state_pair_distance_after_intermediate_cycles':tn,
             'initial_pair_distance':2,'gate_error_lower_bound_from_contraction':1-tn/2,
             'max_single_unitary_defect':uerr,
             'nominal_total_duration':92*d*n,'nominal_segments':92*n}
        result['triangular_bath_cycles'].append(row)
    print(json.dumps(result,indent=2))
    (D/'channel_check_results.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
