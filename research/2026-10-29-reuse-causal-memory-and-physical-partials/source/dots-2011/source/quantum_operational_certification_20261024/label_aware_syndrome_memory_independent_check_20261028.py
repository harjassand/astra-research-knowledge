#!/usr/bin/env python3
"""Exact independent complete-memory and actual label-aware feedback fixtures."""
import itertools
import json
from math import lcm
from pathlib import Path
import numpy as np
import sympy as s

I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
PAULIS=[I,X,Y,Z]
def kron(*xs):
    r=s.ones(1,1)
    for x in xs:r=s.kronecker_product(r,x)
    return r
def clean(A):return A.applyfunc(s.expand)
ESET=[0,4,2,1]
Enc=s.zeros(8,2); Enc[0,0]=1; Enc[7,1]=1
Um=s.zeros(8)
for l,g in itertools.product(range(2),range(4)):Um[(7*l)^ESET[g],4*l+g]=1
XF=[kron(*[X if f&(1<<(2-i)) else I for i in range(3)]) for f in range(8)]
ZP=[kron(*[Z if i==j else I for j in range(3)]) for i in range(3)]
V=(5*s.eye(8)-12*s.I*kron(X,X,Z))/13
assert clean(V.H*V)==s.eye(8)
U=clean(V*Um)
CX=clean(V*XF[7]*V.H)
CI=[clean(V*P*V.H) for P in ZP]
K=[s.diag(1,s.Rational(3,5)),s.Matrix([[0,s.Rational(4,5)],[0,0]])]
assert sum((A.H*A for A in K),s.zeros(2))==I
assert K[0]*K[1]!=K[1]*K[0]
def iid(p):return [p**f.bit_count()*(1-p)**(3-f.bit_count()) for f in range(8)]
q0=[s.Rational(0)]*8;q0[0]=s.Rational(3,5);q0[6]=q0[5]=s.Rational(1,5)
q1=[s.Rational(0)]*8;q1[0]=s.Rational(1,2)
for f in [7,4,2,1]:q1[f]=s.Rational(1,8)
WORLD={
    'memory_mixture_iid': [iid(s.Rational(0)),iid(s.Rational(1,4))],
    'correlated_nonmajority_dominant': [q0,q1],
}
def fmap(weights,f,M):
    return clean(sum((weights[a][f]*K[a]*M*K[a].H for a in range(2)),s.zeros(2)))
def tmap(M):return clean(sum((A*M*A.H for A in K),s.zeros(2)))
def hmap(weights,i,M):
    return clean(sum(((-1 if f&(1<<(2-i)) else 1)*fmap(weights,f,M) for f in range(8)),s.zeros(2)))
def physical(weights,L,M,injections):
    # Physical encoder, actual X injection/error, unknown V; no majority coordinates.
    encoded=Enc*L*Enc.H
    out=s.zeros(16)
    for e in injections:
        for f in range(8):
            A=clean(V*XF[f]*XF[e]*encoded*XF[e].H*XF[f].H*V.H)
            out+=kron(A,fmap(weights,f,M))/len(injections)
    return clean(out)
def model(weights,L,M):
    out=s.zeros(16)
    for g,eg in enumerate(ESET):
        G=s.zeros(4);G[g,g]=1
        ai=clean(sum((fmap(weights,e^eg,M) for e in ESET),s.zeros(2))/4)
        ax=clean(sum((fmap(weights,e^eg^7,M) for e in ESET),s.zeros(2))/4)
        assert ai+ax==tmap(M)/4
        out+=kron(clean(U*kron(L,G)*U.H),ai)
        out+=kron(clean(U*kron(X*L*X,G)*U.H),ax)
    return clean(out)

