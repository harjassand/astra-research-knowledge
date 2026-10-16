#!/usr/bin/env python3
"""Original reproducible numerical checks, not imported author code.
Three measured pulses: A [0,.9], C [.2,1.15], reused A [1.3,2].
A and C share a noncommuting one-qubit bath. Full 8-dimensional
memory+bath input is retained; no bath state is fixed.
"""
import itertools, json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
I2=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex); Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1,-1]).astype(complex)
def kron(*xs):
    ans=np.ones((1,1),complex)
    for x in xs: ans=np.kron(ans,x)
    return ans
I=np.eye(8,dtype=complex); I64=np.eye(64,dtype=complex)
XA=kron(X,I2,I2); XC=kron(I2,X,I2)
ZA=kron(Z,I2,I2); ZC=kron(I2,Z,I2)
HB=.41*kron(I2,I2,Y)
raw=[kron(X,I2,X)+.37*kron(Y,I2,Y)+.23*kron(Z,I2,Z),
     kron(I2,X,Z)+.31*kron(I2,Y,X),
     kron(X,I2,Z)+.29*kron(Y,I2,X)-.19*kron(Z,I2,Y)]
J=[.18,.22,.21]; starts=[0.,.2,1.3]; ends=[.9,1.15,2.]
V=[j*h/np.linalg.norm(h,2) for j,h in zip(J,raw)]
S=[ZA,ZC,ZA]; flip=[XA,XC,XA]
# Corrections map pulse 0 to sector 0, pulse 1 to sector 1, and pulse 2 leaves sector unchanged.
def qbit(i,s): return s if i==0 else ((1-s) if i==1 else 0)
def P(i,s): return (I+(-1)**s*S[i])/2
def op_pre(i,s,g=0): return (S[i] if g else I) @ (flip[i] if qbit(i,s) else I) @ P(i,s)
def ch(K): return np.kron(K.conj(),K)
def gen(active,gamma):
    H=HB+sum((V[i] for i in active),np.zeros_like(I))
    L=-1j*(np.kron(I,H)-np.kron(H.T,I))
    for i in active: L+=gamma*(ch(S[i])-I64)
    return L
base_events=sorted([(starts[i],0,i) for i in range(3)]+[(ends[i],1,i) for i in range(3)])
vecI=I.reshape(-1,order='F')
def effect(M):
    E=(M.conj().T@vecI).reshape(8,8,order='F')
    return (E+E.conj().T)/2

def instrument(gamma):
    records=[{}]; maps=np.array([I64]); active=[]; now=0.
    for when,kind,i in base_events:
        if when>now:
            E=expm(gen(active,gamma)*(when-now)); maps=E@maps
        now=when
        newmaps=[]; newrecords=[]
        for rec,M in zip(records,maps):
            for bit in (0,1):
                K=op_pre(i,bit) if kind==0 else P(i,bit)
                rr=rec.copy(); rr[('s' if kind==0 else 't',i)]=bit
                newmaps.append(ch(K)@M); newrecords.append(rr)
        records,maps=newrecords,np.array(newmaps)
        if kind==0: active.append(i)
        else: active.remove(i)
    total=maps.sum(axis=0)
    rows=[]
    for n in (1,2,3):
        for subset in itertools.combinations(range(3),n):
            selected=[]
            for rec,M in zip(records,maps):
                if all(rec['t',i] != (rec['s',i]^qbit(i,rec['s',i])) for i in subset): selected.append(M)
            E=effect(sum(selected,np.zeros_like(I64)))
            B=[]
            for i in subset:
                tau=ends[i]-starts[i]; d=math.sqrt(gamma*gamma+4*J[i]*J[i])
                B.append(.5*(math.exp(-gamma*tau)*(math.cosh(d*tau)+(gamma/d)*math.sinh(d*tau))-1))
            budget=math.prod(B); mineig=float(np.linalg.eigvalsh(budget*I-E)[0]); maximum=float(np.linalg.eigvalsh(E)[-1])
            assert mineig>=-2e-12, (gamma,subset,maximum,budget)
            rows.append({'subset':list(subset),'effect_max_eigenvalue':maximum,'B_product':budget,'ratio':maximum/budget,'budget_slack_min_eigenvalue':mineig})
    normerr=float(np.linalg.norm(effect(total)-I,2)); assert normerr<2e-12
    return {'gamma':gamma,'complete_instrument_error':normerr,'subsets':rows}

