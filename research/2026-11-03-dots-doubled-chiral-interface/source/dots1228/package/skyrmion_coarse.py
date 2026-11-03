exec(open('producer-workspace/wilson_endpoint.py').read().split('rng=')[0])
rng=np.random.default_rng(43)
for trial in range(10000):
 center=rng.uniform(.5,1.5,3);R=rng.uniform(1.1,1.49)
 xx=np.array(coords)-center;xx=(xx+1.5)%3-1.5;r=np.linalg.norm(xx,axis=1);f=np.pi*np.maximum(1-r/R,0)
 z=np.cos(f)+1j*np.sin(f)*xx[:,2]/np.maximum(r,1e-12)
 phi=np.angle(z)/(2*np.pi)%1;q,_,_=data(phi)
 if q:
  print('center',center,'R',R,'coarse selflink',q,'phi',phi);np.savez(D+'skyrmion_coarse.npz',center=center,R=R,phi=phi,q=q);break
else:print('no nonzero s')
