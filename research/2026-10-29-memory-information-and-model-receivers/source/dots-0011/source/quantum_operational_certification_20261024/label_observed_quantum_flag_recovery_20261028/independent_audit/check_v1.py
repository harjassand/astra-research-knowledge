import numpy as np,json,math,hashlib,time,sys
from pathlib import Path
from fractions import Fraction as F
sys.set_int_max_str_digits(0)
D=Path(__file__).resolve().parent;R=D.parent;plan=json.loads((R/'PLAN_v1.json').read_text());saved=json.loads((R/'results_v2.json').read_text());start=time.time()
n=plan['n'];N=plan['N_training'];A=1<<n
# Independent source record replay and count accumulation, using integer histogram only.
def bits(rng,m):
 out=np.empty((m,n),np.int8);out[:,0]=rng.integers(2,size=m)
 for j in range(1,n):out[:,j]=np.bitwise_xor(out[:,j-1],rng.integers(1000,size=m)==999)
 return out
rng=np.random.default_rng(plan['training_seed']);counts=np.zeros(A,np.int64);hist=np.zeros((A,3,2),np.int64)
for offset in range(0,N,16384):
 m=min(16384,N-offset);e=bits(rng,m);words=np.zeros(m,np.int64)
 for j in range(n):words=2*words+e[:,j]
 ax=rng.integers(3,size=m);u=rng.integers(10,size=m)
 thresholds=np.where(e[:,0]==0,np.where(ax==2,10,5),np.where(ax==0,8,np.where(ax==1,5,1)))
 positive=u<thresholds
 counts+=np.bincount(words,minlength=A)
 hist+=np.bincount(words*6+ax*2+positive,minlength=A*6).reshape(A,3,2)
