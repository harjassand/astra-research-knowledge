#!/usr/bin/env python3
"""Actual Born draws on one noncommuting-sector source; learner receives only records.
Floating optimizer/controls; no theorem acceptance or rational gate compilation is claimed.
"""
from pathlib import Path
import json,itertools,hashlib,time
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize
HERE=Path(__file__).parent
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]).astype(complex);P=[X,Y,Z];P0=[I]+P
B0=[np.kron(p,I) for p in P]
SETTINGS=list(itertools.product(range(3),[-1,1],range(3),range(3)))
OUTCOMES=list(itertools.product([-1,1],repeat=2))
SHADOWS=[]
for j,sg,a,b in SETTINGS:
 SHADOWS.append([np.kron((I+3*x*P[a])/2,(I+3*y*P[b])/2) for x,y in OUTCOMES])
SHADOWS=np.array(SHADOWS)

def generator_only_source():
 V=expm(-1j*(.47*np.kron(X,X)+.31*np.kron(Y,Z)+.19*np.kron(Z,I)+.37*np.kron(I,X)))
 U=np.array([[3.,-1.],[1.,3.]])/np.sqrt(10)
 ad0=[np.diag([1.,.8]),np.array([[0.,.6],[0.,0.]])]
 ad1=[U@k@U.conj().T for k in ad0]
 gauges=[np.array([1.,0]),np.array([1.,1])/np.sqrt(2)]
 K=[V@np.kron(k,g[:,None])/np.sqrt(2) for ks,g in zip([ad0,ad1],gauges) for k in ks]
 def channel(rho):return sum((k@rho@k.conj().T for k in K),np.zeros((4,4),complex))
 probs=[]
 for j,sg,a,b in SETTINGS:
  rho=channel((I+sg*P[j])/2)
  probs.append([np.trace(rho@np.kron((I+x*P[a])/2,(I+y*P[b])/2)).real for x,y in OUTCOMES])
 probs=np.array(probs);assert np.min(probs)>-1e-14 and np.max(abs(probs.sum(1)-1))<1e-12
 C=[channel(p/2) for p in P]
 return V,channel,probs,C

def acquire(N,seed,probabilities):
 rng=np.random.default_rng(seed)
 settings=rng.integers(len(SETTINGS),size=N); uniforms=rng.random(N)
 outputs=(uniforms[:,None]>np.cumsum(probabilities[settings],axis=1)).sum(1)
 assert outputs.max()<4
 counts=np.bincount(settings*4+outputs,minlength=len(SETTINGS)*4).reshape(len(SETTINGS),4)
 assert counts.sum()==N
 return counts

def learner_contrasts(counts):
 N=int(counts.sum());C=[np.zeros((4,4),complex) for _ in range(3)]
 for l,(j,sg,a,b) in enumerate(SETTINGS):C[j]+=3*sg*np.einsum('o,oab->ab',counts[l],SHADOWS[l])/N
 return C

def objective(A,C):return sum(np.trace(a@c).real for a,c in zip(A,C))
def unitary_search(C,seed,starts=4,maxiter=1200):
 # Input is empirical observable matrices only; no source/mixer parameters.
 rng=np.random.default_rng(seed);runs=[];best=None
 for start in range(starts):
  if start==0:U=np.eye(4,dtype=complex)
  else:
   z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));U,r=np.linalg.qr(z);U=U@np.diag(np.diag(r)/abs(np.diag(r))).conj()
  A=[U@b@U.conj().T for b in B0];f=objective(A,C);success=False
  for it in range(maxiter):
   G=1j*sum((a@c-c@a for a,c in zip(A,C)),np.zeros((4,4),complex));G=(G+G.conj().T)/2
   gn=np.linalg.norm(G,'fro');
   if gn<1e-10:success=True;break
   step=2.;accepted=False
   for ls in range(40):
    R=expm(1j*step*G);UU=R@U;AA=[R@a@R.conj().T for a in A];ff=objective(AA,C)
    if ff>=f+1e-4*step*gn*gn:accepted=True;break
    step*=.5
   if not accepted:break
   U,A,f=UU,AA,ff
  runs.append({'start':start,'iterations':it+1,'objective':float(f),'gradient_norm':float(gn),'gradient_tolerance_reached':success})
  if best is None or f>best[0]:best=(f,U,A)
 return best[1],best[2],runs

