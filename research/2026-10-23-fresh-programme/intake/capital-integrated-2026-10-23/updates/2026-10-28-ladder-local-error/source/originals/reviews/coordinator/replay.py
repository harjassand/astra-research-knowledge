"""Coordinator's independent endpoint replays and physical occupation-space check."""
from pathlib import Path
from itertools import combinations_with_replacement
import hashlib,json,math,shutil,subprocess
import numpy as np
from scipy.linalg import eigh,eigh_tridiagonal
from scipy.optimize import brentq
BASE=Path(__file__).resolve().parent.parent;HERE=Path(__file__).resolve().parent
choices={'r11':'continuum_response.py','r24':'response.py','r37':'spectral_response.py','r48':'spectral_response.py'}
replays=[]
for case,script in choices.items():
 dst=HERE/case
 if not dst.exists():shutil.copytree(BASE/'frozen'/case,dst)
 r=subprocess.run(['/usr/local/bin/python3',script],cwd=dst,text=True,capture_output=True,timeout=100)
 (dst/'REPLAY_STDOUT.json').write_text(r.stdout);(dst/'REPLAY_STDERR.txt').write_text(r.stderr)
 row={'case':case,'exit_code':r.returncode}
 if r.returncode==0:
  data=json.loads(r.stdout);row['rho_values']=[x.get('rho') for x in data.get('runs',[data])]
 else:row['error']=r.stderr[-1500:]
 replays.append(row)
def direct(n,g=.2):
 d=2+2*n;h=3*np.eye(d);t=(1+math.sqrt(2))*g/2;s=(math.sqrt(2)-1)*g/2
 for a,j,v in [(0,2,t),(0,2+n,s),(1,2,s),(1,2+n,t)]:h[a,j]=h[j,a]=v
 for j in range(n):h[2+j,2+n+j]=h[2+n+j,2+j]=2
 for a in [2,2+n]:
  for j in range(n-1):h[a+j,a+j+1]=h[a+j+1,a+j]=-.5
 states=[]
 for i,j in combinations_with_replacement(range(d),2):
  if i==j and i<2:continue
  v=[0]*d;v[i]+=1;v[j]+=1;states.append(tuple(v))
 where={v:i for i,v in enumerate(states)};H=np.zeros((len(states),len(states)))
 for col,v in enumerate(states):
  for q,count in enumerate(v):
   if not count:continue
   after=list(v);after[q]-=1
   for p in np.flatnonzero(h[:,q]):
    new=after.copy();amp=math.sqrt(count*(after[p]+1));new[p]+=1
    if tuple(new) in where:H[where[tuple(new)],col]+=h[p,q]*amp
 assert np.max(abs(H-H.T))<1e-13
 eig,U=eigh(H);bare=[0]*d;bare[0]=bare[1]=1
 idx=np.argmax(U[where[tuple(bare)],:]**2);E=eig[idx];psi=U[:,idx]
 f=psi*np.array([v[0]-v[1] for v in states]);specs=[]
 for c,coup in [(5,math.sqrt(2)*g),(1,g)]:
  e,u=eigh_tridiagonal(np.r_[3,np.full(n,c)],np.r_[coup,np.full(n-1,-.5)])
  specs.append((e,u[0,:]**2))
 (ep,wp),(em,wm)=specs
 lp=lambda z:sum(np.sum((w[:,None]*w[None,:])/(e[:,None]+e[None,:]-z)) for e,w in specs)
 ap=ep[(ep>2)&(ep<4)][0];am=em[(em>2)&(em<4)][0]
 root=brentq(lp,2*ap+1e-10,2*am-1e-10,xtol=1e-14);assert abs(E-root)<1e-11
 norm=sum(np.sum((w[:,None]*w[None,:])/(e[:,None]+e[None,:]-E)**2) for e,w in specs)
 a=np.array([np.sum(wp/(ep+x-E)) for x in ep]);b=np.array([np.sum(wm/(em+y-E)) for y in em])
 ff=math.sqrt(2/norm)*(a[:,None]+b[None,:]);ww=wp[:,None]*wm[None,:];errors=[]
 for eta in [.031,.097,.173]:
  z=E+1j*eta;den=ep[:,None]+em[None,:]-z
  full=np.vdot(f,np.linalg.solve(H-z*np.eye(len(H)),f))
  reduced=np.sum(ww*ff**2/den)-np.sum(ww*ff/den)**2/np.sum(ww/den)
  errors.append(float(abs(full-reduced)))
 return {'n':n,'dimension':len(H),'energy':float(E),'source_norm':float(np.vdot(f,f)),
         'norm_error':float(abs(np.vdot(f,f)-np.sum(ww*ff**2))),
         'orthogonality_error':float(abs(np.sum(ww*ff))),
         'regulators':[.031,.097,.173],'response_errors':errors}
checks=[direct(n) for n in [3,6,9]];unchanged=[]
for case in choices:
 m=json.loads((BASE/'frozen'/case/'FROZEN_FILES.json').read_text())
 unchanged.append({'case':case,'unchanged':all(hashlib.sha256((BASE/'frozen'/case/x['file']).read_bytes()).hexdigest()==x['sha256'] for x in m)})
out={'replays':replays,'independent_physical_checks':checks,'frozen_sources':unchanged,
     'scope':'Numerical identity checks; analytic continuum proof assessed separately, no interval decimal or device claim.'}
(HERE/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
