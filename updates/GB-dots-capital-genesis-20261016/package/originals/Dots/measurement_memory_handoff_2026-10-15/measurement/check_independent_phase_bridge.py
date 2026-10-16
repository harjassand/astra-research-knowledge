"""Independent exact-matrix audit of endpoint-measurement virtual-frame transfer.
Two overlapping disjoint memory patches, shared noncommuting bath, then reuse.
Not a stochastic simulation or a threshold test.
"""
import itertools, json
import numpy as np
from scipy.linalg import expm
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1.,-1.]).astype(complex)
def tens(*xs):
    ans=np.array([[1]],complex)
    for x in xs: ans=np.kron(ans,x)
    return ans
D=8; ID=np.eye(D,dtype=complex)
S=[tens(Z,I,I),tens(I,Z,I),tens(Z,I,I)]
XP=[tens(X,I,I),tens(I,X,I),tens(X,I,I)]
P=[[.5*(ID+(-1)**s*S[i]) for s in [0,1]] for i in range(3)]
V=[.31*tens(X,I,X)+.19*tens(Z,I,Y)+.11*tens(Y,I,Z),
   .29*tens(I,Y,Y)+.17*tens(I,Z,X)+.13*tens(I,X,Z),
   .23*tens(Y,I,X)+.21*tens(Z,I,Z)+.09*tens(X,I,Y)]
Hb=.14*tens(I,I,Z)+.08*tens(I,I,X)
# Explicit forced jump paths. Pulses 0 and 1 cross; pulse 2 reuses patch 0.
events=[(0.,'start',0),(.2,'start',1),(.35,'jump',0),(.47,'jump',1),
        (.72,'jump',0),(.91,'jump',1),(1.,'end',0),(1.1,'jump',1),
        (1.2,'end',1),(1.25,'remote',None),(1.3,'start',2),
        (1.47,'jump',2),(1.71,'jump',2),(1.89,'jump',2),(2.,'end',2)]
R=expm(-1j*(.33*tens(X,X,I)+.17*tens(Z,I,Y)))
def qbit(i,s): return [s,1,s^1][i]
eta_final=[0,1,1]
seeds=list(itertools.product([0,1],repeat=3))
records=list(itertools.product([0,1],repeat=6))
def operators(seed,mode):
    # mode actual, explicit virtual wrappers, or fully toggled no-wrapper circuit
    active=set(); parity=[0]*3; last=0.; seq=[]
    for time,kind,i in events:
        h=Hb.copy()
        for j in active:
            if mode=='toggled':
                frame=S[j] if seed[j]^parity[j] else ID
                h=h+frame@V[j]@frame
            else: h=h+V[j]
        seq.append(('fixed',expm(-1j*(time-last)*h),None))
        if kind=='start':
            seq.append(('start',None,i))
            if mode=='virtual' and seed[i]: seq.append(('fixed',S[i],None))
            active.add(i)
        elif kind=='jump':
            if mode!='toggled': seq.append(('fixed',S[i],None))
            parity[i]^=1
        elif kind=='end':
            if mode=='virtual' and seed[i]^parity[i]: seq.append(('fixed',S[i],None))
            seq.append(('end',None,i)); active.remove(i)
        elif kind=='remote': seq.append(('fixed',R,None))
        last=time
    return seq

def kraus(seq,record):
    out=ID.copy()
    for kind,op,i in seq:
        if kind=='start':
            s=record[2*i]; q=qbit(i,s)
            op=(XP[i] if q else ID)@P[i][s]
        elif kind=='end': op=P[i][record[2*i+1]]
        out=op@out
    return out
actual_seq=operators((0,0,0),'actual')
virt_seq=[operators(f,'virtual') for f in seeds]
togg_seq=[operators(f,'toggled') for f in seeds]
max_phase=max_toggle=max_fourier=max_effect=0.
actual_effects={c:np.zeros((D,D),complex) for c in seeds}
fourier_effects={c:np.zeros((D,D),complex) for c in seeds}
for rec in records:
    a=kraus(actual_seq,rec)
    delta=tuple(rec[2*i]^qbit(i,rec[2*i])^rec[2*i+1] for i in range(3))
    phase_eta=(-1)**sum(rec[2*i+1]*eta_final[i] for i in range(3))
    vs=[]
    for f,vseq,tseq in zip(seeds,virt_seq,togg_seq):
        v=kraus(vseq,rec); toggle=kraus(tseq,rec); vs.append(v)
        phase=phase_eta*(-1)**sum(delta[i]*f[i] for i in range(3))
        max_phase=max(max_phase,np.linalg.norm(v-phase*a,2))
        max_toggle=max(max_toggle,np.linalg.norm(v-toggle,2))
    actual_effects[delta]+=a.conj().T@a
    for c in seeds:
        k=sum((-1)**sum(c[i]*f[i] for i in range(3))*v for f,v in zip(seeds,vs))/8
        expected=phase_eta*a if c==delta else np.zeros_like(a)
        max_fourier=max(max_fourier,np.linalg.norm(k-expected,2))
        fourier_effects[c]+=k.conj().T@k
for c in seeds:
    max_effect=max(max_effect,np.linalg.norm(actual_effects[c]-fourier_effects[c],2))
complete=np.linalg.norm(sum(actual_effects.values())-ID,2)
result={'records':len(records),'seed_assignments':len(seeds),
        'max_branch_phase_error':max_phase,'max_toggling_error':max_toggle,
        'max_fourier_selection_error':max_fourier,
        'max_measured_vs_fourier_effect_error':max_effect,'instrument_completeness_error':complete}
print(json.dumps(result,indent=2))
assert max(max_phase,max_toggle,max_fourier,max_effect,complete)<1e-12
