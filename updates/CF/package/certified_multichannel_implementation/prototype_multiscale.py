"""Exploratory high-precision realization. NOT interval certified.

Uses the exact family rescaling for all methods, polynomial projector jets,
superadiabatic recurrence, Kato transport, block phase extraction, and Taylor
block solves. Endpoint error must be independently assessed. No performance
claim against unavailable systems phase-function software is made.
"""
import argparse, json, time
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp

def zero(n=3): return mp.zeros(n)
def eye(n=3): return mp.eye(n)
def dag(A): return A.transpose_conj()
def norm(A): return mp.sqrt(sum(abs(x)**2 for x in A))
def herm(A): return (A+dag(A))/2
def evaluate(C,x):
    V=C[-1].copy()
    for A in C[-2::-1]: V=V*x+A
    return V
def convolution(A,B,L):
    return [sum((A[k]*B[r-k] for k in range(r+1)
                 if k<len(A) and r-k<len(B)),mp.zeros(A[0].rows,B[0].cols))
            for r in range(L+1)]
def ode_jet(G,L):
    C=[mp.eye(G[0].rows)]
    for r in range(L):
        C.append(sum((G[k]*C[r-k] for k in range(min(r,len(G)-1)+1)),
                     mp.zeros(G[0].rows))/(r+1))
    return C
def inverse_jet(C,L):
    V=[C[0]**-1]
    for r in range(1,L+1):
        V.append(-V[0]*sum((C[k]*V[r-k] for k in range(1,min(r,len(C)-1)+1)),zero()))
    return V

def base_jet(c,h,kappa,L):
    D2=mp.diag([1,0,-1]); D1=mp.diag([0,mp.mpf(1)/3,-mp.mpf(1)/3])
    D0=mp.matrix([[-1,1,mp.mpf(1)/3],[1,0,2],[mp.mpf(1)/3,2,1]])
    return [h*kappa*(D2*c*c+D1*c+D0),
            h*h*kappa*(2*D2*c+D1),h**3*kappa*D2]+[zero() for _ in range(max(0,L-2))]

def projectors(A,groups,L,counters):
    vals,Q=mp.eighe(herm(A[0])); counters['eigensystems']+=1
    Qh=dag(Q); AJ=[Qh*M*Q for M in A[:L+1]]
    AJ += [zero() for _ in range(L+1-len(AJ))]
    out=[]
    for group in groups:
        inside=set(group); P=[mp.diag([int(i in inside) for i in range(3)])]
        for r in range(1,L+1):
            S=sum((P[k]*P[r-k] for k in range(1,r)),zero())
            R=-sum((AJ[k]*P[r-k]-P[r-k]*AJ[k] for k in range(1,r+1)),zero())
            X=zero()
            for i in range(3):
                for j in range(3):
                    if (i in inside)==(j in inside): X[i,j]=(-1 if i in inside else 1)*S[i,j]
                    else: X[i,j]=R[i,j]/(vals[i]-vals[j])
            P.append(herm(X))
            counters['projector_jet_orders']+=1
        out.append([Q*X*Qh for X in P])
    return out

def connection(P,L):
    return [herm(1j*sum(((k+1)*Pj[k+1]*Pj[r-k]
                          for Pj in P for k in range(r+1)),zero())) for r in range(L+1)]

def groups_for(A,gap):
    vals=mp.eigsy(herm(A),eigvals_only=True) if all(mp.im(x)==0 for x in A) else mp.eighe(herm(A),eigvals_only=True)
    groups=[[0]]
    for j in (1,2):
        if vals[j]-vals[j-1]<gap: groups[-1].append(j)
        else: groups.append([j])
    return groups

def panel(c,h,kappa,L,N,groups,counters):
    full=L+N+2
    A=base_jet(c,h,kappa,full)
    if len(groups)==1:
        # The exact polynomial trace is zero for this family.
        C=ode_jet([-1j*M for M in A[:3]],L)
        Fp,Fm=evaluate(C,1),evaluate(C,-1)
        tail=sum(norm(X) for X in C[-5:])
        return Fp*dag(Fm),float(tail),0.0,{'groups':[3],'N':0}
    H=A
    previous=None
    originalP=None
    for j in range(N+1):
        order=full-j
        P=projectors(H,groups,order,counters)
        if j==0: originalP=P
        K=connection(P,order-1)
        if j==N: break
        previous=K
        H=[A[r]-K[r] for r in range(len(K))]
    counters['normal_form_stages']+=N+1
    if previous is None: delta=K
    else: delta=[K[r]-previous[r] for r in range(len(K))]
    # A finite Taylor sum only; this is explicitly an empirical indicator.
    residual=sum(norm(X) for X in delta[:L+1])
    W=ode_jet([-1j*X for X in K[:L]],L)
    Wi=inverse_jet(W,L)
    B=convolution(convolution(Wi,H,L),W,L)
    vals,S=mp.eighe(herm(H[0])); counters['eigensystems']+=1
    Sh=dag(S); B=[Sh*X*S for X in B]
    phases=[]; solutions=[]
    for a,group in enumerate(groups):
        size=len(group)
        chi=[]
        for r in range(L):
            C=sum((A[k]*originalP[a][r-k] for k in range(r+1)),zero())
            chi.append(sum(C[i,i] for i in range(3))/size)
        G=[]
        for r in range(L):
            X=mp.matrix([[B[r][i,j] for j in group] for i in group])
            X-=chi[r]*mp.eye(size)
            G.append(-1j*X)
        V=ode_jet(G,L)
        solutions.append(V); phases.append(chi)
    def endpoint(sign):
        D=zero()
        for group,V,chi in zip(groups,solutions,phases):
            phase=sum(chi[r]*mp.mpf(sign)**(r+1)/(r+1) for r in range(len(chi)))
            X=mp.exp(-1j*phase)*evaluate(V,sign)
            for i,ii in enumerate(group):
                for j,jj in enumerate(group): D[ii,jj]=X[i,j]
        return evaluate(W,sign)*S*D*Sh
    Fp,Fm=endpoint(1),endpoint(-1)
    tail=sum(norm(X) for X in W[-5:])
    tail+=sum(sum(norm(X) for X in V[-5:]) for V in solutions)
    tail+=sum(sum(abs(x)/(L-4+j) for j,x in enumerate(C[-5:])) for C in phases)
    return Fp*dag(Fm),float(tail),float(residual),{'groups':[len(g) for g in groups],'N':N}

