#!/usr/bin/env python3
"""Author algebra checks: phase-correct online U(2) tensors and full exact-AA isometry.
Not a gate-level execution of the high-dimensional compiler.
"""
from pathlib import Path
from fractions import Fraction
import itertools,json,math
import numpy as np
from sympy import Rational
from sympy.physics.wigner import clebsch_gordan
ROOT=Path(__file__).resolve().parent

def partitions2(n):return [(n-b,b) for b in range(n//2+1)]
def dd(l):return l[0]-l[1]+1

def embedding(l,mu):
    j=Rational(l[0]-l[1],2);J=Rational(mu[0]-mu[1],2)
    a=dd(l);b=dd(mu);C=np.zeros((a,2,b),complex)
    phase=np.exp(1j*(.137+sum((h+1)*v for h,v in enumerate(l))*.071+mu[1]*.283))
    for ia in range(a):
        for i in range(2):
            for ib in range(b):
                C[ia,i,ib]=complex(clebsch_gordan(j,Rational(1,2),J,j-ia,Rational(1,2)-i,J-ib))*phase
    assert np.max(abs(C.reshape(2*a,b).conj().T@C.reshape(2*a,b)-np.eye(b)))<1e-12
    return C

def memlayout(n):
    states=[]
    for l in partitions2(n):
        for a in range(dd(l)):
            for d in range(dd(l)):states.append((l,a,d))
    return states,{x:i for i,x in enumerate(states)}

def advance(V,n,wrong=False):
    oldstates,_=memlayout(n-1);states,index=memlayout(n)
    oldout=2**(n-1);oldin=2**(n-1)
    old=V.reshape(oldout,len(oldstates),oldin)
    new=np.zeros((oldout*2,len(states),oldin*2),complex)
    for mi,(l,a,d) in enumerate(oldstates):
        for mu in partitions2(n):
            if not ((mu[0]==l[0]+1 and mu[1]==l[1]) or (mu[0]==l[0] and mu[1]==l[1]+1)):continue
            C=embedding(l,mu)
            for ip in range(2):
                for bp in range(dd(mu)):
                    G=C[a,ip,bp].conjugate()
                    if abs(G)<1e-14:continue
                    for jo in range(2):
                        for bd in range(dd(mu)):
                            Fc=C[d,jo,bd].conjugate() if wrong else C[d,jo,bd]
                            coeff=G*math.sqrt(dd(l)/dd(mu))*Fc
                            if abs(coeff)<1e-14:continue
                            for op in range(oldout):
                                new[2*op+jo,index[(mu,bp,bd)],ip::2]+=coeff*old[op,mi,:]
    return new.reshape(oldout*2*len(states),oldin*2)

def perms(d,n):
    out=[]
    for p in itertools.permutations(range(n)):
        a=np.zeros((d**n,d**n),complex)
        for col,idx in enumerate(itertools.product(range(d),repeat=n)):
            row=np.ravel_multi_index(tuple(idx[p[j]] for j in range(n)),(d,)*n);a[row,col]=1
        out.append(a)
    return np.array(out)

res={'scope':'author finite tensor/block algebra only; high-dimensional compiled circuit not executed','online_levels':[]}
V=np.ones((1,1),complex);VW=V.copy()
for n in range(1,5):
    V=advance(V,n);VW=advance(VW,n,True)
    D=2**n;ms=len(memlayout(n)[0]);vv=V.reshape(D,ms,D);ww=VW.reshape(D,ms,D)
    P=perms(2,n);flat=P.reshape(len(P),-1);Gp=np.linalg.pinv(flat.conj()@flat.T,rcond=1e-12)
    maxerr=0;wrongerr=0
    for a in range(D):
        for b in range(D):
            e=np.zeros((D,D),complex);e[a,b]=1
            tw=np.einsum('p,pij->ij',Gp@np.einsum('pij,ij->p',P.conj(),e),P)
            out=vv[:,:,a]@vv[:,:,b].conj().T
            wrongout=ww[:,:,a]@ww[:,:,b].conj().T
            maxerr=max(maxerr,float(np.max(abs(out-tw))))
            wrongerr=max(wrongerr,float(np.max(abs(wrongout-tw))))
    iso=float(np.max(abs(V.conj().T@V-np.eye(D))))
    assert maxerr<2e-12 and iso<2e-12
    res['online_levels'].append({'n':n,'isometry_error':iso,'all_matrix_unit_haar_error':maxerr,
                                 'wrong_conjugated_embedding_haar_error':wrongerr})
assert res['online_levels'][-1]['wrong_conjugated_embedding_haar_error']>.01
# Explicit co-CG at common target mu=(2,1), including nontrivial complex edge phases.
mu=(2,1);pre=[(2,0),(1,1)]
Fs=[];alphas=[];k=2;m=2
for l in pre:
    C=embedding(l,mu);F=math.sqrt(dd(l)/dd(mu))*C.transpose(1,2,0).reshape(2*dd(mu),dd(l))
    Fs.append(F);alphas.extend([math.sqrt(dd(mu)/(k*m*dd(l)))]*dd(l))
F=np.column_stack(Fs);assert np.max(abs(F.conj().T@F-np.eye(4)))<1e-12
J=8*k*math.ceil(math.sqrt(k));theta=math.pi/(4*J+2);c=math.sin(theta)
alpha=np.diag(alphas);weighted=F@alpha;r=np.diag(c/np.array(alphas))
assert np.max(abs(weighted@r-c*F))<1e-12
# Full unitary dilation with good/failure flags, not a success-probability check.
b=math.sqrt(1-c*c)
U=np.block([[c*F,b*F],[b*np.eye(4),-c*np.eye(4)]])
assert np.max(abs(U.conj().T@U-np.eye(8)))<1e-12
Pi=np.diag([1.]*4+[0.]*4);S=np.eye(8)-2*Pi
Q=-U@S@U.conj().T@S
out=np.linalg.matrix_power(Q,J)@U[:,:4]
target=np.vstack([F,np.zeros((4,4))])
err=float(np.linalg.norm(out-target,2));leak=float(np.linalg.norm(out[4:,:],2))
assert err<1e-11 and leak<1e-11
res['full_exact_aa']={'k':k,'iterations':J,'amplitude':c,'max_attenuation':float(max(c/np.array(alphas))),
                     'full_isometry_operator_error':err,'failure_flag_operator_leakage':leak}
res['pass']=True
(ROOT/'explicit_online_random_dimension_reduction_compiler_check.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
