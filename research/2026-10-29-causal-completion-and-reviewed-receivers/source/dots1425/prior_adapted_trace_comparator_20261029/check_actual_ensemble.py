import numpy as np,json
rng=np.random.default_rng(1319);sig=np.array([[.5,.25],[.25,.5]],complex);e,u=np.linalg.eigh(sig);ss=(u*np.sqrt(e))@u.conj().T;X=np.array([[0,1],[1,0]],complex);K=[X@np.diag([1,1/np.sqrt(2)]),X@np.array([[0,1/np.sqrt(2)],[0,0]])];B=[ss[:,j:j+1]@ss[j:j+1,:]/sig[j,j] for j in range(2)]
S=lambda a:-sum(x*np.log(x) for x in np.linalg.eigvalsh(a) if x>1e-14);T=lambda a,b:.5*sum(abs(np.linalg.eigvalsh(a-b)));rows=[]
for d in [1,2,4]:
 base=np.kron(sig,np.eye(d)/d);root=np.kron(ss,np.eye(d)/np.sqrt(d));A=[np.kron(k,np.eye(d)) for k in K];F=lambda r:sum(k@r@k.conj().T for k in A)
 def EB(r):return sum(np.kron(B[j],r[j*d:(j+1)*d,j*d:(j+1)*d]) for j in range(2))
 maximum=0
 for _ in range(100):
  h=rng.normal(size=(2*d,2*d))+1j*rng.normal(size=(2*d,2*d));h=(h+h.conj().T)/2;h-=np.trace(base@h)*np.eye(2*d);h*=.8/max(abs(np.linalg.eigvalsh(h)));pert=root@h@root;pair=[base+pert,base-pert];assert min(np.linalg.eigvalsh(pair[0]))>0 and min(np.linalg.eigvalsh(pair[1]))>0
  delta=S(base)-sum(S(r) for r in pair)/2-S(F(base))+sum(S(F(r)) for r in pair)/2;dist=sum(T(r,EB(r)) for r in pair)/2;ratio=dist/(5*np.sqrt(delta));assert ratio<1;maximum=max(maximum,ratio)
 rows.append({'reference_dimension':d,'ensembles':100,'max_e_over_5sqrt_delta':float(maximum)})
print(rows);open('ACTUAL_ENSEMBLE_CHECKS.json','w').write(json.dumps({'scope':'floating diagnostics, interval coefficient proof separate','rows':rows},indent=2)+'\n')