def run(B,f,s,deadline,L=26,N=3,dps=55):
    mp.mp.dps=dps
    eta=mp.mpf(2)**(-B); umax=1/(2*eta); kappa=mp.mpf(2)**f
    roots_data=json.loads(Path(__file__).with_name('three_channel_scaling_results.json').read_text())
    # Approximate roots are geometry guides only, not certified input enclosures.
    roots=[complex(str(x).replace('*I','j').replace(' ','')) for x in roots_data['complex_discriminant_roots_approximate']]
    tol=2.0**(-s); counters={'eigensystems':0,'projector_jet_orders':0,'normal_form_stages':0,'panels':0,'rejected_panels':0}
    stack=[(-umax,umax)]; U=eye(); records=[]; work_start=time.perf_counter()
    while stack:
        if time.perf_counter()>deadline: raise TimeoutError('native solver row budget exceeded')
        a,b=stack.pop(); c=(a+b)/2; h=(b-a)/2
        distance=min(abs(complex(c)-z) for z in roots)
        if float(h)>0.12*distance:
            stack.extend([(c,b),(a,c)]); continue
        A=base_jet(c,h,kappa,2); groups=groups_for(A[0],8)
        V,tail,res,meta=panel(c,h,kappa,L,N,groups,counters)
        indicator=tail+2*res
        if indicator>tol/2048 or not np.isfinite(indicator):
            counters['rejected_panels']+=1
            # Force direct propagation for a moderate local action rather than
            # indefinitely retrying an asymptotic series in its transition zone.
            if len(groups)>1 and float(norm(A[0]))<12:
                V,tail,res,meta=panel(c,h,kappa,L,0,[[0,1,2]],counters)
                indicator=tail
            if indicator>tol/2048 or not np.isfinite(indicator):
                stack.extend([(c,b),(a,c)]); continue
        U=V*U; counters['panels']+=1
        records.append({'a':str(a),'b':str(b),'indicator_uncertified':indicator,**meta})
        if counters['panels']>1800: raise RuntimeError('prototype panel-count budget exceeded')
    return U,counters,records,time.perf_counter()-work_start

def reference(B,f,rtol=2e-12):
    end=2.0**(B-1); kappa=2.0**f
    def rhs(u,y):
        H=np.array([[u*u-1,1,1/3],[1,u/3,2],[1/3,2,-u*u-u/3+1]],dtype=float)
        return (-1j*kappa*H@y.reshape(3,3)).ravel()
    start=time.perf_counter()
    sol=solve_ivp(rhs,(-end,end),np.eye(3,dtype=complex).ravel(),method='DOP853',rtol=rtol,atol=rtol/100)
    return sol.y[:,-1].reshape(3,3),{'method':'SciPy DOP853 (not a certified or phase-function baseline)','rhs_calls':sol.nfev,'seconds':time.perf_counter()-start,'rtol':rtol,'success':sol.success}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--B',type=int,default=2); ap.add_argument('--f',type=int,default=0)
    ap.add_argument('--s',type=int,default=12); ap.add_argument('--seconds',type=float,default=30)
    ap.add_argument('--L',type=int,default=26); ap.add_argument('--N',type=int,default=3)
    ap.add_argument('--reference',action='store_true'); args=ap.parse_args()
    start=time.perf_counter(); result={'B':args.B,'f':args.f,'s':args.s,'certified':False,'scope':'exploratory numerical prototype only'}
    try:
        U,count,panels,elapsed=run(args.B,args.f,args.s,start+args.seconds,args.L,args.N)
        result.update(status='complete_uncertified',seconds=elapsed,counters=count,panels=panels,
          endpoint=[[[str(mp.re(U[i,j])),str(mp.im(U[i,j]))] for j in range(3)] for i in range(3)],
          unitarity_defect_frobenius=float(norm(dag(U)*U-eye())))
        if args.reference:
            V,ref=reference(args.B,args.f)
            U0=np.array([[complex(U[i,j]) for j in range(3)] for i in range(3)])
            result.update(reference=ref,observed_operator_disagreement=float(np.linalg.norm(U0-V,2)))
    except (TimeoutError,RuntimeError) as exc:
        result.update(status='censored',seconds=time.perf_counter()-start,reason=str(exc))
    out=Path(__file__).with_name(f'prototype_B{args.B}_f{args.f}_s{args.s}.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('panels','endpoint')},indent=2))
