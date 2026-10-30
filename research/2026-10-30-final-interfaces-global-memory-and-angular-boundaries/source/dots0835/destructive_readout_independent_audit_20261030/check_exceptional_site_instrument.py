"""Steane full-logical-Z map under arbitrary local output instruments and bath memory.
Checks the entire logical operator basis, including off-diagonal inputs.
The readout bit on the exceptional site is arbitrary, not its measured DATA Z value.
"""
from pathlib import Path
import numpy as np,json
rng=np.random.default_rng(631004)
H=np.array([[(j>>r)&1 for j in range(1,8)] for r in range(3)],int)
def ind(b):return sum(int(v)<<j for j,v in enumerate(b))
CX=[(np.array([(u>>r)&1 for r in range(3)])@H)%2 for u in range(8)]
enc=np.zeros((128,2),complex)
for l in range(2):
 for c in CX:enc[ind((c+l)%2),l]=1/np.sqrt(8)
labels=[]
for x in range(128):
 bits=np.array([(x>>j)&1 for j in range(7)]); s=H@bits%2;k=ind(s)
 if k:bits[k-1]^=1
 labels.append(int(sum(bits)%2))
def haar(rows,cols):
 z=rng.normal(size=(rows,cols))+1j*rng.normal(size=(rows,cols));q,r=np.linalg.qr(z);return q[:,:cols]
def apply_local(v,A,site):
 out=np.zeros_like(v)
 for x in range(128):
  if (x>>site)&1:continue
  ix=[(x,0),(x,1),(x|(1<<site),0),(x|(1<<site),1)]
  block=np.array([v[a,b] for a,b in ix]);res=A@block
  for j,(a,b) in enumerate(ix):out[a,b]=res[j]
 return out
errs=[];signed_errs=[]
for trial in range(70):
 site=trial%7
 initial=[np.zeros((128,2),complex) for _ in range(2)]
 U=haar(4,4)
 for l in range(2):
  initial[l][:,0]=enc[:,l];initial[l]=apply_local(initial[l],U,site)
 def instrument():
  iso=haar(8,4);result=np.zeros((2,2,2),complex)
  for y in range(2):
   K=iso[4*y:4*y+4];v=[apply_local(a,K,site) for a in initial]
   for x in range(128):
    if (x>>site)&1:continue
    k=labels[x|(y<<site)]
    for l in range(2):
     for lp in range(2):
      result[k,l,lp]+=sum(v[l][xx,b]*v[lp][xx,b].conjugate() for xx in [x,x|(1<<site)] for b in range(2))
  return result
 A=instrument();B=instrument();ideal=np.zeros((2,2,2));ideal[0,0,0]=ideal[1,1,1]=1
 errs.append(float(np.max(np.abs(A-ideal))))
 # A real signed non-CP combination still has the exact classical diagonal form.
 T=1.7*A-2.1*B
 signed_errs.append(float(np.max(np.abs(T-(-.4)*ideal))))
assert max(errs+signed_errs)<1e-12
out={'status':'PASS','trials':70,'all_logical_operator_basis_elements_checked':True,'retained_bath_dimension':2,'arbitrary_exceptional_output_bit_instruments':True,'initial_data_bath_correlations':True,'max_TP_readout_error':max(errs),'max_signed_HP_form_error':max(signed_errs),'scope':'Finite algebra diagnostic, not a Dyson or native-service proof'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
