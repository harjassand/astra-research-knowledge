import numpy as np,json
rng=np.random.default_rng(202610291253)
X=np.array([[0,1],[1,0]],complex);K=[X@np.diag([1,1/np.sqrt(2)]),X@np.array([[0,1/np.sqrt(2)],[0,0]])]
def entropy(a):
 e=np.linalg.eigvalsh(a);e=e[e>1e-15];return -np.sum(e*np.log(e))
rows=[]
for d in [1,2,3,4]:
 A=[np.kron(k,np.eye(d)) for k in K];logsig=np.kron(np.diag(np.log([1/3,2/3])),np.eye(d))
 def f(a):return sum(k@a@k.conj().T for k in A)
 def loss(a,b):return entropy(b)-entropy(a)+np.trace((b-a)@logsig).real
 maximum=(-1,None)
 for i in range(4000):
  g=rng.normal(size=(2*d,2*d))+1j*rng.normal(size=(2*d,2*d));rho=g@g.conj().T;rho/=np.trace(rho)
  if i%2:
   tau=np.trace(rho.reshape(2,d,2,d),axis1=0,axis2=2);base=np.kron(np.diag([1/3,2/3]),tau);a=10**rng.uniform(-4,0);rho=(1-a)*base+a*rho
  out=f(rho);out2=f(out);l1=loss(rho,out);l2=loss(rho,out2)
  if l1>1e-12 and l2/l1>maximum[0]:maximum=(float(l2/l1),i)
 rows.append({'reference_dim':d,'count':4000,'max_two_over_one':maximum[0],'max_index':maximum[1]})
print(rows);open('TWO_STEP_LOSS_CHECKS.json','w').write(json.dumps({'scope':'floating random diagnostic; no universal comparison certified','rows':rows},indent=2)+'\n')
