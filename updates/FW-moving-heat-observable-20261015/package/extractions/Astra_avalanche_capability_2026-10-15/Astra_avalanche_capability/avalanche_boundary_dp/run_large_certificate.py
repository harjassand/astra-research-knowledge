"""Generate exact binary64 strength fixture and exact mechanics; run own C++ only."""
from fractions import Fraction as Q
import numpy as np,json,subprocess,time,pathlib,sys,hashlib
base=pathlib.Path(__file__).parent
M=1<<60
n=int(sys.argv[1]) if len(sys.argv)>1 else 100
kind=sys.argv[2] if len(sys.argv)>2 else 'moderate'
F=Q(n*7,40) if kind=='moderate' else Q(n,8)
T=Q(3,20) if kind=='moderate' else Q(1,20)
U=100000 if kind=='moderate' else 100000000000
s=sorted(map(Q,np.random.RandomState(0).rand(n)),reverse=True)
def ints(q):
 q*=M
 return f'{q.numerator//q.denominator} {-(-q.numerator//q.denominator)}'
js=[0]+[sum(v*m>F for v in s) for m in range(1,n+1)]
lines=[f'{n} {U*1000000}']+[ints(v/T) for v in s]+[ints(F/(T*m)) for m in range(1,n+1)]
lines+=[' '.join(map(str,js))]
lines+=[' '.join(str(int(m==0 or s[j]*m<=F)) for m in range(n+1)) for j in range(n)]
input_text='\n'.join(lines)+'\n'
(base/f'large_input_{n}_{kind}.txt').write_text(input_text)
t=time.perf_counter();r=subprocess.run([str(base/'large_certificate')],input=input_text,text=True,capture_output=True,check=True);elapsed=time.perf_counter()-t
out=json.loads(r.stdout);den=int(out['denominator']);lo=Q(int(out['lower_numerator']),den);hi=Q(int(out['upper_numerator']),den)
out.update(n=n,F=str(F),T=str(T),U=U,lower=float(lo),upper=float(hi),relative_gap=float((hi-lo)/lo),seconds=elapsed,tail_upper=float(Q(int(out['tail_numerator']),den)),input_sha256=hashlib.sha256(input_text.encode()).hexdigest(),strengths_exact=[str(v) for v in s])
(base/f'large_result_{n}_{kind}.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='strengths_exact'},indent=2))
