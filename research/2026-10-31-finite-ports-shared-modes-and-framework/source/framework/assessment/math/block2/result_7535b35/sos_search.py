"""Numerical discovery only; any result is reconstructed with exact arithmetic."""
import numpy as np
best=(10.,None)
for t in np.linspace(0,1,151):
 for z in np.linspace(-1.0,t/2,181):
  T=np.array([[1+1.25*t-z/2,t-z,z-t],[t-z,2*(1-t),z],[z-t,z,1+t/2-z]])
  if np.linalg.eigvalsh(T)[0]<1e-9:continue
  value=np.linalg.inv(T)[2,2]
  if value>=best[0]:continue
  for r in np.linspace(0,t,101):
   G=T-np.diag([r,0,t-r])
   if np.linalg.eigvalsh(G)[0]>=-1e-8:
    best=(value,(t,z,r,np.linalg.eigvalsh(G)));break
print('BEST',best,'QC NU',best[0]/4)
