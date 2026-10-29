import sys,json,numpy as np
sys.path.insert(0,'producer-workspace/prior_adapted_trace_comparator_20261029');from explore_library import maps,P,I
rows=[]
for g in [.5,.7,.95]:
 for eps in [1e-2,1e-4,1e-6,1e-8,1e-10,1e-12]:
  for theta in np.geomspace(1e-8,1,81):
   sig=(I+(1-eps)*(np.sin(theta)*P[0]+np.cos(theta)*P[2]))/2
   a,b,c,T=maps(sig,g);rows.append({'gamma':g,'epsilon':eps,'theta':float(theta),'norm':a,'entry_l1':b,'residual':c})
rows.sort(key=lambda x:x['norm'],reverse=True);print(rows[:10]);open('BOUNDARY.json','w').write(json.dumps(rows,indent=2))
