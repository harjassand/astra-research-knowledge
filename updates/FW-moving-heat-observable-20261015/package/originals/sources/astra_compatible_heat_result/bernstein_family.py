from reconstruct import *
import pickle,json
from pathlib import Path
base=Path(__file__).parent
with open(base/'moving_family.pkl','rb') as f:data=pickle.load(f)
r=data['r'];Sr=data['S'];e=s.eye(18);v1=e[:,0]-e[:,12]+e[:,16];v2=-e[:,13]+e[:,17]
K=12*D1*v1*v1.T+12*D2*v2*v2.T
t=s.symbols('t')

def bernstein(L,U,epsilon=R(1,2000)):
 T=(-(r+1)*(Sr-epsilon*K)).applyfunc(s.cancel)
 # Convert cubic polynomial to Bernstein coefficients on [L,U].
 Tt=T.subs(r,L+(U-L)*t).applyfunc(s.expand)
 pc=[Tt.applyfunc(lambda q:s.Poly(q,t).nth(k)) for k in range(4)]
 B=[sum((pc[k]*R(s.binomial(i,k),s.binomial(3,k)) for k in range(i+1)),s.zeros(18)) for i in range(4)]
 assert (sum((s.binomial(3,i)*t**i*(1-t)**(3-i)*B[i] for i in range(4)),s.zeros(18))-Tt).applyfunc(s.expand)==s.zeros(18)
 ok=[];pivs=[]
 for bb in B:
  ll,dd=bb.LDLdecomposition(hermitian=False)
  ok.append(all(q>0 for q in dd.diagonal()));pivs.append([str(q) for q in dd.diagonal()])
 return ok,B,pivs
for L,U in [(R(-13,5),R(-5,2)),(R(-21,8),R(-5,2)),(R(-8,3),R(-5,2))]:
 ok,B,pivs=bernstein(L,U)
 print('interval',L,U,'Bernstein PD',ok,flush=True)
 if all(ok):
  obj={'lower':str(L),'upper':str(U),'epsilon':'1/2000','bernstein_pivots':pivs,'status':'EXACT_PASS'}
  if L==R(-21,8):
   (base/'family_bernstein_receipt.json').write_text(json.dumps(obj,indent=2)+'\n')
   with open(base/'bernstein_family.pkl','wb') as f:pickle.dump({'lower':L,'upper':U,'epsilon':R(1,2000),'B':B,'pivots':pivs},f)
