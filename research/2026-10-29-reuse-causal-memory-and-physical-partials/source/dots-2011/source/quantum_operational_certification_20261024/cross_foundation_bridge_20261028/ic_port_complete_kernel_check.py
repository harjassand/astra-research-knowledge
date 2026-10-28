#!/usr/bin/env python3
"""Exact ordinary-IC kernel and coherent-controller diagnostics; no source calls."""
from pathlib import Path
from hashlib import sha256
import itertools,json
import sympy as s

HERE=Path(__file__).resolve().parent
I=s.eye(2);zero=s.Matrix([[1,0],[0,0]]);one=I-zero
plus=s.Matrix([[1,1],[1,1]])/2
yp=s.Matrix([[1,-s.I],[s.I,1]])/2
preps=[zero,one,plus,yp];effects=[r/8 for r in preps]
remainder=I-sum(effects,s.zeros(2))
assert all(x>=s.Rational(1,2) for x in remainder.eigenvals())
def inner(A,B):return s.simplify(s.trace(A*B))
def dual_basis(bs):
 G=s.Matrix([[inner(a,b) for b in bs] for a in bs]);assert G.det()!=0
 inv=G.inv()
 ds=[sum((inv[i,j]*bs[j] for j in range(len(bs))),s.zeros(bs[0].rows)) for i in range(len(bs))]
 assert all(inner(ds[i],bs[j])==int(i==j) for i in range(len(bs)) for j in range(len(bs)))
 return ds,G
inputs=[r.T for r in preps];din,gin=dual_basis(inputs);dout,gout=dual_basis(effects)
local=[s.kronecker_product(a,b) for a in inputs for b in effects]
ldual=[s.kronecker_product(a,b) for a in din for b in dout]
assert all(inner(ldual[i],local[j])==int(i==j) for i in range(16) for j in range(16))

# Memory-first ordering. U maps |m,a> -> |a,m xor a>.
U=s.zeros(4)
for m,a in itertools.product(range(2),repeat=2):U[2*a+(m^a),2*m+a]=1
phase=s.diag(1,s.I,-1,1)
V=phase*U
assert U.conjugate().T*U==V.conjugate().T*V==s.eye(4)
rho=zero

def blocks(W):
 return {(b,a):s.Matrix([[W[2*m+b,2*n+a] for n in range(2)] for m in range(2)]) for b,a in itertools.product(range(2),repeat=2)}
BU,BV=blocks(U),blocks(V)
def induce(B,sigma,r,E):
 ans=s.zeros(2)
 for a,c,b,e in itertools.product(range(2),repeat=4):
  ans+=r[a,c]*E[e,b]*B[(b,a)]*sigma*B[(e,c)].conjugate().T
 return s.simplify(ans)

def direct_kernel(B1,B2,state):
 W=s.zeros(16)
 for i,b,j,c,k,d,l,e in itertools.product(range(2),repeat=8):
  r=8*i+4*b+2*j+c;z=8*k+4*d+2*l+e
  W[r,z]=s.trace(B2[(c,j)]*B1[(b,i)]*state*B1[(d,k)].conjugate().T*B2[(e,l)].conjugate().T)
 return s.simplify(W)

kernels={};word_count=0;PSD_checks=[]
for name,B2 in [('UU',BU),('UV',BV)]:
 W=direct_kernel(BU,B2,rho)
 assert W==W.conjugate().T and s.trace(W)==4
 assert all(ev>=0 for ev in W.eigenvals())
 recovered=s.zeros(16)
 for u,v,j,k in itertools.product(range(4),repeat=4):
  sigma=induce(BU,rho,preps[u],effects[v])
  prob=s.simplify(s.trace(induce(B2,sigma,preps[j],effects[k])))
  assert prob==inner(W,s.kronecker_product(local[4*u+v],local[4*j+k]))
  recovered+=prob*s.kronecker_product(ldual[4*u+v],ldual[4*j+k])
  word_count+=1
 assert s.simplify(recovered-W)==s.zeros(16)
 kernels[name]=s.simplify(recovered)
 PSD_checks.append({'schedule':name,'eigenvalues':{str(e):m for e,m in W.eigenvals().items()}})

