exec(open('mixed_reset_purity_probe.py').read().split('best=-1e9')[0])
def root(A):
 w,U=np.linalg.eigh(A);return (U*np.sqrt(np.maximum(w,0)))@U.conj().T
def f(A):return -entropy(A)
def L(c,X,Y):
 C=np.sqrt(c)*root(X)@root(Y);G=np.block([[X,C],[C.conj().T,Y]])
 return f(G)-f(X)-f(Y)
mx=0;mn=100
for k in [2,3,5]:
 for j in range(20):
  z=rng.normal(size=(k,k))+1j*rng.normal(size=(k,k));sig=z@z.conj().T;sig/=np.trace(sig)
  z=rng.normal(size=(k,k))+1j*rng.normal(size=(k,k));eta=z@z.conj().T;eta/=np.trace(eta)
  p=rng.uniform(.01,.99);tau=np.kron(np.diag([1.,0,0]),eta);actual=delta(make(sig,tau,p));S=p*sig/3;Q=(1-p)*eta/3
  formula=L(1/3,3*S,Q)+L(1,S,3*Q)-4*L(.5,S,Q)
  mx=max(mx,abs(actual-formula));mn=min(mn,actual);assert abs(actual-formula)<1e-11 and actual>0
print(dict(status='PASS',complex_noncommuting_cases=60,maximum_source_identity_error=mx,minimum_deficit=mn))
