from pathlib import Path
import runpy,json,sys,numpy as np,sympy as s,hashlib
from fractions import Fraction as F
p=Path('/workspace/scratch/57d8dd795b13/morrey_law_first_stress_20261026/cube_brownian_completion');sys.path.insert(0,str(p));o=p/'same_law_AC';j=json.loads((o/'posterior_hull_bulk_ceiling_receipt.json').read_text());bound=0
for fam in j['families']:
 D=fam['coordinate_denominator'];X=fam['integer_points'];assert s.Matrix([[x[i]-X[0][i]for i in range(3)]for x in X[1:]]).rank()==3
 for x in X:assert max(map(abs,x))<D and D**3-D*sum(v*v for v in x)+2*x[0]*x[1]*x[2]>0
 for poly in fam['S3_polytopes']:
  for A,B,C,b in poly:
   bound=max(bound,128*D*(abs(A)+abs(B)+abs(C)),128*abs(b)+D*(abs(A)+abs(B)+abs(C)))
assert bound<2**63
V=np.load(p/'fully_corrective141_half_K48/candidate_volume_nodes.npy',mmap_mode='r');assert float(np.max(np.abs(V)))*2**40*257**3<2**63
print('EXACT FULL-RANK/PD HULLS AND INT64 SAFETY PASS; plane bound',bound,flush=True)
root=json.loads((p/'fully_corrective141_half_K48/ACTUAL_CORRECTIVE_ROOT.json').read_text());c=next(c for c in root['components']if c['catalog_index']==133);path=Path(c['label']['actual_received_law_identity_path']);src=json.loads(path.read_text());a=json.loads((o/'negative_subtree_posterior_point_receipt.json').read_text());assert hashlib.sha256(path.read_bytes()).hexdigest()==a['source_policy_sha256']==c['label']['sha256'];assert a['root_weight']==c['root_probability'];g=np.load(src['geometry_path']);X=g['states'];A=g['actions'];D=int(g['coordinate_denominator']);N=np.load(src['indexed_DAG_path'])['nodes'];look={(int(t),int(st)):int(ac)for t,st,ac in N};mass={int(N[0,1]):F(1)}
for t in range(int(N[0,0]),a['source_time'],-1):
 nxt={}
 for st,m in mass.items():
  ac=look[t,st];assert ac>=0;ss,l,r,num,den=map(int,A[ac]);assert ss==st
  for child,pr in [(l,F(num,den)),(r,1-F(num,den))]:nxt[child]=nxt.get(child,F())+m*pr
 mass=nxt
assert mass[a['source_state_index']]==F(a['exact_incoming_policy_mass']);layer=[(a['source_state_index'],F(1))]
for t in range(a['source_time'],a['source_time']-3,-1):
 nxt=[]
 for st,m in layer:
  ac=look[t,st];assert ac>=0;ss,l,r,num,den=map(int,A[ac]);assert ss==st
  nxt.extend([(l,m*F(num,den)),(r,m*(1-F(num,den)))])
 layer=nxt
assert [st for st,m in layer]==a['frontier_state_indices'];assert [str(m)for st,m in layer]==a['frontier_probabilities'];assert [[str(F(int(v),D))for v in X[st]]for st,m in layer]==a['frontier_points']
print('NEGATIVE FRONTIER ORIGINAL SOURCE RECONSTRUCTION PASS',flush=True)
old=Path.write_text;Path.write_text=lambda self,data,*aa,**k: len(data) if self.read_text()==data else (_ for _ in ()).throw(AssertionError(str(self)))
try:runpy.run_path(str(p/'receive_posterior_hull_bulk_ceiling.py'),run_name='__main__')
finally:Path.write_text=old
print('NONMUTATING CEILING REPLAY MATCH',flush=True)
