from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
rows=[]
for N in range(2,10):
 c=[F(2*j-(N-1),2) for j in range(N)]
 for L in range(1,N):
  worst=F(0)
  for eta in product([0,1],repeat=N):
   h=sum(c[j]*eta[j] for j in range(N))/N**2
   k=sum(eta[:L])
   bar=(sum(c[j]*eta[j] for j in range(L,N))+F(k,L)*sum(c[:L]))/N**2
   worst=max(worst,abs(h-bar))
   hnext=sum(c[j]*eta[(j+1)%N] for j in range(N))/N**2
   assert hnext-h==(eta[0]-F(sum(eta),N))/N
   assert worst<=F(L*(L-1),2*N*N)
  rows.append({'N':N,'L':L,'maximum_forward_error':str(worst),'certificate':str(F(L*(L-1),2*N*N))})
N=8;L=2;c=[F(2*j-(N-1),2) for j in range(N)];eta=[0]*N;eta[0]=1
h=sum(c[j]*eta[j] for j in range(N))/N**2
bar=F(c[0]+c[-1],2)/N**2
bad=abs(h-bar)
assert bad==F(7,128) and bad>F(L*L,2*N*N)
res={'status':'PASS','forward_cases':len(rows),'rows':rows,'misaligned_kernel_jump':{'N':8,'L':2,'block_offsets':[7,0],'actual_error':str(bad),'invalid_forward_only_bound':str(F(4,128))},'scope':'Exact finite height/alignment checks supplement the analytic proof; no hydrodynamic theorem or hardware validation.'}
Path(__file__).with_name('check_invariant_height_result.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'status':'PASS','forward_cases':len(rows),'misaligned_kernel_jump':res['misaligned_kernel_jump']}))
