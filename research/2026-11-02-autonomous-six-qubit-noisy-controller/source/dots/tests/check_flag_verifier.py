from itertools import product
from math import exp
# Roots: a1,a2,b1,b2,b3. W=Hamming weight of true virtual witness.
parents=[(0,2),(5,4),(1,3),(7,4),(6,),(8,),(6,8)]
funcs=[lambda x:x[0]^x[1],lambda x:x[0]^x[1],lambda x:x[0]^x[1],lambda x:x[0]^x[1],lambda x:x[0],lambda x:x[0],lambda x:x[0]&x[1]]
weights=[1]*7
for i in reversed(range(7)):
 weights[i]=1+sum(weights[j] for j in range(i+1,7) if 5+i in parents[j])
wmax=max(weights); B=6; D=2; R=3; c=1
kappa=1.; gamma=1000.; eps=1/12; alpha=.01
a0=1-eps*B; A0=D+eps*B
u=kappa*c*(1-exp(-alpha*a0))
v=gamma*(1-exp(-alpha*eps))/wmax-kappa*R*((1-exp(-alpha*a0))+(exp(alpha*A0)-1))
assert v>0

def calc(z):
 W=(z[0]^z[2]^z[4])+(z[1]^z[3]^z[4])
 bad=[z[5+i]!=funcs[i]([z[t] for t in parents[i]]) for i in range(7)]
 E=sum(w*e for w,e in zip(weights,bad))
 return W,E,bad
max_res=-1e99
for zz in product((0,1),repeat=12):
 z=list(zz); W,E,bad=calc(z); Q=W+eps*E
 drift=edrift=0.
 for i,err in enumerate(bad):
  if err:
   t=z.copy();t[5+i]^=1;Wt,Et,_=calc(t);dq=Wt+eps*Et-Q
   assert Wt==W and Et<=E-1
   drift+=gamma*dq;edrift+=gamma*(exp(alpha*dq)-1)
 for b,out in [(2,9),(3,10),(4,11)]:
  if z[out]:
   t=z.copy();t[b]^=1;Wt,Et,_=calc(t);dq=Wt+eps*Et-Q
   assert abs(Wt-W)<=D and abs(Et-E)<=B
   drift+=kappa*dq;edrift+=kappa*(exp(alpha*dq)-1)
 meanbound=-kappa*a0*c*W+(kappa*R*(a0+A0)-gamma*eps/wmax)*E
 ebound=-u*W-v*E
 assert drift<=meanbound+1e-9,(z,drift,meanbound)
 assert edrift<=ebound+1e-9,(z,edrift,ebound)
 max_res=max(max_res,edrift-ebound)
 # Inverse reversible Boolean circuit gives each original violation bit.
 t=z.copy()
 for i in reversed(range(7)):
  t[5+i]^=funcs[i]([t[q] for q in parents[i]])
 assert t[5:]==[int(e) for e in bad]
print('PASS: all 4096 physical bit configurations; exact mean/exponential generator bounds and verifier-frame inverse.')
print('weights=',weights,'wmax=',wmax,'epsilon=',eps,'gamma=',gamma,'alpha=',alpha,'u=',u,'v=',v,'max residual=',max_res)
print('Finite classical-algebra check only; not a quantum-syndrome hardware construction or lifetime simulation.')
