import numpy as np,json,math
from scipy.linalg import expm
from pathlib import Path
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1.,-1.]);sig=[X,Y,Z];rng=np.random.default_rng(295052)
def kronall(xs):
 o=np.ones((1,1))
 for x in xs:o=np.kron(o,x)
 return o
def matchings(ids):
 if not ids:yield [];return
 a=ids[0]
 for b in ids[1:]:
  for rest in matchings([i for i in ids[1:] if i!=b]):yield [(a,b)]+rest
def mv(n,pairs):
 v=np.zeros(2**n)
 for z in range(2**n):
  bits=[(z>>(n-1-i))&1 for i in range(n)];v[z]=np.prod([0 if bits[a]==bits[b] else (-1 if bits[a] else 1)/np.sqrt(2) for a,b in pairs])
 return v
rows=[]
for n in [4,6]:
 ops=[[kronall([sig[a] if i==j else I for i in range(n)]) for a in range(3)] for j in range(n)]
 J=[sum(ops[i][a] for i in range(n))/2 for a in range(3)]
 vals,vec=np.linalg.eigh(sum(j@j for j in J));V=vec[:,abs(vals)<1e-8];d=V.shape[1];P=V@V.conj().T;D=2**n
 matches=[mv(n,m) for m in matchings(list(range(n)))];assert np.linalg.norm(sum(np.outer(v,v) for v in matches)/len(matches)-P/d)<1e-12
 for case in range(12):
  hs=rng.normal(size=(n,3))*(case+1)/80;hs[0]=0
  H=sum(hs[i,a]*ops[i][a]/2 for i in range(n) for a in range(3));W=expm(-1j*H)
  H0=.2*X+.3*Z
  Hsrc=np.kron(np.eye(D),H0)+rng.normal()*np.kron(J[0],X)+rng.normal()*np.kron(J[1]@J[1],Z)+rng.normal()*np.kron(J[2],Y)
  U=expm(-1j*Hsrc);A=np.kron(W.conj().T,I)@U@np.kron(W,I)
  blocks=A.reshape(D,2,D,2)
  B=np.einsum('ij,jaib->ab',P,blocks)/d
  Hbad=I-B.conj().T@B
  passEff=np.zeros((2,2),complex)
  for v in matches:
   bm=np.einsum('j,jaib,i->ab',v.conj(),blocks,v);passEff+=bm.conj().T@bm/len(matches)
  qEff=I-passEff
  leakage=np.linalg.norm((np.eye(D)-P)@W@V,'fro')**2/d
  variance=np.trace(P@H@H).real/d
  formula=n/(4*(n-1))*np.sum((hs-hs.mean(axis=0))**2)
  assert abs(variance-formula)<1e-10
  rawmax=np.linalg.eigvalsh(Hbad).max();qminus=np.linalg.eigvalsh(qEff-Hbad).max()
  assert rawmax<=4*leakage+1e-10 and leakage<=variance+1e-10 and qminus<1e-10
  rows.append({'n':n,'case':case,'max_bath_raw_bell_loss':rawmax,'four_mean_leakage':4*leakage,'four_exact_variance':4*variance,'largest_q_minus_raw_effect':qminus})
pars=[]
for h in range(5,31):
 B=2**h;n=4*h;t=B//8;b=B//32;N=t+b+1
 assert (t-b+1)**2/(2*N)>=3*B/128
 C=(n+2)/(n-1);s=1/(C+1);assert s>=1/3
 for g in [.0001,.35,4]:
  delta=.05;ell=math.log(25*(n-1)/delta);m=math.ceil(450500000*n*ell/g**2)
  e=(31*ell+math.sqrt((31*ell)**2+1800*m*ell))/m
  assert e<=g/(500*math.sqrt(n))
  gl=g-2*e;assert 2*math.sqrt(6)*e/gl<1
  assert 12*math.pi**2*n*e**2/gl**2<1/512
 pars.append({'h':h,'soundness_exponent_lower':3*B/128,'service_probability':s})
out={'full_physical_bath_effect_checks':rows,'parameter_checks':pars,'scope':'24 n4/n6 exact collective joint-memory unitary fixtures plus h5..30 arithmetic. No adaptive acquisition trajectory or hardware circuit simulation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print('PASS',len(rows),'physical cases;',len(pars),'parameter rows')
