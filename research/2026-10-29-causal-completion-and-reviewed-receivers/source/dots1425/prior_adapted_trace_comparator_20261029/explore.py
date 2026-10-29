import numpy as np,json
P=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1])];I=np.eye(2);X=P[0]
def fun(a,f):e,u=np.linalg.eigh(a);return (u*f(e))@u.conj().T
def phi_K(g):return [X@np.diag([1,np.sqrt(1-g)]),X@np.array([[0,np.sqrt(g)],[0,0]])]
def apply(K,a):return sum(k@a@k.conj().T for k in K)
def kernel(x):return 1. if abs(x)<1e-9 else x/np.sinh(x)
def maps(sig,g):
 K=phi_K(g);nu=apply(K,sig);ss=fun(sig,np.sqrt);ni=fun(nu,lambda x:1/np.sqrt(x));R=[ss@k.conj().T@ni for k in K]
 s,u=np.linalg.eigh(sig);v,w=np.linalg.eigh(nu)
 def rb(y):
  y=w.conj().T@y@w;out=np.zeros((2,2),complex)
  for a in range(2):
   for b in range(2):
    E=np.zeros((2,2),complex);E[a,b]=1;z=u.conj().T@apply(R,w@E@w.conj().T)@u
    for i in range(2):
     for j in range(2):out[i,j]+=y[a,b]*z[i,j]*kernel((np.log(s[i]/s[j])-np.log(v[a]/v[b]))/2)
  return u@out@u.conj().T
 def psi(a):return rb(apply(K,a))
 B=[ss[:,j:j+1]@ss[j:j+1,:]/sig[j,j] for j in range(2)]
 def eb(a):return a[0,0]*B[0]+a[1,1]*B[1]
 M=np.array([[np.trace(p@(q-psi(q))).real/2 for q in P] for p in P]);N=np.array([[np.trace(p@(q-eb(q))).real/2 for q in P] for p in P]);T=N@np.linalg.inv(M)
 return np.linalg.norm(T,2),np.sum(abs(T)),np.linalg.norm(psi(sig)-sig),T
rows=[]
for g in [.5,.7,.95]:
 for r in [.01,.5,.9,.99,.9999,1-1e-8]:
  for theta in np.linspace(0,np.pi,21):
   sig=(I+r*(np.sin(theta)*P[0]+np.cos(theta)*P[2]))/2
   norm,bound,res,T=maps(sig,g);rows.append({'gamma':g,'radius':r,'theta':float(theta),'spectralnorm':float(norm),'entry_l1':float(bound),'stationary_residual':float(res)})
rows.sort(key=lambda x:x['spectralnorm'],reverse=True);print(rows[:5]);open('CHECKS.json','w').write(json.dumps({'scope':'floating finder only; no uniform analytic bound or diamond claim','rows':rows},indent=2)+'\n')