def fit_block(A,C):
 def expect(M):return (M+sum((a@M@a for a in A),np.zeros_like(M)))/4
 L=[[expect((A[k]@C[j]+C[j]@A[k])/2) for j in range(3)] for k in range(3)]
 S=[[(L[k][j]+L[j][k])/2 for j in range(3)] for k in range(3)]
 Sb=np.block(S);Sb=(Sb+Sb.conj().T)/2
 fitted=[sum((A[k]@S[k][j] for k in range(3)),np.zeros((4,4),complex)) for j in range(3)]
 return float(np.linalg.eigvalsh(Sb).min()),float(np.sqrt(sum(np.linalg.norm(a-b,'fro')**2 for a,b in zip(fitted,C)))),Sb

def sign(M):
 v,U=np.linalg.eigh((M+M.conj().T)/2);return (U*np.where(v>=0,1.,-1.))@U.conj().T

def scalar_whitening(C):
 G=np.array([[np.trace(a@b).real for b in C] for a in C]);v,U=np.linalg.eigh(G)
 if v.min()<=0:return None
 W=U@np.diag(v**-.5)@U.T
 return [sign(sum(C[k]*W[k,j] for k in range(3))) for j in range(3)]
def operator_whitening(C):
 G=np.block([[(a@b+b@a)/2 for b in C] for a in C]);G=(G+G.conj().T)/2;v,U=np.linalg.eigh(G)
 if v.min()<=0:return None,float(v.min())
 W=(U*v**-.5)@U.conj().T
 A=[sign(sum(C[k]@W[4*k:4*k+4,4*j:4*j+4] for k in range(3))) for j in range(3)]
 return A,float(v.min())

def decoder_from_XZ(A):
 Q=np.kron((np.eye(4)+A[2])/2,I)+np.kron((np.eye(4)-A[2])/2,X)
 CX=np.kron(np.eye(4),np.diag([1.,0]))+np.kron(A[0],np.diag([0.,1.]))
 W=Q@CX@Q
 def decode(M):
  out=W@np.kron(M,I/2)@W.conj().T
  return np.trace(out.reshape(4,2,4,2),axis1=0,axis2=2)
 return decode,float(np.linalg.norm(W.conj().T@W-np.eye(8),2))
def bell_fidelity(channel):
 val=0j
 for a,b in itertools.product(range(2),repeat=2):
  e=np.zeros((2,2),complex);e[a,b]=1;val+=channel(e)[a,b]/4
 return float(val.real)
def score_decoder(A,V,source):
 dec,ur=decoder_from_XZ(A)
 loss=1-bell_fidelity(lambda rho:dec(source(rho)))
 T=np.zeros((2,2),complex)
 for r,s in itertools.product(range(2),repeat=2):
  g=np.zeros((2,2),complex);g[r,s]=1
  T[s,r]=sum(dec(V@np.kron(np.eye(2,dtype=complex)[[a]].T@np.eye(2,dtype=complex)[[b]],g)@V.conj().T)[a,b]/4 for a,b in itertools.product(range(2),repeat=2))
 T=(T+T.conj().T)/2
 return {'native_Bell_loss':loss,'worst_gauge_inverse_Bell_loss':float(1-np.linalg.eigvalsh(T).min()),'actual_three_reflection_unitarity_residual':ur}

