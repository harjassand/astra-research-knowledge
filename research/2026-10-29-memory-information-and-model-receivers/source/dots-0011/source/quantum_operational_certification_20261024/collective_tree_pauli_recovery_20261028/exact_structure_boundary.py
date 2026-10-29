#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
Q=[[F(46,100),F(39,100),F(8,100),F(7,100)],[F(45,100),F(40,100),F(8,100),F(7,100)],[F(44,100),F(41,100),F(8,100),F(7,100)]]
words=list(product(range(4),repeat=3));base={x:Q[0][x[0]]*Q[1][x[1]]*Q[2][x[2]] for x in words}
other={x:p-(F(1,100)*(-1)**sum(a==1 for a in x) if all(a in [0,1] for a in x) else 0) for x,p in base.items()}
assert min(other.values())>0 and sum(other.values())==1
for i,j in [(0,1),(0,2),(1,2)]:
 for a,b in product(range(4),repeat=2):
  assert sum(p for x,p in base.items() if x[i]==a and x[j]==b)==sum(p for x,p in other.items() if x[i]==a and x[j]==b)
a=max(base,key=base.get);b=max(other,key=other.get)
assert a==(0,0,0) and b==(0,0,1)
# All one-qubit Bloch contractions strictly positive.
chars=[[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]]
lam=[[sum(t*q for t,q in zip(ch,Q[i])) for ch in chars] for i in range(3)];assert min(x for row in lam for x in row)>0
out={'status':'EXACT_RATIONAL_CHECKS_PASS','tree_oracle_word':a,'tree_oracle_fidelity':str(base[a]),'same_pairs_non_tree_oracle_word':b,'same_pairs_non_tree_oracle_fidelity':str(other[b]),'identity_fidelity_non_tree':str(other[a]),'gap':str(other[b]-other[a]),'all_pair_marginals_exactly_equal':True,'one_site_bloch_contractions':[[str(x) for x in row] for row in lam],'all_probabilities_positive':True,'non_tree_table':{''.join('IXYZ'[a] for a in x):str(p) for x,p in other.items()}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='non_tree_table'},indent=2))
