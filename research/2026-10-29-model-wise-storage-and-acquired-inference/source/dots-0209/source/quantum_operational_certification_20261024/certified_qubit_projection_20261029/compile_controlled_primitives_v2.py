"""Expand each rational two-level gate into addressed, two-controlled one-qubit primitives."""
from finite_povm_synthesis_v1 import *
from pathlib import Path
import json,time

def parse(z):return C(F(z[0]),F(z[1]))
def gate_matrix(g):return [[parse(x) for x in row] for row in g['matrix']]
def adjacent(a,b,M):
 diff=a^b;assert diff.bit_count()==1;target=diff.bit_length()-1
 if (a>>target)&1:M=[[M[1][1],M[1][0]],[M[0][1],M[0][0]]]
 return {'target':target,'controls':[[j,(a>>j)&1] for j in range(3) if j!=target],'matrix':[[x.data() for x in row] for row in M]}
def apply_primitive(U,p):
 target=p['target'];a=sum(value<<j for j,value in p['controls']);b=a|(1<<target)
 apply_rows(U,[a,b],gate_matrix(p))
def expand(g):
 if g['kind']=='basis_phase':
  j=g['basis'];z=parse(g['phase']);a=j&~1;b=a|1
  M=[[z,Z],[Z,O]] if not(j&1) else [[O,Z],[Z,z]]
  return [adjacent(a,b,M)]
 a,b=g['basis'];G=gate_matrix(g);path=[a]
 for bit in range(3):
  if (a^b)&(1<<bit):path.append(path[-1]^(1<<bit))
 swaps=[adjacent(path[i],path[i+1],[[Z,O],[O,Z]]) for i in range(len(path)-2)]
 return swaps+[adjacent(path[-2],path[-1],G)]+list(reversed(swaps))

P=Path(__file__).parent;src=json.loads((P/'check_povm_synthesis_v1.json').read_text());out=[];start=time.time()
for r in src['runs']:
 direct=eye(8);compiled=eye(8);primitives=[]
 for g in r['gates']:
  if g['kind']=='basis_phase':
   z=parse(g['phase']);j=g['basis'];direct[j]=[z*x for x in direct[j]]
  else:apply_rows(direct,g['basis'],gate_matrix(g))
  ps=expand(g);primitives+=ps
  for p in ps:
   assert mm(adj(gate_matrix(p)),gate_matrix(p))==eye(2)
   apply_primitive(compiled,p)
 assert compiled==direct
 assert len(primitives)==r['two_controlled_one_qubit_primitives_upper']
 out.append({'seed':r['seed'],'primitive_count':len(primitives),'exact_compiled_unitary_equals_rational_two_level_circuit':True,'primitives':primitives,'correction_channel_half_diamond_upper':r['correction_channel_half_diamond_upper'],'labels':r['labels']})
 print(r['seed'],len(primitives),flush=True)
(P/'compile_controlled_primitives_v2.json').write_text(json.dumps({'status':'PASS_EXACT_PRIMITIVE_COMPILATION','elapsed_seconds':time.time()-start,'qubit_order':'bit0=accessible flag; bits1,2=trusted zero ancillas; measure bits1,2 then discard flag','runs':out},indent=2)+'\n')
