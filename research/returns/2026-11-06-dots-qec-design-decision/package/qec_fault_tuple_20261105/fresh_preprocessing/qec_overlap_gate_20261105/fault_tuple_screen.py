"""Floating gate for a route-collapsed ordered-fault cover; no certificate yet."""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
ROOT=Path(__file__).resolve().parent

def run(d=13,D=20,N=64):
 ts=time.perf_counter();path=ROOT.parent/'canonical_qec_circuit_gate_20261105'/f'd{d}_r{d}_p1_1000_graph.json';G=json.loads(path.read_text());edges=G['edges'];cost=np.array(G['costs']);p=np.array([x['p_float'] for x in G['errors']]);nd=G['internal_vertices'];nv=max(max(e) for e in edges)+1
 rows=[];cols=[];data=[]
 for e,(u,v) in enumerate(edges):rows.extend((u,v));cols.extend((v,u));data.extend((cost[e],cost[e]))
 A=csr_matrix((data,(rows,cols)),shape=(nv,nv));Al=A[:nd,:nd]
 dl=dijkstra(A,directed=False,indices=G['left'],min_only=True);dr=dijkstra(A,directed=False,indices=G['right'],min_only=True);dl=dl.astype(int);dr=dr.astype(int)
 dist=dijkstra(Al,directed=False,limit=D-1);rr,cc=np.nonzero(dist<D);ds=dist[rr,cc].astype(np.int16);del dist;rr=rr.astype(np.int32);cc=cc.astype(np.int32)
 near=csr_matrix((np.ones(len(rr),dtype=np.int8),(rr,cc)),shape=(nd,nd));K=csr_matrix((np.exp2(-ds.astype(float))-2.**(-D),(rr,cc)),shape=(nd,nd));shell={int(k):csr_matrix((np.ones(np.sum(ds==k),dtype=np.int8),(rr[ds==k],cc[ds==k])),shape=(nd,nd)) for k in sorted(set(ds))}
 L=set(G['left']);R=set(G['right']);B={};starts=[]
 for c in sorted(set(cost)):
  br=[];bc=[];bv=[]
  for e,(u,v) in enumerate(edges):
   if cost[e]!=c:continue
   for x,y in [(u,v),(v,u)]:
    if x not in R and y not in L:starts.append((x,y,e,int(c-dl[x])))
    if x<nd and y not in L:br.append(x);bc.append(y);bv.append(p[e]*2.**c)
  B[int(c)]=csr_matrix((bv,(br,bc)),shape=(nd,nv))
 def Kapply(j):return K@j+2.**(-D)*np.sum(j,axis=0)
 v=np.ones(nv);v[nd:]=0;rho=0.
 for it in range(500):
  j=sum(M@v for M in B.values());vv=np.zeros(nv);vv[:nd]=Kapply(j);rho=float(np.max(vv));vv/=rho
  err=np.max(abs(vv-v));v=vv
  if err<1e-11:break
 result={'scope':'floating feasibility only','distance':d,'cut_distance':D,'modulus':N,'vertices':nv,'internal_vertices':nd,'near_pairs':len(rr),'distance_shells':list(shell),'spectral_radius_diagnostic':rho,'spectral_iterations':it+1,'setup_seconds':time.perf_counter()-ts}
 if rho>=.999:
  result['gate']='scalar contraction fails this screen';print(json.dumps(result,indent=2));(ROOT/f'fault_tuple_screen_d{d}_D{D}_N{N}.json').write_text(json.dumps(result,indent=2)+'\n');return
 del K
 residues=np.arange(N);base=np.zeros((nv,N));base[:nd]=np.exp2(-dr[:nd,None].astype(float))*np.exp2(-((residues[None,:]-dr[:nd,None])%N).astype(float));base[list(R)]=np.exp2(-residues.astype(float));H=base.copy()
 for it in range(500):
  j=sum(M@np.roll(H,-c,axis=1) for c,M in B.items());new=base.copy();jD=np.roll(j,D,axis=1)
  new[:nd]+=2.**(-D)*(np.sum(jD,axis=0)[None,:]-near@jD)
  for k,M in shell.items():new[:nd]+=2.**(-k)*(M@np.roll(j,k,axis=1))
  err=float(np.max(abs(new-H)));H=new
  if err<1e-19:break
 Z=sum(p[e]*2.**s*H[y,s%N] for x,y,e,s in starts)
 result.update({'folded_normalizer':float(Z),'folded_iterations':it+1,'last_absolute_update':err,'total_seconds':time.perf_counter()-ts,'raw_table_bytes':H.nbytes,'gate':'finite positive scalar screen'})
 np.savez_compressed(ROOT/f'fault_tuple_float_d{d}_D{D}_N{N}.npz',H=H,dl=dl,dr=dr,near_rows=rr,near_cols=cc,near_distances=ds,states=starts)
 (ROOT/f'fault_tuple_screen_d{d}_D{D}_N{N}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--distance',type=int,default=13);a.add_argument('--cut-distance',type=int,default=20);a.add_argument('--modulus',type=int,default=64);v=a.parse_args();run(v.distance,v.cut_distance,v.modulus)
