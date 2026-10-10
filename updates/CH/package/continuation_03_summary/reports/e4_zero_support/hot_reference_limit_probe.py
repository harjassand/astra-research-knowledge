import numpy as np,math,json

def gp_limit(P,Qinv):
 A=np.linalg.inv(P)
 B=Qinv@A/4
 vals,vecs=np.linalg.eig(B)
 if np.max(np.abs(vals.imag))>1e-7:return None
 vals=vals.real
 if min(vals)<-1e-10 or max(vals)>=1-1e-9:return None
 hv=np.array([1. if x<1e-13 else math.atanh(math.sqrt(x))/math.sqrt(x) for x in vals])
 G=A@vecs@np.diag(hv)@np.linalg.inv(vecs)
 return (G.real+G.real.T)/2

def gap(eta,u,k,p):
 v=1.5;ce=math.sqrt(2);se=math.sqrt(eta);sl=math.sqrt(1-eta);c=math.sqrt(k*p)
 Pb=np.array([[u+k,-se*c],[-se*c,eta*p+(1-eta)*v]])
 Pe=np.array([[u+k,sl*c,0],[sl*c,(1-eta)*p+eta*v,-se*ce],[0,-se*ce,v]])
 Gb=gp_limit(Pb,np.diag([1/u,0]));Ge=gp_limit(Pe,np.diag([1/u,0,1/v]))
 if Gb is None or Ge is None:return None
 Tb=np.diag([1,se]);Te=np.array([[1.,0.],[0.,-sl],[0.,0.]])
 D=Te.T@Ge@Te-Tb.T@Gb@Tb
 return np.linalg.eigvalsh(D)[0]

if __name__=='__main__':
 rng=np.random.default_rng(314873)
 out=[]
 for eta in [.750001,.7501,.751,.752,.755,.758,.76,.7605,.761,.762]:
  best=(1,None);valid=0
  for i in range(16000):
   u=.5+10**rng.uniform(-6,3)
   k=10**rng.uniform(-5,4)
   p=10**rng.uniform(-5,4)
   g=gap(eta,u,k,p)
   if g is None:continue
   valid+=1
   if g<best[0]:best=(g,[u,k,p])
  row={'eta':eta,'valid':valid,'gap':best[0],'u_k_p':best[1]};print(json.dumps(row),flush=True);out.append(row)
 with open('work/continuation_03/reports/e4_zero_support/hot_reference_limit_probe.json','w') as f:json.dump({'status':'formal limiting family floating-point only','rows':out},f,indent=2)
