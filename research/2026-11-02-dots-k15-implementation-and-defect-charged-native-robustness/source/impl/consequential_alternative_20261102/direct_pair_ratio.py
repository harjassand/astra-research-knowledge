import sys
sys.path.insert(0,'producer-workspace/consequential_alternative_20261102')
from direct_pair_search import *
a=np.array([313,-717,1627,-3027,4551,-5436,4983,-3270,1324,-220]);b=np.array([361,-895,1938,-3422,4866,-5464,4646,-2754,945,-106]);z=np.r_[a/np.linalg.norm(a),b/np.linalg.norm(b)]
p=Pair(e=.78)
def obj(z):
 r=p.calc(z,cut=1e-14);db=1-r['CB'];de=1-r['CE']
 if min(db,de)<1e-9:return 100.
 return -np.log(db/de)
print('start',obj(z),p.calc(z),flush=True)
r=minimize(obj,z,method='BFGS',options={'maxiter':250,'gtol':1e-6,'eps':1e-5})
out={'z':r.x.tolist(),'fun':r.fun,'calc':p.calc(r.x),'nit':r.nit,'message':str(r.message)};print(out,flush=True)
open('producer-workspace/direct_pair_ratio_results.json','w').write(json.dumps(out,indent=2))
for e in [.775,.78,.781,.7818,.782]:
 for M in [64,100]:
  p=Pair(e=e,M=M)
  for cut in [1e-12,1e-14,1e-16]:print(e,M,cut,p.calc(r.x,cut=cut),flush=True)
