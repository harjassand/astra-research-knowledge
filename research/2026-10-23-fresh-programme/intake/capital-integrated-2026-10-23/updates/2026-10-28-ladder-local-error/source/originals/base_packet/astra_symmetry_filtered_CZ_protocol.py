#!/usr/bin/env python3
"""Exact finite-Fock coherent CZ pulse calculation for symmetry-sorted gapped baths.
Time-dependent symmetric coupling ramp, exact plateau, local Z echo when bath uncoupled.
No radiation channels projected out; no Markov approximation. Finite chain is diagnostic,
not a thermodynamic-limit fidelity certificate.
"""
import numpy as np,math,json,sys
from scipy.linalg import eigh
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply
sys.path.insert(0,'/mnt/data')
from astra_symmetry_filtered_embedded_pair import evaluate

def build_onebody(n,g):
    d=2+2*n
    h=np.diag(np.r_[3.,3.,np.full(n,5.),np.full(n,1.)])
    iu,il=2,2+n
    h[0,iu]=h[iu,0]=g;h[1,iu]=h[iu,1]=g
    h[0,il]=h[il,0]=g/math.sqrt(2); h[1,il]=h[il,1]=-g/math.sqrt(2)
    for j in range(n-1):
        for start in (iu,il):h[start+j,start+j+1]=h[start+j+1,start+j]=-.5
    return h

def build_two(n,g):
    h=build_onebody(n,g)
    d=len(h)
    basis=[(i,j) for i in range(d) for j in range(i,d) if not (i==j and i in (0,1))]
    lookup={a:i for i,a in enumerate(basis)}
    H2=np.zeros((len(basis),len(basis)))
    for a,(i,j) in enumerate(basis):
        H2[a,a]=h[i,i]+h[j,j]
        if i==j:
            for k in np.flatnonzero(h[:,i]):
                if k==i:continue
                H2[lookup[tuple(sorted((i,int(k))))],a]+=math.sqrt(2)*h[k,i]
        else:
            for idx,other in ((i,j),(j,i)):
                for k in np.flatnonzero(h[:,idx]):
                    if k==idx:continue
                    to=tuple(sorted((int(k),other)))
                    if to in lookup:H2[lookup[to],a]+=(math.sqrt(2) if k==other else 1)*h[k,idx]
    assert np.max(abs(H2-H2.T))<1e-13
    return H2,basis

def run(g=.16,n=6,ramp_time=120.,steps=120):
    h0=build_onebody(n,0);hg=build_onebody(n,g)
    H0,basis=build_two(n,0);Hg,_=build_two(n,g)
    ev1,Q1=eigh(hg); ev2,Q2=eigh(Hg)
    # value from exact spectral convolution (n version)
    data=evaluate(g,n)
    chi=data['connected_shift']
    # two on/off ramps per echo, integrated interaction for a single on/hold/off cycle
    samples=np.linspace(0,1,101)
    gs=g*np.sin(np.pi*samples/2)**2
    vals=np.array([evaluate(float(max(q,1e-5)),n)['connected_shift'] if q else 0. for q in gs])
    area_one_ramp=np.trapezoid(vals,samples)*ramp_time
    hold=(math.pi/2-2*abs(area_one_ramp))/abs(chi)
    assert hold>0
    def evolve(x,H_a,H_b,ev,U):
        H_a=csr_matrix(H_a); W=csr_matrix(H_b-H_a)
        dt=ramp_time/steps
        for j in range(steps):
            s=(j+.5)/steps
            gain=g*math.sin(.5*math.pi*s)**2
            x=expm_multiply((-1j*dt)*(H_a+gain/g*W),x,traceA=-1j*dt*np.sum(H_a.diagonal()))
        x=U@(np.exp(-1j*ev*hold)[:,None]*(U.conj().T@x))
        for j in range(steps):
            s=1-(j+.5)/steps
            gain=g*math.sin(.5*math.pi*s)**2
            x=expm_multiply((-1j*dt)*(H_a+gain/g*W),x,traceA=-1j*dt*np.sum(H_a.diagonal()))
        return x
    # one-photon code input matrix, two columns
    d=len(h0);X=np.zeros((d,2),complex);X[0,0]=X[1,1]=1
    Z1=np.ones(d);Z1[0]=-1
    Y=evolve(X,h0,hg,ev1,Q1)
    Y=Z1[:,None]*Y
    Y=evolve(Y,h0,hg,ev1,Q1)
    Y=Z1[:,None]*Y
    Q=Y[:2,:]
    # ideal single-qubit phase from trace, so ideal comparison diagonal phi I
    phase1=np.angle(np.trace(Q))
    n1_error=np.linalg.norm(Y-X*np.exp(1j*phase1),ord=2)
    n2=len(basis);V=np.zeros((n2,1),complex);V[basis.index((0,1)),0]=1
    Z2=np.array([-1 if (i==0 or j==0) else 1 for i,j in basis])
    Y2=evolve(V,H0,Hg,ev2,Q2)
    Y2=Z2[:,None]*Y2
    Y2=evolve(Y2,H0,Hg,ev2,Q2)
    Y2=Z2[:,None]*Y2
    # ideal CZ pair phase = - e^{2 i phase1}
    n2_error=np.linalg.norm(Y2+V*np.exp(2j*phase1))
    pair_amp=(V.conj().T@Y2)[0,0]
    result=dict(n=n,g=g,ramp_time=ramp_time,steps=steps,hold_time=hold,total_time=4*ramp_time+2*hold,
       onebody_phase=phase1,pair_amp=[pair_amp.real,pair_amp.imag],
       conditioned_pair_phase_error=float(abs(pair_amp/np.exp(2j*phase1)+1)),
       full_onebody_code_error=n1_error,full_pair_error=float(n2_error),
       total_code_operator_bound=float(max(n1_error,n2_error)),
       pair_energy=data['pole'], connected_shift=chi, parity_pair_isolation_gap=data['isolated_pair_gap'])
    return result

if __name__=='__main__':
    args=sys.argv[1:]
    g=float(args[0]) if len(args)>0 else .16
    ramp=float(args[1]) if len(args)>1 else 120.
    steps=int(args[2]) if len(args)>2 else 120
    ans=run(g=g,ramp_time=ramp,steps=steps)
    print(json.dumps(ans,indent=2))
    with open('/mnt/data/astra_symmetry_filtered_CZ_protocol_results.json','w') as f:json.dump(ans,f,indent=2)