# Contract first output to second input using an arbitrary controller Kraus L.
# This keeps the first input as a Choi/Bell reference, including its phases.
def link(W,L):
 J=s.zeros(4)
 for i,b,k,d in itertools.product(range(2),repeat=4):
  val=0
  for q,e,r,f in itertools.product(range(2),repeat=4):
   val+=L[r,q]*s.conjugate(L[f,e])*W[8*i+4*q+2*r+b,8*k+4*e+2*f+d]
  J[2*i+b,2*k+d]=s.simplify(val)
 return J

def direct_endpoint(W1,W2,L):
 total=W2*s.kronecker_product(I,L)*W1
 # Initial memory |0>; final memory is discarded.
 Ks=[s.Matrix([[total[2*m+b,a] for a in range(2)] for b in range(2)]) for m in range(2)]
 J=s.zeros(4)
 for K in Ks:
  vec=s.Matrix([K[b,a] for a in range(2) for b in range(2)])
  J+=vec*vec.conjugate().T
 return s.simplify(J)

coherent=s.Matrix([[s.Rational(3,5),-4*s.I/5],[s.Rational(4,5),3*s.I/5]])
assert coherent.conjugate().T*coherent==I
J=link(kernels['UU'],coherent)
assert J==direct_endpoint(U,U,coherent)
assert s.trace(J)==2 and all(ev>=0 for ev in J.eigenvals())
# Retained classical instrument record selects the second native action.
L0=s.diag(1,s.Rational(4,5));L1=s.Matrix([[0,s.Rational(3,5)],[0,0]])
assert L0.conjugate().T*L0+L1.conjugate().T*L1==I
J0=link(kernels['UU'],L0);J1=link(kernels['UV'],L1)
assert J0==direct_endpoint(U,U,L0)
assert J1==direct_endpoint(U,V,L1)
assert s.trace(J0+J1)==2
assert all(ev>=0 for ev in s.diag(J0,J1).eigenvals())
# Output trace of total Choi = input identity, including adaptive source choice.
assert s.Matrix([[sum((J0+J1)[2*a+b,2*c+b] for b in range(2)) for c in range(2)] for a in range(2)])==I

# Gauge-related physical memories: different matrices, equal kernel.
H=s.Matrix([[1,1],[1,-1]])/s.sqrt(2)
Ug=s.kronecker_product(H,I)*U*s.kronecker_product(H,I)
Vg=s.kronecker_product(H,I)*V*s.kronecker_product(H,I)
rhog=H*rho*H
assert rhog!=rho and s.simplify(Ug-U)!=s.zeros(4)
assert s.simplify(direct_kernel(blocks(Ug),blocks(Ug),rhog)-kernels['UU'])==s.zeros(16)
assert s.simplify(direct_kernel(blocks(Ug),blocks(Vg),rhog)-kernels['UV'])==s.zeros(16)

# Inadequate real-only input/output alphabet: arbitrary word lengths remain
# blind for these memoryless ports, while one Bell input separates perfectly.
Up=s.diag(1,s.I);Um=s.diag(1,-s.I)
realps=[zero,one,plus]
blind=0
for r,E in itertools.product(realps,repeat=2):
 assert inner(E,Up*r*Up.conjugate().T)==inner(E,Um*r*Um.conjugate().T)
 blind+=1
vp=s.Matrix([Up[b,a] for a in range(2) for b in range(2)])
vm=s.Matrix([Um[b,a] for a in range(2) for b in range(2)])
assert (vp.conjugate().T*vm)[0]==0
Bp=vp*vp.conjugate().T/2;Bm=vm*vm.conjugate().T/2
assert sum(abs(ev)*mult for ev,mult in (Bp-Bm).eigenvals().items())/2==1
max_ic=max(abs(inner(E,Up*r*Up.conjugate().T)-inner(E,Um*r*Um.conjugate().T)) for r,E in itertools.product(preps,effects))
assert max_ic==s.Rational(1,8)

# Complete rectangular Choi/Frobenius constant dominance, exact integers.
constant_cases=0
for d,p,q,b,Hh in itertools.product(range(1,9),range(1,5),range(1,5),range(1,5),range(0,11)):
 # sqrt(d/2)<=d and d sqrt(p q b/2)<=d p q b.
 assert d<=2*d*d and p*q*b<=2*(p*q*b)**2
 constant_cases+=1

