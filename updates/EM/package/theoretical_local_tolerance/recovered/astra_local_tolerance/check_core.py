"""Finite diagnostics for the local-port tolerant predictive certification theorem.
These numerical tests do not replace the analytic proofs in research_note.md.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
import mpmath as mp
from scipy.linalg import eigh

mp.mp.dps = 110
OUT = Path(__file__).parent
counts = {'multiprecision': 0, 'floating_point': 0}
maxima = {'moment_error': mp.mpf(0), 'jacobi_prefix_error': mp.mpf(0),
          'boundary_error': mp.mpf(0), 'control_gram_ratio': 0.0,
          'controlled_occupation_ratio': 0.0, 'reflection_error': 0.0}

def check_mp(ok: bool, message: str) -> None:
    if not bool(ok):
        raise AssertionError(message)
    counts['multiprecision'] += 1

def check_fp(ok: bool, message: str) -> None:
    if not bool(ok):
        raise AssertionError(message)
    counts['floating_point'] += 1

def jacobi(xs, weights):
    p0 = [mp.mpf(0)] * len(xs)
    p1 = [mp.mpf(1)] * len(xs)
    bprev = mp.mpf(0)
    diag, bonds = [], []
    for j in range(len(xs)):
        a = sum(w*x*p*p for x,w,p in zip(xs,weights,p1))
        diag.append(a)
        if j+1 == len(xs):
            break
        rem = [(x-a)*p-bprev*old for x,p,old in zip(xs,p1,p0)]
        bn = mp.sqrt(sum(w*r*r for w,r in zip(weights,rem)))
        bonds.append(bn)
        p0,p1 = p1,[r/bn for r in rem]
        bprev=bn
    return diag,bonds

def construct(d: int, eta: str = '0.125'):
    e=mp.mpf(eta); delta=e*e/(64*d*d); m=2*d
    xs=[delta+(1-delta)*(1-mp.cos(mp.pi*j/m))/2 for j in range(m+1)]
    ws=[]
    for j in range(m+1):
        w=mp.mpf(1)
        for k in range(m+1):
            if k!=j: w*= -xs[k]/(xs[j]-xs[k])
        ws.append(w)
    L=mp.cosh(m*mp.acosh((1+delta)/(1-delta)))
    A=(1+L)/2
    xg=[mp.mpf(0)]+[xs[j] for j in range(1,m,2)]
    wg=[1/A]+[-ws[j]/A for j in range(1,m,2)]
    xb=[xs[j] for j in range(0,m+1,2)]
    wb=[ws[j]/A for j in range(0,m+1,2)]
    ag,bg=jacobi(xg,wg); ab,bb=jacobi(xb,wb)
    return dict(d=d,eta=e,delta=delta,xs=xs,ws=ws,L=L,A=A,
                xg=xg,wg=wg,xb=xb,wb=wb,ag=ag,bg=bg,ab=ab,bb=bb,
                T=4/delta,gamma=e/(16*(4/delta)))

def array_jacobi(a,b):
    return np.diag([float(v) for v in a])+np.diag([-float(v) for v in b],1)+np.diag([-float(v) for v in b],-1)

def oneparticle(c, rounded=False):
    d=c['d']; l=d+1
    ag=np.array([float(v) for v in c['ag']]); ab=ag.copy(); ab[-1]=float(c['ab'][-1])
    bonds=np.array([float(v) for v in c['bg']]); gamma=float(c['gamma'])
    if rounded:
        qmax=min(float(c['eta']/(96*c['T'])),float(c['eta']/(1200*d**3)))
        q=2.0**(-math.ceil(math.log2(1/qmax)))
        ag=np.rint(ag/q)*q; ab=np.rint(ab/q)*q
        bonds=np.floor(bonds/q)*q; gamma=math.floor(gamma/q)*q
    else: q=0.0
    A0=np.diag(ag)+np.diag(-bonds,1)+np.diag(-bonds,-1)
    A1=np.diag(ab)+np.diag(-bonds,1)+np.diag(-bonds,-1)
    C0=np.zeros((2*l,2*l)); C0[:l,:l]=A0; C0[l:,l:]=A1
    C0[0,l]=C0[l,0]=-gamma
    perm=np.r_[np.arange(l,2*l),np.arange(l)]
    C1=C0[np.ix_(perm,perm)]
    return C0,C1,perm,q

def manybody(C):
    n=C.shape[0]; dim=1<<n
    H=np.zeros((dim,dim),complex)
    edges=[(i,j,-C[i,j]) for i in range(n) for j in range(i+1,n) if C[i,j]!=0]
    for s in range(dim):
        occ=[(s>>i)&1 for i in range(n)]
        H[s,s]=sum((1+C[i,i])*occ[i] for i in range(n))+sum(occ[i]*occ[j] for i,j,_ in edges)
        for i,j,b in edges:
            if occ[i]!=occ[j]: H[s^(1<<i)^(1<<j),s]=-b
    return H,edges

def local_gate(V,G,S,n):
    # Work directly with computational bit-index blocks; column count is unchanged.
    out=np.empty_like(V)
    env=[i for i in range(n) if i not in S]
    for z in range(1<<len(env)):
        base=sum(((z>>k)&1)<<site for k,site in enumerate(env))
        inds=[base+sum(((a>>k)&1)<<site for k,site in enumerate(S)) for a in range(1<<len(S))]
        out[inds,:]=G@V[inds,:]
    return out

def evolve(V,evals,evecs,t):
    return evecs@(np.exp(-1j*t*evals)[:,None]*(evecs.conj().T@V))

def run():
    cases=[]
    for d in [1,2,3,4,6,8,12,18,24]:
      for eta in ['0.125','0.04']:
        c=construct(d,eta); delta=c['delta']; A=c['A']; rho=1-1/A
        check_mp(abs(sum(c['ws'])-1)<mp.mpf('1e-85'),'weight sum')
        check_mp(abs(sum(abs(w) for w in c['ws'])-c['L'])<mp.mpf('1e-85'),'Chebyshev total variation')
        check_mp(all(((-1)**j)*w>0 for j,w in enumerate(c['ws'])),'weight signs')
        check_mp(c['ws'][0]>=1,'endpoint interpolation weight')
        check_mp(abs(sum(c['wg'])-1)<mp.mpf('1e-85'),'good probability sum')
        check_mp(abs(sum(c['wb'])-1)<mp.mpf('1e-85'),'bad probability sum')
        check_mp(rho <= c['eta']**2/9,'good leakage bound')
        check_mp(c['wb'][0]>=1-rho-mp.mpf('1e-90'),'bad low-level concentration')
        check_mp(min(c['wg']+c['wb'])>=delta/2,'polynomial weight floor')
        for k in range(2*d+1):
            diff=abs(sum(w*x**k for x,w in zip(c['xg'],c['wg']))-sum(w*x**k for x,w in zip(c['xb'],c['wb'])))
            maxima['moment_error']=max(maxima['moment_error'],diff)
            check_mp(diff<mp.mpf('1e-85'),'matched moment')
        err=max([abs(c['ag'][i]-c['ab'][i]) for i in range(d)]+[abs(x-y) for x,y in zip(c['bg'],c['bb'])])
        maxima['jacobi_prefix_error']=max(maxima['jacobi_prefix_error'],err)
        check_mp(err<mp.mpf('1e-75'),'Jacobi shared prefix')
        err=abs(c['ab'][-1]-c['ag'][-1]-(1+delta)/2)
        maxima['boundary_error']=max(maxima['boundary_error'],err)
        check_mp(err<mp.mpf('1e-75'),'last diagonal difference')
        check_mp(min(c['bg'])>=c['eta']/(300*d**3),'hopping lower bound')
        check_mp(max(c['bg'])<=mp.mpf('.5')+mp.mpf('1e-85'),'hopping upper bound')
        # Uniform-in-time conclusions have analytic proofs; these are selected-time diagnostics.
        tstar=mp.pi/delta
        Fb=sum(w*mp.exp(-1j*tstar*x) for x,w in zip(c['xb'],c['wb']))
        check_mp((1-mp.re(Fb))/2>=1-rho-mp.mpf('1e-80'),'explicit bad local signal')
        for frac in ['0','0.001','0.1','0.25','0.6','1']:
            t=mp.mpf(frac)*c['T']
            F=sum(w*mp.exp(-1j*t*x) for x,w in zip(c['xg'],c['wg']))
            vecsq=1-mp.re(F)
            check_mp(vecsq<=2*rho+mp.mpf('1e-85'),'uniform good vector bound')
        C0,C1,perm,_=oneparticle(c)
        R0,R1,_,q=oneparticle(c,True)
        check_fp(np.linalg.norm(C1-C0[np.ix_(perm,perm)],2)<1e-13,'one-particle reflection')
        check_fp(np.linalg.norm(R0-C0,2)<=3*q+1e-14,'dyadic rounding norm')
        check_fp(np.max(np.sum(np.abs(R0-np.diag(np.diag(R0))),axis=1))<=1+1e-13,'hopping row sum')
        for B in [C0,C1,R0,R1]:
            check_fp(np.linalg.eigvalsh(B)[0]>=-float(c['gamma'])-3*q-1e-13,'active-band lower bound')
        # Long-time candidate fidelity and local trace distance for connected, rounded cases.
        metrics=[]
        for B in [C0,C1,R0,R1]:
            ev,Q=eigh(B); seed=Q[0,:]
            F=np.dot(seed**2,np.exp(-1j*float(tstar)*ev))
            Dloc=.5*np.sqrt((1-abs(F)**2)**2+abs(1-F)**2)
            Dglob=np.sqrt(max(0,1-abs((1+F)/2)**2))
            metrics.append((Dloc,Dglob))
        check_fp(metrics[0][1]<float(c['eta']),'connected good trajectory at tstar')
        check_fp(metrics[1][0]>.75,'connected bad local trajectory at tstar')
        check_fp(metrics[2][1]<float(c['eta']),'rounded good trajectory at tstar')
        check_fp(metrics[3][0]>.75,'rounded bad local trajectory at tstar')
        cases.append({'d':d,'eta':eta,'T':float(c['T']),'dyadic_step':q,
                      'tstar_good_global':metrics[2][1],'tstar_bad_local':metrics[3][0]})
    # Small interacting many-body examples with arbitrary joint port-control pulses.
    rng=np.random.default_rng(184729)
    control_records=[]
    for d in [1,2,3]:
        c=construct(d); C0,C1,perm,_=oneparticle(c)
        H0,edges=manybody(C0); H1,_=manybody(C1); n=C0.shape[0]; l=d+1
        bitperm=np.array([sum(((s>>i)&1)<<int(perm[i]) for i in range(n)) for s in range(1<<n)])
        er=np.linalg.norm(H1-H0[np.ix_(bitperm,bitperm)],2)
        maxima['reflection_error']=max(maxima['reflection_error'],float(er))
        check_fp(er<1e-11,'full interacting isospectral reflection')
        ev0,Q0=eigh(H0); ev1,Q1=eigh(H1)
        check_fp(np.max(abs(ev0-ev1))<1e-10,'many-body spectra')
        check_fp(abs(ev0[0])<1e-10 and ev0[1]>.9,'unique vacuum and constant gap')
        # Embedded arbitrary input on the two central port sites.
        S=[0,l]; E=np.zeros((1<<n,4),complex)
        for a in range(4): E[((a&1)<<S[0])+(((a>>1)&1)<<S[1]),a]=1
        endpoints=[d,2*l-1]; R=d
        for tau in [.1,.3,.6]:
            if tau>R/2: continue
            for trial in range(4):
                V0=E.copy(); V1=E.copy(); elapsed=0.0
                for seg in range(4):
                    Z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
                    G,_=np.linalg.qr(Z)
                    V0=local_gate(V0,G,S,n); V1=local_gate(V1,G,S,n)
                    dt=tau/4; elapsed+=dt
                    V0=evolve(V0,ev0,Q0,dt); V1=evolve(V1,ev1,Q1,dt)
                    qbound=sum(elapsed**j/math.factorial(j) for j in range(R,80))
                    for V in [V0,V1]:
                        for x in endpoints:
                            inds=np.array([s for s in range(1<<n) if (s>>x)&1])
                            amp=np.linalg.norm(V[inds,:],2)
                            maxima['controlled_occupation_ratio']=max(maxima['controlled_occupation_ratio'],float(amp/max(qbound,1e-100)))
                            check_fp(amp<=qbound+2e-12,'controlled occupation cone')
                err=np.linalg.norm(np.eye(4)-V0.conj().T@V1,2)
                bound=8*tau**(2*R+1)/((2*R+1)*math.factorial(R)**2)
                maxima['control_gram_ratio']=max(maxima['control_gram_ratio'],float(err/bound))
                check_fp(err<=bound+2e-12,'forward-channel Gram bound')
                control_records.append({'d':d,'tau':tau,'trial':trial,'gram_norm':float(err),'proved_bound':bound})
    report={'status':'PASS','scope':'finite numerical diagnostics, not independent proof validation',
            'seed':184729,'precision_decimal_digits':mp.mp.dps,'counts':counts,
            'maxima':{k:str(v) if isinstance(v,mp.mpf) else v for k,v in maxima.items()},
            'constructed_cases':cases,'controlled_manybody_cases':control_records}
    (OUT/'diagnostics.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ['constructed_cases','controlled_manybody_cases']},indent=2))

if __name__=='__main__': run()
