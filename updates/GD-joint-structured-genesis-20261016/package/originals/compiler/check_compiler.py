#!/usr/bin/env python3
"""Independent small-matrix checks; numpy/scipy only, deterministic seeds."""
import itertools, json
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize

I2=np.eye(2,dtype=complex)
P1=[I2,np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]
TOL=2e-9
rng=np.random.default_rng(661216)

def basis(n):
    labels=[]; mats=[]
    for inds in itertools.product(range(4),repeat=n):
        p=np.array([[1]],complex)
        for i in inds: p=np.kron(p,P1[i])
        labels.append(''.join('IXYZ'[i] for i in inds)); mats.append(p)
    return labels,np.asarray(mats)

def coefficients(A,P):
    return np.einsum('aij,ij->a',P.conj(),A)/A.shape[0]

def residual(C,H,P):
    d=H.shape[0]; S=np.zeros((d,d),complex)
    for a,b in zip(*np.nonzero(abs(C)>1e-15)): S+=C[a,b]*(P[b]@P[a])
    s=np.trace(S).real/d
    R=-(S-s*np.eye(d))/2-1j*(H-np.trace(H)*np.eye(d)/d)
    return coefficients(R,P),s,S

def generator(C,H,P,rho):
    out=-1j*(H@rho-rho@H)
    for a,b in zip(*np.nonzero(abs(C)>1e-15)):
        V=P[b]@P[a]
        out+=C[a,b]*(P[a]@rho@P[b]-(V@rho+rho@V)/2)
    return out

def direct_choi(C,H,P,lam):
    d=H.shape[0]; J=np.zeros((d*d,d*d),complex)
    for i in range(d):
        for j in range(d):
            E=np.zeros((d,d),complex); E[i,j]=1
            J+=np.kron(E+generator(C,H,P,E)/lam,E)/d
    return (J+J.conj().T)/2

def compiler(C,H,P):
    b,s,S=residual(C,H,P)
    Cp=np.linalg.pinv(C,hermitian=True,rcond=1e-11)
    obstruction=np.linalg.norm(b-C@Cp@b)
    if obstruction>1e-8: return None,obstruction,None
    lam=s+np.vdot(b,Cp@b).real
    vals,vecs=np.linalg.eigh(C)
    Q=vecs[:,vals>1e-10]*np.sqrt(vals[vals>1e-10])
    z=np.linalg.pinv(Q,rcond=1e-11)@b # z_j=conj(alpha_j)
    jumps=[sum(Q[a,j]*P[a] for a in range(len(P)))+z[j].conjugate()*np.eye(H.shape[0]) for j in range(Q.shape[1])]
    assert np.linalg.norm(sum(K.conj().T@K for K in jumps)-lam*np.eye(H.shape[0]))<TOL
    d=H.shape[0]
    for i in range(d):
        for j in range(d):
            E=np.zeros((d,d),complex); E[i,j]=1
            got=sum(K@E@K.conj().T for K in jumps)-lam*E
            assert np.linalg.norm(got-generator(C,H,P,E))<TOL
    return lam,obstruction,jumps

results={}
labels,Pall=basis(1); P=Pall[1:]; X,Y,Z=P; zero=np.zeros((2,2),complex)
k=.7; ell=np.array([np.sqrt(k)/2,1j*np.sqrt(k)/2,0])
C=np.outer(ell,ell.conj())
raw=[]
for rate in [.1,1,10,100]:
    J=direct_choi(C,zero,P,rate)
    minor=np.linalg.det(J[np.ix_([0,3],[0,3])]).real
    assert abs(minor+k*k/(16*rate*rate))<1e-10
    raw.append([rate,float(np.linalg.eigvalsh(J)[0]),float(minor)])
assert compiler(C,zero,P)[0] is None
results['amplitude_damping_obstruction']=raw
for h in [0,.19]:
    gamma=np.sqrt(k*k/16+h*h)
    D=C.copy(); D[2,2]+=gamma
    rate,_,_=compiler(D,h*Z,P)
    assert abs(rate-(k/2+gamma+(k*k/16+h*h)/gamma))<TOL
    if h==0:
        J=direct_choi(D,zero,P,rate)
        reset=np.kron(np.diag([1,0]),np.eye(2))/2
        assert np.linalg.norm(J-reset)<TOL
    results[f'amplitude_repair_h_{h}']={'gamma':gamma,'minimum_rate':rate}

