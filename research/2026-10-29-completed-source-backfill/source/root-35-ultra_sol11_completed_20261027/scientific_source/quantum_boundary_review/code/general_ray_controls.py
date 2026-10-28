"""Exact larger finite-ray endpoints and complete ordinary entropy controls.

No producer imports. A general non-TP direction explicitly pays the nine-
Weyl flag; direct CMI uses the resulting full486-state extension.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import sympy as s
import numpy as np
import mpmath as mp
import json,time
from exact_controls import ROOT,channel,depolarize
from coherent_fixtures import householder,simple,numeric,record,entropy_mp,direct_cmi

def ceil_log2(x):
    x=s.Rational(x);k=0;power=1
    while power*x.q<x.p:k+=1;power*=2
    return k

def acquire(name,C,H,m,M):
    begin=time.monotonic();r=C.rows;d=3*r
    omega=s.Matrix([int(i==j)for i in range(3)for j in range(3)]);p=omega*omega.T/3
    A0=s.kronecker_product(omega*omega.T,C);ell=s.trace((s.eye(9*r)-s.kronecker_product(p,s.eye(r)))*H)
    assert s.trace(H)==1 and 0<ell<=1
    eps=m*ell**2/(2**14*r*r);margin=eps*ell/2;normalizer=3*s.trace(C)+eps
    kappa=M/m;L=ceil_log2(24*r/ell);K=ceil_log2(4*kappa);j=int(s.ceiling(4*K/ell));k=2*L+j+1;old=m/s.Integer(2)**k
    X=A0+eps*H;rho=X/normalizer;nrho=channel(X,r)/normalizer;erho=depolarize(X,r)/normalizer
    physical=s.Matrix(3,3,lambda a,b:sum(H[a*d+i,b*d+i]for i in range(d)))
    uniform=physical==s.eye(3)/3
    exact_seconds=time.monotonic()-begin
    mp.mp.dps=70;entropy_start=time.monotonic()
    delta=-entropy_mp(rho)-entropy_mp(erho)+2*entropy_mp(nrho)
    assert delta>mp.mpf(int((margin/normalizer).p))/int((margin/normalizer).q)
    mp_seconds=time.monotonic()-entropy_start
    # A classical flag is explicit in the A,F,R tensor ordering.
    twirl_start=time.monotonic();flag=1;twirled=numeric(rho)
    if not uniform:
        zeta=-s.Rational(1,2)+s.sqrt(3)*s.I/2
        shift=s.Matrix(3,3,lambda a,b:int(a==(b+1)%3));clock=s.diag(1,zeta,zeta**2)
        average=s.zeros(3);tensor=np.zeros((3,9,d,3,9,d),dtype=complex)
        for a in range(3):
            for b in range(3):
                U=simple(shift**a*clock**b);assert simple(U.H*U)==s.eye(3)
                average+=U*physical*U.H/9
                lift=np.kron(numeric(U),np.eye(d));block=lift@numeric(rho)@lift.conjugate().T/9
                f=3*a+b;tensor[:,f,:,:,f,:]=block.reshape(3,d,3,d)
        assert simple(average)==s.eye(3)/3
        twirled=tensor.reshape(27*d,27*d);flag=9
    cmi,error=direct_cmi(twirled,r*flag)
    assert abs(cmi-np.log(3)-float(delta))<5e-11
    direct_seconds=time.monotonic()-twirl_start
    block=X[:d,d:2*d];square=simple(block*block);outside=square!=s.zeros(d)
    out={'name':name,'r':r,'C':record(C),'H':record(H),'m':str(m),'M_for_old_comparison_only':str(M),
         'trace_H_exact':'1','leakage_exact':str(ell),'new_epsilon':str(eps),'new_raw_Delta_lower':str(margin),
         'new_normalized_CMI_excess_lower':str(margin/normalizer),
         'old_receiver':{'L':L,'K':K,'j':j,'k':k,'epsilon':str(old),'new_epsilon_over_old':str(eps/old)},
         'rational_log_margin':'5/9-1/8192-1/2=4087/73728>0',
         'physical_marginal_H':record(physical),'original_marginal_uniform':uniform,
         'explicit_Weyl_flag_values':flag,'reference_dimension_before':d,'reference_dimension_after':d*flag,
         'full_extension_dimension_for_direct_CMI':9*d*flag,
         'off_diagonal_reference_block_square_nonzero':outside,
         'mp70_normalized_Delta':mp.nstr(delta,65),'direct_CMI_minus_log3':cmi-np.log(3),
         'direct_CMI_identity_error':abs(cmi-np.log(3)-float(delta)),
         'antisymmetric_marginal_error':error,
         'exact_input_receiver_seconds':exact_seconds,'ordinary_mp70_entropy_seconds':mp_seconds,
         'ordinary_flag_construction_and_full_CMI_seconds':direct_seconds,
         'scope':'Exact rational receiver endpoint and matrix inputs; mp/dense entropy values are diagnostics, not certified logarithm intervals. No physical channel acquired.'}
    if name=='outside_reset_closure':
        assert ell==s.Rational(8,9)and eps==s.Rational(1,20736)and margin==s.Rational(1,46656)
        assert margin/normalizer==s.Rational(4,559881)
        expected=eps**2*s.diag(1,1,0)/1296;assert square==expected
        out['exact_nonzero_square']=record(square)
    (ROOT/f'results/general_ray_{name}.json').write_text(json.dumps(out,indent=2)+'\n')
    summary={k:v for k,v in out.items()if k not in ('C','H','physical_marginal_H','exact_nonzero_square')}
    print(json.dumps(summary,indent=2),flush=True)
    return summary

def main():
    Sa=s.zeros(3);Sa[0,1]=Sa[1,0]=1
    star=(s.eye(9)+s.kronecker_product(Sa,s.diag(1,-1,0))/4)/9
    assert min(star.eigenvals())==s.Rational(1,12)
    first=acquire('outside_reset_closure',s.eye(1),star,s.Integer(1),s.Integer(1))
    R=householder(list(range(1,19)))*householder([j*j+j+2 for j in range(1,19)])
    weights=[s.Rational(j+1)for j in range(18)];weights=[x/sum(weights)for x in weights]
    assert R.T*R==s.eye(18)and min(weights)>0
    H=R*s.diag(*weights)*R.T
    second=acquire('arbitrary_nonTP',s.diag(1,4),H,s.Integer(1),s.Integer(4))
    (ROOT/'results/general_ray_summary.json').write_text(json.dumps({'status':'PASS_STRONGER_FINITE_RAY_ENDPOINTS_AND_CMI','rows':[first,second]},indent=2)+'\n')

if __name__=='__main__':main()
