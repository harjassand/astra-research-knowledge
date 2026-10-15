from pathlib import Path
import pathlib,subprocess,json,itertools,random,hashlib
from fractions import Fraction as Q
import mpmath as mp
b=pathlib.Path(str(Path(__file__).resolve().parent.parent / 'avalanche_boundary_dp'));a=pathlib.Path(__file__).parent
src=(b/'large_certificate.cpp').read_text(); M=1<<60;D=1000000
subprocess.run(['g++','-O3','-std=c++17','-x','c++','-o',str(a/'certificate'),'-'],input=src,text=True,check=True)
res={'recomputed_certificates':[]}
for kind in ['moderate','author']:
 for n in [100,400]:
  f=b/f'large_input_{n}_{kind}.txt'; inp=f.read_text();old=json.loads((b/f'large_result_{n}_{kind}.json').read_text())
  new=json.loads(subprocess.check_output([str(a/'certificate')],input=inp,text=True))
  assert all(new[k]==old[k] for k in new)
  assert hashlib.sha256(inp.encode()).hexdigest()==old['input_sha256']
  strengths=list(map(Q,old['strengths_exact'])); F=Q(old['F']);T=Q(old['T']);lines=inp.splitlines();
  def pair(q):
   q*=M;return [q.numerator//q.denominator,-(-q.numerator//q.denominator)]
  assert [list(map(int,s.split())) for s in lines[1:1+n]]==[pair(s/T) for s in strengths]
  assert [list(map(int,s.split())) for s in lines[1+n:1+2*n]]==[pair(F/T/m) for m in range(1,n+1)]
  assert list(map(int,lines[1+2*n].split()))==[0]+[sum(s*m>F for s in strengths) for m in range(1,n+1)]
  assert [list(map(int,s.split())) for s in lines[2+2*n:]]==[[int(m==0 or s*m<=F) for m in range(n+1)] for s in strengths]
  res['recomputed_certificates'].append({'n':n,'kind':kind,'exact_match':True,'input_mechanics_verified':True})
# Expose unchanged production fixed-time value function, replacing only integration/output.
probe=src[:src.index(' W prev=0,t=1;')]+''' W tick;while(cin>>tick){I z=value(tick);cout<<tick<<" "<<z.l<<" "<<z.h<<"\\n";} }'''
(a/'probe.cpp').write_text(probe)
subprocess.run(['g++','-O3','-std=c++17',str(a/'probe.cpp'),'-o',str(a/'probe')],check=True)
mp.mp.dps=80
fix=json.loads((b/'certified_fixture.json').read_text());s=list(map(Q,fix['strengths_exact_rationals']));n=len(s);F=Q(fix['F']);T=Q(fix['T'])
lines=[f'{n} 100000000000000']+[' '.join(map(str,pair(v/T))) for v in s]+[' '.join(map(str,pair(F/T/m))) for m in range(1,n+1)]
lines+=[' '.join(map(str,[0]+[sum(v*m>F for v in s) for m in range(1,n+1)]))]
lines+=[' '.join(str(int(m==0 or v*m<=F)) for m in range(n+1)) for v in s]
ticks=[0,1,1000,1000000,10**8,10**9,10**10,10**11,10**12,10**13,10**14]
out=subprocess.check_output([str(a/'probe')],input='\n'.join(lines+list(map(str,ticks)))+'\n',text=True)
def m(q):return mp.mpf(q.numerator)/q.denominator
checks=[]
for row in out.splitlines():
 tick,lo,hi=map(int,row.split());p=[mp.exp(-mp.exp(-m(v/T))*mp.mpf(tick)/D) for v in s];g=mp.mpf(0)
 for bits in itertools.product([0,1],repeat=n):
  k=max([0]+[c for c in range(1,n+1) if sum(x and v*c>F for x,v in zip(bits,s))>=c])
  if k:g+=mp.exp(-m(F/T/k))*mp.fprod(p[j] if x else 1-p[j] for j,x in enumerate(bits))
 assert mp.mpf(lo)/M<=g<=mp.mpf(hi)/M,(tick,lo,hi,g)
 checks.append({'ticks':tick,'reference':mp.nstr(g,25),'interval_width':str(Q(hi-lo,M))})
res['n5_fixed_u_independent_enumeration']=checks
(a/'result.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
