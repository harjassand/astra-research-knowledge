"""A nonmodular law on which this reference compiler has no useful admitted cut.
No kinetic computation or complexity lower bound for other methods is claimed.
"""
from fractions import Fraction as F
from math import comb
from model import discover_partition
import json
from pathlib import Path
n=18;limit=6
model=dict(n=n,edges={(i,j):F(2+(i+j)%2) for i in range(n) for j in range(i+1,n)},fields=[F(2) if i%3 else F(1,2) for i in range(n)],nu=[F(1+i%3,2) for i in range(n)],target=0,kappa=F(1))
groups,search=discover_partition(model,max_local_bits=limit)
min_cut=comb(n,2)-(n//limit)*comb(limit,2)
out={'coordinates':n,'interaction_edges':len(model['edges']),'selected_block_sizes':list(map(len,groups)),'selected_R':search['selected']['R'],'best_possible_product_bound_at_max_block_size_at_least':str(F(2)**min_cut),'minimum_cross_edges_for_any_admitted_partition':min_cut,'compiled':False,'reason':'The implemented explicit cross-term expansion and the product comparison constant are prohibitive. No global model is enumerated. This is a compiler/access-structure failure, not hardness for every method.'}
json.dump(out,open(Path(__file__).with_suffix('.json'),'w'),indent=2);print(json.dumps(out,indent=2))
