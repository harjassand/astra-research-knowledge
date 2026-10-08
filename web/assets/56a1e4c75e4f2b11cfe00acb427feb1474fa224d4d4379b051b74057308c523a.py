"""Small finite diagnostics for proof/acquisition; not theorem validation.
Run: OPENBLAS_NUM_THREADS=1 python3 outputs/research/sol_collective_critical/checks.py
NumPy plus Python stdlib. No continuum oracle, large acquisition, or circuit run.
"""
from fractions import Fraction as F
from itertools import combinations
import json
import math
from pathlib import Path
import numpy as np

RNG = np.random.default_rng(81012611)
TOL = 1e-8


def sector(L, m, J=1.0):
    xs = list(combinations(range(1, L), m))
    ix = {x:i for i,x in enumerate(xs)}
    T = np.zeros((len(xs), len(xs)))
    W = np.zeros(len(xs))
    for i,x in enumerate(xs):
        occ = set(x)
        T[i,i] = 2*J*L**2*((1 in occ)+(L-1 in occ))
        W[i] = sum(v+1 in occ for v in x)
        for v in x:
            for dest in (v-1,v+1):
                if 1<=dest<L and dest not in occ:
                    y = tuple(sorted((occ-{v})|{dest}))
                    T[i,i] += 2*J*L**2
                    T[i,ix[y]] -= 2*J*L**2
    return xs,T,L*np.diag(W)


def heat(A, tau):
    e,u = np.linalg.eigh(A)
    return (u*np.exp(-tau*e))@u.T


def polar(C):
    G=C.T@C
    e,u=np.linalg.eigh(G)
    return C@((u*(e**-.5))@u.T)


def inertia(matrix):
    """Exact rational symmetric congruence, including all-zero-diagonal 2x2.
    Returns (negative,zero,positive); no float decisions.
    """
    A=[list(row) for row in matrix]
    neg=zero=pos=0
    while A:
        n=len(A)
        p=next((i for i in range(n) if A[i][i]),None)
        if p is not None:
            order=[p]+[i for i in range(n) if i!=p]
            A=[[A[i][j] for j in order] for i in order]
            a=A[0][0]
            neg += a<0
            pos += a>0
            A=[[A[i][j]-A[i][0]*A[0][j]/a for j in range(1,n)]
               for i in range(1,n)]
        else:
            pair=next(((i,j) for i in range(n) for j in range(i+1,n)
                       if A[i][j]),None)
            if pair is None:
                zero+=n
                break
            i,j=pair
            order=[i,j]+[k for k in range(n) if k not in pair]
            A=[[A[i][j] for j in order] for i in order]
            b=A[0][1]
            neg+=1
            pos+=1
            A=[[A[i][j]-(A[i][0]*A[1][j]+A[i][1]*A[0][j])/b
                for j in range(2,n)] for i in range(2,n)]
    return int(neg),int(zero),int(pos)


ratio_errors=[]
convex_margins=[]
leak_ratios=[]
weighted_b_margins=[]
for L in (4,6,8):
    tau=.07
    ts=[]
    vs=[]
    for m in range(L):
        _,T,V=sector(L,m)
        ts.append(T);vs.append(V)
    for g in (.1,.4,.7):
        zs=np.array([np.trace(heat(T+g*V,tau)) for T,V in zip(ts,vs)])
        for lam in (-1.1,0.,.8):
            weights=zs*np.exp(tau*lam*np.arange(L))
            ps=weights/weights.sum()
            ratio_errors.append(abs(ps[0]*ps[2]/ps[1]**2-zs[2]/zs[1]**2))
        dh=.03
        zminus=np.trace(heat(ts[2]+(g-dh)*vs[2],tau))
        zplus=np.trace(heat(ts[2]+(g+dh)*vs[2],tau))
        convex_margins.append(zminus+zplus-2*zs[2])
    for m in (2,3):
        T,V=ts[m],vs[m]
        for g,h in ((.2,.3),(.6,.4),(.4,.41)):
            e,u=np.linalg.eigh(T+g*V)
            f,v=np.linalg.eigh(T+h*V)
            for R in (2.1*e[0],3*e[0],4*e[0]):
                for i in np.flatnonzero(e<=R/2):
                    psi=u[:,i]
                    leak=float(np.linalg.norm(v[:,f>R].T@psi)**2)
                    rhs=8*(g-h)**2*e[i]/(.1**2*R)
                    leak_ratios.append(leak/rhs if rhs else 0.)
                    bv=v.T@V@psi
                    lhs=float(np.sum(bv*bv/(f+1)))
                    bound=e[i]/(g*h)
                    weighted_b_margins.append(bound-lhs)