complete_entries=0;signed_entries=0;world_biases={}
for world,weights in WORLD.items():
    assert all(sum(q)==1 and min(q)>=0 for q in weights)
    biases=[[sum(((-1 if f&(1<<(2-i)) else 1)*q[f] for f in range(8)),s.Rational(0)) for i in range(3)] for q in weights]
    assert min(v for row in biases for v in row)>=0
    world_biases[world]=[[str(v) for v in row] for row in biases]
    for a,b in itertools.product(range(2),repeat=2):
        M=s.zeros(2);M[a,b]=1
        assert physical(weights,I/2,M,ESET)==kron(s.eye(8)/8,tmap(M))
        assert physical(weights,X/2,M,ESET)==kron(CX/8,tmap(M))
        for i in range(3):
            out=s.zeros(16)
            for e in ESET:
                out+=(-1 if e&(1<<(2-i)) else 1)*physical(weights,Z/2,M,[e])/4
            assert clean(out)==kron(CI[i]/8,hmap(weights,i,M));signed_entries+=256
        for l,m in itertools.product(range(2),repeat=2):
            L=s.zeros(2);L[l,m]=1
            assert physical(weights,L,M,ESET)==model(weights,L,M);complete_entries+=256
    if world=='memory_mixture_iid':
        for a,p in enumerate([s.Rational(0),s.Rational(1,4)]):
            t=1-2*p
            hz=[sum((weights[a][e^g]-weights[a][e^g^7] for e in ESET),s.Rational(0))/4 for g in ESET]
            assert hz==[(3*t-t**3)/8]+[(t+t**3)/8]*3

# Enumerate actual product readouts as a retained-MEMORY instrument, not scalar
# Born probabilities only. The signed empirical shadows have the claimed joint
# output-plus-memory means, including off-diagonal memory coherences.
weights=WORLD['correlated_nonmajority_dominant']
omega=s.Matrix([[s.Rational(3,5),s.I/5],[-s.I/5,s.Rational(2,5)]])
assert omega.det()>0
outputs={(j,sgn,e):physical(weights,(I+sgn*PAULIS[j])/2,omega,[e])
         for j,sgn,e in itertools.product([1,3],[-1,1],ESET)}
D=1
for out in outputs.values():
    for v in out:D=lcm(D,int(s.re(v).q),int(s.im(v).q))
def nums(A,den):
    rr=np.empty(A.shape,dtype=object);ii=np.empty(A.shape,dtype=object)
    for a,b in itertools.product(range(A.rows),range(A.cols)):
        r=s.re(A[a,b])*den;j=s.im(A[a,b])*den
        assert r.q==j.q==1;rr[a,b]=int(r);ii[a,b]=int(j)
    return rr,ii
meas=[]
for axes,bits in itertools.product(itertools.product([1,2,3],repeat=3),itertools.product([-1,1],repeat=3)):
    pis=[(I+bit*PAULIS[axis])/2 for axis,bit in zip(axes,bits)]
    mr,mi=nums(kron(*pis),8);zr,zi=nums(kron(*[3*pi-I for pi in pis]),8)
    meas.append((mr.T.reshape(64),mi.T.reshape(64),zr,zi))
accum={v:[np.zeros((16,16),dtype=object),np.zeros((16,16),dtype=object)] for v in ['unsigned','X',0,1,2]}
events=0
for (j,sgn,e),out in outputs.items():
    rr,ii=nums(out,D)
    rr=rr.reshape(8,2,8,2).transpose(0,2,1,3).reshape(64,4)
    ii=ii.reshape(8,2,8,2).transpose(0,2,1,3).reshape(64,4)
    for mr,mi,zr,zi in meas:
        pr=(mr@rr-mi@ii).reshape(2,2);pi=(mr@ii+mi@rr).reshape(2,2)
        assert pr[0,0]+pr[1,1]>=0 and pi[0,0]+pi[1,1]==0
        real=np.kron(zr,pr)-np.kron(zi,pi);imag=np.kron(zr,pi)+np.kron(zi,pr)
        coeffs={'unsigned':1,'X':2*sgn if j==1 else 0}
        coeffs.update({i:2*sgn*(-1 if e&(1<<(2-i)) else 1) if j==3 else 0 for i in range(3)})
        for v,c in coeffs.items():accum[v][0]+=c*real;accum[v][1]+=c*imag
        events+=1
