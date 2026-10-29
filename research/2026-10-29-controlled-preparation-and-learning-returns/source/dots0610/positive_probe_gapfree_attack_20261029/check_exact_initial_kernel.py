# Exact nontrivial2D initial quadrature certificate (uniform potential, no exp oracle).
from fractions import Fraction as F
from pathlib import Path
import json
p=Path(__file__).parent;T=8;d=2;gamma=4*((10*d*T-1).bit_length());r=F(1,8);S=[[F(5,8),F(0)],[F(0),F(5,24)]];mu=[F(7,9),F(0)];rows=[]
for n in [4,8,16]:
 pts=[]
 for i in range(n):
  a=F(2*n+2*i+1,4*n)
  for j in range(n):
   z=F(2*j+1-n,n);pts.append(((a,a*z),a))
 total=sum(w for x,w in pts);m=[sum(x[i]*w for x,w in pts)/total for i in range(2)];M=[[sum(x[i]*x[j]*w for x,w in pts)/total for j in range(2)] for i in range(2)]
 err=sum(abs(m[i]-mu[i]) for i in range(2));diag=[M[i][i]-F(50,99)*S[i][i] for i in range(2)];assert M[0][1]==0 and min(diag)>0
 lev=max(sum(x[i]*x[i]/S[i][i] for i in range(2)) for x,w in pts);assert lev<F(3,2)*d*gamma*gamma
 rows.append({'grid_n':n,'support':n*n,'exact_mean_L1_error':str(err),'required_mean_tolerance':str(r/(4*T*T)),'mean_pass':err<=r/(4*T*T),'exact_M_minus_50_over99_W_diagonal':list(map(str,diag)),'max_exact_support_leverage':str(lev),'PSD_and_support_certificates':True})
assert rows[-1]['mean_pass']
out={'status':'PASS_EXACT_RATIONAL_INITIAL_QUADRATURE_CERTIFICATE','body':'{(a,y):1/2<=a<=1, -a<=y<=a}','potential':'uniform, cumulative estimator0','exact_continuous_mean':list(map(str,mu)),'exact_continuous_second_moment':[[str(v) for v in row] for row in S],'scope':'Exact2D initial-round kernel only. Does not certify nonuniform exponential integration or execute35D learner.','rows':rows};(p/'exact_initial_kernel_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