# Predetermined finite Poisson-path support points. This verifies pathwise identities;
# the master-equation tests above average all Poisson histories exactly.
jumps=[(.12,0),(.53,0),(.27,1),(.75,1),(1.07,1),(1.57,2)]
counts=[sum(i==j for _,j in jumps) for i in range(3)]
path_events=sorted([(t,'pre',i) for i,t in enumerate(starts)]+[(t,'post',i) for i,t in enumerate(ends)]+[(t,'jump',i) for t,i in jumps])
def branch(bits,g):
    K=I.copy(); now=0.; active=[]
    for when,kind,i in path_events:
        if when>now:
            H=HB+sum((V[j] for j in active),np.zeros_like(I))
            K=expm(-1j*H*(when-now))@K
        now=when
        if kind=='pre':
            K=op_pre(i,bits[2*i],g[i])@K; active.append(i)
        elif kind=='post':
            correction=(S[i] if (g[i]+counts[i])%2 else I)
            K=P(i,bits[2*i+1])@correction@K; active.remove(i)
        else: K=S[i]@K
    return K

def actual_branch(bits):
    # No boundary wrappers at all.
    K=I.copy(); now=0.; active=[]
    for when,kind,i in path_events:
        if when>now:
            H=HB+sum((V[j] for j in active),np.zeros_like(I)); K=expm(-1j*H*(when-now))@K
        now=when
        if kind=='pre': K=op_pre(i,bits[2*i])@K; active.append(i)
        elif kind=='post': K=P(i,bits[2*i+1])@K; active.remove(i)
        else: K=S[i]@K
    return K

def path_check():
    phase_error=0.; fourier_error=0.; total=np.zeros_like(I)
    gs=list(itertools.product((0,1),repeat=3)); records=list(itertools.product((0,1),repeat=6))
    for bits in records:
        A=actual_branch(bits); total+=A.conj().T@A
        ds=[bits[2*i]^qbit(i,bits[2*i])^bits[2*i+1] for i in range(3)]
        eta_phase=(-1)**sum(counts[i]*bits[2*i+1] for i in range(3))
        tracked=[branch(bits,g) for g in gs]
        for g,B in zip(gs,tracked):
            expected=eta_phase*((-1)**sum(g[i]*ds[i] for i in range(3)))*A
            phase_error=max(phase_error,float(np.linalg.norm(B-expected,2)))
        for chi in gs:
            F=sum(((-1)**sum(chi[i]*g[i] for i in range(3)))*B for g,B in zip(gs,tracked))/8
            expected=eta_phase*A if list(chi)==ds else np.zeros_like(A)
            fourier_error=max(fourier_error,float(np.linalg.norm(F-expected,2)))
    normerr=float(np.linalg.norm(total-I,2))
    assert max(phase_error,fourier_error,normerr)<2e-12
    return {'records':64,'virtual_seed_assignments_per_record':8,'phase_identity_error':phase_error,'fourier_delta_identity_error':fourier_error,'complete_path_instrument_error':normerr}

out={'description':'Exact matrix exponentials for the Lindblad-averaged actual instrument, plus separate fixed-path boundary/Fourier identities. Floating-point verification only; proof is in REPORT.md.','physical_dimension':8,'pulse_starts':starts,'pulse_ends':ends,'J':J,'shared_bath_commutator_norm':float(np.linalg.norm(V[0]@V[1]-V[1]@V[0],2)),'path':path_check(),'rate_runs':[instrument(g) for g in [0.,.3,2.,7.]]}
Path(__file__).with_name('shared_bath_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
