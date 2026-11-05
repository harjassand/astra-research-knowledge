import numpy as np, json,sys

def update(j,g):
 # Inputs j>0. Source order is old gauge, payload, new carrier.
 ap=(2*j*g-1)/(2*j+1);bp=np.sqrt(j/(j+1))*(g+2*j+2)/(2*j+1)
 am=((2*j+2)*g+1)/(2*j+1);bm=np.sqrt((j+1)/j)*(2*j-g)/(2*j+1)
 wp=(j+1)/(2*j+1)*(j+.5)*(j+1.5);wm=j/(2*j+1)*(j-.5)*(j+.5)
 A=wp*ap*ap+wm*am*am;B=wp*bp*bp+wm*bm*bm;C=wp*ap*bp-wm*am*bm
 phi=.5*np.arctan2(2*C,A-B)
 co=np.cos(phi);si=np.sin(phi)
 gp=ap*co+bp*si;gm=am*co-bm*si
 return gp,gm,(A+B+np.sqrt((A-B)**2+4*C*C))/2,phi

def exact(nmax):
 states=[(.5,1.,1.)]
 for n in range(2,nmax+1):
  mom=sum(p*g*g*j*(j+1) for j,g,p in states);gg=sum(p*g*g for j,g,p in states)
  print(json.dumps(dict(n=n,branches=len(states),retained_moment=mom,Y_energy=3*n*(n-1)/8-mom,mean_gamma2=gg,energy_over_n2=(3*n*(n-1)/8-mom)/n**2)),flush=True)
  nxt=[]
  for j,g,p in states:
   if j==0:nxt.append((.5,1.,p));continue
   gp,gm,val,phi=update(j,g);pp=(j+1)/(2*j+1)
   nxt +=[(j+.5,abs(float(gp)),p*pp),(j-.5,abs(float(gm)) if j>.5 else 0.,p*(1-pp))]
  states=nxt

def mc(nmax,samples=200000):
 rng=np.random.default_rng(8123);j=np.full(samples,.5);g=np.ones(samples)
 for n in range(2,nmax+1):
  if n<=10 or n%25==0:
   mom=np.mean(g*g*j*(j+1));ener=3*n*(n-1)/8-mom
   print(json.dumps(dict(n=n,retained_moment=float(mom),Y_energy=float(ener),mean_gamma2=float(np.mean(g*g)),energy_over_n2=float(ener/n**2),max_gamma=float(np.max(g)))),flush=True)
  positive=j>0;inds=np.flatnonzero(positive);jj=j[inds];gg=g[inds];gp,gm,val,phi=update(jj,gg);upper=rng.random(len(inds))<(jj+1)/(2*jj+1)
  j[~positive]=.5;g[~positive]=1
  j[inds]=jj+np.where(upper,.5,-.5);g[inds]=np.abs(np.where(upper,gp,gm));g[j==0]=0
if __name__=='__main__':
 if sys.argv[1]=='exact':exact(int(sys.argv[2]))
 else:mc(int(sys.argv[2]),int(sys.argv[3]))
