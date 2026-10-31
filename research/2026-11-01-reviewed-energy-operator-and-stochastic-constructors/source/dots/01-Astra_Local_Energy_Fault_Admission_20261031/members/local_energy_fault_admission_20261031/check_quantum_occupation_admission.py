"""Small dense diagnostic only; not a certified numerical proof or gate backend."""
import itertools, json, math
import numpy as np
from scipy.linalg import expm, eigvalsh
from pathlib import Path
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1,-1]).astype(complex)
sm=np.array([[0,1],[0,0]],complex); n=sm.conj().T@sm

def op(a,slot,total=3):
    out=np.array([[1]],complex)
    for j in range(total): out=np.kron(out,a if j==slot else I)
    return out

ns=[op(n,i) for i in range(2)]; sms=[op(sm,i) for i in range(2)]
sysX=op(X,2);sysY=op(Y,2);sysZ=op(Z,2)
D=8; Id=np.eye(D,dtype=complex)
rng=np.random.default_rng(20261031)
beta=.125; gamma=1-2*beta; b=.5; a=.2; tau=.3
hop=beta*(sms[0].conj().T@sms[1]+sms[1].conj().T@sms[0])
weight_checks=[]
for _ in range(40):
    u=rng.random(2);V=(Id+u[0]*ns[0])@(Id+u[1]*ns[1])
    comm=1j*(hop@V-V@hop)
    rhs=beta*sum(u)*(ns[0]@V/(1+u[0])+ns[1]@V/(1+u[1]))
    weight_checks.append(float(eigvalsh(rhs-comm).min()))

rows=[]
for lam in [256.,4096.]:
    jumps=[math.sqrt(lam)*s for s in sms]+[math.sqrt(a)*s.conj().T for s in sms]
    C=sum(L.conj().T@L for L in jumps)
    base=lam*hop+sysZ/3
    Ks=[math.sqrt(lam)*b*ns[0]@sysX,math.sqrt(lam)*b*ns[1]@sysY]
    jumpadj=sum(np.kron(L.T,L.conj().T) for L in jumps)
    def cross(z,w):
        effect=Id.copy()
        for j in [1,0]:
            Hz=base+z[j]*Ks[j];Hw=base+w[j]*Ks[j]
            G=(np.kron(Id,1j*Hz.conj().T-C/2)
               +np.kron((-1j*Hw-C/2).T,Id)+jumpadj)
            effect=(expm(tau*G)@effect.reshape(-1,order='F')).reshape((D,D),order='F')
        return effect
    configs=list(itertools.product([0.,1.],repeat=2))
    signs=[(-1)**(2-sum(z)) for z in configs]
    gram=np.zeros((D,D),complex)
    for z,sz in zip(configs,signs):
        for w,sw in zip(configs,signs): gram+=sz*sw*cross(z,w)
    gram=(gram+gram.conj().T)/2
    amp=math.sqrt(max(0.,float(eigvalsh(gram).max())))
    R=gamma*math.sqrt(lam)/(8*b);Cbound=(1+a*tau)/2
    eta=math.exp(Cbound/2)/(R-1)
    z=(1j*R,-1j*R)
    tilted=cross(z,z);tilted=(tilted+tilted.conj().T)/2
    tilted_norm=math.sqrt(float(eigvalsh(tilted).max()))
    rows.append(dict(lam=lam,R=R,eta=eta,selected_two_amplitude=amp,
                     selected_bound=eta**2,gram_min=float(eigvalsh(gram).min()),
                     tilted_norm=tilted_norm,tilted_bound=math.exp(Cbound),
                     tilted_hermiticity=float(np.linalg.norm(tilted-tilted.conj().T))))
    assert amp<=eta**2+1e-8
    assert tilted_norm<=math.exp(Cbound)+1e-8
assert min(weight_checks)>-1e-12
record={'scope':'Double-precision algebra/dilation diagnostic only; no certified rounding bound.',
        'source_qubits':2,'system_qubits':1,'selected_locations':2,
        'all_source_hopping_and_injection_on':True,
        'initial_state_scope':'operator Gram/effect norms, not one chosen input state',
        'min_hopping_weight_slack':min(weight_checks),'rows':rows}
print(json.dumps(record,indent=2))
if __name__=='__main__':
    Path(__file__).with_name('quantum_occupation_admission_checks.json').write_text(json.dumps(record,indent=2)+'\n')