# Count-only sorting/reshuffling and data-dependent projection instrument.
L=4;tau=.11;g=.38;lam=.7
physical=[];probs=[];normalized=[];embeds=[]
for m in range(L):
    xs,T,V=sector(L,m)
    em=np.zeros((2**(L-1),len(xs)))
    for j,x in enumerate(xs):
        em[sum(1<<(v-1) for v in x),j]=1
    A=T+g*V
    z=np.trace(heat(A,tau))
    normalized.append(heat(A,tau)/z)
    physical.append(em@(heat(A,tau)*np.exp(tau*lam*m))@em.T)
    embeds.append(em)
    probs.append(z*np.exp(tau*lam*m))
Z=sum(probs);probs=np.array(probs)/Z
rho=sum(physical)/Z
target=np.kron(rho,rho)
dim=len(rho)
swap=np.array([j*dim+i for i in range(dim) for j in range(dim)])
exact=np.zeros_like(target);projected=np.zeros_like(target)
passed=0.
for m in range(L):
    for k in range(m,L):
        wt=probs[m]*probs[k]*(1 if m==k else 2)
        gamma=np.kron(normalized[m],normalized[k])
        embed=np.kron(embeds[m],embeds[k])
        source=embed@gamma@embed.T
        exact+=wt*(source if m==k else (source+source[swap][:,swap])/2)
        # Any count-dependent estimate is legal; n=2 is too small for the
        # uniform statistical good event, so this checks only TP/gentle algebra.
        h=.13+.07*(m+k)
        qs=[]
        for t in (m,k):
            _,T,V=sector(L,t)
            e,u=np.linalg.eigh(T+h*V)
            R=58.
            keep=e<=R
            qs.append(u[:,keep]@u[:,keep].T)
        P=np.kron(*qs)
        out=embed@P@gamma@P@embed.T
        projected+=wt*(out if m==k else (out+out[swap][:,swap])/2)
        passed+=wt*np.trace(out)
projected[0,0]+=1-passed
instrument_error=float(np.linalg.norm(np.linalg.eigvalsh(projected-target),1))
gentle_bound=2*math.sqrt(max(0,1-passed))+1-passed

# Qubit three-copy Schur: spin 1/2 multiplicity I_2 is discarded/reprepared.
basis=np.eye(8)
col=[basis[:,0],(basis[:,1]+basis[:,2]+basis[:,4])/math.sqrt(3),
     (basis[:,3]+basis[:,5]+basis[:,6])/math.sqrt(3),basis[:,7],
     (basis[:,2]-basis[:,4])/math.sqrt(2),
     math.sqrt(2/3)*basis[:,1]-(basis[:,2]+basis[:,4])/math.sqrt(6),
     (basis[:,3]-basis[:,5])/math.sqrt(2),
     (basis[:,3]+basis[:,5])/math.sqrt(6)-math.sqrt(2/3)*basis[:,6]]
schur=np.column_stack(col)
schur_errors=[]
for _ in range(20):
    x=RNG.normal(size=(2,2))+1j*RNG.normal(size=(2,2))
    sigma=x@x.conj().T;sigma/=np.trace(sigma)
    t=np.kron(np.kron(sigma,sigma),sigma)
    transformed=schur.T@t@schur
    restored=np.zeros_like(transformed)
    restored[:4,:4]=transformed[:4,:4]
    block=transformed[4:,4:].reshape(2,2,2,2)
    retained=np.einsum('abcb->ac',block)
    restored[4:,4:]=np.kron(retained,np.eye(2)/2)
    schur_errors.append(float(np.linalg.norm(restored-transformed)))

