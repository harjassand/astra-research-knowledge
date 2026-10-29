"""Exact binary polynomial existence certificates and sufficient dense circuit budgets."""
import json
from pathlib import Path
p=Path(__file__).parent
def deg(x):return x.bit_length()-1
def mod(a,b):
 while a and deg(a)>=deg(b):a^=b<<(deg(a)-deg(b))
 return a
def mul(a,b):
 z=0
 while b:
  if b&1:z^=a
  a<<=1;b>>=1
 return z
def gcd(a,b):
 while b:a,b=b,mod(a,b)
 return a
out=[]
for h in range(5,12):
 for f in range((1<<h)|1,1<<(h+1),2):
  x=2;valid=True;res=[]
  for j in range(1,h+1):
   x=mod(mul(x,x),f)
   if j<=h//2:
    g=gcd(x^2,f);res.append(g)
    if g!=1:valid=False;break
  if valid and x==2:break
 B=(1<<h)-1;bound=h*h*B*(B-1)+3*h*h*B+3*h*B
 out.append({'h':h,'irreducible_polynomial_integer':f,'all_gcds_through_floor_h_over_2':res,'frobenius_final_x':x,'B':B,'buffer_qubits':h*B,'sufficient_dense_one_field_linear_transform_CNOT_upper_bound':bound,'scope':'Constructive sufficient bound, not executed dense compilation and not a lower bound. Other gates/calibration/storage/outer correction/readout remain.'})
(p/'field_and_control_bounds.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
