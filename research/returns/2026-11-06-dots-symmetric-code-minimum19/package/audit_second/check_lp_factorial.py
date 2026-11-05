"""Recheck lower-length rational separators using the factorial 6j formula."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from verify_interval_dual_replay import exact_rational_six

ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
records=[]
for item in json.loads((BASE/'exact_lp_certificates.json').read_text()):
    n=item['n'];D=n+1
    M=[[F((2*k+1)*(-1)**(n+k+l))*exact_rational_six(n,n,2*k,n,n,2*l)
        for l in range(D)] for k in range(D)]
    saved=json.loads((BASE/f'transform_n{n}.json').read_text())
    assert all(M[i][j]==F(saved[i][j]) for i in range(D) for j in range(D))
    G=[[2*M[i][j]-int(i==j) for j in range(D)] for i in range(D)]
    y=list(map(F,item['inequality_multipliers']));z=list(map(F,item['equality_multipliers']));beta=F(item['beta'])
    assert len(y)==2*D and len(z)==4 and all(v>=0 for v in y)
    for i in range(D):
        residual=beta-y[i]-sum(G[j][i]*y[D+j] for j in range(D))-sum(G[j+1][i]*z[j] for j in range(4))
        assert residual==int(i==0)
    bound=beta*D/2;assert bound==F(item['upper_a0'])
    assert (bound<1)==(n<=17)
    records.append({'n':n,'upper_a0':str(bound),'excluded':bound<1})
out={'checks':records,'all_exact_checks_passed':True,
     'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(ROOT/'lp_factorial_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
