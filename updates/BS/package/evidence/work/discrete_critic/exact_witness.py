#!/usr/bin/env python3
"""Exact finite-word range certificate for five-letter discrete witness.
The analytic equilibrium inequality is in RESULT.md, not proved by this script.
"""
from fractions import Fraction as R
from pathlib import Path
import itertools,json,hashlib,time,sys
start=time.perf_counter()
half="--half" in sys.argv
eps=R(1,2) if half else R(1)
lo,hi=(-29_000_000,81_000_000) if half else (-7_000_000,16_000_000)
certgap=R(29,20000) if half else R(29,10000)
if half and 44**2*(R(311,120)**2+R(10729,600)**2)>=796**2:
 raise RuntimeError("half geometric constant")
root=Path(__file__).resolve().parents[2]
c=json.loads((root/'work/hidden_equilibrium/certificate.txt').read_text())
a=lambda k:[[R(t) for t in row] for row in c[k]]
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
T=lambda a:list(map(list,zip(*a)))
mul=lambda a,b:[[dot(row,col) for col in T(b)] for row in a]
sub=lambda a,b:[x-y for x,y in zip(a,b)]
v=a('points');H=a('H');Q=a('Q');L=a('L');fa=a('facets');N=[[eps*x/10 for x in row[1:]] for row in fa];off=[eps*row[0]/10 for row in fa]
NtN=mul(T(N),N);det=NtN[0][0]*NtN[1][1]-NtN[0][1]*NtN[1][0];inv=[[NtN[1][1]/det,-NtN[0][1]/det],[-NtN[1][0]/det,NtN[0][0]/det]];C=mul(inv,T(N));CN=mul(C,N)
if CN!=[[R(1),R(0)],[R(0),R(1)]]:raise RuntimeError('left inverse')
K=[[eps*L[j][i]+R(i==j) for j in range(8)] for i in range(8)]
P=[[eps*Q[i][j]+R(i==j) for j in range(10)] for i in range(10)]
q=list(map(R,json.loads((root/'work/discrete_critic/SEED_CHECK.json').read_text())['shifted_interpolation']['qcoeff_exact']))
q=[eps*x for x in q]
ff={};dd={}
for u,j in itertools.product(range(6),repeat=2):
 f=[R(0)]*8;d=[R(0)]*5
 if u==0:
  rhs=[R(j==k+1)-off[k] for k in range(5)];f[0]=R(1);f[1:3]=[dot(row,rhs) for row in C];d=sub(rhs,[dot(row,f[1:3]) for row in N])
 else:f[2+u]=R(1)
 ff[u,j]=f;dd[u,j]=d
labels=[0]*5+list(range(1,6));fhidden=[[sum(P[i][j]*ff[labels[i],labels[j]][k] for j in range(10)) for k in range(8)] for i in range(10)]
if fhidden!=H:raise RuntimeError('target feature mismatch')
for i in range(10):
 dr=[sum(P[i][j]*dd[labels[i],labels[j]][k] for j in range(10)) for k in range(5)]
 if any(dr):raise RuntimeError('target residual mismatch')
gg={}
for a0,b0,c0 in itertools.product(range(6),repeat=3):gg[a0,b0,c0]=sub(ff[b0,c0],[dot(row,ff[a0,b0]) for row in K])
alpha=eps*R(3,1000);beta=eps*R(1,125000);circle=R(664,75) if half else R(836,75);ch=796 if half else 503;lam=R(ch**2,4)/alpha;mu=R(36,25*4)/beta
minimum=None;maximum=None;minword=None;maxword=None;wordcount=0
for w in itertools.product(range(6),repeat=5):
 fminus=ff[w[2],w[1]];fplus=ff[w[2],w[3]];p0=R(w[2]==0)
 s2=dot(fminus[1:3],fplus[1:3]);rh=dot(dd[w[2],w[1]],dd[w[2],w[3]]);rt=dot(gg[w[2],w[1],w[0]],gg[w[2],w[3],w[4]])
 sq=q[0]*p0+q[1]*(fminus[1]+fplus[1])/2+q[2]*(fminus[2]+fplus[2])/2+q[3]*fminus[1]*fplus[1]+q[4]*(fminus[1]*fplus[2]+fminus[2]*fplus[1])/2
 value=sq+circle*(p0-s2)+alpha*(p0+s2)+beta*p0+lam*rh+mu*rt
 if minimum is None or value<minimum:minimum,minword=value,w
 if maximum is None or value>maximum:maximum,maxword=value,w
 if value<R(lo) or value>R(hi):raise RuntimeError('range')
 wordcount+=1
g=-eps*R(c['farkas_drift_pairing'])/2;target=-g+alpha+beta/2
if target>=-certgap:raise RuntimeError('gap')
report={'status':'PASS','epsilon':str(eps),'circle_constant':str(circle),'sqrt_Rh_constant':ch,'arithmetic':'fractions.Fraction','word_count':wordcount,'source_sha256':hashlib.sha256((root/'work/hidden_equilibrium/certificate.txt').read_bytes()).hexdigest(),'F_left_inverse':[[str(x) for x in row] for row in C],'q':list(map(str,q)),'alpha':str(alpha),'beta':str(beta),'Lambda':str(lam),'Mu':str(mu),'minimum_exact':str(minimum),'maximum_exact':str(maximum),'minimum_numeric':float(minimum),'maximum_numeric':float(maximum),'min_word':minword,'max_word':maxword,'range_certified':[lo,hi],'target_expectation_exact':str(target),'target_expectation_numeric':float(target),'target_gap_certified':str(certgap),'elapsed_seconds':time.perf_counter()-start}
(root/'work/discrete_critic'/('EXACT_WITNESS_HALF.json' if half else 'EXACT_WITNESS.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','word_count','minimum_numeric','maximum_numeric','target_expectation_numeric','elapsed_seconds']},indent=2))
