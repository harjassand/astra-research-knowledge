"""Executable exact-integer tail/rate budgets; no large circuit matrices constructed."""
from pathlib import Path
import sys,math,json
from fractions import Fraction
Q=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Q/'learned_pauli_algebra_compiler_20261029'))
from negative_binomial_budget_v1 import tail_ratio,budget

def ceildiv(a,b):return (a+b-1)//b
def log_upper(num,den):
 # Integerupperbound onln(den/num), via ln2<1. No floatacceptance.
 c=0
 while num*(1<<c)<den:c+=1
 return c

def typed(B,k0,t):
 h=max(1,(B-1).bit_length());u=max(1,ceildiv(h,k0));s=u*k0//h
 assert 4*t<B and 2*s*h>=u*k0
 return dict(B=B,t=t,h=h,u=u,stripes=s,J=u*B,K=s*h*(B-4*t),padding_per_group=u*k0-s*h)

def fixed(n,k0,en,ed,dn,dd):
 m=2*(n-k0);qnum=1;qden=2
 # Conservativeexplicitversion usingcertifiedlnupperbound.
 B=max(24*m+8,128*log_upper(en,ed)+8);t=B//8
 a,b=tail_ratio(m,t,1,2);assert a*ed<=b*en
 x=typed(B,k0,t);J=x['J'];L=ceildiv(max(2*J,8*log_upper(dn,dd))*qden,qnum)
 rate=Fraction(qnum*x['K'],qden*n*J);assert rate>=Fraction(k0,8*n)
 return dict(n=n,k0=k0,m=m,service_probability='1/2',**x,epsilon_fault=f'{en}/{ed}',exact_fault_tail=float(Fraction(a,b)),cap_error_bound=f'{dn}/{dd}',max_source_calls=L,expected_calls_upper=2*J,expected_normalized_payload_rate=float(rate),certified_rate_lower=float(Fraction(k0,8*n)),worst_case_cap_normalized_rate=x['K']/(n*L),control_error_not_included=True)

def seeded_remote(n,k0,B,qn,qd,en,ed,dn,dd):
 m=2*(n-k0);pn=qd-qn;assert 0<pn*4<=qd
 t=budget(m,pn,qd,en,ed);x=typed(B,k0,t);J=x['J']
 P=max(ceildiv(4*pn*J,qd),6*log_upper(dn,dd));seed=n*P;L=J+P
 a,b=tail_ratio(m,t,pn,qd);assert a*ed<=b*en
 net=x['K']-seed
 return dict(n=n,k0=k0,m=m,service_probability=f'{qn}/{qd}',**x,epsilon_fault=f'{en}/{ed}',exact_fault_tail=float(Fraction(a,b)),seed_abort_bound=f'{dn}/{dd}',probe_cap=P,source_call_cap=L,trusted_seed_ebits=seed,output_ebits=x['K'],conservative_net_ebits=net,conservative_net_rate_per_capped_physical_input=net/(n*L),interface='Resourceversion: trustedpresharedentanglementseed + reference teleportation + classicalfeedback; NOTunassistedcapacity')

def run():
 cases=[fixed(8,4,1,1000,1,1000),fixed(128,64,1,1000000,1,1000000),fixed(128,1,1,1000,1,1000)]
 remote=seeded_remote(128,64,200000,99,100,1,1000000,1,1000000)
 print(json.dumps(dict(fixed_rate_cases=cases,paid_remote_case=remote,scope='Budgetsandintegerchecks only; hugeoutercircuitsnotmaterialized'),indent=2))
if __name__=='__main__':run()
