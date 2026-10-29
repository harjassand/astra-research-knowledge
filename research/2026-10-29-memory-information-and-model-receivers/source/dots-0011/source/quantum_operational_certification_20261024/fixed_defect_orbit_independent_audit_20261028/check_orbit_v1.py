#!/usr/bin/env python3
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import itertools,json,numpy as np
HERE=Path(__file__).parent

def tableaux(shape):
 k=sum(shape);out=[]
 def rec(w,counts):
  if len(w)==k:out.append(tuple(w));return
  for r in range(len(shape)):
   if counts[r]<shape[r] and (r==0 or counts[r]<counts[r-1]):
    cc=counts.copy();cc[r]+=1;rec(w+[r],cc)
 rec([],[0]*len(shape));return out

def reps(shape):
 tabs=tableaux(shape);idx={t:i for i,t in enumerate(tabs)};d=len(tabs);k=sum(shape);S=[]
 for a in range(k-1):
  A=np.zeros((d,d))
  for z,t in enumerate(tabs):
   con=[sum(t[i]==t[p] for i in range(p+1))-1-t[p] for p in [a,a+1]];ax=con[1]-con[0];A[z,z]=1/ax
   sw=list(t);sw[a],sw[a+1]=sw[a+1],sw[a];sw=tuple(sw)
   if sw!=t and sw in idx:A[idx[sw],z]=np.sqrt(1-1/ax**2)
  assert np.max(abs(A@A-np.eye(d)))<1e-12;S.append(A)
 return tabs,S

def permrep(g,S):
 w=list(g);steps=[]
 for value in range(len(w)):
  p=w.index(value)
  while p>value:w[p],w[p-1]=w[p-1],w[p];steps.append(p-1);p-=1
 U=np.eye(len(S[0]))
 for a in steps:U=S[a]@U
 return U

def main():
 rows=[]
 for lam,mu,j in [((3,1),(2,2),2),((3,2),(3,1,1),2),((4,2),(4,2),2),((4,2),(3,3),2)]:
  k=sum(lam);lt,ls=reps(lam);mt,ms=reps(mu);d=len(lt);D=len(mt);L=mathprod(range(k-j+1,k+1));n=k-j
  def group(tabs):
   out={}
   for idx,t in enumerate(tabs):
    prefix=t[:n];alpha=tuple(prefix.count(r) for r in range(max(prefix)+1));tail=t[n:];out.setdefault((alpha,tail),{})[prefix]=idx
   return out
  lg,mg=group(lt),group(mt);seeds=[]
  for (alpha,tailL),li in lg.items():
   for (beta,tailM),mi in mg.items():
    if alpha!=beta:continue
    assert set(li)==set(mi);A=np.zeros((D,d));scale=np.sqrt(d/len(li))
    for t in li:A[mi[t],li[t]]=scale
    assert np.linalg.norm(A,2)<=np.sqrt(L)+1e-10;seeds.append(A)
  S=len(seeds);cosets=list(itertools.permutations(range(k),j));B=[]
  for images in cosets:
   g=[a for a in range(k) if a not in images]+list(images);U=permrep(g,ms);V=permrep(g,ls)
   for A in seeds:B.append((U@A@V.T).ravel()/np.sqrt(d))
  B=np.array(B).T;F=B@B.T;eigs=np.linalg.eigvalsh(F);pos=eigs[eigs>1e-8];assert min(pos)>=1-1e-10
  index={t:i for i,t in enumerate(cosets)};J=[]
  for a in range(k):
   Q=np.zeros((L,L))
   for b0 in range(a):
    for col,t in enumerate(cosets):
     tt=tuple(a if v==b0 else b0 if v==a else v for v in t);Q[index[tt],col]+=1
   J.append(Q)
  # Generic commuting combination; integer joint eigenvalues identify tableau.
  rng=np.random.default_rng(711);weights=rng.normal(size=k);C=sum(w*A for w,A in zip(weights,J));_,V=np.linalg.eigh(C);groups={};maxjoint=0
  for col in range(L):
   v=V[:,col];contents=[int(round(v@A@v)) for A in J];maxjoint=max(maxjoint,max(np.linalg.norm(A@v-c*v) for A,c in zip(J,contents)))
   shape=[]
   for content in contents:
    options=[r for r in range(len(shape)+1) if (r==len(shape) or r==0 or shape[r]<shape[r-1]) and ((shape[r] if r<len(shape) else 0)-r)==content]
    assert len(options)==1,(contents,shape,options);r=options[0]
    if r==len(shape):shape.append(1)
    else:shape[r]+=1
   groups.setdefault(tuple(shape),[]).append(col)
  assert maxjoint<1e-8
  Z=np.zeros((L,L));sector=[]
  for shape,cols in groups.items():
   dim=len(tableaux(shape));h=len(cols)//dim;assert dim*h==len(cols) and shape[0]>=n
   P=V[:,cols]@V[:,cols].T;Z+=np.sqrt(dim/(L*h))*P;sector.append({'shape':shape,'dimension':dim,'H_fixed_dimension':h,'frame_eigenvalue':L*h/dim})
  A=B@np.kron(Z,np.eye(S));P=A@A.T;projerr=np.max(abs(P@P-P));assert projerr<1e-9
  vals,U=np.linalg.eigh(P);U=U[:,vals>.5];R=U.shape[1];VV=U.T@A;assert np.max(abs(VV@VV.T-np.eye(R)))<1e-9
  K=min(2,d);code=np.eye(d)[:,:K];opsA=[A[:,a].reshape(D,d)*np.sqrt(d) for a in range(A.shape[1])];opsF=[U[:,a].reshape(D,d)*np.sqrt(d) for a in range(R)]
  WA=np.concatenate([E@code for E in opsA],axis=1);WF=np.concatenate([E@code for E in opsF],axis=1);alpha=max(1.,np.linalg.norm(WA,2))*2
  def recovery(W):
   u,s,vh=np.linalg.svd(W,full_matrices=False);z=s/alpha;f=1.5*z-.5*z**3;return (vh.T*f)@u.T
  RA=recovery(WA);RF=recovery(WF);intertwine=np.max(abs(RA-np.kron(VV.T,np.eye(K))@RF));assert intertwine<1e-9
  rows.append({'lambda':lam,'mu':mu,'j':j,'d':d,'D':D,'cosets':L,'seeds':S,'frame_columns':B.shape[1],'selected_dimension':R,'min_positive_frame_eigenvalue':float(min(pos)),'predicted_sectors':sector,'JM_joint_error':float(maxjoint),'Parseval_projector_error':float(projerr),'soft_recovery_isometry_error':float(intertwine)})
  print(rows[-1],flush=True)
 (HERE/'check_orbit_v1.json').write_text(json.dumps(rows,indent=2)+'\n')
def mathprod(it):
 n=1
 for a in it:n*=a
 return n
if __name__=='__main__':main()
