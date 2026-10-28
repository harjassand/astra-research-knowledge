#!/usr/bin/env python3
"""Independent exact endpoint fixtures. Not a generic GLS run or gate compiler.
No author check code imported. Deliberately exercises rational TP, complex
Choi composition, nonphysical signed projection and near-isometry completion.
"""
from pathlib import Path
import sympy as s
import itertools, json, hashlib
P=Path(__file__).resolve().parent; R=s.Rational; I=s.I

def tidy(A): return A.applyfunc(s.simplify)
def eq(A,B): assert tidy(A-B)==s.zeros(*A.shape)
def pt(A,m,n): return s.Matrix(m,m,lambda i,j:sum(A[i*n+x,j*n+x] for x in range(n)))
def f2(A): return s.simplify(s.trace(A.H*A))
def psd(A):
    # Independent exact principal-minor criterion, feasible only for small fixtures.
    for z in range(1,A.rows+1):
        for ix in itertools.combinations(range(A.rows),z):
            assert s.simplify(A.extract(ix,ix).det())>=0

def hb(d,tracezero=False):
    out=[]
    for j in range(d-int(tracezero)):
        A=s.zeros(d);A[j,j]=1
        if tracezero:A[-1,-1]=-1
        out.append(A)
    for j in range(d):
        for k in range(j):
            A=s.zeros(d);A[j,k]=A[k,j]=1;out.append(A)
            A=s.zeros(d);A[j,k]=I;A[k,j]=-I;out.append(A)
    return out

basis_cases=0
for m,n in itertools.product(range(1,5),repeat=2):
    bm,bn=hb(m),hb(n,True)
    Gm=s.Matrix(len(bm),len(bm),lambda j,k:s.trace(bm[j]*bm[k]))
    Gn=s.Matrix(len(bn),len(bn),lambda j,k:s.trace(bn[j]*bn[k]))
    valsm=list(Gm.eigenvals());valsn=list(Gn.eigenvals())
    if valsn:
        assert min(x*y for x in valsm for y in valsn)>=1
        assert max(x*y for x in valsm for y in valsn)<=4*n
    assert len(bm)*len(bn)==m*m*(n*n-1)
    for A in bm:
        for B in bn:eq(pt(s.kronecker_product(A,B),m,n),s.zeros(m))
    basis_cases+=1

radius_cases=0
for m,n,a,b,ell,g in itertools.product(range(1,4),range(1,4),range(1,4),range(1,4),[R(1,3),R(1),R(3)],[R(0),R(1,5),R(7)]):
    s0=ell*m+g+1;t0=b*s0+1;r=1/(8*(n*n+n*ell+b+1));T=2*t0
    assert 2*n*r<R(1,n)
    assert (2+2*n*ell)*r<1 and (1+2*b)*r<1
    assert r<t0 and r<T-t0
    W=2+4*b+2*b*n*ell+8*m*n*n
    coefficient=1+(1+4*b+2*b*n*ell)/2+4*m*n*n
    assert coefficient==(W+1)/2 and coefficient/(4*W)<1
    radius_cases+=1

# Exact zero-diagonal separator in a complex Hermitian block.
h=R(2,3)+I*R(5,7);d=R(11,13)
Q=s.Matrix([[0,h],[s.conjugate(h),d]])
v=s.Matrix([1,-s.conjugate(h)/(d+1)])
witness=s.simplify((v.H*Q*v)[0])
assert witness==-s.simplify(abs(h)**2*(d+2)/(d+1)**2) and witness<0
# Lift a nontrivial complex Schur witness, independently using a factorization.
B=s.Matrix([[1,I],[R(1,3),R(1,2)]]);D=s.diag(2,-R(1,5))
Q2=B*D*B.H;v2=B.H.inv()*s.Matrix([0,1])
assert s.simplify((v2.H*Q2*v2)[0])==-R(1,5)

