exec(open('producer-workspace/refined_charge.py').read().split('results=[]')[0])
for r in [1,2,3,4,6,8]:
 N=3*r
 for tag,phi in [('a',pa),('b',pb)]:
  u=sampled(phi,r).reshape(N,N,N,2,2);diff=[]
  for axis in range(3):
   d=u-np.roll(u,1,axis=axis);norm=np.sqrt(np.sum(abs(d)**2,axis=(-2,-1))/2);diff.append(norm)
  print(r,tag,'max link matrix norm',max(float(np.max(v)) for v in diff),'mean',float(np.mean(diff)),flush=True)
