"""Root direct-limit certificate, exact Green/coarse solves + checked resolvents.

Finite input-only prototype. No permutation enumeration, finite boost, mixing
tail, acquired code, or floating acceptance. Same-team Erlang library is pinned.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import importlib.util,json,hashlib,time,resource,argparse
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ge_erlang_snapshot',HERE/'DEPENDENCY_erlang_certificate.v0001.py')
lib=importlib.util.module_from_spec(spec);spec.loader.exec_module(lib)

class GreenLDL:
 def __init__(self,rows):
  self.rows=rows;n=len(rows);a=[{j:F(x) for j,x in row.items() if j>=i} for i,row in enumerate(rows)];self.cols=[];self.diag=[]
  for i in range(n):
   pivot=a[i][i];assert pivot>0
   self.diag.append(pivot);ns=sorted(j for j,x in a[i].items() if j>i and x);c={j:a[i][j]/pivot for j in ns};self.cols.append(c)
   for k,j in enumerate(ns):
    for ell in ns[k:]:
     v=a[j].get(ell,F(0))-c[j]*a[i][ell]
     if v:a[j][ell]=v
     else:a[j].pop(ell,None)
   a[i].clear()
 def solve(self,b):
  u=list(map(F,b))
  for i,c in enumerate(self.cols):
   for j,v in c.items():u[j]-=v*u[i]
  x=[u[i]/self.diag[i] for i in range(len(u))]
  for i in reversed(range(len(u))):x[i]-=sum((v*x[j] for j,v in self.cols[i].items()),F(0))
  assert all(sum((v*x[j] for j,v in row.items()),F(0))==b[i] for i,row in enumerate(self.rows))
  assert all(v>=0 for v in x)
  return x

def solve_dense(a,b):
 n=len(b);a=[list(map(F,row))+[F(b[i])] for i,row in enumerate(a)]
 for i in range(n):
  pivot=next(j for j in range(i,n) if a[j][i]);a[i],a[pivot]=a[pivot],a[i];v=a[i][i];a[i]=[x/v for x in a[i]]
  for j in range(n):
   if j!=i:
    v=a[j][i]
    if v:a[j]=[x-v*y for x,y in zip(a[j],a[i])]
 return [row[-1] for row in a]

def components(n,edges,a):
 adj=[[] for _ in range(n)]
 for (x,y),v in zip(edges,a):
  assert v>=0
  if v:adj[x].append(y);adj[y].append(x)
 seen=set();out=[]
 for v in range(n):
  if v in seen:continue
  c=[];todo=[v];seen.add(v)
  while todo:
   x=todo.pop();c.append(x)
   for y in adj[x]:
    if y not in seen:seen.add(y);todo.append(y)
  out.append(sorted(c))
 return out

def certify(n,edges,r,a,shape=16,shift=20,precision=205):
 start=time.perf_counter();cpu=time.process_time();edges=[tuple(sorted(e)) for e in edges];assert len(set(edges))==len(edges);assert len(edges)==len(r)==len(a);assert shape>=2 and shift>0
 original,indices=lib.pair_matrix(n,edges,r);blocks=components(n,edges,a);owner={v:i for i,c in enumerate(blocks) for v in c};bc=list(combinations(range(len(blocks)),2));bi={c:i for i,c in enumerate(bc)}
 b=[ri if ai==0 else 0 for ri,ai in zip(r,a)];w=[[F(0) for _ in blocks] for _ in blocks]
 for (x,y),v in zip(edges,b):
  i,j=owner[x],owner[y]
  if i!=j:w[i][j]+=v;w[j][i]+=v
 beta=[[w[i][j]/len(blocks[i]) for j in range(len(blocks))] for i in range(len(blocks))]
 K=[[F(0) for _ in bc] for _ in bc]
 for z,(i,j) in enumerate(bc):
  K[z][z]=sum(beta[i])+sum(beta[j])
  for u,v in [(i,j),(j,i)]:
   for dest,rate in enumerate(beta[u]):
    if dest!=v and dest!=u and rate:K[z][bi[tuple(sorted((dest,v)))]]-=rate
 fast_ids=[i for i,x in enumerate(a) if x];h={};G={};green_receipts=[]
 for ci,c in enumerate(blocks):
  if len(c)<2:continue
  local={x:i for i,x in enumerate(c)};ce=[(local[x],local[y]) for (x,y),v in zip(edges,a) if v and owner[x]==ci];ca=[v for (x,y),v in zip(edges,a) if v and owner[x]==ci];rows,_=lib.pair_matrix(len(c),ce,ca);lp=list(combinations(c,2));li={p:i for i,p in enumerate(lp)};fac=GreenLDL(rows);hs=fac.solve([1]*len(rows));exits=[]
  for z in bc:
   rhs=[F(0)]*len(rows)
   if ci in z:
    dest=z[1] if z[0]==ci else z[0]
    for pi,(x,y) in enumerate(lp):rhs[pi]=sum(F(v) for (u,t),v in zip(edges,b) if (u in (x,y) and owner[t]==dest) or (t in (x,y) and owner[u]==dest))
   exits.append(fac.solve(rhs))
  for ei in fast_ids:
   if owner[edges[ei][0]]==ci:
    pi=li[edges[ei]];h[ei]=hs[pi];G[ei]=[xs[pi] for xs in exits]
  green_receipts.append({'vertices':c,'pair_states':len(rows),'factor_entries':len(rows)+sum(len(x) for x in fac.cols),'exact_residuals_zero':True})
 hist,fr,res,witness=lib.solve_history(original,[indices[i] for i in fast_ids],shape,shift,precision)
 qhist=[];v=[F(1)]*len(bc);mat=[[F(int(i==j))+K[i][j]/shift for j in range(len(bc))] for i in range(len(bc))]
 for j in range(1,shape):
  v=solve_dense(mat,v) if bc else [];assert all(0<=x<=1 for x in v);qhist.append(v)
 atom=sum(F(a[ei])*h[ei]*hist[shape-2][1][ii] for ii,ei in enumerate(fast_ids))*shift/(shape-1)
 boundary=F(0)
 for j in range(1,shape):
  u=hist[j-1][1];v=qhist[shape-j-1]
  boundary+=sum(F(a[ei])*u[ii]*sum((g*x for g,x in zip(G[ei],v)),F(0)) for ii,ei in enumerate(fast_ids))/(shape-1)
 cdf,terms=lib.gamma_cdf_lower(shape,shift);bound=(atom+boundary)/cdf
 return {'method':'direct exact averaged endpoint via positive Green/coarse/Erlang certificate','n':n,'edges':edges,'original_rates':r,'fast_design_rates':a,'actual_fast_components':blocks,'shape':shape,'shift':shift,'precision':precision,'green_receipts':green_receipts,'h':{str(edges[i]):str(h[i]) for i in fast_ids},'G':{str(edges[i]):list(map(str,G[i])) for i in fast_ids},'coarse_K':[[str(x) for x in row] for row in K],'coarse_pair_states':len(bc),'original_pair_states':len(original),'atom_average_upper_exact':str(atom),'boundary_average_upper_exact':str(boundary),'gamma_cdf_lower_exact':str(cdf),'direct_average_TV_upper_exact':str(bound),'direct_average_TV_upper_display':float(bound),'direct_average_certified_at_005':bound<=F(1,20),'finite_boost':None,'boosted_generator_mixing_tail':None,'original_factor_receipt':fr,'residual_receipts':res,'dyadic_original_solve_witnesses':witness,'coarse_resolvent_history':[[str(x) for x in v] for v in qhist],'wall_seconds':time.perf_counter()-start,'local_process_cpu_seconds':time.process_time()-cpu,'peak_process_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Internal exact finite certificate under direct-limit theorem; no physical model, novelty or broad superiority validation.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--case',choices=['path6','path12','path20','branch6','dimer','bad_partition'],default='path6');p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 if args.case.startswith('path'):
  n=int(args.case[4:]);edges=[(i,i+1) for i in range(n-1)];r=[10**i for i in range(n-1)];a=[0,0]+[1]*(n-3)
 elif args.case=='branch6':n=6;edges=[(0,1),(1,2),(2,3),(2,4),(2,5)];r=[1,10,100,1000,10000];a=[0,0,1,1,1]
 elif args.case=='bad_partition':n=6;edges=[(0,1),(1,2),(2,3),(2,4),(3,4)];r=[1,10,10**6,10**6,10**6];a=[0,0,1,1,1]
 else:n=3;edges=[(0,1),(1,2)];r=[0,1];a=[1,0]
 v=certify(n,edges,r,a);v['case']=args.case;v['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();args.output.write_text(json.dumps(v,indent=2)+'\n');print(json.dumps({k:v[k] for k in ['case','actual_fast_components','direct_average_TV_upper_display','direct_average_certified_at_005','wall_seconds','local_process_cpu_seconds']}))
if __name__=='__main__':main()
