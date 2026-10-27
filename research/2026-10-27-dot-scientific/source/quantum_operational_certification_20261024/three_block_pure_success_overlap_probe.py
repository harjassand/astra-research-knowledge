exec(open('mixed_reset_purity_probe.py').read().split('best=-1e9')[0])
rng=np.random.default_rng(39803)
def val(p,w,r):
 tau=np.zeros((6,6))
 for i in range(3):
  v=np.array([np.sqrt(1-r[i]),np.sqrt(r[i])]);tau[2*i:2*i+2,2*i:2*i+2]=w[i]*np.outer(v,v)
 return delta(make(np.diag([0.,1.]),tau,p))
for case in range(120):
 p=rng.uniform(.01,.99);w=rng.dirichlet([.4]*3);r=rng.uniform(.001,.999,3)
 for i in range(3):
  h=1e-5;rp=r.copy();rm=r.copy();rp[i]+=h;rm[i]-=h;d=(val(p,w,rp)-val(p,w,rm))/(2*h)
  if d<-1e-6:print('FAIL',case,p,w,r,i,d,flush=True);np.savez('three_block_pure_success_overlap_failure.npz',p=p,w=w,r=r,i=i,derivative=d);raise SystemExit
print('bounded120 coordinate derivative PASS')
