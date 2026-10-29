from fractions import Fraction as F
from pathlib import Path
import json
base=Path('producer-workspace/quaternion_algebraic_completion_20261029');G=[F(x) for x in json.loads((base/'input.json').read_text())['perturbed']];A=sum(map(abs,G));assert A>0
rows=[]
for k in [0,4,16,64,256]:
 T=2**k;p=F(1,3);R=F(1)
 while R*R<F(720**2*T,35)/p:R*=2
 eps=R/(4*T*T);last=eps/(4*A)
 assert sum(abs(last*g) for g in G)==eps/4
 shifts=[F(j)*eps/(4*A*6973) for j in range(1,6974)]
 assert all(shifts[j]<shifts[j+1] for j in range(6972)) and shifts[-1]==last
 # Worst sign-aligned representative query coefficient has O(logT) bits;
 # adding the fixed-direction shifts preserves that order.
 f=F(720*T)/(2*p)+R/2
 bitmax=max(max((f+shifts[j]*g).numerator.bit_length(),(f+shifts[j]*g).denominator.bit_length()) for j in [0,3486,6972] for g in G)
 rows.append({'log2T':k,'distinct_trials':len(shifts),'perturbation_l1_exact':str(eps/4),'representative_trial_coefficient_bits':bitmax})
out={'scope':'Exact finite shift list/scaling checks only; universal resultant/extractor is not implemented or run.','fixed_direction_l1':str(A),'rows':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