# A signed Pauli channel with a known unrestricted-CPTP nearest channel.
# Bell input negative mass lower bounds all CPTP choices; identity attains a.
Id=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-I],[I,0]])
def choi(ks):
    vs=[s.Matrix([K[o,i] for i in range(K.cols) for o in range(K.rows)]) for K in ks]
    return sum((v*v.H for v in vs),s.zeros(vs[0].rows))
Jid=choi([Id]);Jx=choi([X]);a=R(1,7);Jhat=(1+a)*Jid-a*Jx
assert min(Jhat.eigenvals())==-2*a
eq(pt(Jhat,2,2),Id)
assert sum(abs(x)*mult for x,mult in ((Jhat-Jid)/2).eigenvals().items())/2==a
# TP repair exactly, including complex off-diagonal unitary Choi.
repair_cases=[]
Uc=s.Matrix([[R(3,5),I*R(4,5)],[I*R(4,5),R(3,5)]])
JU=choi([Uc]);JUX=choi([Uc*X])
for e in [R(1,1000),R(1,97),R(1,32)]:
    C=(1+e)*JU-e*JUX;ac=4*e
    assert min(C.eigenvals())>=-ac
    Cp=tidy((C+2*ac*s.eye(4))/(1+4*ac))
    eq(pt(Cp,2,2),Id);psd(Cp-ac/(1+4*ac)*s.eye(4))
    displacement=s.simplify(sum(abs(x)*mult for x,mult in (Cp-C).eigenvals().items()))
    assert displacement<=16*ac
    repair_cases.append({'e':str(e),'trace_norm_displacement':str(displacement),'bound':str(16*ac)})

# Complete depolarization recovery optimum over ALL CPTP decoders is 3/4:
# any output state has Bell overlap 1/4, and maximally mixed output attains it.
Jdep=s.eye(4)/2;delta=Jdep-Jid;Z=s.eye(4)/2+Jid/2
psd(Z-delta);psd(Z+delta);eq(pt(Z,2,2),R(3,2)*Id)
phi=Jid/2
for state in [s.diag(1,0),Id/2,s.Matrix([[R(1,2),I*R(1,3)],[-I*R(1,3),R(1,2)]])]:
    psd(state)
    assert s.trace(phi*s.kronecker_product(Id/2,state))==R(1,4)

