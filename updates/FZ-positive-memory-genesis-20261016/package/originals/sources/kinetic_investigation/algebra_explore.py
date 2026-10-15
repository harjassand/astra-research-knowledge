import sympy as s
import numpy as np
k,u=s.symbols('k u',positive=True)
a=[1+u,s.Integer(1),1-u]
K=s.zeros(3)
for i in range(3):
    den=sum(a[j] for j in range(3) if j!=i)+k
    for j in range(3):
        if i!=j: K[i,j]=den/((2+k)**2*a[j])
print('det(I-K)=',s.factor((s.eye(3)-K).det()))
print('k=0=',s.factor((s.eye(3)-K).det().subs(k,0)))
K0=K.subs({k:s.Rational(1,10**6),u:s.Rational(1,100)})
vals,vecs=np.linalg.eig(np.array(K0,float)); idx=np.argmax(vals.real)
v=vecs[:,idx].real;v=v/v.min()
v=s.Matrix([s.Rational(round(z*10**9),10**9) for z in v])
print('rho=',vals[idx]);print('v=',v.T)
print('Kv-v=',[float(x) for x in K0*v-v]); print('exact strict positive=',all(x>0 for x in K0*v-v))
# local second-order prediction for triangle pi uniform, S offdiag1/2.
f=s.Matrix([1,0,-1]); S=(s.ones(3)-s.eye(3))/2
print('a=',sum((S*(f.applyfunc(lambda z:z*z)))[i]-(S*f)[i]**2 for i in range(3))/3)
