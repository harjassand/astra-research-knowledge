"""Construct, then independently integer-check, a rational upper resolvent."""
import json,time,subprocess,hashlib
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from screen import model,ROOT

def build(N=64):
 ts=time.perf_counter();path=ROOT.parent/'canonical_qec_circuit_gate_20261105/d13_r13_p1_1000_graph.json'
 G,states,p,costs,w,T,starts,end=model(path,True);n=len(states);D=1<<64;cmax=int(max(costs));wb=64+cmax;qb=52
 q=[];conversion=F(0)
 for e in G['errors']:
  p0=F(e['p_mid']);k=(p0.numerator*D*2//p0.denominator+1)//2;q.append(k);conversion+=abs(F(k,D)-p0)+F(e['p_radius'])
 wn=[((D-q[e])<<(cmax-int(costs[e]))) if b==0 else (q[e]<<(cmax+int(costs[e]))) for u,v,e,b in states]
 A=sum(T.values()).tocsr();A.sort_indices();row=A.indptr.astype(np.uint64);col=A.indices.astype(np.uint32)
 v=np.ones(n)
 for _ in range(300):v=1+A@v
 W=np.ceil(4*v).astype(np.uint64)
 H=np.load(ROOT/f'table_N{N}_geo1.npz')['H'];U=np.ceil(H*2.**qb).astype(np.uint64)
 delta=np.array([costs[e]*(2*b-1) for u,v,e,b in states],dtype=np.int8)
 binary=ROOT/f'certificate_input_N{N}.bin';output=ROOT/f'certified_table_N{N}.bin'
 with binary.open('wb') as f:
  np.array([n,len(col),N,wb,qb],dtype=np.uint64).tofile(f)
  for x in [row,col,np.array([x%2**64 for x in wn],dtype=np.uint64),np.array([x>>64 for x in wn],dtype=np.uint64),delta,end.astype(np.uint8),W,U]:x.tofile(f)
 subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'certify_table.cpp'),'-o',str(ROOT/'certify_table')],check=True)
 r=subprocess.run([str(ROOT/'certify_table'),str(binary),str(output)],check=True,capture_output=True,text=True);cert=json.loads(r.stdout)
 U=np.fromfile(output,dtype=np.uint64).reshape(n,N);Znum=sum(wn[int(s)]*int(U[s,int(delta[s])%N]) for s in starts);Z=F(Znum,1<<(wb+qb))
 meta={'scope':'exact dyadic supersolution for rounded input law; conversion TV explicitly bounded','input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'modulus':N,'q_noise_denominator_exponent':64,'q_numerators':q,'weight_numerators':[str(x) for x in wn],'weight_denominator_exponent':wb,'table_denominator_exponent':qb,'Z_exact':str(Z),'Z_float':float(Z),'conversion_TV_upper_exact':str(conversion),'conversion_TV_upper':float(conversion),'certificate':cert,'table_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'setup_seconds':time.perf_counter()-ts}
 np.savez(ROOT/f'automaton_N{N}.npz',states=states,starts=starts,end=end,row=row,col=col,delta=delta,W=W)
 (ROOT/f'certificate_N{N}.json').write_text(json.dumps(meta,indent=2)+'\n')
 print(json.dumps({k:v for k,v in meta.items() if k not in ['q_numerators','weight_numerators']},indent=2))
if __name__=='__main__':build()
