from pathlib import Path
import json,sys
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent/'outer_grs_distillation_20261028'))
from grs_wrapper_v1 import GF
cases=json.loads((P/'direct_outer_checks_v1.json').read_text())['cases'];result=[]
for c in cases:
 h=c['h'];g=GF(h,c['field_modulus']);prefix=[]
 for gate in c['binary_encoder_gates']:
  if any(i>=h for i in gate[1:]):break
  prefix.append(gate)
 assert prefix[:h]==[['H',j] for j in range(h)]
 linear=prefix[h:];pairs=0
 for x in range(g.q):
  for z in range(g.q):
   y=[(z>>j)&1 for j in range(h)]
   for kind,i,j in linear:
    if kind=='CX':y[j]^=y[i]
    elif kind=='SW':y[i],y[j]=y[j],y[i]
    else:raise AssertionError(kind)
   yf=sum(bit<<j for j,bit in enumerate(y))
   assert (x&z).bit_count()%2==g.trace(g.mul(x,yf));pairs+=1
 result.append({'B':c['B'],'h':h,'exact_Fourier_character_pairs':pairs})
out={'status':'PASS','cases':result,'scope':'Emitted first-symbol H/CNOT/SWAP realizes trace Fourier, including inverse trace-Gram orientation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