gap_margins=[];inertia_cases=0
for L in range(4,8):
    _,T,V=sector(L,2)
    for g in (F(1,10),F(7,10)):
        A=[[F(int(T[i,j]))+g*F(int(V[i,j])) for j in range(len(T))]
           for i in range(len(T))]
        a=len(A);Dbar=a;R=F(80);K=2*Dbar+2;s=R/K;Delta=s/4
        eig=np.linalg.eigvalsh(np.array(A,dtype=float))
        for j in range(1,K+1):
            E=R+(F(j)-F(1,2))*s
            iv=[]
            for end in (E-Delta,E+Delta):
                shifted=[[A[i][k]-(end if i==k else 0) for k in range(a)]
                         for i in range(a)]
                iv.append(inertia(shifted))
                floats=np.linalg.eigvalsh(np.array(shifted,dtype=float))
                assert iv[-1][0]==int(np.sum(floats<-1e-7))
                inertia_cases+=1
            if iv[0][1]==iv[1][1]==0 and iv[0][0]==iv[1][0]:
                gap_margins.append(float(np.min(abs(eig-float(E)))-float(Delta)))
                break
        else:
            raise AssertionError('pigeonhole threshold failure')

column_margins=[];polar_ratios=[]
for a in range(4,9):
    for d in range(1,min(a,4)):
        u,_=np.linalg.qr(RNG.normal(size=(a,d)))
        P=u@u.T;Bb=math.comb(a,d)
        sets=list(combinations(range(a),d))
        dets=[np.linalg.det(P[:,I].T@P[:,I]) for I in sets]
        column_margins.append(max(dets)-1/Bb)
        nu=.1;zeta=nu/(1024*a*2**d*Bb**2)
        noise=RNG.normal(size=(a,a));noise=(noise+noise.T)/2
        noise*=zeta/np.linalg.norm(noise,2)
        Pt=P+noise
        I=max(sets,key=lambda I:np.linalg.det(Pt[:,I].T@Pt[:,I]))
        C=P[:,I];Ct=Pt[:,I]
        error=float(np.linalg.norm(polar(Ct)-polar(C),2))
        polar_ratios.append(error/(8*Bb**1.5*zeta))

poly_margins=[]
for gap in (.2,.4,.7):
    q=40
    for x in np.r_[np.linspace(-1,-gap,40),np.linspace(gap,1,40)]:
        b=1.;series=1.;power=1.
        for k in range(1,q+1):
            b*= (2*k-1)/(2*k);power*=1-x*x;series+=b*power
        proj=(1-x*series)/2
        err=abs(proj-(x<0))
        bound=math.exp(-(q+1)*gap**2)/(2*gap**2)
        poly_margins.append(bound-err)

out={
    'status':'FINITE-EVIDENCE; small matrix/count diagnostics only',
    'ratio_cases':len(ratio_errors),'max_ratio_error':max(ratio_errors),
    'min_convex_second_difference':min(convex_margins),
    'leakage_cases':len(leak_ratios),'max_leakage_to_bound_ratio':max(leak_ratios),
    'min_weighted_contact_margin':min(weighted_b_margins),
    'count_shuffle_exact_error':float(np.linalg.norm(exact-target)),
    'dependent_projection_trace_error':instrument_error,
    'dependent_projection_gentle_bound':gentle_bound,
    'schur_cases':len(schur_errors),'max_schur_exact_error':max(schur_errors),
    'rational_inertia_cases':inertia_cases,'min_public_gap_margin':min(gap_margins),
    'column_cases':len(column_margins),'min_column_determinant_margin':min(column_margins),
    'max_polar_to_bound_ratio':max(polar_ratios),
    'scalar_sign_cases':len(poly_margins),'min_sign_polynomial_bound_margin':min(poly_margins),
    'omitted':['large inverse-constant acquisition','growing-n circuit execution',
               'continuum convergence proof','external validity','priority']}
assert max(ratio_errors)<TOL
assert min(convex_margins)>-TOL
assert max(leak_ratios)<=1+TOL
assert min(weighted_b_margins)>=-TOL
assert np.linalg.norm(exact-target)<TOL
assert instrument_error<=gentle_bound+TOL
assert max(schur_errors)<TOL
assert min(gap_margins)>-TOL
assert min(column_margins)>-TOL
assert max(polar_ratios)<=1+TOL
assert min(poly_margins)>-TOL
out['passed']=True
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
