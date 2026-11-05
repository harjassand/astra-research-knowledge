"""Independent finite checks: sphere pairing, routed insertion, and AKLT PEPS.
Exact fractions for both classical expansions; independent floating quantum state.
"""
from fractions import Fraction as F
from itertools import product,combinations
from collections import defaultdict
from pathlib import Path
import json,sys,math,time
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'square_aklt_boundary_operation_20261105'))
from open_trail_sampler import suppression,true_contact_count,edge
from exact_loop_birth_sampler import canonical
from crossed_loop_influence import variants

def grid_graph(w,h):
 V=[(x,y) for x in range(w) for y in range(h)];idx={v:i for i,v in enumerate(V)}
 E=[]
 for x,y in V:
  for dx,dy in [(1,0),(0,1)]:
   if(x+dx,y+dy) in idx:E.append((idx[x,y],idx[x+dx,y+dy]))
 return V,E

def pairings(es):
 if not es:return [()]
 if len(es)==2:return [((es[0],es[1]),)]
 assert len(es)==4
 a,b,c,d=es
 return [((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))]

def sphere_partition(n,E,source=None):
 total=F(0);terms=0
 for mask in range(1<<len(E)):
  selected=[e for k,e in enumerate(E) if(mask>>k)&1]
  if source is not None:selected.append(source)
  inc=[[] for _ in range(n)]
  for k,(a,b) in enumerate(selected):inc[a].append(k);inc[b].append(k)
  ds=list(map(len,inc))
  if any(d not in(0,2,4) for d in ds):continue
  den=3**ds.count(2)*15**ds.count(4)
  for routing in product(*(pairings(x) for x in inc)):
   parent=list(range(len(selected)))
   def find(x):
    while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
    return x
   for local in routing:
    for a,b in local:parent[find(a)]=find(b)
   cycles=len({find(k) for k in range(len(selected))})
   total+=F(3**cycles,den);terms+=1
 return total,terms

def quantum_vbs(n,E):
 deg=[0]*n
 for i,j in E:deg[i]+=1;deg[j]+=1
 shape=tuple(d+1 for d in deg);psi=np.zeros(math.prod(shape))
 stride=[math.prod(shape[i+1:]) for i in range(n)]
 for mask in range(1<<len(E)):
  k=[0]*n
  for e,(i,j) in enumerate(E):
   b=(mask>>e)&1;k[i]+=b;k[j]+=1-b
  a=(-1.0 if mask.bit_count()%2 else 1.0)
  for d,x in zip(deg,k):a/=math.sqrt(math.comb(d,x))
  psi[sum(x*s for x,s in zip(k,stride))]+=a
 psi/=np.linalg.norm(psi)
 coords=np.indices(shape).reshape(n,-1);indices=np.arange(len(psi))
 def corr(i,j):
  ki,kj=coords[i],coords[j];di,dj=deg[i],deg[j]
  diagonal=np.dot(psi*psi,(di/2-ki)*(dj/2-kj))
  valid=(ki>0)&(kj<dj)
  dest=indices[valid]-stride[i]+stride[j]
  coef=np.sqrt(ki[valid]*(di-ki[valid]+1)*(kj[valid]+1)*(dj-kj[valid]))
  return float(diagonal+np.dot(psi[valid]*psi[dest],coef))
 def quad(i,j):
  si,sj=deg[i]/2,deg[j]/2
  qi=(si-coords[i])**2-si*(si+1)/3
  qj=(sj-coords[j])**2-sj*(sj+1)/3
  return float(np.dot(psi*psi,qi*qj))
 corr.quadrupole=quad
 return corr,deg,len(psi)

def loop_configs(w,h):
 cat=json.loads((ROOT/'square_aklt_loop_audit_20261105/loop_catalog_through12.json').read_text());loops={}
 for item in cat:
  for p in variants(item['cyclic_vertices']):
   mx=max(x for x,y in p);my=max(y for x,y in p)
   for dx in range(w-mx):
    for dy in range(h-my):loops[canonical([(x+dx,y+dy) for x,y in p])]=F(item['activity'])
 items=list(loops.items());out=[]
 def rec(i,chosen,weight):
  if i==len(items):out.append((tuple(chosen),weight));return
  rec(i+1,chosen,weight)
  route,a=items[i];closedpath=tuple(route)+(route[0],)
  fac=suppression(closedpath,chosen)
  if fac:rec(i+1,chosen+[route],weight*a*fac)
 rec(0,[],F(1));return out

