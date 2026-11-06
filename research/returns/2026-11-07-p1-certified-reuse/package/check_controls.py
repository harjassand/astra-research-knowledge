"""Replay the nonreciprocal control without installing any dependency."""
import json
from fractions import Fraction as Q
from pathlib import Path
from memory import require,replay_acquisition,row_norm
from run import QuantizedSource

here=Path(__file__).resolve().parent
record=json.loads((here/'NONRECIPROCAL_CONTROL.json').read_text())
acquisition=record['acquisition']
n=4;H=[[Q(int(i==j)) for j in range(n)] for i in range(n)]
for i in range(n-1):H[i][i+1]=Q(1,10);H[i+1][i]=Q(-1,10)
S=[[H[i][j]-Q(int(i==j)) for j in range(n)] for i in range(n)]
require(all(S[i][j]==-S[j][i] for i in range(n) for j in range(n)))
require(row_norm(S)<=Q(1,5))
# Symmetric part is I, and ||H|| <= ||I||+||S|| <= 6/5.
contract=acquisition['contract']
require(contract['structure']=='accretive' and contract['a']=='1'
        and contract['b']=='6/5' and contract['ports']==[0,1])
replay=replay_acquisition(acquisition)
source=QuantizedSource(H)
for entry in acquisition['history']:
    report=source(list(map(Q,entry['query'])),contract['precision_bits'])
    require([str(x) for x in report]==entry['report'])
require(Q(acquisition['A'][0][1])>0 and Q(acquisition['A'][1][0])<0,
        'Incorrectly symmetrized a nonreciprocal operator')
print(json.dumps({'status':'PASS','replay':replay,'native_recheck_work':source.counts()},indent=2))
