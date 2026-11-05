"""Independent graph, distance-potential, normalizer and full-row audit."""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json, subprocess, time
import numpy as np

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--distance',type=int,default=13)
args=parser.parse_args();started=time.perf_counter()
folder=ROOT.parent/'qec_design_direct_20261105'/'qec_fault_tuple_20261105'/f'd{args.distance}'
meta=json.loads((folder/'parameters.json').read_text());G=json.loads((folder/'input_graph.json').read_text())
assert hashlib.sha256((folder/'input_graph.json').read_bytes()).hexdigest()==meta['source_sha256']
for name,h in meta['sha256'].items(): assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==h
nd,nv,N,D,Q,qden=(meta[k] for k in ['nd','nv','N','D','Q','qden'])
assert nd==G['internal_vertices'] and N==64 and qden==64 and 0<D<=64 and Q<=63
assert nv==1+max(max(edge) for edge in G['edges']) and nd<nv<1000000
edges=np.array(G['edges'],dtype=np.uint32);m=len(edges)
assert m==len(G['costs'])==len(G['errors']) and all(0<c<=15 for c in G['costs'])
cost=np.array(G['costs'],dtype=np.uint8)
side=np.zeros(nv,dtype=np.uint8);side[G['left']]=1;side[G['right']]=2
assert set(G['left']).isdisjoint(G['right']) and all(x>=nd for x in G['left']+G['right'])
assert set(G['left']+G['right'])==set(range(nd,nv))
degree=np.bincount(edges.ravel(),minlength=nv);assert np.all(degree[nd:]==1)
q=[];bias=F(0)
for e in G['errors']:
    p=F(e['p_mid']);radius=F(e['p_radius']);assert 0<p<1 and 0<=radius<min(p,1-p)
    integer=(p*(1<<qden)+F(1,2)).numerator//(p*(1<<qden)+F(1,2)).denominator
    q.append(integer);bias+=abs(p-F(integer,1<<qden))+radius
assert q==meta['q_numerators'] and bias==F(meta['conversion_TV_upper_exact'])
dl=np.array(meta['dl'],dtype=np.int64);dr=np.array(meta['dr'],dtype=np.int64)
assert len(dl)==len(dr)==nv and min(dl)>=0 and min(dr)>=0 and max(dl)<65536 and max(dr)<65536
assert max(dl)==meta['dlmax'] and np.all(dl[G['left']]==0) and np.all(dr[G['right']]==0)
distance=np.load(folder/'distance.npy');U=np.load(folder/'U.npy');Jlo=np.load(folder/'J_lo.npy');Jhi=np.load(folder/'J_hi.npy')
assert distance.shape==(nd,nd) and U.shape==(nv,N) and Jlo.shape==Jhi.shape==(nd,N)
assert distance.dtype==np.uint8 and U.dtype==Jlo.dtype==Jhi.dtype==np.uint64
assert np.all(distance<=D) and np.all(distance.diagonal()==0) and np.array_equal(distance,distance.T)
assert np.all(U>0)
potential_checks=0
for (u,v),c in zip(edges,G['costs']):
    u,v,c=int(u),int(v),int(c)
    assert abs(int(dl[u])-int(dl[v]))<=c and abs(int(dr[u])-int(dr[v]))<=c
    if u<nd and v<nd:
        # For every target x, the stored distance is an admissible potential:
        # d(v,x)<=c(v,u)+d(u,x). Chaining along a real clean segment proves
        # lower-bound validity without trusting the floating shortest paths.
        assert np.all(np.abs(distance[u].astype(np.int16)-distance[v].astype(np.int16))<=c)
        potential_checks+=2*nd

starts=[];Z=F(0)
for e,(u,v) in enumerate(edges):
    for x,y in [(int(u),int(v)),(int(v),int(u))]:
        if side[x]==2 or side[y]==1: continue
        score=G['costs'][e]-int(dl[x]);starts.append([x,y,e,score])
        Z+=F(q[e],1<<qden)*F(2)**score*F(int(U[y,score%N]),1<<Q)
assert np.array_equal(np.array(starts,dtype=np.int64),np.load(folder/'starts.npy'))
assert Z==F(meta['Z_exact'])

audit_input=ROOT/f'd{args.distance}_independent_input.bin'
with audit_input.open('wb') as f:
    np.array([nv,nd,m,N,D,Q,qden],dtype=np.uint64).tofile(f)
    for a in [edges[:,0].copy(),edges[:,1].copy(),cost,np.array(q,dtype=np.uint64),
              dl.astype(np.uint16),dr.astype(np.uint16),side,distance,U,Jlo,Jhi]:a.tofile(f)
exe=ROOT/'check_rows'
subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'check_rows.cpp'),'-o',str(exe)],check=True)
check=subprocess.run([str(exe),str(audit_input)],check=True,capture_output=True,text=True)
receipt=json.loads(check.stdout)
out=dict(status='PASS: independent full-denominator certificate and admissible distance proofs',
         distance=args.distance,source_sha256=meta['source_sha256'],rows=receipt,
         interior_distance_potential_inequalities=potential_checks,boundary_potential_edges=2*m,
         exact_normalizer=str(Z),exact_conversion_TV=str(bias),
         copied_input_hashes=meta['sha256'],elapsed_seconds=time.perf_counter()-started)
(ROOT/f'd{args.distance}_certificate_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