def path_expansion(w,h,root,configs):
 neighbors={}
 for x in range(w):
  for y in range(h):neighbors[x,y]=[(x+dx,y+dy) for dx,dy in[(1,0),(0,1),(-1,0),(0,-1)] if 0<=x+dx<w and 0<=y+dy<h]
 Z=sum(a for c,a in configs);sums=defaultdict(F);bare=defaultdict(F);counts=defaultdict(int);revisit=0
 def rec(vs,used):
  nonlocal revisit
  if len(vs)>1 and vs[-1]!=root:
   p=tuple(vs);r=true_contact_count(p);a=F(1,3)**len(used)*F(3,5)**r
   avg=sum(weight*suppression(p,loops) for loops,weight in configs)/Z
   sums[p[-1]]+=a*avg;bare[p[-1]]+=a;counts[p[-1]]+=1
   if vs.count(root)>1 or vs.count(vs[-1])>1:revisit+=1
  for p in neighbors[vs[-1]]:
   e=edge(vs[-1],p)
   if e not in used:rec(vs+[p],used|{e})
 rec([root],set());return sums,bare,counts,revisit

def main():
 start=time.monotonic();V,E=grid_graph(3,3);Z,zt=sphere_partition(9,E)
 qc,deg,dim=quantum_vbs(9,E)
 results=[];maxerr=0
 for i,j in combinations(range(9),2):
  num,nt=sphere_partition(9,E,(i,j));G=num/Z
  sign=(-1)**(sum(V[i])+sum(V[j]));expected=sign*F(deg[i]+2,2)*F(deg[j]+2,2)*G
  observed=qc(i,j);err=abs(observed-float(expected));maxerr=max(maxerr,err)
  assert err<2e-12,(i,j,expected,observed)
  results.append({'i':V[i],'j':V[j],'classical_staggered_G':str(G),'quantum_expected':str(expected),'quantum_direct':observed})
 configs=loop_configs(3,3);assert sum(a for c,a in configs)==Z
 root=(1,1);ps,bare,counts,revisits=path_expansion(3,3,root,configs)
 for j,v in enumerate(V):
  if v==root:continue
  num,_=sphere_partition(9,E,(V.index(root),j));assert ps[v]==num/Z,(v,ps[v],num/Z)
 # Spin2 open-boundary identity-mixture purification:2x2cores,2ancillaleaves/core.
 V2,E2=grid_graph(2,2);fullE=E2[:]
 for core in range(4):
  fullE.extend([(core,4+2*core),(core,5+2*core)])
 qc2,d2,dim2=quantum_vbs(12,fullE);Z2,_=sphere_partition(4,E2);decor=[];quad=[]
 configs2=loop_configs(2,2)
 for i,j in combinations(range(4),2):
  num,_=sphere_partition(4,E2,(i,j));expected=(-1)**(sum(V2[i])+sum(V2[j]))*9*num/Z2
  got=qc2(i,j);assert abs(got-float(expected))<2e-12
  qexpected=F(0)
  for loops,weight in configs2:
   mi=[route.count(V2[i]) for route in loops];mj=[route.count(V2[j]) for route in loops]
   y=F(98*sum(a*b for a,b in zip(mi,mj)),(2*sum(mi)+3)*(2*sum(mj)+3))
   qexpected+=weight*y/Z2
  qgot=qc2.quadrupole(i,j);assert abs(qgot-float(qexpected))<2e-12,(i,j,qgot,qexpected)
  quad.append({'i':V2[i],'j':V2[j],'exact_closed_loop_estimator':str(qexpected),'direct_purified_VBS':qgot})
  decor.append({'i':V2[i],'j':V2[j],'expected_spin2_correlation':str(expected),'direct_purified_VBS':got})
 out={'classical_exact_3x3_Z':str(Z),'exact_loop_configuration_count':len(configs),'variable_degree_quantum_dimension':dim,'all_36_pairs_verified':True,'largest_quantum_float_error':maxerr,'root_open_path_counts':{str(k):v for k,v in counts.items()},'endpoint_revisit_paths_checked':revisits,'all_8_root_path_decompositions_exact':True,'root_bare_path_masses':{str(k):str(v) for k,v in bare.items()},'spin2_identity_boundary_purification_dimension':dim2,'spin2_identity_boundary_pairs':decor,'spin2_quadrupole_pairs':quad,'pair_results':results,'elapsed_seconds':time.monotonic()-start,'scope':'Exact Fraction sphere-pairing and routed-path identities. Independent quantum amplitudes evaluated in binary64. Open rectangle with explicit virtual-identity boundary mixture for spin2check.'}
 (HERE/'identity_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k not in('pair_results','spin2_identity_boundary_pairs','spin2_quadrupole_pairs')},indent=2))
if __name__=='__main__':main()
