"""Independent GF(2) verification of the 53-element local Fano minor.

No CMR or external dependency is required. The sole construction dependency is
bdl_matrices.py, implementing BDL Sec. 3.2.2 at the unsubdivided ell=3 block.
"""
from two_square_minor import build
from bdl_matrices import rank
import json
from pathlib import Path
T,columns=build()
c=json.loads(Path(__file__).with_name('two_square_fano.json').read_text())
contract=c['contract'];retain=c['retain']
P=[int(x,16) for x in c['projection_rows_hex']]
assert T.validate()==[16,34,19,16,18]
assert rank([columns[i] for i in contract])==16
assert rank(P)==3
assert all((row&columns[i]).bit_count()%2==0 for row in P for i in contract)
image=[sum(((row&columns[i]).bit_count()%2)<<j for j,row in enumerate(P)) for i in retain]
assert image==list(range(1,8))
assert len(set(contract+retain))==23
print('Verified: exact RX of two adjacent Tanner squares has augmented Fano minor.')
print('Contraction rank = 16; quotient rank = 3; retained columns =',image)
print('Retained indices =',retain)
print('Projection rows =',c['projection_rows_supports'])
