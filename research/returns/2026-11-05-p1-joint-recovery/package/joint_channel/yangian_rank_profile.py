import numpy as np
from scipy.sparse.linalg import eigsh
from pathlib import Path
HERE=Path(__file__).resolve().parent
src=(HERE / 'yangian_gap.py').read_text().split('for n in map(int,sys.argv')[0]
exec(src)
for n in [2,4,6,8,10]:
 Q,G=schur(n); yz=Yz(n); Q0=Q[:,G[0,0]]; D=yz@Q0
 vals=np.linalg.eigvalsh(3*D.conj().T@D)
 print(n,len(vals),'minY2J0',vals[:min(8,len(vals))], 'mean',np.mean(vals), flush=True)
