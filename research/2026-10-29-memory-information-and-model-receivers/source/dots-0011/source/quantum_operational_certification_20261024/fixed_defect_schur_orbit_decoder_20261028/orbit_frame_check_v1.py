#!/usr/bin/env python3
"""Small explicit orbit/Parseval fixtures; no source samples or CG oracle."""
import numpy as np,itertools,math,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent

def partitions(n,top=None):
 if n==0:yield ();return
 for x in range(min(n,top or n),0,-1):
  for r in partitions(n-x,x):yield (x,)+r

def tableaux(shape):
 k=sum(shape);out=[]
 def go(rows,path):
  if len(path)==k:out.append(tuple(path));return
  for r in range(len(shape)):
   if rows[r]<shape[r] and (r==0 or rows[r]<rows[r-1]):
    z=rows.copy();z[r]+=1;go(z,path+[(r,z[r]-1)])
 go([0]*len(shape),[]);return out

def reps(shape):
 ts=tableaux(shape);idx={t:i for i,t in enumerate(ts)};d=len(ts);k=sum(shape);ops=[]
 for j in range(k-1):
  U=np.zeros((d,d))
  for a,t in enumerate(ts):
   r=(t[j+1][1]-t[j+1][0])-(t[j][1]-t[j][0]);U[a,a]=1/r
   q=list(t);q[j],q[j+1]=q[j+1],q[j];b=idx.get(tuple(q))
   if b is not None:U[b,a]=math.sqrt(max(0,1-1/r**2))
  assert np.max(abs(U@U-np.eye(d)))<1e-12;ops.append(U)
 return ts,ops

def permrep(g,ops):
 arr=list(range(len(g)));U=np.eye(ops[0].shape[0])
 for i in range(len(g)):
  j=arr.index(g[i])
  for a in range(j-1,i-1,-1):arr[a],arr[a+1]=arr[a+1],arr[a];U=U@ops[a]
 assert arr==list(g);return U

def dim(shape):
 k=sum(shape);den=1
 for r,row in enumerate(shape):
  for c in range(row):den*=row-c+sum(int(z>c) for z in shape[r+1:])
 return math.factorial(k)//den

def fixed_h(shape,k,j):
 return sum(t[:k-j]==tuple((0,c) for c in range(k-j)) for t in tableaux(shape))

def content(shape):return sum(c-r for r,row in enumerate(shape) for c in range(row))

rows=[]
for lam,mu,j in [((2,2),(2,2),2),((3,2),(4,1),2),((4,2),(3,3),2),((4,2),(4,2),2),((4,3),(4,3),2)]:
 k=sum(lam);tl,ul=reps(lam);tm,um=reps(mu);d=len(tl);D=len(tm);ll={t:i for i,t in enumerate(tl)};mm={t:i for i,t in enumerate(tm)}
 # H invariant matrix units grouped by common exact prefix shape and suffix paths.
 def group(ts):
  z={}
  for idx,t in enumerate(ts):
   pre=t[:k-j];counts=tuple(sum(r==a for r,c in pre) for a in range(max(x[0] for x in pre)+1));suffix=t[k-j:]
   z.setdefault(counts,{}).setdefault(suffix,{})[pre]=idx
  return z
 gl,gm=group(tl),group(tm);seeds=[]
 for a in sorted(set(gl)&set(gm)):
  for p,pi in gm[a].items():
   for q,qi in gl[a].items():
    A=np.zeros((D,d));da=len(qi)
    assert set(qi)==set(pi)
    for pre,x in qi.items():A[pi[pre],x]=math.sqrt(d/da)
    seeds.append(A)
 s=len(seeds);assert s
 tuples=list(itertools.permutations(range(k),j));L=len(tuples);ti={t:i for i,t in enumerate(tuples)}
 cos=[]
 for t in tuples:
  g=tuple(x for x in range(k) if x not in t)+t;cos.append(g)
 # Central class-sum on coset module. Defect2 shapes have distinct content eigenvalues.
 J=np.zeros((L,L))
 for a,b in itertools.combinations(range(k),2):
  for q,t in enumerate(tuples):
   tt=tuple(b if x==a else a if x==b else x for x in t);J[ti[tt],q]+=1
 ev,U=np.linalg.eigh(J);Z=np.zeros((L,L));selected=[]
 for nu in partitions(k):
  if nu[0]<k-j:continue
  h=fixed_h(nu,k,j);dn=dim(nu);mask=abs(ev-content(nu))<1e-7
  assert sum(mask)==h*dn
  Pro=U[:,mask]@U[:,mask].T;Z+=math.sqrt(dn/(L*h))*Pro;selected.append((nu,h,dn))
 cols=[]
 for g in cos:
  a=permrep(g,ul);b=permrep(g,um)
  for F in seeds:cols.append((b@F@a.T).reshape(-1)/math.sqrt(d))
 B=np.column_stack(cols);G=B@B.T;A=B@np.kron(Z,np.eye(s));AA=A@A.T
 eig=np.linalg.eigvalsh(AA);err=float(np.max(np.minimum(abs(eig),abs(eig-1))));assert err<1e-9
 # Full Hom conjugation central class sum, selected isotypic projection independently.
 JJ=np.zeros((D*d,D*d))
 for a,b in itertools.combinations(range(k),2):
  g=list(range(k));g[a],g[b]=g[b],g[a];vl=permrep(g,ul);vm=permrep(g,um);JJ+=np.kron(vm,vl)
 ee,V=np.linalg.eigh(JJ);wanted=np.zeros_like(JJ)
 for nu,h,dn in selected:
  vv=V[:,abs(ee-content(nu))<1e-7];wanted+=vv@vv.T
 err2=float(np.max(abs(AA-wanted)));assert err2<1e-9
 row={'lambda':lam,'mu':mu,'j':j,'d':d,'D':D,'L':L,'seed_count':s,'M':L*s,'reference_rank':int(sum(eig>.5)),'parseval_eigen_error':err,'full_isotypic_projector_entry_error':err2,'seed_max_norm':float(max(np.linalg.norm(x,2) for x in seeds)),'normalization_bound':math.sqrt(L*L*s)}
 rows.append(row);print(row,flush=True)
out={'status':'floating finite representation check; not QSVT or hardware execution','rows':rows,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(P/'orbit_frame_check_v1.json').write_text(json.dumps(out,indent=2)+'\n')
