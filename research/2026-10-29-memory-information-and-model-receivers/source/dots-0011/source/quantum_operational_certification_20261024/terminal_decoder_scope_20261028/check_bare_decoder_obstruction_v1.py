#!/usr/bin/env python3
"""Exact integer/rational check; no random sampling."""
from pathlib import Path
import json,collections,itertools
from fractions import Fraction as F
import compare_decoder_extensions_v1 as m
HERE=Path(__file__).parent
rows=[]
for a,b in itertools.product(range(16),repeat=2):
 _,reps=m.decoder(a,b);words=[r['pauli'] for r in reps];weights=[sum(x!='I' for x in w) for w in words];x,y,z=words
 union=sum(i!='I' or j!='I' for i,j in zip(x,z));diff=sum(i!='I' and j!='I' and i!=j for i,j in zip(x,z))
 assert min(weights)>=3 and diff%2==1 and sum(weights)==2*union+diff
 # Exhaustively enumerate all 4^5 independent Pauli errors at rational p.
 for p in [F(0),F(1,100),F(1,10),F(3,4),F(1)]:
  keep=F(0)
  for err in itertools.product('IXYZ',repeat=5):
   wt=sum(t!='I' for t in err);pr=(p/3)**wt*(1-p)**(5-wt)
   anti=lambda w:sum(u!='I' and v!='I' and u!=v for u,v in zip(err,w))%2
   if not anti(x) and not anti(z):keep+=pr
  q=1-F(4,3)*p;formula=(1+sum(q**w for w in weights))/4
  assert keep==formula
 rows.append({'kx':a,'kz':b,'representatives':reps,'weights':weights,'union':union,'different':diff,'first_order_infidelity':str(F(sum(weights),3))})
mn=min(F(r['first_order_infidelity']) for r in rows)
assert mn==3
out={'status':'PASS_EXACT_ALL_256_EXTENSIONS_AND_5_RATIONAL_NOISE_VALUES','minimum_first_order_infidelity_coefficient':str(mn),'histogram':dict(collections.Counter(r['first_order_infidelity'] for r in rows)),'rows':rows}
(HERE/'bare_decoder_obstruction_check_v1.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],out['histogram'])
