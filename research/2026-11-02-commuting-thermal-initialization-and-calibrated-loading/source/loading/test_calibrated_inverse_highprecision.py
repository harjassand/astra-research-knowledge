import sys,json,mpmath as mp
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'recursive_initialization'/'helpers'))
from actual_rx_rung import build
mp.mp.dps=80
c=build(3);n=len(c['qs']);Z=c['Z'];cols=[sum(((z>>i)&1)<<j for j,z in enumerate(Z)) for i in range(n)]
valid={0}
for v in cols:valid|={s^v for s in list(valid)}
S=sorted(valid);ix={s:j for j,s in enumerate(S)};perms=[[ix[s^v] for s in S] for v in cols]
out=[]
for beta,qstr in [(2,'0.001'),(4,'0.0000001'),(4,'0.000000001')]:
 q=mp.mpf(qstr);p=[mp.exp(-beta*s.bit_count()) for s in S];z=sum(p);p=[v/z for v in p];pre=p[:]
 for perm in perms[::-1]:pre=[((1-q)*pre[i]-q*pre[perm[i]])/(1-2*q) for i in range(len(p))]
 j=min(range(len(pre)),key=pre.__getitem__);cur=pre[:]
 for perm in perms:cur=[(1-q)*cur[i]+q*cur[perm[i]] for i in range(len(p))]
 out.append(dict(beta=beta,q=qstr,min_pre=mp.nstr(pre[j],60),min_syndrome=S[j],min_ratio=mp.nstr(min(a/b for a,b in zip(pre,p)),60),final_l1=mp.nstr(sum(abs(a-b) for a,b in zip(cur,p)),10),normalization=mp.nstr(sum(pre),60),precision_digits=80))
(ROOT/'calibrated_inverse_highprecision_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
