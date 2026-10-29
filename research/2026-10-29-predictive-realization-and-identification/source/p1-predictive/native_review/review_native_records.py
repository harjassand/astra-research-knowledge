#!/usr/bin/env python3
"""Independent frozen-record review. No producer/consumer imports or redraw.

First reconstructs confidence/endpoints from public records. Only afterwards
constructs private truth independently for exact killed-equation comparison.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, permutations
import datetime, hashlib, json, math, time
import numpy as np

HERE=Path(__file__).resolve().parent
SRC=HERE.parent/'native_excursions'
EXPECTED={
 'NATIVE_EXCURSION_RECORD.json':'9b4a4c8c8fa00b3d9494ffa51be4ac30f8c48d00ff18cdbd9b8929973e4c3d3c',
 'NATIVE_EXCURSION_CERTIFICATE.json':'96b23d2b010d280332a737289b0420e7bf9af93d4263b6ac30a54a306423b9bf',
 'NATIVE_EXCURSION_RAW.npz':'89e32b56b02e73c82b11ca48dc64d089c1feb49295693d42a8dbbd8d0fac9490',
 'macro_run/NATIVE_EXCURSION_RECORD.json':'57d66dc6e6db1de046ce175c04db3ad6304a7999dbae1d569ac77dbd3f8f6df3',
 'macro_run/NATIVE_EXCURSION_CERTIFICATE.json':'9cb74b25688f20031158bbffec1d679e5acfd98c2605fd8d2a34ff1d818c05d8',
 'macro_run/NATIVE_EXCURSION_RAW.npz':'838157871d261d593c31b4ee7c4a251f16f81691667700a64311c0905d43e63f',
 'consume_excursion_record.py':'5842a87505c29c92db94a779446dc1676dddb5cfc4d50b686acd9d08686c73d8',
}

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def farray(a): return [[F(x) for x in row] for row in a]
def fvec(a): return list(map(F,a))
def dot(a,b): return sum((x*y for x,y in zip(a,b)),F())
def sub(a,rows):return [[a[i][j] for j in rows] for i in rows]

def ldlt_solve(a,b):
 n=len(b)
 if not n:return []
 low=[[F(i==j) for j in range(n)] for i in range(n)];diag=[]
 for j in range(n):
  dj=a[j][j]-sum(low[j][k]**2*diag[k] for k in range(j))
  assert dj>0,'grounded matrix not positive definite'
  diag.append(dj)
  for i in range(j+1,n):
   low[i][j]=(a[i][j]-sum(low[i][k]*diag[k]*low[j][k] for k in range(j)))/dj
 y=[]
 for i in range(n):y.append(b[i]-sum(low[i][j]*y[j] for j in range(i)))
 z=[y[i]/diag[i] for i in range(n)];x=[F()]*n
 for i in range(n-1,-1,-1):x[i]=z[i]-sum(low[j][i]*x[j] for j in range(i+1,n))
 assert all(dot(a[i],x)==b[i] for i in range(n))
 return x

def tree_interval(pl,pu):
 n=len(pl);lo=[F()]*n;hi=[F()]*n
 for edge_set in combinations(list(combinations(range(n),2)),n-1):
  graph=[[] for _ in range(n)]
  for i,j in edge_set:graph[i].append(j);graph[j].append(i)
  for root in range(n):
   parent={root:root};stack=[root]
   while stack:
    i=stack.pop()
    for j in graph[i]:
     if j not in parent:parent[j]=i;stack.append(j)
   if len(parent)!=n:continue
   a=b=F(1)
   for i in range(n):
    if i!=root:a*=pl[i][parent[i]];b*=pu[i][parent[i]]
   lo[root]+=a;hi[root]+=b
 return lo,hi

def all_simple_ratio_bounds(pl,pu):
 n=len(pl);rat=[[None]*n for _ in range(n)]
 for i in range(n):
  rat[i][i]=F(1)
  for j in range(n):
   if i==j:continue
   others=[k for k in range(n) if k not in [i,j]];candidates=[]
   for length in range(len(others)+1):
    for middle in permutations(others,length):
     path=(i,)+middle+(j,);p=F(1)
     for a,b in zip(path[:-1],path[1:]):
      if not pl[b][a]:break
      p*=pu[a][b]/pl[b][a]
     else:candidates.append(p)
   assert candidates
   rat[i][j]=min(candidates)
 return rat

def source_truth(m):
 # Independent incidence construction from the inspected private design.
 wb=[F(1),F(5,4),F(3,4),F(3,2)]+([F(1),F(9,8)] if m==6 else [])
 weights=wb+[F(1,2)]*(2*m);edges=[]
 for i in range(m):
  edges.append((i,(i+1)%m,F(1,8)))
  edges.extend((i,m+2*i+j,(weights[i]-F(1,4))/2) for j in range(2))
 if m==4:edges.extend((m+i,m+(i+1)%(2*m),F(1,16)) for i in range(2*m))
 else:
  for region in range(3):
   edges.extend((m+4*region+k,m+4*region+(k+1)%4,F(1,16)) for k in range(4))
 lap=[[F()]*(3*m) for _ in range(3*m)]
 for i,j,value in edges:
  lap[i][i]+=value;lap[j][j]+=value;lap[i][j]-=value;lap[j][i]-=value
 return weights,lap

def review_one(directory):
 record=json.loads((directory/'NATIVE_EXCURSION_RECORD.json').read_text())
 cert=json.loads((directory/'NATIVE_EXCURSION_CERTIFICATE.json').read_text())
 m=record['port_count'];assert m in (4,6) and cert['query_count']==2**m-1
 horizon=F(record['horizon']);scale=record['tick_scale']
 allowance=F(record['contracts']['timestamp_absolute_allowance'])
 assert horizon==24 and allowance==F(1,524288)
 raw=np.load(directory/'NATIVE_EXCURSION_RAW.npz',allow_pickle=False);raw_checks=[]
 for row in record['rows']:
  i=row['port'];ep=raw[f'endpoint_{i}'];ticks=raw[f'ticks_{i}'];n=row['n']
  assert ep.dtype==np.int16 and ticks.dtype==np.uint32
  assert len(ep)==len(ticks)==n
  assert np.all((ep>=-1)&(ep<m)) and np.all(ticks<=int(horizon)*scale)
  assert np.all(ticks[ep==-1]==int(horizon)*scale)
  counts=np.bincount(ep.astype(np.int64)+1,minlength=m+1).tolist()
  assert counts[0]==row['pending_count'] and counts[1:]==row['endpoint_counts']
  total=sum(map(int,ticks));squares=sum(int(x)**2 for x in ticks)
  assert total==int(row['sum_ticks']) and squares==int(row['sum_squared_ticks'])
  sha=hashlib.sha256(ep.tobytes()+ticks.tobytes()).hexdigest();assert sha==row['raw_sha256']
  raw_checks.append({'port':i,'n':n,'pending':counts[0],'array_sha256':sha})

 assert sum(F(3**j,math.factorial(j)) for j in range(9))>20
 failure=F(2*m*(m+2),160000);assert F(cert['failure_probability_upper'])==failure
 pl=farray(cert['P_lower']);pu=farray(cert['P_upper'])
 ul=fvec(cert['u_lower']);uu=fvec(cert['u_upper'])
 vl=fvec(cert['v_lower']);vu=fvec(cert['v_upper']);tail=F(1,160000)
 for i,row in enumerate(record['rows']):
  n=row['n'];bounds=cert['observation_bounds'][i]
  perr=F(bounds['endpoint_error']);r1=F(bounds['first_error']);r2=F(bounds['second_error'])
  assert perr>=0 and perr**2>=F(12,2*n)
  base1=r1-F(2)*horizon*12/(3*n)-allowance
  base2=r2-F(2)*horizon**2*12/(3*n)-2*horizon*allowance-allowance**2
  assert base1>=0 and base1**2>=F(192,n)
  assert base2>=0 and base2**2>=F(9216,n)
  ol=[max(F(),F(x,n)-perr) for x in row['endpoint_counts']]
  ou=[min(F(1),F(x,n)+perr+tail) for x in row['endpoint_counts']]
  assert sum(ol)<=1<=sum(ou)
  for j in range(m):
   feasible_lo=max(ol[j],1-sum(ou[k] for k in range(m) if k!=j))
   feasible_hi=min(ou[j],1-sum(ol[k] for k in range(m) if k!=j))
   assert pl[i][j]<=feasible_lo<=feasible_hi<=pu[i][j]
  mu1=F(int(row['sum_ticks']),n*scale);mu2=F(int(row['sum_squared_ticks']),n*scale**2)
  assert F(bounds['first_truncated_mean'])==mu1 and F(bounds['second_truncated_mean'])==mu2
  assert ul[i]==max(F(),mu1-r1) and uu[i]==mu1+r1+2*tail
  assert vl[i]==max(F(),mu2-r2) and vu[i]==mu2+r2+104*tail

 rat=all_simple_ratio_bounds(pl,pu);assert rat==farray(cert['stationary_ratio_upper'])
 if m==4:tree_lo,tree_hi=tree_interval(pl,pu)
 slo=[];shi=[]
 for i in range(m):
  lo=tree_lo[i]/(tree_lo[i]+sum(tree_hi[j] for j in range(m) if i!=j)) if m==4 else F()
  hi=tree_hi[i]/(tree_hi[i]+sum(tree_lo[j] for j in range(m) if i!=j)) if m==4 else F(1)
  slo.append(max(lo,1/(1+sum(rat[i][j] for j in range(m) if j!=i))))
  shi.append(min(hi,1/(1+sum(1/rat[j][i] for j in range(m) if j!=i))))
 assert slo==fvec(cert['stationary_event_lower']) and shi==fvec(cert['stationary_event_upper'])
 lower=[[F()]*m for _ in range(m)];upper=[[F()]*m for _ in range(m)]
 for i,j in combinations(range(m),2):
  lo=max(slo[i]*pl[i][j],slo[j]*pl[j][i]);hi=min(shi[i]*pu[i][j],shi[j]*pu[j][i]);assert 0<=lo<=hi
  for a,b in [(i,j),(j,i)]:lower[a][b]=-lo;upper[a][b]=-hi
  lower[i][i]+=lo;lower[j][j]+=lo;upper[i][i]+=hi;upper[j][j]+=hi
 assert lower==farray(cert['S_lower']) and upper==farray(cert['S_upper'])
 blo=[slo[i]*(1+ul[i]) for i in range(m)];bhi=[shi[i]*(1+uu[i]) for i in range(m)]
 clo=dot(slo,vl)/2;chi=dot(shi,vu)/2
 assert blo==fvec(cert['b_lower']) and bhi==fvec(cert['b_upper'])
 assert clo==F(cert['c_lower']) and chi==F(cert['c_upper'])
 reconstructed=[]
 for item in cert['queries']:
  target=item['target_ports'];r=[i for i in range(m) if i not in target]
  dlow=sum(slo[i] for i in r)+dot(slo,ul);dhigh=sum(shi[i] for i in r)+dot(shi,uu)
  b0=[blo[i] for i in r];b1=[bhi[i] for i in r]
  tl=(clo+dot(b0,ldlt_solve(sub(upper,r),b0)))/dhigh
  tu=(chi+dot(b1,ldlt_solve(sub(lower,r),b1)))/dlow
  assert tl==F(item['lower']) and tu==F(item['upper']) and tu/tl==F(item['factor'])
  reconstructed.append((target,tl,tu))
 assert len({tuple(a) for a,_,_ in reconstructed})==2**m-1
 macro_reconstructed=[]
 if m==6:
  groups=record['contracts']['module_ports'];assert groups==[[0,1],[2,3],[4,5]]
  assert record['contracts']['module_separation']=='Every cross-module edge has two resolved port endpoints; an interior excursion remains in its departure module.'
  for item in cert['macro_queries']:
   target=item['target_modules'];r=[i for j,g in enumerate(groups) if j not in target for i in g]
   cl=sum(slo[i]*vl[i] for i in r)/2;cu=sum(shi[i]*vu[i] for i in r)/2
   dl=sum(blo[i] for i in r);du=sum(bhi[i] for i in r)
   b0=[blo[i] for i in r];b1=[bhi[i] for i in r]
   tl=(cl+dot(b0,ldlt_solve(sub(upper,r),b0)))/du
   tu=(cu+dot(b1,ldlt_solve(sub(lower,r),b1)))/dl
   assert tl==F(item['lower']) and tu==F(item['upper']) and tu/tl==F(item['factor'])
   macro_reconstructed.append((target,tl,tu))
  assert len(macro_reconstructed)==6

 # Only after frozen public endpoint reconstruction: inspect exact private
 # design as an external truth control. It supplies no certificate narrowing.
 w,l=source_truth(m);wb=w[:m];wi=w[m:];li=sub(l,list(range(m,3*m)))
 t=ldlt_solve(li,wi);second=ldlt_solve(li,[2*wi[i]*t[i] for i in range(2*m)])
 absorption=[ldlt_solve(li,[-l[i][j] for i in range(m,3*m)]) for j in range(m)]
 s=[x/sum(wb) for x in wb];u=[];v=[];p=[]
 for i in range(m):
  assert l[i][i]/w[i]==1
  entry=[-l[i][k]/w[i] for k in range(m,3*m)]
  u.append(dot(entry,t));v.append(dot(entry,second))
  p.append([(-l[i][j]/w[i] if i!=j else F())+dot(entry,absorption[j]) for j in range(m)])
  assert sum(p[-1])==1
 for j in range(2*m):assert sum(-l[m+j][i] for i in range(m))/wi[j]>=F(1,2)
 for i in range(m):
  assert slo[i]<=s[i]<=shi[i] and ul[i]<=u[i]<=uu[i] and vl[i]<=v[i]<=vu[i]
  for j in range(m):assert pl[i][j]<=p[i][j]<=pu[i][j]
 actual_s=[[s[i]*(F(i==j)-p[i][j]) for j in range(m)] for i in range(m)]
 actual_b=[s[i]*(1+u[i]) for i in range(m)];actual_c=dot(s,v)/2
 assert actual_c==dot(wi,t)/sum(wb) and sum(actual_b)==sum(w)/sum(wb)
 for i,j in combinations(range(m),2):
  assert actual_s[i][j]==actual_s[j][i]
  assert -lower[i][j]<=-actual_s[i][j]<=-upper[i][j]
 truths=[]
 for target,tl,tu in reconstructed:
  comp=[i for i in range(3*m) if i not in target];wc=[w[i] for i in comp]
  exact=dot(wc,ldlt_solve(sub(l,comp),wc))/sum(wc)
  r=[i for i in range(m) if i not in target];br=[actual_b[i] for i in r]
  via=(actual_c+dot(br,ldlt_solve(sub(actual_s,r),br)))/(sum(actual_b)-sum(s[i] for i in target))
  assert exact==via and tl<=exact<=tu
  truths.append({'target_ports':target,'exact_mean':str(exact),'display':float(exact),'inside_released_interval':True})
 macro_truth=[]
 for target,tl,tu in macro_reconstructed:
  r=[i for i in range(m) if i//2 not in target]
  comp=r+[m+j for j in range(2*m) if j//4 not in target]
  wc=[w[i] for i in comp];exact=dot(wc,ldlt_solve(sub(l,comp),wc))/sum(wc)
  for j in range(2*m):
   for k in range(2*m):
    if j//4!=k//4:assert l[m+j][m+k]==0
   for i in range(m):
    if i//2!=j//4:assert l[m+j][i]==0
  br=[actual_b[i] for i in r];cr=sum(s[i]*v[i] for i in r)/2
  assert sum(br)==sum(wc)/sum(wb)
  via=(cr+dot(br,ldlt_solve(sub(actual_s,r),br)))/sum(br)
  assert exact==via and tl<=exact<=tu
  macro_truth.append({'target_modules':target,'exact_mean':str(exact),'display':float(exact),'inside_released_interval':True})
 maximum=max(tu/tl for _,tl,tu in reconstructed)
 outward=F(1384681,1000000) if m==4 else F(1702809,1000000)
 assert maximum<outward
 macro_max=max((tu/tl for _,tl,tu in macro_reconstructed),default=F())
 if m==6:assert macro_max<F(1700920,1000000)
 cost={key:sum(row['cost'][key] for row in record['rows']) for key in record['rows'][0]['cost']}
 ticktime=sum(F(int(row['sum_ticks']),scale) for row in record['rows'])
 timegap=cost['elapsed_native_time']-cost['initial_holding_time']-float(ticktime)
 assert -1e-7<=timegap<=sum(row['n'] for row in record['rows'])/scale+1e-7
 return {'ports':m,'raw_trials_verified':sum(r['n'] for r in record['rows']),
  'raw_checks':raw_checks,'confidence_failure_upper':str(failure),
  'confidence_event_count':m*(m+2),'exact_port_query_checks':truths,
  'exact_whole_region_query_checks':macro_truth,
  'maximum_factor_display':float(maximum),'outward_factor':str(outward),
  'macro_maximum_factor_display':float(macro_max),'macro_outward_factor':'212615/125000' if m==6 else None,
  'recorded_costs':cost,'native_time_minus_initial_and_ticks':timegap}

def main():
 start=time.perf_counter();receipts=[]
 for name,sha in EXPECTED.items():
  p=SRC/name;actual=digest(p);assert actual==sha,(name,actual)
  receipts.append({'path':name,'sha256':actual,'bytes':p.stat().st_size,
   'mtime_utc':datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()})
 results=[review_one(SRC),review_one(SRC/'macro_run')]
 first=json.loads((SRC/'first_consumer/NATIVE_EXCURSION_CERTIFICATE.json').read_text())
 firstmax=max(F(x['factor']) for x in first['queries'])
 assert results[0]['maximum_factor_display']<float(firstmax)
 assert all(digest(SRC/name)==sha for name,sha in EXPECTED.items())
 out={'status':'PASS at the stated conditional mathematical and synthetic scope',
  'frozen_inputs':receipts,'producer_or_consumer_imports':0,'source_sampling_calls':0,'RNG_calls':0,
  'results':results,'earlier_tree_only_factor_display':float(firstmax),
  'scope_limit':'Ideal independent native samples, exact port preparation, calibrated clocks, tail warranty, timestamp allowance and macro separator are supplied. PCG64/float source code is a synthetic implementation; review is not physical validation or a full distributional roundoff proof.',
  'wall_seconds':time.perf_counter()-start}
 (HERE/'NATIVE_RECORDS_INDEPENDENT_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':out['status'],'results':[{k:r[k] for k in ['ports','raw_trials_verified','confidence_failure_upper','maximum_factor_display','macro_maximum_factor_display','recorded_costs']} for r in results],
  'earlier_tree_only_factor_display':out['earlier_tree_only_factor_display'],'wall_seconds':out['wall_seconds']},indent=2))

if __name__=='__main__':main()
