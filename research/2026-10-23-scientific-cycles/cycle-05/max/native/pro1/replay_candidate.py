#!/usr/bin/env python3
"""Exact candidate, boundary kernel, and separable decomposition diagnostics.

Standard library only; no bath truncation. All algebraic checks are rational.
Decimal transcendental numbers are observations; analytic bounds are in the
written proof. This script does not simulate long-time dynamics or compile codes.
"""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import platform
import resource
import sys
import time

root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate_rep',root/'representation/exact_representation.py')
r=importlib.util.module_from_spec(spec); sys.modules[spec.name]=r; spec.loader.exec_module(r)
G=r.G

def run():
    start=time.perf_counter()
    beta=F(1,512); b=beta**2; a=1-b
    delta=b*b/512; q=F(1,2)-delta
    x=q*q; y=q*(1-q)/2; z=(1-q)**2/4; c=-b/128
    u=beta/8; kappa=a*b*b/128
    assert x+4*y+4*z==1 and y>abs(c) and u*u<y
    rho=[[G() for j in range(9)] for i in range(9)]
    rho[0][0]=G(x)
    for i in (1,2):
        for j in (1,2):rho[3*i+j][3*i+j]=G(z)
        rho[3*i][3*i]=rho[i][i]=G(y)
        rho[3*i][i]=rho[i][3*i]=G(c)
    avg=[[G() for j in range(9)] for i in range(9)]
    for color in (1,2):
        for phase in (G(F(1)),G(F(0),F(1)),G(F(-1)),G(F(0),F(-1))):
            local=[]
            for sign in (1,-1):
                m=[[G() for j in range(3)] for i in range(3)]
                for j,d in enumerate((q,(1-q)/2,(1-q)/2)):m[j][j]=G(d)
                m[color][0]=phase*(sign*u)
                m[0][color]=phase.conjugate()*(sign*u)
                local.append(m)
            for i in range(9):
                for j in range(9):
                    avg[i][j]=avg[i][j]+local[0][i//3][j//3]*local[1][i%3][j%3]*F(1,8)
    assert avg==rho
    spectra=[x]+[z]*4+[y+c]*2+[y-c]*2
    assert sum(spectra)==1 and min(spectra)>=F(1,16) and max(spectra)<=F(1,4)
    lower=2*delta-28*c*c-7*delta*delta
    assert lower>F(1,2**45)
    kernel={}
    for sign,cc in [('stabilizing',c),('opposite',-c)]:
        ps={-2:x*a*a,-1:2*a*b*(x+2*y+cc),0:b*b+4*y*a*a-6*cc*a*b,
             1:4*a*b*(y+2*z+cc),2:4*z*a*a}
        pzero=[1-ps[1]-2*y*a*a-ps[2],ps[1]+2*y*a*a,ps[2]]
        pone=[ps[-2]+ps[-1],ps[0],ps[1],ps[2]]
        assert sum(ps.values())==sum(pzero)==sum(pone)==1
        assert min(list(ps.values())+pzero+pone)>=0
        drift=sum(j*p for j,p in ps.items())
        assert drift==(-kappa if sign=='stabilizing' else 3*kappa)
        assert sum(j*p for j,p in enumerate(pzero))==drift+2*a*(x+y*(1+b)+b*cc)
        assert sum((j-1)*p for j,p in enumerate(pone))==drift+x*a*a
        kernel[sign]={'bulk':{str(j):str(p) for j,p in ps.items()},
                      'root':[str(p) for p in pzero], 'level_one':[str(p) for p in pone],
                      'bulk_drift':str(drift)}
    # Exact same-spectrum counterexample coefficients.
    assert 3*kappa>2*delta and 6*kappa>4*delta
    with localcontext() as ctx:
        ctx.prec=100
        dec=lambda f:Decimal(f.numerator)/Decimal(f.denominator)
        theta=dec(kappa)/32
        C=64*(3*theta).exp()/dec(kappa)**2
        M0=(Decimal(2)/3)/(1-theta.exp()/3)
        ent=-sum(dec(p)*dec(p).ln()/Decimal(2).ln() for p in spectra)
        observed={'entropy_bits':str(ent),'rate_bits_per_forward_call':str(ent/2),
                  'theta':str(theta),'C0':str(C),'initial_moment':str(M0),
                  'inverse_theta':str(1/theta),
                  'mean_depth_bound':str(C.ln()/theta),
                  'decimal_precision':ctx.prec,'transcendental_numbers_are_not_interval_certificates':True}
    return {'status':'passed','beta':str(beta),'kappa':str(kappa),
            'density_and_eight_product_decomposition_exact':True,
            'analytic_entropy_excess_lower_bound':str(lower),
            'strict_rate_gain_lower_bound':'1/70368744177664',
            'opposite_coherence_same_spectrum':True,'kernels':kernel,'observed':observed,
            'bath_truncation_used':False,'long_time_dynamics_simulated':False,
            'quantum_encoder_compiled':False,
            'wall_seconds':time.perf_counter()-start,
            'max_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'python':platform.python_version(),
            'scope':'Exact finite identities and observed numbers only; all-time and coding claims use written proofs.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output'); args=p.parse_args()
    s=json.dumps(run(),indent=2)+'\n'
    if args.output:Path(args.output).write_text(s)
    print(s,end='')
