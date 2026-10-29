from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
ROOT=Path(__file__).parent

def root4(x):
 lo,hi=0,1
 while hi**4<x:hi*=2
 while lo+1<hi:
  mid=(lo+hi)//2
  if mid**4<x:lo=mid
  else:hi=mid
 return hi
out=[]
for h in [5,8,12,20,30,40,50,60,80]:
 B=2**h;ell=16*h;N=ell*B;J=N;T=9*N;u=(h-1)//2;t=(B//8)*(u+1);b=t//4
 assert t>=F(N,256)
 exp_h=F((t-b+1)**2,2*(t+b+1));assert exp_h>=F(3*t,16)>=F(3*N,4096)
 p=F(1,3);s=F(2,9);a=F(4,9);assert p+s+a==1 and 2*s/a==1 and s*T==2*N
 m=root4(625*T);eps=F(5,m);M=(2*m+1)**3;logupper=M.bit_length();eta=F(1)
 while eta>p/2 or eta*eta>p*logupper/T:eta/=2
 L=F(9,2)*eps*eps*T+45*(logupper/eta+eta*T/p)
 failure=F(32,3)*L/(b+1);beta0=F(2,2**(7*h));R=16
 bitcap=(2*R*15*h*N*N).bit_length();codefail=beta0**R+F(R*15*h,2**bitcap)
 assert codefail>=beta0**R and F(R*15*h,2**bitcap)<=F(1,2*N*N)
 volume=sum(comb(ell,w)*3**w for w in range(1,h));normalizer=F(2**(ell+h)-1,2**(2*ell)-1)
 assert volume*normalizer<beta0
 assert F(h*B//2,4*T)==F(1,1152)
 out.append(dict(h=h,B=str(B),ell=ell,J=str(J),T=str(T),t=str(t),b=str(b),payload_qubits=str(h*B//2),
 source_spins=4,exposure_rate='1/1152',soundness_exponent_exact=str(exp_h),
 low_weight_volume=str(volume),single_code_rejection_union_bound=str(volume*normalizer),
 validation_abort_bound=str(failure),validation_abort_float=float(failure),net_size=str(M),eta=str(eta),
 code_attempt_cap=R,per_generator_bit_attempt_cap=bitcap,code_abort_bound=str(codefail)))
res={'scope':'Exact rational parameter/source-exposure certificates; high-h instances not physically executed. Readiness includes role-shortage exponential and learner/key sampler abort beyond displayed validation term.','cases':out}
(ROOT/'fixed_port_parameters.json').write_text(json.dumps(res,indent=2)+'\n')
for row in out:print(row['h'],row['validation_abort_float'],row['exposure_rate'])
