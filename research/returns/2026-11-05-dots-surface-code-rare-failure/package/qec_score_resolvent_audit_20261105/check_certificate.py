"""Independent arbitrary-precision audit of the uint128 supersolution certificate."""
import json,hashlib,time
from pathlib import Path
from fractions import Fraction as F
import numpy as np
start=time.perf_counter();root=Path(__file__).resolve().parents[1];src=root/'qec_score_resolvent_20261105';meta=json.loads((src/'certificate_N64.json').read_text());a=np.load(src/'automaton_N64.npz');states=a['states'];starts=a['starts'];ends=a['end'];row=a['row'];col=a['col'];delta=a['delta'];W=a['W'];N=meta['modulus'];wb=meta['weight_denominator_exponent'];qb=meta['table_denominator_exponent'];D=1<<wb;Q=1<<qb
U=np.fromfile(src/'certified_table_N64.bin',dtype=np.uint64).reshape(len(states),N).astype(object);wn=list(map(int,meta['weight_numerators']));graphpath=root/'canonical_qec_circuit_gate_20261105/d13_r13_p1_1000_graph.json';G=json.loads(graphpath.read_text());nd=G['internal_vertices'];adj={}
assert hashlib.sha256(graphpath.read_bytes()).hexdigest()==meta['input_sha256']
assert hashlib.sha256((src/'certified_table_N64.bin').read_bytes()).hexdigest()==meta['table_sha256']
assert len({tuple(e) for e in G['edges']})==len(G['edges'])
for e,(u,v) in enumerate(G['edges']):adj.setdefault(u,[]).append((v,e));adj.setdefault(v,[]).append((u,e))
sid={tuple(map(int,x)):i for i,x in enumerate(states)};shortcut={tuple(sorted(e)):c for e,c in zip(G['edges'],G['costs'])};left=set(G['left']);right=set(G['right']);expectedstarts=[];tv=F(0);qs=meta['q_numerators'];P=1<<64
for e,rec in enumerate(G['errors']):
 mid,rad=F(rec['p_mid']),F(rec['p_radius']);q=F(qs[e],P)
 assert abs(mid-q)<=F(1,2*P);tv+=abs(mid-q)+rad
assert tv==F(meta['conversion_TV_upper_exact'])
for i,(u,v,e,b) in enumerate(states):
 u,v,e,b=map(int,(u,v,e,b));c=G['costs'][e]
 assert int(delta[i])==c*(2*b-1)
 assert wn[i]==((P-qs[e])<<(wb-64-c) if b==0 else qs[e]<<(wb-64+c))
 assert bool(ends[i])==(v in right)
 if u in left:expectedstarts.append(i)
 expected=[]
 if v<nd:
  for z,f in adj[v]:
   if z==u:continue
   shorter=shortcut.get(tuple(sorted((u,z))),10**9)<c+G['costs'][f]
   for bb in [0,1]:
    if not(b==bb==0 and shorter):expected.append(sid[v,z,f,bb])
 assert sorted(expected)==list(map(int,col[row[i]:row[i+1]]))
assert set(expectedstarts)==set(map(int,starts))
min_scalar_slack=None;min_folded_slack=None;maxproduct=0;maxaccum=0;maxterminal=0
# Cache each row shifted by its own incoming score increment. The supersolution
# transition is indexed at (r+delta[next]) mod N, not (r-delta[next]).
shifted=[np.roll(U[j],-int(delta[j])) for j in range(len(states))]
for i in range(len(states)):
 js=list(map(int,col[row[i]:row[i+1]]));scal=sum(wn[j]*int(W[j]) for j in js);slack=(int(W[i])-1)*D-scal
 assert slack>=0;min_scalar_slack=slack if min_scalar_slack is None else min(min_scalar_slack,slack)
 rhs=np.zeros(N,dtype=object)
 for j in js:
  product=wn[j]*shifted[j];maxproduct=max(maxproduct,int(max(product)));rhs+=product
 maxaccum=max(maxaccum,int(max(rhs)))
 if ends[i]:
  # Verify the STRONGER rounded-up terminal inequality used in the checker,
  # then the actual exact terminal mass separately.
  terminal=np.array([(1<<(qb-r)) if r<=qb else 1 for r in range(N)],dtype=object)*D
  exact=np.array([1<<(wb+qb-r) for r in range(N)],dtype=object)
  assert all(t>=e for t,e in zip(terminal,exact));maxterminal=max(maxterminal,int(max(terminal)))
  rhs+=terminal
 slacks=U[i]*D-rhs;assert all(s>=0 for s in slacks)
 v=int(min(slacks));min_folded_slack=v if min_folded_slack is None else min(min_folded_slack,v)
maxU=int(np.max(U));maxW=int(np.max(W));assert maxproduct<1<<128 and maxaccum+maxterminal+D<1<<128;assert maxU<1<<64
znum=sum(wn[int(s)]*int(U[int(s),int(delta[s])%N]) for s in starts);z=F(znum,D*Q);assert z==F(meta['Z_exact'])
# W>=1+TW establishes an exact weighted-norm contraction, without floating rho.
contract=1-F(1,maxW)
out={'status':'PASS: independent arbitrary-precision structure, all scalar/folded inequalities, normalizer and TV budget','states':len(states),'modulus':N,'folded_states_checked':len(states)*N,'transitions':len(col),'minimum_scalar_integer_slack':str(min_scalar_slack),'minimum_folded_integer_slack':str(min_folded_slack),'maximum_product_bits':maxproduct.bit_length(),'maximum_accumulator_plus_terminal_bits':(maxaccum+maxterminal+D).bit_length(),'uint128_safe_on_actual_input':True,'exact_weighted_norm_contraction_upper':str(contract),'Z_exact':str(z),'TV_bound_exact':str(tv),'terminal_rounding_note':'The table certificate rounds terminal weights upward when r>52. The sampler must still use exact 2^-r terminal mass, or explicitly correct the overstatement.','elapsed_seconds':time.perf_counter()-start}
Path(__file__).with_name('certificate_audit_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
