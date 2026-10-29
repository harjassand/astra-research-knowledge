#!/usr/bin/env python3
"""Exact parity-scope counterexample for the15-state native fixture."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,math
ROOT=Path(__file__).resolve().parent
def main():
    n=15
    w=[F(1)]*5+[F(16,15)]*10
    f=[[F(0) for j in range(n)] for i in range(n)]
    for e in range(5):
        i=e;j=(e+1)%5
        for o in range(2):
            x=5+2*e+o;p=F(5,8) if o==0 else F(3,8)
            for port,a,b in [(i,p,1-p),(j,1-p,p)]:
                f[port][x]=w[x]*a;f[x][port]=w[x]*b
    Q=[[f[i][j]/w[i] for j in range(n)] for i in range(n)]
    for i in range(n):Q[i][i]=-sum(Q[i])
    theta=list(range(5))+[5+2*e+1-o for e in range(5) for o in range(2)]
    Qstar=[[w[j]*Q[j][i]/w[i] for j in range(n)] for i in range(n)]
    assert Qstar==[[Q[theta[i]][theta[j]] for j in range(n)] for i in range(n)]
    assert all(w[theta[i]]==w[i] and theta[theta[i]]==i for i in range(n))
    assert all(theta[i]==i for i in range(5))
    assert all(sum(w[i]*Q[i][j] for i in range(n))==0 for j in range(n))
    assert all(Q[i][i]==Q[theta[i]][theta[i]] for i in range(n))
    broken=sum(f[i][j]!=f[j][i] for i in range(n) for j in range(i+1,n))
    assert broken==20
    result={"status":"PASS","stationary_balance":"exact","involution":theta,
      "Q_star_equals_theta_Q_theta":"exact on all225 entries",
      "stationary_weights_and_escape_rates_parity_invariant":True,
      "all_native_ports_fixed_by_theta":True,
      "ordinary_detailed_balance_broken_edges":broken,
      "ordinary_entropy_unnormalized":"(16/3)log(5/3)>0",
      "ordinary_entropy_rate":"(16/47)log(5/3)>0",
      "generalized_parity_entropy_rate":"0 exactly",
      "ordinary_entropy_rate_float":(16/47)*math.log(5/3),
      "Q":[[str(v) for v in row] for row in Q],"weights":[str(x) for x in w],
      "source_observations":0,"preparations":0,
      "scope":"Two reversal conventions for the same abstract generator; not a demonstrated passive physical implementation.",
      "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/"PARITY_SCOPE_CHECK.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ["Q","weights"]},indent=2))
if __name__=="__main__":main()

