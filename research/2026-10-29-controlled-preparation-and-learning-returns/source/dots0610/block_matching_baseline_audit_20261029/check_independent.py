import numpy as np,sympy as S,itertools,json,sys
from pathlib import Path
p=Path(__file__).parent;s=p.parent/'block_matching_baseline_20261029';sys.path.insert(0,str(s));import check_tensor_baseline as author
rng=np.random.default_rng(202610290525)
I=S.eye(2);X=S.Matrix([[0,1],[1,0]]);Y=S.Matrix([[0,-S.I],[S.I,0]]);Z=S.diag(1,-1)
vs=[S.Matrix([1,0]),S.Matrix([S.Rational(1,2),S.sqrt(3)/2]),S.Matrix([S.Rational(1,2),-S.sqrt(3)/2])]
def frameact(A):return S.simplify(sum([(v.conjugate().T*A*v)[0]*(v*v.conjugate().T) for v in vs],S.zeros(2))/3)
for A,lam in [(I,S.Rational(1,2)),(X,S.Rational(1,4)),(Y,0),(Z,S.Rational(1,4))]:assert frameact(A)==lam*A
# Independent correlated multi-Kraus channel: input memory2, outputmemory3, true two-dimensional leakage.
rows=[]
for h in [1,2,3]:
 d=1<<h;out=d+2;mi=2;mo=3
 for case in range(3):
  Q=np.linalg.qr(rng.normal(size=(2*out*mo,d*mi))+1j*rng.normal(size=(2*out*mo,d*mi)))[0]
  Ks=Q.reshape(2,out*mo,d*mi);Bs=[sum(K.reshape(out,mo,d,mi)[i,:,i,:] for i in range(d))/d for K in Ks];Hraw=np.eye(mi)-sum(B.conj().T@B for B in Bs)
  Ds=[np.c_[np.eye(d),np.zeros((d,2))]]
  for l in range(2):
   D=np.zeros((d,out));D[0,d+l]=1;Ds.append(D)
  Ls=[np.kron(D,np.eye(mo))@K for D in Ds for K in Ks]
  Cs=[sum(L.reshape(d,mo,d,mi)[i,:,i,:] for i in range(d))/d for L in Ls];Hcomp=np.eye(mi)-sum(C.conj().T@C for C in Cs)
  gap=Hraw-Hcomp;extra=sum(C.conj().T@C for C in Cs[2:]);assert np.linalg.norm(gap-extra)<1e-12
  def fail(states,raw):
   F=np.eye(mi,dtype=complex)
   for v in states:
    read=np.kron((np.r_[v,0,0] if raw else v).conj()[None,:],np.eye(mo));prep=np.kron(v[:,None],np.eye(mi))
    for K in (Ks if raw else Ls):
     a=read@K@prep;F-=a.conj().T@a/len(states)
   return F
  Fm=fail(author.product_states([np.array(v,float).reshape(-1) for v in vs],h),True)
  Fs=fail(author.product_states(author.six,h),False)
  vals=[np.linalg.eigvalsh(gap).min(),np.linalg.eigvalsh(2*Fm-Hraw).min(),np.linalg.eigvalsh(2*Fm-Hcomp).min(),np.linalg.eigvalsh(1.5*Fs-Hcomp).min()]
  assert min(vals)>-1e-12
  rows.append({'h':h,'case':case,'input_memory':mi,'output_memory':mo,'source_Kraus':2,'leakage_dimension':2,'PSD_minima_completion_raw_matching_completed_matching_completed_six':list(map(float,vals))})
# Gauge identity from actual stored learned fixture.
a=np.load(s/'received_fixture.npz');EB=author.E4();R=EB.conj().T@a['Vhat'].conj().T@a['E'];res=np.linalg.norm(a['E']-a['Vhat']@EB@R);assert res<1e-12
assert np.linalg.norm(R+np.array(X,float))<1e-12
# Preserve the complete decoder channel: good branch R† EB† Vhat†, fixed reset unaffected.
expected0=R.conj().T@EB.conj().T@a['Vhat'].conj().T;assert np.linalg.norm(a['Ds'][0]-expected0)<1e-12
# Wrong ordering rotates reset |0> to |1>, trace distance1 for leakage.
wrong=R.conj().T@np.diag([1,0])@R;assert np.linalg.norm(wrong-np.diag([0,1]))<1e-12
out={'exact_single_block_matching_Pauli_frame':True,'multi_Kraus_changed_memory_dimension_fixtures':rows,'learned_gauge_R_plus_X_residual':float(np.linalg.norm(R+np.array(X,float))),'learned_encoder_reconstruction_residual':float(res),'learned_good_decoder_gauge_residual':float(np.linalg.norm(a['Ds'][0]-expected0)),'wrong_gauge_after_reset_leakage_trace_distance':1.0,'scope':'Exact symbolic one-block frame; floating correlated channel and frozen-fixture checks; no certified numerical intervals.'};(p/'independent_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