mom=hist[:,:,1]-hist[:,:,0];raw=np.load(R/'training_counts_v1.npz')
assert np.array_equal(counts,raw['counts']) and np.array_equal(mom,raw['mom'])
selected=[int(np.argmax(counts[a*A//2:(a+1)*A//2]))+a*A//2 for a in range(2)]
assert selected==saved['selected_words']==[0,255]
t=int(counts[0]-counts[255]);h=[3*int(v) for v in mom[0]-mom[255]];L=sum(v*v for v in h);assert t*t<L
B=plan['measurement_stereographic_denominator'];tx=F(round(B*h[0]/(math.sqrt(L)+h[2])),B);ty=F(round(B*h[1]/(math.sqrt(L)+h[2])),B);z=1+tx*tx+ty*ty
assert tx==F(saved['projector_parameters']['tx']) and ty==F(saved['projector_parameters']['ty'])
b=[2*tx/z,2*ty/z,(1-tx*tx-ty*ty)/z];assert sum(v*v for v in b)==1
scale=1<<120;upper=F(math.isqrt(L*scale*scale)+1,scale);slack=(upper-sum(F(v)*w for v,w in zip(h,b)))/(2*N)
assert slack==F(saved['empirical_optimization_slack_upper']) and slack>=0
# Exact Born probabilities for learned projector, independently in Bloch form.
p0=[(1+b[2])/2,(1+F(3,5)*b[0]-F(4,5)*b[2])/2]
assert [str(p) for p in p0]==saved['exact_projector_p0_by_feature']
Nh=plan['N_holdout'];rngh=np.random.default_rng(plan['holdout_seed']);e=bits(rngh,Nh);word=np.zeros(Nh,np.int64)
for j in range(n):word=word*2+e[:,j]
decision=np.zeros(Nh,np.int8)
for a in range(2):
 ids=np.where(e[:,0]==a)[0];p=p0[a];decision[ids]=(rngh.integers(p.denominator,size=len(ids))>=p.numerator)
# Physical corrected Z output: e XOR selected decision, no hidden loss oracle needed.
corrected=e^decision[:,None];success=np.all(corrected==0,axis=1);hold=np.load(R/'holdout_counts_v1.npz')
assert np.array_equal(hold['feature'],e[:,0]) and np.array_equal(hold['decision'],decision) and np.array_equal(hold['success'],success)
k=int(np.count_nonzero(~success));assert k==saved['holdout_failures']==2201
# Independent integer polynomial, factored to avoid author's recurrence.
coeff=0;choose=1
for j in range(k+1):
 if j:choose=choose*(Nh-j+1)//j
 coeff=19*coeff+choose
num=19**(Nh-k)*coeff;den=20**Nh
assert 1000*num<=den and saved['exact_tail_pass']
assert hashlib.sha256(str(num).encode()).hexdigest()==saved['exact_tail_numerator_sha256']
assert hashlib.sha256(str(den).encode()).hexdigest()==saved['exact_tail_denominator_sha256']
# Confidence and regret, exact rational exponential series.
def eup(x):return 1/sum(x**j/math.factorial(j) for j in range(101))
dp=F(1,500);dr=F(1,200);fp=2*A*eup(2*N*dp*dp);fr=6*A*eup(N*dr*dr/(6+F(8,3)*dr));failure=fp+fr
eps=F(173206,100000)*dr;assert eps*eps>=3*dr*dr and eps>=dp
regret=4*(dp+eps)+slack;assert regret==F(saved['oracle_regret_bound']) and failure==F(saved['simultaneous_failure_bound_exact'])
w=F(999,1000)**7;true=w*(p0[0]+1-p0[1])/2
assert abs(float(true)-saved['posthoc_true_Fe'])<1e-15
oracle=float(w)*(1+math.sqrt(.9))/2;nogauge=float(w)/2
assert abs(oracle-saved['posthoc_full_CPTP_oracle'])<1e-15 and abs(nogauge-saved['posthoc_no_gauge_oracle'])<1e-15
# Full joint CPTP-to-gauge-POVM reduction; independent complex random Kraus check.
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex);P=[I,X,Y,Z];rng2=np.random.default_rng(62831)
err=normerr=0.;mineig=1.
for rep in range(100):
 V=np.linalg.qr(rng2.normal(size=(16,4))+1j*rng2.normal(size=(16,4)))[0];Ks=V.reshape(8,2,4);J=sum(np.outer(K.reshape(-1),K.reshape(-1).conj()) for K in Ks)
 effects=[]
 for p in P:
  phi=p.reshape(-1)/np.sqrt(2);H=np.kron(phi.conj()[None,:],I);effects.append((H@J@H.conj().T).T/2)
 normerr=max(normerr,float(np.max(abs(sum(effects)-I))));mineig=min(mineig,min(np.linalg.eigvalsh(M)[0] for M in effects))
 prob=rng2.random(4);prob/=sum(prob);taus=[]
 for i in range(4):
  V=rng2.normal(size=(2,2))+1j*rng2.normal(size=(2,2));tau=V@V.conj().T;tau/=np.trace(tau);taus.append(tau)
 score=sum(prob[i]*np.trace(effects[i]@taus[i]).real for i in range(4));direct=0.
 for i in range(4):
  vals,vecs=np.linalg.eigh(taus[i])
  for a in range(2):
   NK=np.sqrt(prob[i]*vals[a])*np.kron(P[i],vecs[:,a,None]);direct+=sum(abs(np.trace(K@NK))**2 for K in Ks)/4
 err=max(err,abs(score-direct))
assert err<1e-12 and normerr<1e-12 and mineig>0
# Invisible phase counterexample, exact Pauli-label algebra: I/Zall split each Xword.
# Zall is diagonal on every actual bit-flip |0...0> probe output; saved records identical.
# Every prior coefficient matrix m_a tau_a is halved, so FULL oracle exactly halves.
phase_oracle=oracle/2
out={'status':'independent exact ordinary-data replay and quantum-reduction checks','training_records_replayed':N,'fresh_holdout_records_replayed':Nh,'all_counts_match':True,'holdout_failures':k,'exact_tail_pass':True,'regret':str(regret),'training_failure_bound':str(failure),'true_Fe':float(true),'full_CPTP_oracle':oracle,'no_flag_oracle':nogauge,'invisible_phase_counterexample_full_CPTP_oracle':phase_oracle,'Pauli_POVM_score_error':err,'POVM_normalization_error':normerr,'minimum_random_effect_eigenvalue':float(mineig),'elapsed_seconds':time.time()-start,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'GOVERNING_LABEL_OBSERVED_FLAG_RECOVERY_v1.md',R/'PLAN_v1.json',R/'learn_and_recover_v1.py',R/'reanalyse_v2.py',R/'results_v2.json',R/'training_counts_v1.npz',R/'holdout_counts_v1.npz']}}
(D/'results_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
