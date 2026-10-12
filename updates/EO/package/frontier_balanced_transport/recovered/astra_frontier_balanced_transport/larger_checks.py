"""Reproduce the larger finite-ring exact certificate examples."""
from experiments import *
records=[]
for n in (8,12,16):
    H,J,_,edges=model(n); gamma=Q(1,2); raw=[A(H,J)]
    if n<=12: raw.append(off(A(H,A(H,raw[0]))))
    start=time.perf_counter()
    f,g,coef=optimal_upper_basis(H,J,raw,n,edges,gamma)
    low,up,gap=certificate(H,J,f,g,n,gamma)
    records.append({'n':n,'directions':len(raw),'D_lower_exact':str(max(4*low,Q(4,9))),
        'D_upper_exact':str(4*up),'D_lower':float(max(4*low,Q(4,9))),
        'D_upper':float(4*up),'f_terms':len(f),'g_terms':len(g),
        'seconds':time.perf_counter()-start})
(ROOT/'larger_checks.json').write_text(json.dumps(records,indent=2))
print(json.dumps(records,indent=2))