# Complex correlated, rank-deficient, noncommuting two-qubit noise.
labels,Pall=basis(2); P=Pall[1:]; m=len(P)
active=[labels[1:].index(s) for s in ['XI','YI','IZ','XZ']]
V=np.zeros((m,2),complex)
V[active]=.15*(rng.normal(size=(4,2))+1j*rng.normal(size=(4,2)))
C=V@V.conj().T
H=.11*P[labels[1:].index('ZX')]+.07*P[labels[1:].index('YI')]
b,s,_=residual(C,H,P)
gamma=np.abs(b); D=C+np.diag(gamma)
rate,obs,jumps=compiler(D,H,P)
assert rate<=s+2*np.sum(abs(b))+TOL
assert np.linalg.eigvalsh(direct_choi(D,H,P,rate))[0]>-TOL
assert np.linalg.eigvalsh(direct_choi(D,H,P,rate*.999))[0]<-1e-8
results['correlated_repair']={'original_rank':int(np.linalg.matrix_rank(C)), 'added_pauli_directions':int(np.sum(gamma>1e-12)), 'minimum_rate':rate,'analytic_ceiling':float(s+2*np.sum(abs(b))), 'kraus_count':len(jumps),'range_residual':obs}

# Optimize positive diagonal floor in the fixed allowed directions.
idx=np.where(gamma>1e-12)[0]
def objective(x):
    D=C.copy(); D[idx,idx]+=x
    return float(np.trace(D).real+np.vdot(b,np.linalg.pinv(D,hermitian=True,rcond=1e-12)@b).real)
opt=minimize(objective,gamma[idx],bounds=[(1e-9,None)]*len(idx),method='L-BFGS-B',options={'maxiter':1000,'ftol':1e-13})
assert opt.success
results['correlated_floor_optimization']={'simple_floor_min_rate':rate,'optimized_rate':float(opt.fun),'optimizer_success':bool(opt.success)}

# A-priori fixed bounds/floors; actual signed C and H sampled afterward.
robust=[]
for n in [1,2,3]:
    labels,Pall=basis(n); labels=labels[1:]; P=Pall[1:]; m=len(P); d=2**n
    orig=[i for i,l in enumerate(labels) if sum(c!='I' for c in l)<=min(2,n)][:min(8,m)]
    M=np.zeros((m,m))
    for a in orig: M[a,a]=.025+.005*(a%3)
    for a in orig:
        for bb in orig:
            if a<bb and (a+bb)%3!=0: M[a,bb]=M[bb,a]=.012
    u=np.zeros(m)
    for a in orig[::3]: u[a]=.017
    tau=np.zeros(m)
    for a,bb in zip(*np.nonzero(M)):
        if a==bb: continue
        coeff=coefficients(P[bb]@P[a],P)
        tau+=M[a,bb]*np.abs(coeff)
    beta=tau/2+u
    r=M.sum(axis=1); floor=r+beta
    cap=2*(M.sum()+u.sum())
    worst=-1; worst_mineig=1; count=0; maxweight=0
    for p in np.where(floor>0)[0]: maxweight=max(maxweight,sum(c!='I' for c in labels[p]))
    for trial in range(20):
        C=np.zeros((m,m),complex)
        for a in orig: C[a,a]=rng.uniform(-M[a,a],M[a,a])
        for a in orig:
            for bb in orig:
                if a<bb and M[a,bb]:
                    C[a,bb]=M[a,bb]*rng.random()*np.exp(2j*np.pi*rng.random()); C[bb,a]=C[a,bb].conjugate()
        h=rng.uniform(-1,1,size=m)*u; H=sum(h[a]*P[a] for a in range(m))
        b,s,_=residual(C,H,P)
        assert np.max(abs(b)-beta)<TOL
        D=C+np.diag(floor)
        assert np.linalg.eigvalsh(D-np.diag(beta))[0]>-TOL
        rate,obs,_=compiler(D,H,P)
        assert rate is not None and rate<=cap+TOL
        mineig=float(np.linalg.eigvalsh(direct_choi(D,H,P,cap))[0])
        assert mineig>-TOL
        worst=max(worst,rate); worst_mineig=min(worst_mineig,mineig); count+=1
    # Exact cancellation leaves zero-beta/noise directions singular, still valid.
    C=-np.diag(np.diag(M)); H=np.zeros((d,d),complex)
    D=C+np.diag(floor); rate,obs,_=compiler(D,H,P)
    assert rate is not None
    robust.append({'qubits':n,'samples':count,'noise_labels':len(orig),'floor_labels':int(np.sum(floor>0)),'zero_beta_labels':int(np.sum(beta==0)),'maximum_floor_weight':maxweight,'uniform_ceiling':float(cap),'largest_exact_minimum':float(worst),'worst_choi_eigenvalue_at_ceiling':worst_mineig,'singular_case_range_residual':obs})
results['fixed_design_signed_C']=robust

