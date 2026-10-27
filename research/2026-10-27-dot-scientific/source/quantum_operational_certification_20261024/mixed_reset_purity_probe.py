exec(open('sigma_fixed_flag_probe.py').read().split('best=')[0])
def entropy(A):
 e=np.linalg.eigvalsh(A);e=e[e>1e-13];return -np.dot(e,np.log(e))
def make(s,tau,p):
 A,K=build(s,np.zeros(len(tau)),p)
 return A+(1-p)*np.kron(np.eye(3)/3,tau)
def delta(A):
 d=len(A)//3;return 2*entropy(N(A,d))-entropy(A)-entropy(ptr(A,d))-np.log(3)
best=-1e9
for j in range(300):
 k=2;d=3*k
 z=rng.normal(size=(k,k))+1j*rng.normal(size=(k,k));s=z@z.conj().T;s/=np.trace(s)
 z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));tau=z@z.conj().T;tau/=np.trace(tau)
 z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));h=z+z.conj().T;h-=np.trace(h)*np.eye(d)/d;h/=np.linalg.norm(h)
 p=rng.uniform(.02,.98);A=make(s,tau,p);O=N(A,d);R=ptr(A,d);H=(1-p)*np.kron(np.eye(3)/3,h)
 val=metric(A,H)+metric(R,(1-p)*h)-2*metric(O,H)
 if val>best:
  best=val;np.savez('mixed_reset_purity_hessian_best.npz',sigma=s,tau=tau,p=p,h=h,hessian=val)
 if val>1e-6: print('FAIL',j,val,'deficit',delta(A));break
print('best',best)
