import itertools,json
from pathlib import Path
P={'I':(0,0),'X':(1,0),'Y':(1,1),'Z':(0,1)}
G=['XZZXI','IXZZX','XIXZZ','ZXIXZ']
def comm(a,b):return sum(P[x][0]*P[y][1]+P[x][1]*P[y][0] for x,y in zip(a,b))%2
assert all(not comm(a,b) for a,b in itertools.product(G,repeat=2))
rows=[]
for j in range(5):
 for p in 'XYZ':
  e=['I']*5;e[j]=p;e=''.join(e);sy=tuple(comm(e,g) for g in G);assert any(sy);rows.append({'error':e,'syndrome':sy})
assert len({r['syndrome'] for r in rows})==15
for p in ['XXXXX','ZZZZZ']:assert all(not comm(p,g) for g in G)
assert comm('XXXXX','ZZZZZ')==1
res={'stabilizers':G,'single_error_syndromes':rows,'all15_nonzero_syndromes_unique':True,'recursion':'p_next <=10 p^2 for independent possibly nonidentical Pauli ports bounded byp','examples':[{'level':l,'source_service_calls':5**l,'logical_error_bound':(.1**(2**l))/10} for l in range(1,5)]}
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(res['examples'])