# Noncommuting proposal clocks need no Trotter approximation.
labels,Pall=basis(1); P=Pall[1:]; X,Y,Z=P
C1=np.diag([.3,0,.2]); H1=.07*X
C2=np.diag([0,.4,.1]); H2=.09*Y
r1,_,_=compiler(C1,H1,P); r2,_,_=compiler(C2,H2,P)
def superop(C,H):
    cols=[]
    for j in range(4):
        E=np.zeros((2,2),complex); E.reshape(-1)[j]=1
        cols.append(generator(C,H,P,E).reshape(-1))
    return np.stack(cols,axis=1)
G1=superop(C1,H1); G2=superop(C2,H2); G=G1+G2; lam=r1+r2; Phi=np.eye(4)+G/lam; t=2.1
poisson=np.exp(-lam*t)*np.eye(4,dtype=complex); term=poisson.copy()
for j in range(1,80): term=term@Phi*(lam*t/j); poisson+=term
assert np.linalg.norm(G1@G2-G2@G1)>1e-4
err=float(np.linalg.norm(poisson-expm(t*G)))
assert err<TOL
results['noncommuting_clock_sum']={'total_rate':lam,'commutator_norm':float(np.linalg.norm(G1@G2-G2@G1)),'poisson_series_error':err}
# Explicit weight-two inputs generate a weight-four floor; signed bound is tight.
def kron_all(*args):
    out=np.array([[1]],complex)
    for a in args: out=np.kron(out,a)
    return out
P=np.array([kron_all(P1[1],P1[1],I2,I2),kron_all(I2,I2,P1[3],P1[3]),kron_all(P1[1],P1[1],P1[3],P1[3])])
C=np.zeros((3,3),complex); C[0,1]=C[1,0]=.03
H=np.zeros((16,16),complex)
floor=np.array([.03,.03,.03]); D=C+np.diag(floor)
rate,obs,_=compiler(D,H,P)
assert abs(rate-.12)<TOL
assert np.linalg.eigvalsh(D)[0]>-TOL
assert np.linalg.eigvalsh(direct_choi(D,H,P,rate))[0]>-TOL
results['weight_four_singular_signed_example']={'input_paulis':['XXII','IIZZ'],'product_floor':'XXZZ','floor_rates':floor.tolist(),'minimum_and_uniform_ceiling':rate,'noise_matrix_rank':int(np.linalg.matrix_rank(D)),'range_residual':obs}
# Closed-form, four-Kraus pair compiler; test commuting and anticommuting edges.
pair_errors=[]
for commutes in [False,True]:
    P=kron_all(P1[1],I2)
    Q=kron_all(I2,P1[3]) if commutes else kron_all(P1[2],P1[3])
    omega=1 if commutes else -1j
    R=Q@P/omega
    d=4; M=.12
    for trial in range(12):
        z=M*rng.random()*np.exp(2j*np.pi*rng.random()); radius=abs(z); phase=z/radius
        a=float((z*omega).real)
        Kp=np.sqrt((M+radius)/2)*(P+phase.conjugate()*Q)
        Km=np.sqrt((M-radius)/2)*(P-phase.conjugate()*Q)
        Kr=np.sqrt(M)*R-a/np.sqrt(M)*np.eye(d)
        K0=np.sqrt(max(0,M-a*a/M))*np.eye(d)
        Ks=[Kp,Km,Kr,K0]; rate=4*M
        tp=float(np.linalg.norm(sum(K.conj().T@K for K in Ks)-rate*np.eye(d)))
        C=np.diag([M,M,M]).astype(complex); C[0,1]=z; C[1,0]=z.conjugate()
        basis3=np.array([P,Q,R]); H=np.zeros((d,d),complex)
        err=0
        for i in range(d):
            for j in range(d):
                E=np.zeros((d,d),complex); E[i,j]=1
                err=max(err,float(np.linalg.norm(sum(K@E@K.conj().T for K in Ks)-rate*E-generator(C,H,basis3,E))))
        assert max(err,tp)<TOL
        pair_errors.append(max(err,tp))
results['explicit_pair_kraus']={'commuting_and_anticommuting_cases':24,'maximum_error':max(pair_errors),'maximum_kraus_count':4}
# Purely dissipative Gaussian dephasing can also fail finite-rate compilation.
A=np.diag([-1,0,1]).astype(complex)
P=np.array([A/np.sqrt(2/3),np.diag([1,-2,1])/np.sqrt(2)])
C=np.diag([2/3,0]); H=np.zeros((3,3),complex)
rate,obs,_=compiler(C,H,P)
assert rate is None
mineig=float(np.linalg.eigvalsh(direct_choi(C,H,P,10))[0])
assert mineig<0
results['qutrit_hermitian_jump_obstruction']={'range_residual':float(obs),'choi_minimum_at_rate_10':mineig}
print(json.dumps(results,indent=2))
