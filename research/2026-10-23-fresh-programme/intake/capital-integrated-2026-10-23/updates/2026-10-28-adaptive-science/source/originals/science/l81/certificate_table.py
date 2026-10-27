"""Calculate proved schedules; no numerical TV estimation."""
from pathlib import Path
import csv, math
from covariance_sampler import explicit_schedule, safe_bound, ordinary_bound
rows=[]
for d in [16,256,4096,65536,1048576,16777216,4294967296]:
    for eps in ([.1,.01] if d<=1048576 else [.1]):
        n,k=explicit_schedule(d,eps);base=math.ceil(math.sqrt(d)/(2*eps))
        rows.append(dict(d=d,epsilon=eps,n=n,k=k,corrected_queries=n+4*k,
                         corrected_TV_bound=safe_bound(d,n,k),ordinary_queries=base,
                         ordinary_TV_bound=ordinary_bound(d,base)))
        assert safe_bound(d,n,k)<=eps+1e-14
p=Path(__file__).resolve().parent/'certificate_table.csv'
with p.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(p.read_text())
