"""Same-tripod coherent resonance and dissipative recovery.
Exact constant co-moving-frame matrix exponentials; no time discretization.
Decay histories are charged via lost no-emission norm, not postselected away.
The final half-diamond bound is a sufficient bound on the specified initial code.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm, eigvalsh, svdvals

g=2.;beta=1.;Omega=(g*g-beta*beta)/(2*g)
X=np.array([[0.,1.],[1.,0.]])
Z=np.diag([1.,-1.])
I=np.eye(2)
G=g*I+beta*X;HE=Omega*Z
# Atom basis [spectator s, logical d, bright b, excited e].
Y=np.zeros((4,4),dtype=complex);Y[1,2]=-1j;Y[2,1]=1j
BE=np.zeros((4,4));BE[2,3]=BE[3,2]=1.
Pe=np.diag([0.,0.,0.,1.])
Pbe=np.diag([0.,0.,1.,1.])
P0=np.eye(8,dtype=complex)[:,:4]
H0=np.kron(np.eye(4),HE)+np.kron(BE,G)
Rfinal=np.kron(expm(-1j*np.pi*Y),I)
psi=np.zeros(8,dtype=complex);psi[2]=1.
c=beta/np.sqrt(2*(g*g+beta*beta))
predicted=float(np.sin(np.pi*c)**2)
records=[]
for kappa in [0.,0.5,2.,8.]:
    case=[]
    for T in [10.,30.,100.,300.,1000.,3000.,10000.]:
        Hrot=H0-(np.pi/T)*np.kron(Y,I)-0.5j*kappa*np.kron(Pe,I)
        Knj=Rfinal@expm(-1j*T*Hrot)
        out=Knj@psi
        leak=float(np.real(out.conj()@np.kron(Pbe,I)@out))
        target=np.kron(expm(-1j*np.pi*Y),expm(-1j*T*HE))@P0
        Kcode=Knj@P0
        delta=float(svdvals(Kcode-target)[0])
        qmatrix=np.eye(4)-Kcode.conj().T@Kcode
        qmax=max(0.,float(eigvalsh(qmatrix)[-1]))
        qinput=max(0.,float(1.-np.real(out.conj()@out)))
        case.append({'T':T,'no_emission_bright_excited_probability':leak,
                     'emission_probability_input':qinput,
                     'emission_probability_max_code':qmax,
                     'no_emission_operator_error':delta,
                     'full_half_diamond_upper_bound':min(1.,delta+qmax/2)})
    records.append({'kappa':kappa,'runs':case})
assert abs(records[0]['runs'][-1]['no_emission_bright_excited_probability']-predicted)<1e-5
assert records[2]['runs'][-1]['full_half_diamond_upper_bound']<0.004
result={'g':g,'beta':beta,'Omega':Omega,
        'resonant_source_overlap_including_bright_fraction':c,
        'coherent_limit_bright_excited_probability':predicted,
        'cases':records,
        'scope':'Eight dimensional exact no-emission matrices. All emissions charged. No device model or rounding certification.'}
Path(__file__).with_name('tripod_resonance_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
