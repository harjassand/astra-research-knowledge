from exact_verify import F,top,ROOT
from exact_failure import weighted
from itertools import combinations
import json
es=list(combinations(range(4),2))+[(i+4,j+4)for i,j in combinations(range(4),2)]+[(i,i+4)for i in range(4)];w=[F(1)]*12+[F(1,1000)]*4;p=[F(1)]*4+[-F(1)]*4
A,K,T,f=weighted(8,es,w,p);m=len(es);d=[1-T[i][i]for i in range(m)];U=[F(2001,500)]*m;L=[-F(2001,500)]*12+[F(0)]*4
upslack=[d[i]*U[i]-f[i]-top([max(T[i][j]*L[j],T[i][j]*U[j],F(0))for j in range(m)if j!=i],2)for i in range(m)]
loslack=[f[i]-top([max(-T[i][j]*L[j],-T[i][j]*U[j],F(0))for j in range(m)if j!=i],2)-d[i]*L[i]for i in range(m)]
assert min(upslack+loslack)>=0
hi=[f[i]+top([max(T[i][j]*L[j],T[i][j]*U[j],F(0))for j in range(m)if j!=i],3)for i in range(m)];lo=[f[i]-top([max(-T[i][j]*L[j],-T[i][j]*U[j],F(0))for j in range(m)if j!=i],3)for i in range(m)]
assert max(map(abs,hi+lo))==4
out={'epsilon':'1/1000','all_U':'2001/500','internal_L':'-2001/500','bridge_L':'0','min_supersolution_slack':str(min(upslack+loslack)),'max_flow_bound':str(max(map(abs,hi+lo))),'total_positive_injection':'4','note':'Exact interval bound matches the simpler universal positive-injection bound; not evidence of an advance.'}
(ROOT/'exact_weak_cut.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
