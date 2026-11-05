"""Propose a table numerically; verify a conservative exact integer supersolution."""
import argparse,hashlib,json,shutil,subprocess,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
ROOT=Path(__file__).resolve().parent

def build(d=13,D=64,N=64):
 ts=time.perf_counter();out=ROOT/f'd{d}';out.mkdir(exist_ok=True);src=ROOT.parent/'canonical_qec_circuit_gate_20261105'/f'd{d}_r{d}_p1_1000_graph.json';G=json.loads(src.read_text());shutil.copy2(src,out/'input_graph.json')
 a=np.load(ROOT.parent/'qec_overlap_gate_20261105'/f'fault_tuple_float_d{d}_D{D}_N{N}.npz');H=a['H'];dl=a['dl'].astype(np.uint16);dr=a['dr'].astype(np.uint16);rr=a['near_rows'];cc=a['near_cols'];ds=a['near_distances'];nd=G['internal_vertices'];nv=len(dl);m=len(G['edges']);Q=56;den=1<<64
 side=np.zeros(nv,dtype=np.uint8);side[G['left']]=1;side[G['right']]=2;edges=np.array(G['edges'],dtype=np.uint32);cost=np.array(G['costs'],dtype=np.uint8);q=[];bias=F(0)
 for e in G['errors']:
  p=F(e['p_mid']);k=(2*p.numerator*den//p.denominator+1)//2;q.append(k);bias+=abs(F(k,den)-p)+F(e['p_radius'])
 dist=np.full((nd,nd),D,dtype=np.uint8);dist[rr,cc]=ds
 K=csr_matrix((np.exp2(-ds.astype(float))-2.**(-D),(rr,cc)),shape=(nd,nd));br=[];bc=[];bv=[]
 for e,(u,v) in enumerate(edges):
  for x,y in [(u,v),(v,u)]:
   if x<nd and side[y]!=1:br.append(x);bc.append(y);bv.append((q[e]/den)*2.**int(cost[e]))
 B=csr_matrix((bv,(br,bc)),shape=(nd,nv));v=np.ones(nv)
 for _ in range(200):
  j=B@v;new=np.ones(nv);new[:nd]+=K@j+2.**(-D)*j.sum();v=new
 W=np.ceil(4*v).astype(np.uint64);del K,B
 U=np.ceil(H*2.**Q).astype(np.uint64);binary=out/'certificate_input.bin'
 with binary.open('wb') as f:
  np.array([nv,nd,m,N,D,Q,16],dtype=np.uint64).tofile(f)
  for x in [edges[:,0].copy(),edges[:,1].copy(),cost,np.array(q,dtype=np.uint64),dl,dr,side,dist,W,U]:x.tofile(f)
 subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'certify_tuple.cpp'),'-o',str(ROOT/'certify_tuple')],check=True)
 r=subprocess.run([str(ROOT/'certify_tuple'),str(binary),str(out/'verified')],check=True,capture_output=True,text=True);receipt=json.loads(r.stdout)
 U=np.fromfile(out/'verified_U.bin',dtype=np.uint64).reshape(nv,N);jlo=np.fromfile(out/'verified_Jlo.bin',dtype=np.uint64).reshape(nd,N);jhi=np.fromfile(out/'verified_Jhi.bin',dtype=np.uint64).reshape(nd,N)
 dlmax=int(max(dl));Znum=0;starts=[]
 for e,(u,v) in enumerate(edges):
  for x,y in [(int(u),int(v)),(int(v),int(u))]:
   if side[x]!=2 and side[y]!=1:
    s=int(cost[e])-int(dl[x]);w=q[e]*(1<<(int(cost[e])+dlmax-int(dl[x])))*int(U[y,s%N]);Znum+=w;starts.append([x,y,e,s])
 Z=F(Znum,1<<(64+Q+dlmax))
 for name,array in [('U',U),('J_lo',jlo),('J_hi',jhi),('distance',dist),('W',W),('starts',np.array(starts,dtype=np.int64))]:np.save(out/(name+'.npy'),array)
 meta={'scope':'exact rounded graph law with explicit conversion TV; no new sampling result yet','distance':d,'N':N,'D':D,'Q':Q,'qden':64,'nd':nd,'nv':nv,'q_numerators':q,'dl':dl.tolist(),'dr':dr.tolist(),'dlmax':dlmax,'Z_exact':str(Z),'Z_float':float(Z),'conversion_TV_upper_exact':str(bias),'conversion_TV_upper':float(bias),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'certificate':receipt,'build_seconds':time.perf_counter()-ts}
 meta['sha256']={name+'.npy':hashlib.sha256((out/(name+'.npy')).read_bytes()).hexdigest() for name in ['U','J_lo','J_hi','distance','W','starts']}
 (out/'parameters.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({k:v for k,v in meta.items() if k not in ['q_numerators','dl','dr']},indent=2),flush=True)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--distance',type=int,default=13);v=a.parse_args();build(v.distance)
