import numpy as np,itertools,json
from pathlib import Path
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]).astype(complex);pa={'I':I,'X':X,'Y':Y,'Z':Z}
def kron(xs):
 a=np.ones((1,1),complex)
 for x in xs:a=np.kron(a,x)
 return a
def word(s):return kron([pa[c] for c in s])
proj=np.eye(32,dtype=complex)
for st in ['XZZXI','IXZZX','XIXZZ','ZXIXZ']:proj=proj@(np.eye(32)+word(st))/2
v0=proj[:,0];v0/=np.linalg.norm(v0);V=np.column_stack([v0,word('XXXXX')@v0]);errors=[np.eye(32,dtype=complex)]
for i in range(5):
 for p in [X,Y,Z]:errors.append(kron([p if j==i else I for j in range(5)]))
D=[V.conj().T@E for E in errors];assert np.max(abs(sum(d.conj().T@d for d in D)-np.eye(32)))<1e-12
cs=lambda ks:sum((np.outer(k.reshape(-1),k.reshape(-1).conj()) for k in ks),np.zeros((16,16),complex))
good=[];bad=[];Bg=[];Bb=[];accept_paths=0
# Probe outcome conditions control later memory instruments but never inspect payload.
for labels in itertools.product(range(3),repeat=5):
 for outcomes in itertools.product(range(2),repeat=2):
  if not (outcomes[0]==0 or outcomes[1]==1):continue
  mem=I.copy();h=0;oi=0
  for t,r in enumerate(labels):
   theta=.13+.07*h+.02*t;R=np.cos(theta)*I+1j*np.sin(theta)*Y
   a=np.array([.94-.02*h,.68+.03*h]);B0=np.diag(a);S=np.diag(np.sqrt(1-a*a)/np.sqrt(2));Bs=[B0,R@S,Z@R@S];assert np.max(abs(sum(b.conj().T@b for b in Bs)-I))<1e-12
   mem=Bs[r]@mem
   if t in [1,3]:
    z=outcomes[oi];oi+=1;P0=np.diag([np.sqrt(.7),np.sqrt(.25)]);P1=np.diag([np.sqrt(.3),np.sqrt(.75)]);mem=[P0,P1][z]@mem;h=z
  E=kron([[I,X,Z][r] for r in labels]);count=sum(r!=0 for r in labels);ks=[np.kron(d@E@V,mem) for d in D]
  if count<=1:good+=ks;Bg.append(np.kron(I,mem))
  else:bad+=ks;Bb.append(np.kron(I,mem))
  accept_paths+=1
JG=cs(good);JBg=cs(Bg);JB=cs(bad);JBb=cs(Bb)
def trace_payload_choi(J):return np.trace(J.reshape(2,2,4,2,2,4),axis1=0,axis2=3)
def effect(J):return np.trace(J.reshape(4,4,4,4),axis1=0,axis2=2).T
res={'five_qubit_code_decoder_TP':True,'retained_memory_dim':2,'data_only_accepted_paths':accept_paths,'t':1,'good_identity_memory_residual':float(abs(JG-JBg).max()),'bad_actual_memory_marginal_residual':float(abs(trace_payload_choi(JB)-trace_payload_choi(JBb)).max()),'bad_effect_match':float(abs(effect(JB)-effect(JBb)).max()),'bad_effect_norm':float(np.linalg.eigvalsh(effect(JB))[-1]),'scope':'Exact algebra tested in floating Choi arithmetic; adaptive memory probes and classical-only postselection. Not the actual acquisition confidence threshold or hardware.'}
assert max(res[k] for k in ['good_identity_memory_residual','bad_actual_memory_marginal_residual','bad_effect_match'])<1e-11
Path(__file__).with_name('cp_closure_checks.json').write_text(json.dumps(res,indent=2)+'\n');print(res)
