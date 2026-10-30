import numpy as np,json
# Actual six jumps; zero continuation at D=0.
steps=[(-1,0,1),(1,0,-1),(-1,1,0),(1,-1,0),(-2,0,2),(1,0,-1)]
rows=[]
for eta in [.5,.9,.99]:
 for s in [2.,4.]:
  for n in [32,64,128,256]:
   states=[(a,n-a-d,d) for d in range(1,n+1) for a in range(n-d+1)]
   vals=[]
   for a,c,d in states:
    x=a+3; z=x+eta*c
    fs=np.array([x**-s/(x**3+n*d),z**-s/(z**3+n*d)])
    drift=-a*(a-1)*fs
    rates=[a*(a-1),a*d,a*d,c*d,a*(a-1),d*(d-1)]
    for (da,dc,dd),rate in zip(steps,rates):
     if not rate:continue
     if d+dd==0:nxt=np.zeros(2)
     else:
      xx=x+da;zz=xx+eta*(c+dc)
      nxt=np.array([xx**-s/(xx**3+n*(d+dd)),zz**-s/(zz**3+n*(d+dd))])
     drift+=rate*(nxt-fs)
    vals.append((a,c,d,x,drift[0],drift[1]))
   best=None
   for ratio in np.geomspace(.01,1e6,81):
    worst=max(vals,key=lambda v:(v[4]+ratio*v[5])*v[3]**(s+1))
    margin=-(worst[4]+ratio*worst[5])*worst[3]**(s+1)
    if best is None or margin>best['margin']:
     best={'ratio':float(ratio),'margin':float(margin),'worst_state':worst[:3]}
   rows.append(dict(eta=eta,s=s,n=n,**best))
json.dump(rows,open('recovery_chemical_review_20261030/check_resolvent_drift.json','w'),indent=2)
print(json.dumps(rows,indent=2))
