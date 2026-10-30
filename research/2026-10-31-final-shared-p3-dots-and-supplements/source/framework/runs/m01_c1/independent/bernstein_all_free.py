"""Exact compact-chart Bernstein certificate for arbitrary output polarizations."""
import sys,json,itertools,math,time
sys.dont_write_bytecode=True
from fractions import Fraction as F
from pathlib import Path
here=Path(__file__).parent
raw=json.loads((here/'all_free.json').read_text());groups={}
for m,c in raw:
 key=(m[0]+m[1],m[2]+m[3],m[4]+m[5])
 if min(key)>0:groups.setdefault(key,[]).append((m,F(c)))
cache={}
def Bmat(d):
 if d in cache:return cache[d]
 mat=[[sum((F((-1)**(k-j)*2**j*math.comb(k,j)*math.comb(i,j),math.comb(d,j)) for j in range(min(k,i)+1)),F(0)) for i in range(d+1)] for k in range(d+1)]
 cache[d]=mat;return mat

def init(terms,chart,key):
 deg=key;inds=list(itertools.product(*(range(d+1) for d in deg)));bs=[F(0) for _ in inds]; mats=[Bmat(d) for d in deg]
 for m,c in terms:
  powers=[m[2*j+chart[j]] for j in range(3)]
  for n,idx in enumerate(inds):
   cc=c
   for j in range(3):cc*=mats[j][powers[j]][idx[j]]
   bs[n]+=cc
 return deg,bs

def split(deg,bs,axis):
 shape=[d+1 for d in deg];strides=[shape[1]*shape[2],shape[2],1];left=bs.copy();right=bs.copy();other=[j for j in range(3) if j!=axis]
 for coords in itertools.product(*(range(shape[j]) for j in other)):
  base=sum(coords[k]*strides[other[k]] for k in range(2));ids=[base+i*strides[axis] for i in range(shape[axis])];row=[bs[i] for i in ids];ll=[row[0]];rr=[row[-1]]
  while len(row)>1:
   row=[(a+b)/2 for a,b in zip(row,row[1:])];ll.append(row[0]);rr.append(row[-1])
  for idx,vv in zip(ids,ll):left[idx]=vv
  for idx,vv in zip(ids,reversed(rr)):right[idx]=vv
 return left,right

def certify(deg,bs):
 queue=[('',bs,(0,0,0))];leaves=[];visited=0
 while queue:
  path,coeff,depth=queue.pop();visited+=1
  if min(coeff)>=0:leaves.append((path,str(min(coeff))));continue
  if max(depth)>=14 or visited>200000:raise RuntimeError(('unresolved',path,min(coeff),len(queue)))
  axis=min(range(3),key=lambda j:(depth[j]/max(deg[j],1),j));dd=list(depth);dd[axis]+=1;L,R=split(deg,coeff,axis)
  queue.append((path+str(axis)+'1',R,tuple(dd)));queue.append((path+str(axis)+'0',L,tuple(dd)))
 return leaves,visited

if __name__=='__main__':
 result=[];start=time.time()
 for key,terms in sorted(groups.items()):
  for chart in itertools.product([0,1],repeat=3):
   deg,bs=init(terms,chart,key);leaves,visited=certify(deg,bs)
   result.append({'degree':list(key),'chart':list(chart),'leaves':leaves})
   print(key,chart,'leaves',len(leaves),'visited',visited,'elapsed',round(time.time()-start,2),flush=True)
 (here/'all_free_bernstein_certificate.json').write_text(json.dumps(result))
 print('ALL CHARTS CERTIFIED',len(result),'LEAVES',sum(len(r['leaves']) for r in result),'time',time.time()-start,flush=True)
