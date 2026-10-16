from rigorous_pair_certificate import certify
from fractions import Fraction
from pathlib import Path
import json
n=6;e=[(i,i+1) for i in range(5)];r=[1,10,100,1000,10000]
rows=[]
for start,W,eps in [(3,10**10,Fraction(1,1000)),(4,10**12,Fraction(1,10000))]:
    q=r[:start]+[W]*(n-1-start)
    row=certify(n,e,r,q,start,eps)
    row['retained_intensity']=sum(r[:start]);rows.append(row)
Path(__file__).with_name('accuracy_curve_results.json').write_text(json.dumps(rows,indent=2))
