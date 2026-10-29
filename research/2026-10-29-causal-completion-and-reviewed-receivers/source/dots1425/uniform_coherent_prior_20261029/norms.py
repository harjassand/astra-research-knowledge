import numpy as np,json
from lib import maps,P,I
out=[]
for g in [.5,.7,.95]:
 for eps in [.9,.5,.1,.01,1e-4,1e-8]:
  for theta in np.linspace(0,np.pi,31):
   sig=(I+(1-eps)*(np.sin(theta)*P[0]+np.cos(theta)*P[2]))/2
   M,N,T=maps(sig,g);out.append({'gamma':g,'eps':eps,'theta':float(theta),'psi_norm':float(np.linalg.norm(np.eye(3)-M,2)),'min_symmetric_gap':float(np.linalg.eigvalsh((M+M.T)/2)[0]),'T_norm':float(np.linalg.norm(T,2)),'E_deficit_norm':float(np.linalg.norm(N,2))})
print('psi',max(out,key=lambda x:x['psi_norm']));print('gap',min(out,key=lambda x:x['min_symmetric_gap']));print('E',max(out,key=lambda x:x['E_deficit_norm']));open('NORMS.json','w').write(json.dumps(out,indent=2))