# Small same-record full-CPTP recovery SDP, solved numerically with both primal/dual checks.
def hermitian_basis(n):
 out=[]
 for a in range(n):
  m=np.zeros((n,n),complex);m[a,a]=1;out.append(m)
 for a in range(n):
  for b in range(a+1,n):
   m=np.zeros((n,n),complex);m[a,b]=m[b,a]=1/np.sqrt(2);out.append(m)
   m=np.zeros((n,n),complex);m[a,b]=1j/np.sqrt(2);m[b,a]=-1j/np.sqrt(2);out.append(m)
 return np.array(out)
E8=hermitian_basis(8);E4=hermitian_basis(4)
def partialout(J):return np.trace(J.reshape(2,4,2,4),axis1=0,axis2=2)
TP=np.array([[np.trace(e@partialout(f)).real for f in E8] for e in E4]);target=np.array([np.trace(e).real for e in E4])
def sdp_recovery(C,return_choi=False):
 Q=sum((np.kron(p,c.T)/4 for p,c in zip(P,C)),np.zeros((8,8),complex));qvec=np.array([np.trace(e@Q).real for e in E8])
 unpack=lambda x:np.einsum('k,kab->ab',x,E8)
 def psd(x):return np.linalg.eigvalsh(unpack(x))
 def psdjac(x):
  ev,U=np.linalg.eigh(unpack(x));return np.array([[np.vdot(U[:,j],e@U[:,j]).real for e in E8] for j in range(8)])
 x0=np.array([np.trace(e@np.eye(8)/2).real for e in E8])
 sol=minimize(lambda x:-qvec@x,x0,jac=lambda x:-qvec,method='SLSQP',constraints=[{'type':'eq','fun':lambda x:TP@x-target,'jac':lambda x:TP},{'type':'ineq','fun':psd,'jac':psdjac}],options={'ftol':1e-11,'maxiter':1000})
 J=unpack(sol.x);J=(J+J.conj().T)/2;J-=np.kron(I/2,partialout(J)-np.eye(4));mu=max(0.,-np.linalg.eigvalsh(J).min())+1e-12;J=(J+mu*np.eye(8))/(1+2*mu)
 # Dual minimize TrY, I2 tensorY>=Q.
 unpack4=lambda x:np.einsum('k,kab->ab',x,E4)
 dybasis=np.array([np.kron(I,e) for e in E4]);tr4=np.array([np.trace(e).real for e in E4])
 def dualpsd(x):return np.linalg.eigvalsh(np.kron(I,unpack4(x))-Q)
 def dualjac(x):
  ev,U=np.linalg.eigh(np.kron(I,unpack4(x))-Q);return np.array([[np.vdot(U[:,j],e@U[:,j]).real for e in dybasis] for j in range(8)])
 d0=(np.linalg.eigvalsh(Q).max()+1)*tr4
 dual=minimize(lambda x:tr4@x,d0,jac=lambda x:tr4,method='SLSQP',constraints=[{'type':'ineq','fun':dualpsd,'jac':dualjac}],options={'ftol':1e-11,'maxiter':1000})
 YY=unpack4(dual.x);shift=max(0.,-np.linalg.eigvalsh(np.kron(I,YY)-Q).min())+1e-12;YY+=shift*np.eye(4)
 primal=np.trace(Q@J).real;dualval=np.trace(YY).real
 def decode(M):return np.array([[np.trace(J[4*a:4*a+4,4*b:4*b+4]@M.T) for b in range(2)] for a in range(2)])
 meta={'primal_success':bool(sol.success),'dual_success':bool(dual.success),'primal_iterations':int(sol.nit),'dual_iterations':int(dual.nit),'numerical_primal_dual_gap':float(dualval-primal),'minimum_repaired_Choi_eigenvalue':float(np.linalg.eigvalsh(J).min()),'TP_residual':float(np.linalg.norm(partialout(J)-np.eye(4))),'empirical_Bell_loss':float(.75-primal)}
 return (decode,meta,J) if return_choi else (decode,meta)