den=D*8*8*16*27
targets={'unsigned':kron(s.eye(8)/8,tmap(omega)),'X':kron(CX/8,tmap(omega))}
targets.update({i:kron(CI[i]/8,hmap(weights,i,omega)) for i in range(3)})
for v,target in targets.items():
    rr,ii=nums(target,den);assert np.array_equal(accum[v][0],rr) and np.array_equal(accum[v][1],ii)

# Exact known-matrix rounding fixture where the fitted coordinate reflections
# do NOT commute. Diagonal truncation itself has a certified Frobenius residual.
b=s.Rational(1,8);c=b/8;r=s.Rational(1,10000)
co=(1-r*r)/(1+r*r);si=2*r/(1+r*r)
S=[co*ZP[0]+si*kron(X,X,I),ZP[1],ZP[2]]
assert all(A*A==s.eye(8) for A in S)
assert S[0]*S[1]!=S[1]*S[0]
assert 2*(1-co)<=c*c
That=sum(S,s.zeros(8));Chat=s.diag(*That.diagonal())
residual=sum(s.re(v)**2+s.im(v)**2 for v in That-Chat)
assert residual<=(b/8)**2
SZ=s.diag(*[s.sign(v) for v in Chat.diagonal()]);BX=XF[7]
BZ=(ZP[0]+ZP[1]+ZP[2]-ZP[0]*ZP[1]*ZP[2])/2
assert SZ==BZ and SZ*SZ==s.eye(8) and BX*SZ+SZ*BX==s.zeros(8)
CZ=kron((s.eye(8)+SZ)/2,I)+kron((s.eye(8)-SZ)/2,X)
CXgate=kron(s.eye(8),s.diag(1,0))+kron(BX,s.diag(0,1))
SWAP=s.zeros(16)
for l,g,a in itertools.product(range(2),range(4),range(2)):SWAP[(4*a+g)*2+l,(4*l+g)*2+a]=1
assert CZ*CXgate*CZ==kron(Um,I)*SWAP*kron(Um.H,I)

# Rational budget/sign inequalities over representative funded resolutions.
budget_cases=0
for b in [s.Rational(1,4),s.Rational(1,8),s.Rational(1,32)]:
    c=b/8
    for gamma in [s.Rational(1,8),s.Rational(1,80),s.Rational(1,800)]:
        stage=0;a=s.Rational(1,128)
        while a>c*gamma/5:stage+=1;a/=2
        assert a>b*gamma/80
        N=8*27/a**2
        assert N<51200*27/(b*b*gamma*gamma)
        cumulative=sum(8*27/(s.Rational(1,128)/4**0/2**j)**2 for j in range(stage+1))
        assert cumulative<s.Rational(4,3)*N
        e=s.Rational(5,4)*a;h=gamma-e
        assert h>e and 2*e<=c*(2*h-e)
        assert b/(2-b/2)<b
        budget_cases+=1

out={'status':'PASS_COMPLETE_MEMORY_LABEL_AWARE_CONTRASTS_NONCOMMUTING_FIT_AND_BUDGETS',
     'source_outcomes':0,'rng_draws':0,'memory_dimension':2,'noncommuting_memory_Kraus':True,
     'complete_channel_matrix_entries':complete_entries,'complete_signed_memory_entries':signed_entries,
     'actual_injection_probe_readout_memory_events':events,'feedback_output_integer_denominator':str(D),
     'world_component_biases':world_biases,
     'noncommuting_fitted_coordinate_controls':True,'final_rounding_Frobenius_residual_squared':str(residual),
     'literal_coherent_extraction_entries':256,'finite_budget_cases':budget_cases,
     'production_tomography_or_general_Jacobi_compiler_executed':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
