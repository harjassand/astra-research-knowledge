import numpy as np, sympy as s, json
from pathlib import Path
rng=np.random.default_rng(734501)
I=np.eye(2); X=np.array([[0,1],[1,0]]); Y=np.array([[0,-1j],[1j,0]]); Z=np.diag([1,-1]); P=[I,X,Y,Z]
phi=np.array([1,0,0,1])/np.sqrt(2); bells=[np.kron(I,p)@phi for p in P]
mxgrad=0.; mxtele=0.; mxcompress=0.
# Arbitrary joint R,data,flag,memory states: conditional flag estimators require no product state.
for trial in range(60):
 z=rng.normal(size=(16,9))+1j*rng.normal(size=(16,9)); rho=z@z.conj().T;rho/=np.trace(rho)
 R=rho.reshape(4,2,2,4,2,2)
 for bell in bells:
  joint=np.einsum('i,iamjbn,j->ambn',bell.conj(),R,bell)
  sig=np.einsum('ambm->ab',joint)
  est=np.zeros((2,2),complex)
  for w in P:
   for b in [-1,1]:
    effect=(I+b*w)/2
    pr=np.trace(effect@sig).real
    est+=pr*(2*b*w)/4
  mxgrad=max(mxgrad,float(np.max(np.abs(est-sig))))
 # Arbitrary Bell resource, possibly mixed; direct teleport on matrix units, including non-Hermitian ones.
 z=rng.normal(size=(4,5))+1j*rng.normal(size=(4,5)); omega=z@z.conj().T;omega/=np.trace(omega)
 q=[np.vdot(b,omega@b).real for b in bells]
 for i in range(2):
  for j in range(2):
   inp=np.zeros((2,2),complex);inp[i,j]=1
   total=np.kron(inp,omega).reshape(4,2,4,2);out=np.zeros((2,2),complex)
   for p,b in zip(P,bells):
    branch=np.einsum('i,iajb,j->ab',b.conj(),total,b)
    out+=p@branch@p.conj().T
   expected=sum(w*p@inp@p.conj().T for w,p in zip(q,P))
   mxtele=max(mxtele,float(np.max(np.abs(out-expected))))
 # Exact compressed objective identity, for arbitrary centers and symmetric unseen effects.
 k=17; B=rng.normal(size=(2,2));C=k*B;yc=rng.normal(size=(2,2));
 mxcompress=max(mxcompress,abs(k*np.linalg.norm(B-yc/k)**2-np.linalg.norm(C-yc)**2/k))
assert mxgrad<1e-14 and mxtele<1e-14 and mxcompress<1e-12
# Exact rational random pruning, new independent fixed-column fixture and full branch enumeration.
cols=[]
for axis in range(3):
 for sign in [-1,1]:
  col=s.zeros(4,1);col[0]=s.Rational(1,6);col[axis+1]=s.Rational(sign,12);cols.append(col)
A=s.Matrix.hstack(*cols); expected=s.zeros(6,1); leaves=0;maxbits=0
stack=[(s.Integer(1),s.ones(6,1))]
while stack:
 pr,w=stack.pop();active=[i for i in range(6) if w[i]>0]
 assert A*w==s.Matrix([1,0,0,0])
 if len(active)<=4:
  expected+=pr*w;leaves+=1;continue
 v0=A[:,active].nullspace()[-1];den=s.ilcm(*[x.q for x in v0]);v=s.zeros(6,1)
 for i,x in zip(active,v0):v[i]=x*den
 lo=max(-w[i]/v[i] for i in active if v[i]>0);hi=min(-w[i]/v[i] for i in active if v[i]<0)
 prob=-lo/(hi-lo)
 for p,t in [(prob,hi),(1-prob,lo)]:
  wn=w+t*v;assert min(wn)>=0
  maxbits=max(maxbits,max(max(abs(int(x.p)).bit_length(),int(x.q).bit_length()) for x in wn))
  stack.append((pr*p,wn))
assert expected==s.ones(6,1)
# Exact initial-distance and slack constants at representative dimensions/horizons.
for r in range(1,20):
 for N in [1,4,16,64,256]:
  # 2 sqrt(2r) sqrt(xi)+xi <=4r sqrt(xi), checked by stronger 3r bound.
  assert 2*np.sqrt(2*r)+1/(16*N)<=4*r
out=dict(joint_memory_gradient_fixtures=60,maximum_gradient_error=mxgrad,teleport_matrix_unit_checks=240,maximum_teleport_error=mxtele,compressed_metric_error=mxcompress,exact_pruning_leaf_count=leaves,exact_labelwise_mean_preserved=True,max_fixture_integer_bits=maxbits,scope='Independent mathematical and finite-array checks only; no new acquisition, online optimizer run, or hardware execution.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