# Check input-first complex composition convention against actual Kraus products.
K=[s.diag(R(3,5),1),s.Matrix([[0,0],[R(4,5),0]])]
L=[Uc*s.diag(1,R(5,13)),Uc*s.Matrix([[0,R(12,13)],[0,0]])]
eq(sum((A.H*A for A in K),s.zeros(2)),Id)
eq(sum((A.H*A for A in L),s.zeros(2)),Id)
N,C=choi(K),choi(L)
composed=s.Matrix(4,4,lambda ia,jb:sum(N[2*(ia//2)+y,2*(jb//2)+z]*C[2*y+ia%2,2*z+jb%2] for y,z in itertools.product(range(2),repeat=2)))
eq(composed,choi([B*A for A in K for B in L]))
# Full linear coefficient norm bound via Cauchy-Schwarz is uniform for arbitrary
# complex perturbations, not just TP/PSD; verify its exact 16x16 operator Gram.
units=[]
for j,k in itertools.product(range(4),repeat=2):
    E=s.zeros(4);E[j,k]=1
    out=s.Matrix(4,4,lambda ia,jb:sum(N[2*(ia//2)+y,2*(jb//2)+z]*E[2*y+ia%2,2*z+jb%2] for y,z in itertools.product(range(2),repeat=2)))
    units.append(s.Matrix(list(out)))
SL=s.Matrix.hstack(*units)
assert max((SL.H*SL).eigenvals())<=f2(N)<=4

# Independent exact QR completion: complex Fourier isometry times a near-I
# triangular perturbation, so the thin-Q answer is known independently.
F=s.Matrix([[I**(j*k)/2 for k in range(4)] for j in range(4)]);eq(F.H*F,s.eye(4))
V=F[:,:2];eps=R(1,1000);Rt=s.Matrix([[1+eps,2*eps],[0,1-eps]])
A=V*Rt;work=A.copy();Qleft=s.eye(4);givens=0;pivot_floor=[]
for j in range(2):
    pivot=max(range(j,4),key=lambda row:float(s.simplify(abs(work[row,j])**2)))
    if pivot!=j:
        Pm=s.eye(4);Pm.row_swap(j,pivot);work=tidy(Pm*work);Qleft=tidy(Pm*Qleft)
    pivot_floor.append(str(s.simplify(abs(work[j,j])**2)))
    assert abs(work[j,j])**2>R(1,16)
    for row in range(j+1,4):
        aa,bb=work[j,j],work[row,j]
        rr=s.sqrt(s.simplify(abs(aa)**2+abs(bb)**2))
        G=s.eye(4);G[j,j]=s.conjugate(aa)/rr;G[j,row]=s.conjugate(bb)/rr;G[row,j]=-bb/rr;G[row,row]=aa/rr
        eq(G.H*G,s.eye(4));work=tidy(G*work);Qleft=tidy(G*Qleft);givens+=1
    assert work[j,j]>0
E=s.eye(4)[:,:2];eq(work,E*Rt);Qthin=tidy(Qleft.H*E);eq(Qthin,V)
eq(Qleft.H*Qleft,s.eye(4))
Gram=A.H*A;gramerr=f2(Gram-s.eye(2));herr=f2(Rt-s.eye(2))
assert gramerr<R(1,64) and herr<=4*gramerr

# Padding-output cleanup is an actual CPTP channel, not an illicit truncation.
K0=s.Matrix.hstack(s.eye(3),s.zeros(3,1));K1=s.zeros(3,4);K1[0,3]=1
eq(K0.H*K0+K1.H*K1,s.eye(4))
for i,j in itertools.product(range(3),repeat=2):
    M=s.zeros(3);M[i,j]=1;embedded=K0.H*M*K0
    eq(K0*embedded*K0.H+K1*embedded*K1.H,M)
leak=s.zeros(4);leak[3,3]=1;out=K0*leak*K0.H+K1*leak*K1.H
eq(out,s.diag(1,0,0))

def logceil(d):return (d-1).bit_length()
dimension_cases=0
for p,k in itertools.product(range(1,101),repeat=2):
    D=2**(logceil(p)+logceil(k*p));q=logceil(p)+logceil(k*p)
    assert D<=4*k*p*p
    assert q-logceil(k)<=2*logceil(p)
    dimension_cases+=1

# Guarded finite-bit SK algebra: exact Pauli commutator and rational sphere chart.
Zpa=s.diag(1,-1);sigmas=[X,Y,Zpa]
sk_cases=0
for raw in [(1,0,0),(0,1,0),(0,0,1),(2,3,6),(-2,3,6),(1,2,2)]:
    hh=s.Matrix(raw)/10000;hn=s.sqrt((hh.T*hh)[0])
    coord=min(range(3),key=lambda j:abs(hh[j]));axis=s.eye(3)[:,coord]
    cross=hh.cross(axis);cn=s.sqrt((cross.T*cross)[0])
    assert cn>=hn/2
    aa=cross/cn;ff=s.sqrt(hn/2)*aa;gg=-s.sqrt(hn/2)*(hh/hn).cross(aa)
    eq(tidy(ff.cross(gg)),-hh/2)
    FM=sum((ff[j]*sigmas[j] for j in range(3)),s.zeros(2))
    GM=sum((gg[j]*sigmas[j] for j in range(3)),s.zeros(2))
    HM=sum((hh[j]*sigmas[j] for j in range(3)),s.zeros(2))
    eq((I*FM)*(I*GM)-(I*GM)*(I*FM),I*HM)
    sk_cases+=1
for ts in [(R(1,17),R(1,23),R(-2,19)),(R(0),R(0),R(0))]:
    den=1+sum(t*t for t in ts);w=(2-den)/den;vv=[2*t/den for t in ts]
    Us=w*Id+I*sum((vv[j]*sigmas[j] for j in range(3)),s.zeros(2))
    eq(Us.H*Us,Id);assert s.simplify(Us.det())==1
# Scalar inequalities certify roomy recurrence slack, without floating exp.
assert R(64,3)+1<100 and 100*3+4+2<512
assert 512+R(4096,64)<4096
bj=64;dyadic=[]
for j in range(1,21):
    prev=bj;bj=(3*prev)//2-12
    exponent=R(3,2)*prev-bj
    assert 12<=exponent<=13 and bj>prev
    assert 38*R(3,2)**j+26<=bj<=40*R(3,2)**j+24
    assert (3**(j+1)-1)//2<=2*3**j
    dyadic.append(bj)

# Guarded known-unitary Cayley roots: includes roots at a naive branch cut.
Rot=s.Matrix([[R(3,5),R(4,5)],[-R(4,5),R(3,5)]])
close=-(R(999999)**2-1)/(R(999999)**2+1)+I*2*R(999999)/(R(999999)**2+1)
root_inputs=[-Id,s.diag(1,-1),Rot*s.diag(I,-I)*Rot.T,s.diag(close,-1)]
charts=[]
for UU in root_inputs:
    eq(UU.H*UU,Id)
    for zeta in [1,I,-1,-I]:
        MM=Id+zeta*UU
        if min((MM.H*MM).eigenvals())>R(1,4):break
    else:raise AssertionError('No safe Cayley phase chart')
    TT=tidy(-I*(zeta*UU-Id)*MM.inv());eq(TT.H,TT)
    assert max(abs(x) for x in TT.eigenvals())<=4
    PP=Id+TT*TT
    assert min(PP.eigenvals())>=1 and max(PP.eigenvals())<=17
    # Squaring the commuting positive-root expression avoids representation
    # of an unnecessarily large exact algebraic square-root field.
    eq(tidy((Id+I*TT)**2*PP.inv()),zeta*UU)
    charts.append(str(zeta))
assert R(7,10)*2<s.sqrt(2)  # one eigenvalue excludes at most one .7-near cut

source=P/'ACCESSIBLE_ENDPOINT_RATIONAL_SDP_AND_COMPILER.md'
result={'status':'PASS_EXACT_FIXTURES_NOT_GENERIC_SOLVER_OR_COMPILER',
'source_sha256_at_check':hashlib.sha256(source.read_bytes()).hexdigest(),
'independent_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
'rational_basis_dimension_cases':basis_cases,'inner_radius_and_slack_cases':radius_cases,
'complex_zero_diagonal_witness':str(witness),'signed_projection_unrestricted_optimum':str(a),
'rational_tp_repair_cases':repair_cases,'depolarization_all_cptp_recovery_optimum':'3/4',
'complex_kraus_composition':'EXACT','composition_lipschitz_squared_operator_norm':str(max((SL.H*SL).eigenvals())),
'completion_exact_unitarity':True,'completion_thin_isometry_equals_independent_reference':True,
'completion_givens_count':givens,'completion_pivot_squared_magnitudes':pivot_floor,
'completion_cholesky_error_squared':str(herr),'completion_gram_error_squared':str(gramerr),
'padded_output_cleanup':'EXACT_CPTP_FIXES_LOGICAL_SUBSPACE','dimension_and_ancilla_cases':dimension_cases,
'guarded_sk_exact_pauli_cases':sk_cases,'guarded_sk_dyadic_precision_exponents':dyadic,'guarded_sk_rational_unit_quaternion_chart':'EXACT','guarded_cayley_root_phase_charts':charts,'executed_generic_rounded_ellipsoid':False,'executed_finite_gate_compiler':False,'hardware_or_source_calls':0}
(P/'accessible_endpoint_independent_check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
