import os;os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import sys,json,time,math,argparse,numpy as np
from scipy.optimize import minimize
from schur_channel import SchurChannel,sym_power
ROOT=os.path.dirname(os.path.dirname(__file__))
def flat(A):return np.r_[A.real.ravel(),A.imag.ravel()]
def unflat(x):m=len(x)//2;return (x[:m]+1j*x[m:]).reshape(2,-1)
def con(x):
 A=unflat(x);return float(np.linalg.norm(A)**2-1)
def cjac(x):return 2*x
def detcon(x):
 A=unflat(x);return float(np.linalg.det(A@A.conj().T).real-.0475)
def djac(x):
 A=unflat(x);G=A@A.conj().T;adj=np.array([[G[1,1],-G[0,1]],[-G[1,0],G[0,0]]]);return flat(2*adj@A)
def main():
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=6);p.add_argument('--v',type=float,default=.38);p.add_argument('--r',type=float,default=3);p.add_argument('--K',type=int,default=3);p.add_argument('--starts',type=int,default=4);p.add_argument('--maxiter',type=int,default=100);p.add_argument('--out',required=True);p.add_argument('--baseline-only',action='store_true');p.add_argument('--physical',action='store_true');a=p.parse_args()
 spec=next(s for s in json.load(open(ROOT+('/certified_repetition_quantizers.json' if a.physical else '/highnoise_jointflags_results.json'))) if s['v']==a.v and s['r']==a.r and s['K']==a.K)
 if a.physical:spec['Ic1']=float(spec['Ic1_cdf'])
 eng=SchurChannel(a.n,spec['w'],spec['pauli'],True);n=a.n;d=n+1;rng=np.random.default_rng(20261103+n)
 A=np.zeros((2,d),complex);A[0,0]=A[1,-1]=1/math.sqrt(2);starts=[('repetition',A)]
 seeds=json.load(open(ROOT+'/primary_xz_symmetry_seeds.json'));seed=next((s for s in seeds if s['n']==n),None)
 if seed:
  A=np.array(seed['ensemble_real'])+1j*np.array(seed['ensemble_imag']);A/=np.linalg.norm(A);starts.append(('primary',A))
  H=np.array([[1,1],[1,-1]])/math.sqrt(2);starts.append(('primary_hadamard',A@sym_power(H,n).T))
 while len(starts)<a.starts:
  A=rng.normal(size=(2,d))+1j*rng.normal(size=(2,d));A/=np.linalg.norm(A)
  if np.linalg.det(A@A.conj().T).real>.06:starts.append(('random',A))
 result=dict(args=vars(a),flags=spec,memory_bytes=eng.bytes,blocks=len(eng.meta),baselines=[],results=[])
 for label,A in starts:
  t=time.time();val,g=eng.coherent(A,True);item=dict(label=label,ic=float(val),seconds=time.time()-t,gradientnorm=float(np.linalg.norm(g)),refeig=np.linalg.eigvalsh(A@A.conj().T).tolist());result['baselines'].append(item);print('baseline',item,flush=True)
 json.dump(result,open(a.out,'w'),indent=2)
 if a.baseline_only:return
 for idx,(label,A) in enumerate(starts[:a.starts]):
  calls=[0];t=time.time()
  def fg(x):
   val,g=eng.coherent(unflat(x),True);calls[0]+=1
   if calls[0]%10==0:print('progress',idx,calls[0],float(val),'sec',time.time()-t,flush=True)
   return -float(val),-flat(g)
  opt=minimize(fg,flat(A),jac=True,method='SLSQP',constraints=[{'type':'eq','fun':con,'jac':cjac},{'type':'ineq','fun':detcon,'jac':djac}],options={'ftol':1e-10,'maxiter':a.maxiter})
  AA=unflat(opt.x);val=eng.coherent(AA);item=dict(label=label,ic=float(val),calls=calls[0],seconds=time.time()-t,success=bool(opt.success),message=opt.message,trace_error=con(opt.x),refeig=np.linalg.eigvalsh(AA@AA.conj().T).tolist(),A_real=AA.real.tolist(),A_imag=AA.imag.tolist());result['results'].append(item);json.dump(result,open(a.out,'w'),indent=2);print('result',{k:v for k,v in item.items() if not k.startswith('A_')},flush=True)
if __name__=='__main__':main()