def main():
 V,source,probs,trueC=generator_only_source();trueB=[V@b@V.conj().T for b in B0]
 noiseless={}
 U,A,runs=unitary_search(trueC,710,starts=6);gap,res,_=fit_block(A,trueC)
 noiseless['variational']={**score_decoder(A,V,source),'generator_Frobenius_error':float(np.sqrt(sum(np.linalg.norm(a-b,'fro')**2 for a,b in zip(A,trueB)))),'candidate_gap':gap,'candidate_residual':res,'search':runs}
 for name,AA in [('raw_sign',[sign(c) for c in trueC]),('scalar_whitening',scalar_whitening(trueC))]:noiseless[name]=score_decoder(AA,V,source)
 AA,ogap=operator_whitening(trueC);noiseless['operator_whitening']={'block_gap':ogap,**({} if AA is None else score_decoder(AA,V,source))}
 dec,meta=sdp_recovery(trueC);noiseless['full_CPTP_SDP']={**meta,'native_Bell_loss':1-bell_fidelity(lambda rho:dec(source(rho)))}
 noiseless['exact_inverse']=score_decoder(trueB,V,source)
 rows=[];countsout={};total=0;starttime=time.time()
 for N in [4096,16384,65536]:
  for rep in range(4):
   seed=202610280000+N+rep;counts=acquire(N,seed,probs);countsout[f'N{N}_rep{rep}']=counts;C=learner_contrasts(counts);total+=N
   U,A,runs=unitary_search(C,seed+900000,starts=4);gap,res,S=fit_block(A,C)
   a=np.sqrt(16*9*16/N);kappa=max(0.,gap/2);certificate=None if kappa==0 else 2*(res+np.sqrt(12)*a)/kappa
   result={'N':N,'replicate':rep,'record_seed':seed,'variational':{**score_decoder(A,V,source),'generator_Frobenius_error':float(np.sqrt(sum(np.linalg.norm(a-b,'fro')**2 for a,b in zip(A,trueB)))),'candidate_block_gap_float':gap,'candidate_fit_residual_float':res,'declared_simultaneous_operator_confidence_radius':float(a),'provisional_candidate_kappa_float':kappa,'theorem_error_bound_float':certificate,'passes_target_delta_0_1':bool(certificate is not None and certificate<=.1),'search':runs}}
   for name,AA in [('raw_sign',[sign(c) for c in C]),('scalar_whitening',scalar_whitening(C))]:result[name]=None if AA is None else score_decoder(AA,V,source)
   AA,ogap=operator_whitening(C);result['operator_whitening']={'block_gap':ogap,**({} if AA is None else score_decoder(AA,V,source))}
   dec,meta=sdp_recovery(C);result['full_CPTP_SDP']={**meta,'native_Bell_loss':1-bell_fidelity(lambda rho:dec(source(rho)))}
   rows.append(result);print(json.dumps({'N':N,'rep':rep,'elapsed':time.time()-starttime,'variational_loss':result['variational']['native_Bell_loss'],'SDP_loss':result['full_CPTP_SDP']['native_Bell_loss'],'gap':gap,'certificate':certificate}),flush=True)
 np.savez_compressed(HERE/'ordinary_counts.npz',**countsout)
 out={'status':'COMPLETED_FLOATING_SAMPLED_PILOT','one_fixed_hidden_source':True,'total_individually_rng_drawn_source_blocks':total,'independent_banks':len(rows),'physical_output_readouts':2*total,'logical_preparations':total,'noiseless_diagnostics':noiseless,'runs':rows,'scope':'Floating candidate search and numerical SDP comparison. Every source block has individual setting/outcome RNG draws; no source parameters passed to learner. Candidate gap/residual diagnostics are floating, not an exact rational accepted certificate or hardware controls. No theorem acceptance at target is inferred from small actual scoring error. No sampled unknown payload or continuing-memory trajectory.','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':out['status'],'total':total,'seconds':time.time()-starttime}),flush=True)
if __name__=='__main__':main()
