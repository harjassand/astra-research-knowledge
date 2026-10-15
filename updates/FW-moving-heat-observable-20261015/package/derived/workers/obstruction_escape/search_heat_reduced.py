exec(open(__file__.replace('search_heat_reduced.py','search_heat.py')).read().split('rng=np.random.default_rng')[0])
def reduced(z,full=False):
 zz=np.r_[np.zeros(4),z];_,g0=fg(zz);cc=g0[:4];bb=np.zeros((4,4))
 for k,n in enumerate(modes):
  mat=np.outer(z[2*k:2*k+2]/scales[4+2*k:4+2*k+2],n).ravel();bb+=np.dot(n,n)*np.array(hf(*mat))
 B=-np.linalg.solve(bb,cc)
 val,gg=fg(np.r_[B,z]);return (val,gg[4:],B) if full else (val,gg[4:])
rng=np.random.default_rng(200+mi);best=None
for i in range(200):
 z=rng.normal(size=dim-4);z/=np.linalg.norm(z)
 sol=minimize(lambda z:reduced(z),z,jac=True,method='SLSQP',constraints=[{'type':'eq','fun':lambda z:z@z-1,'jac':lambda z:2*z}],options={'ftol':1e-11,'maxiter':400})
 if best is None or sol.fun<best.fun:
  best=sol;print('mode set',mi,'iteration',i,'best',sol.fun,'status',sol.success,flush=True)
 if best.fun < -1e-7:break
val,gg,B=reduced(best.x,True);ZZ=np.r_[B,best.x]
np.savez(out/f'heat_reduced_modes{mi}.npz',modes=modes,z=ZZ,scales=scales,value=best.fun,N=N)
print('modes',modes.tolist(),'B',B.tolist(),'raw coefficients',(ZZ/scales).tolist(),'value',best.fun,flush=True)
