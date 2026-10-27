exec(open('pure_physical_mixed_logical_reset_check.py').read().split('mx=0')[0])
def multi(X,Ys,c):
 k=X.shape[0];G=np.zeros(((len(Ys)+1)*k,)*2,complex);G[:k,:k]=X
 for i,Y in enumerate(Ys,1):
  C=np.sqrt(c)*root(X)@root(Y);G[:k,i*k:(i+1)*k]=C;G[i*k:(i+1)*k,:k]=C.conj().T;G[i*k:(i+1)*k,i*k:(i+1)*k]=Y
 return f(G)-f(X)-sum(f(Y) for Y in Ys)
mx=0
for case in range(40):
 k=2 if case<20 else 3
 def rnd():
  Z=rng.normal(size=(k,k))+1j*rng.normal(size=(k,k));return Z@Z.conj().T
 sig=rnd();sig/=np.trace(sig);T1=rnd();T2=rnd();z=np.trace(T1+T2);T1/=z;T2/=z;p=rng.uniform(.03,.97)
 tau=np.zeros((3*k,3*k),complex);tau[:k,:k]=T1;tau[k:2*k,k:2*k]=T2
 actual=delta(make(sig,tau,p));S=p*sig/3;Q1=(1-p)*T1/3;Q2=(1-p)*T2/3
 formula=multi(3*S,[Q1,Q2],1/3)+L(1,S,3*Q1)+L(1,S,3*Q2)-2*(multi(S,[Q1,Q2],.5)+L(.5,S,Q1)+L(.5,S,Q2))
 mx=max(mx,abs(actual-formula));assert abs(actual-formula)<1e-11
print('source identity PASS40',mx)
