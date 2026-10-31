"""Exact finite-matrix witness for failure of a positive quantum bright gap.
The qutrit has code basis |s>,|d> and bright |b>. G=gI+bX>0.
A closed rank-two code-projector loop has finite leakage even as its speed goes to zero.
Run with Python, NumPy and SciPy. Floating point diagnostic, not interval proof.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm, eigh

g,b=2.,1.
Omega=(g*g-b*b)/(2*g)
X=np.array([[0.,1.],[1.,0.]])
Z=np.diag([1.,-1.])
G=g*np.eye(2)+b*X
HE=Omega*Z
Q=np.diag([0.,0.,1.])
Y=np.zeros((3,3),dtype=complex)
Y[1,2]=-1j;Y[2,1]=1j
H0=np.kron(np.eye(3),HE)+np.kron(Q,G)
psi=np.zeros(6,dtype=complex);psi[2]=1.
Pb=np.kron(Q,np.eye(2))
Rfinal=expm(-1j*np.pi*Y)
c=b/np.sqrt(g*g+b*b)
records=[]
for T in [10.,30.,100.,300.,1000.,3000.,10000.]:
    Hrot=H0-(np.pi/T)*np.kron(Y,np.eye(2))
    out=np.kron(Rfinal,np.eye(2))@expm(-1j*T*Hrot)@psi
    leak=float(np.real(out.conj()@Pb@out))
    records.append({'T':T,'bright_probability':leak})
expected=float(np.sin(np.pi*c)**2)
e,vec=eigh(HE+G)
assert np.allclose(e[0],Omega)
assert np.allclose(abs(vec[0,0]),c)
assert abs(records[-1]['bright_probability']-expected)<1e-5
# A measured Zeno path with exactly the same projectors avoids this resonance.
# All-dark branch: K = |s><s| - cos(pi/N)^N |d><d|.
zeno=[]
for N in [10,30,100,300,1000,3000,10000]:
    q=float(np.cos(np.pi/N)**N)
    zeno.append({'N':N,'survival_worst_input':q*q,
                 'failure_worst_input':1-q*q,'union_bound':N*np.sin(np.pi/N)**2})
result={'g':g,'b':b,'Omega':Omega,'gain_spectrum':np.linalg.eigvalsh(G).tolist(),
        'dark_upper_energy':Omega,'bright_spectrum':e.tolist(),
        'source_overlap':c,'asymptotic_leakage':expected,
        'adiabatic_loop':records,'same_projector_zeno_loop':zeno}
Path(__file__).with_name('positive_gap_counterexample_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
