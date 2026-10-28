#!/usr/bin/env python3
"""Direct encoder/recovery verification, non-Pauli product channels and entangling patch CPTP."""
from pathlib import Path
import itertools,json
import numpy as np
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P={'I':I,'X':X,'Y':Y,'Z':Z}
def kron(xs):
 r=np.ones((1,1))
 for A in xs:r=np.kron(r,A)
 return r
def pw(w):return kron([P[a] for a in w])
G=[pw(w) for w in ['XZZXI','IXZZX','XIXZZ','ZXIXZ']];proj=np.eye(32)
for g in G:proj=proj@(np.eye(32)+g)/2
z=proj[:,0];z=z/np.linalg.norm(z);C=np.column_stack([z,pw('XXXXX')@z]);Fs=[np.eye(32)]+[pw('I'*i+a+'I'*(4-i)) for i in range(5) for a in 'XYZ'];Rs=[C.conj().T@F.conj().T for F in Fs]
assert np.array_equal(C.conj().T@C,np.eye(2))
assert np.array_equal(sum(R.conj().T@R for R in Rs),np.eye(32))
for a,b in itertools.product(range(16),repeat=2):assert np.array_equal(C.conj().T@Fs[a].conj().T@Fs[b]@C,np.eye(2) if a==b else np.zeros((2,2)))
bell=np.array([1,0,0,1])/np.sqrt(2);jid=np.outer(bell,bell)
def choi(Ks,d):
 phi=np.eye(d).reshape(-1)/np.sqrt(d)
 return sum(np.outer(np.kron(Ik,np.eye(d))@phi,(np.kron(Ik,np.eye(d))@phi).conj()) for Ik in Ks)
def ad(g,U):return [U@np.diag([1,np.sqrt(1-g)])@U.conj().T,U@np.array([[0,np.sqrt(g)],[0,0]])@U.conj().T]
axes=[(3*I-4j*A)/5 for A in [X,Y,Z,X+0*Y,Y]]
single=[]
for site in range(5):
 ks=ad(.64,axes[site]);outs=[]
 for K in ks:
  E=kron([K if i==site else I for i in range(5)])
  outs.extend(R@E@C for R in Rs)
 err=np.linalg.norm(choi(outs,2)-jid);assert err<1e-12;single.append(err)
products=[]
for g in [.01,.03,.08]:
 local=[ad(g*(.6+.1*i),axes[i]) for i in range(5)];decoded=[]
 for picks in itertools.product(range(2),repeat=5):
  E=kron([local[i][picks[i]] for i in range(5)])
  decoded.extend(R@E@C for R in Rs)
 J=choi(decoded,2);h=np.abs(np.linalg.eigvalsh(J-jid)).sum()/2
 ps=[1-np.sqrt(1-g*(.6+.1*i))+g*(.6+.1*i)/2 for i in range(5)]
 B=(np.prod([1+2*p for p in ps])-1-2*sum(ps))/2
 assert 2*h<=B+1e-12
 products.append({'gamma_max':g,'Choi_half_distance':float(h),'complete_logical_upper_from_Choi':float(2*h),'product_expansion_bound':float(B)})
# Direct TWO-code, ten-carrier encoder; apply arbitrary entangling CPTP on a patch.
C2=np.kron(C,C);rng=np.random.default_rng(202610282105);M=rng.normal(size=(12,4))+1j*rng.normal(size=(12,4));Q,_=np.linalg.qr(M);Ks=[Q[4*k:4*k+4,:] for k in range(3)]
assert np.linalg.norm(sum(K.conj().T@K for K in Ks)-np.eye(4))<1e-12
phi4=np.eye(4).reshape(-1)/2;id4=np.outer(phi4,phi4);patches=[]
for site in range(5):
 sites=[site,5+site];other=[i for i in range(10) if i not in sites];perm=sites+other+[10];inverse=np.argsort(perm);decoded=[]
 for K in Ks:
  block=C2.reshape([2]*10+[4]).transpose(perm).reshape(4,-1)
  applied=(K@block).reshape([2]*10+[4]).transpose(inverse).reshape(32,32,4)
  for Ra,Rb in itertools.product(Rs,repeat=2):
   D=np.einsum('ai,bj,ijk->abk',Ra,Rb,applied,optimize=True).reshape(4,4);decoded.append(D)
 J=choi(decoded,4);err=np.linalg.norm(J-id4);assert err<1e-12
 patches.append({'patch':site,'actual_entangling_Kraus':3,'decoded_logical_Kraus':len(decoded),'joint_logical_choi_identity_residual':float(err)})
# A common bad fitting coin remains a logical error, unlike independent local averages.
h=.001;LX=C.conj().T@pw('XXXXX')@C;assert np.array_equal(LX,X)
correlated=(1-h)*jid+h*np.outer(np.kron(X,I)@bell,np.kron(X,I)@bell)
loss=np.abs(np.linalg.eigvalsh(correlated-jid)).sum()/2;assert abs(loss-h)<1e-14
out={'status':'PASS_DIRECT_STANDARD_CODE_AND_INTERLEAVED_ENTANGLING_PATCH_BRIDGE','source_draws':0,'rng_draws_for_native_source':0,'exact_dyadic_KL_matrix_pairs':256,'encoder_and_decoder_TP_exact_dyadic':True,'single_nonPauli_site_residuals':single,'product_nonPauli_cases':products,'direct_ten_carrier_patch_CPTP_cases':patches,'common_program_logical_error':float(loss),'scope':'Exact dyadic code matrices, floating Kraus-channel checks; no learned source counts or hardware. Random Kraus fixture is mathematical stress data, not a noise measurement.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
