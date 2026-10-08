"""Floating transcription check of the analytically exact 405-point orbits.
This does not replace the exact star proof and is labelled FINITE-EVIDENCE.
Requires NumPy and SymPy. Exact rational selection uses SPIN2_SELECTOR.py.
"""
from pathlib import Path
from fractions import Fraction
import json, platform
import numpy as np
from sympy import S
from sympy.physics.wigner import clebsch_gordan
from SPIN2_SELECTOR import VERTICES,select,strings

d=5;j=2;m=np.arange(2,-3,-1);Jp=np.zeros((d,d),complex)
for k in range(1,d):Jp[k-1,k]=np.sqrt((j-m[k])*(j+m[k]+1))
Jy=(Jp-Jp.T)/2j;e,V=np.linalg.eigh(Jy)
nodes,weights=np.polynomial.legendre.leggauss(5);N=9
seeds=[np.array([1,0,0,0,0],complex),np.array([0,0,1,0,0],complex),np.array([1,0,0,np.sqrt(2),0],complex)/np.sqrt(3)]
ts=[]
for ell in range(1,5):
    tensors=[]
    for q in range(-ell,ell+1):
        tensors.append(np.array([[np.sqrt(5)*(-1)**(2-m2)*complex(clebsch_gordan(S(2),S(2),S(ell),S(m1),S(-m2),S(q))) for m2 in m] for m1 in m]))
    ts.append(tensors)
rows=[];sms=[]
for p,psi in enumerate(seeds):
    sm=np.zeros((25,25),complex);povm=np.zeros((5,5),complex);choi=np.zeros_like(sm);count=0
    for a in range(N):
        Ua=np.diag(np.exp(-1j*(2*np.pi*a/N)*m))
        for c in range(N):
            Uc=np.diag(np.exp(-1j*(2*np.pi*c/N)*m))
            for node,weight in zip(nodes,weights):
                Ub=(V*np.exp(-1j*np.arccos(node)*e))@V.conj().T
                v=Ua@Ub@Uc@psi;P=np.outer(v,v.conj());wt=weight/(2*N*N)
                pv=P.reshape(-1);sm+=5*wt*np.outer(pv,pv.conj());povm+=5*wt*P;choi+=5*wt*np.kron(P.T,P);count+=1
    errors=[]
    for ell,tensors in enumerate(ts):
        mu=float(VERTICES[p][ell])
        for T in tensors:errors.append(float(np.linalg.norm((sm@T.reshape(-1)).reshape(5,5)-mu*T)))
    row={'seed':'FNC'[p],'outcomes':count,'povm_sum_error':float(np.linalg.norm(povm-np.eye(5))),'max_multipole_error':max(errors),'min_choi_eigenvalue':float(np.linalg.eigvalsh(choi)[0])}
    assert count==405 and row['povm_sum_error']<1e-11 and row['max_multipole_error']<1e-11 and row['min_choi_eigenvalue']>-1e-11
    rows.append(row);sms.append(sm)

selected=select([Fraction(7,12)]*4)
mix=sum(float(w)*sm for w,sm in zip(selected['weights'],sms))
traces=np.outer(np.eye(5).reshape(-1),np.eye(5).reshape(-1))/5
expected=(np.eye(25)+5*traces)/6
mixerr=float(np.linalg.norm(mix-expected));assert mixerr<1e-11
result={'status':'FINITE-EVIDENCE','scope':'Finite orbit cubature transcription only; analytic/exact proofs separate','python':platform.python_version(),'numpy_version':np.__version__,'rows':rows,'cloner_selector':strings(selected),'cloner_depolarizing_superoperator_error':mixerr}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