# Explicit decoder mechanism: exact feasible diamond-SDP certificates and
# Kraus/Stinespring normalization, not a generic numerical optimizer run.
def choi_from_kraus(Ks):
 J=s.zeros(4)
 for K in Ks:
  z=s.Matrix([K[b,a] for a in range(2) for b in range(2)])
  J+=z*z.conjugate().T
 return s.simplify(J)
def compose_choi(N,C):
 return s.Matrix([[s.simplify(sum(N[2*i+y,2*j+z]*C[2*y+a,2*z+b]
                   for y,z in itertools.product(range(2),repeat=2)))
                  for j,b in itertools.product(range(2),repeat=2)]
                  for i,a in itertools.product(range(2),repeat=2)])
def trace_out(J):
 return s.Matrix([[sum(J[2*i+b,2*j+b] for b in range(2)) for j in range(2)] for i in range(2)])
def check_decoder_certificate(N,Ks,Z,t):
 C=choi_from_kraus(Ks);assert trace_out(C)==I
 DD=compose_choi(N,C)-choi_from_kraus([I])
 assert all(ev>=0 for ev in (Z-DD).eigenvals())
 assert all(ev>=0 for ev in (Z+DD).eigenvals())
 assert all(ev>=0 for ev in (t*I-trace_out(Z)).eigenvals())
 # Environment label l is retained only in this mathematical isometry.
 W=s.Matrix.vstack(*Ks)
 assert s.simplify(W.conjugate().T*W)==I
 return C
Nunit=choi_from_kraus([coherent])
Cunit=check_decoder_certificate(Nunit,[coherent.conjugate().T],s.zeros(4),s.Rational(0))
Nerase=s.kronecker_product(I,zero)
Kdepol=[]
for a,b in itertools.product(range(2),repeat=2):
 K=s.zeros(2);K[a,b]=1/s.sqrt(2);Kdepol.append(K)
Jid=choi_from_kraus([I]);Zerase=s.eye(4)/2+Jid/2
Cdep=check_decoder_certificate(Nerase,Kdepol,Zerase,s.Rational(3,2))
assert Cdep==s.eye(4)/2
# Every decoder of an erasure yields a replacer state sigma, whose Bell
# fidelity is exactly 1/4. This proves the matching 3/4 lower error.
a,bb,cc=s.symbols('a bb cc',real=True)
sigma=s.Matrix([[a,bb+s.I*cc],[bb-s.I*cc,1-a]])
assert s.simplify(s.trace((Jid/2)*s.kronecker_product(I,sigma)/2))==s.Rational(1,4)

out={'status':'PASS exact IC kernel and coherent-controller checks',
 'source_sha256':sha256((HERE/'IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY.md').read_bytes()).hexdigest(),
 'input_Gram_determinant':str(gin.det()),'output_Gram_determinant':str(gout.det()),
 'IC_local_basis_size':16,'two_slot_kernel_dimension':16,
 'exact_scalar_word_and_Born_checks':word_count,'exact_kernel_reconstructions':2,
 'coherent_reference_recycling_output_checks':1,'adaptive_retained_record_branch_checks':2,
 'gauge_equivalent_kernel_checks':2,'real_only_blind_single_call_checks':blind,
 'inadequate_alphabet_Bell_trace_distance':'1','full_IC_max_witness_gap':str(max_ic),
 'rectangular_constant_cases':constant_cases,'kernel_spectra':PSD_checks,
 'exact_decoder_SDP_feasibility_certificates':2,'exact_Kraus_Stinespring_checks':2,
 'exact_decoder_optimal_errors':['0','3/4'],
 'coherent_endpoint_normalized_Bell_output':[[str(x) for x in J.row(i)/2] for i in range(4)],
 'source_calls':0,'episode_starts':0,'RNG_calls':0,'hardware_executions':0,
 'generic_QE_executed':False,'candidate_feasibility_executed':False,'recovery_SDP_executed':False,
 'floating_point_used':False}
(HERE/'ic_port_complete_kernel_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['coherent_endpoint_normalized_Bell_output','kernel_spectra']},indent=2))
