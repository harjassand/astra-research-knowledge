#!/usr/bin/env python3
"""Certified label-only Poisson-to-fixed-time correlation reconstruction.

Consumes exact moments or explicit moment error. It does not infer a hidden
rate cap or independent stationary preparations from one dependent trace.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import comb
import argparse
import json
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'entropy_witnesses'))
from entropy_cone import log_bounds,exponential_bounds
from quadratic_trace import ceil_sqrt


def rho_upper(cap,clock,bits=80):
    cap,clock=Q(cap),Q(clock)
    if cap<=0 or clock<=0:raise ValueError('positive kinetic cap and independent clock rate required')
    square=4*cap*cap/(clock*clock+4*cap*cap)
    while True:
        rho=ceil_sqrt(square,bits)
        if rho<1:return rho,bits
        bits+=32


def plan(cap,clock,time,tolerance=Q(1,1000),alpha=Q(1,40),max_degree=512):
    cap,clock,time,tolerance,alpha=map(Q,(cap,clock,time,tolerance,alpha))
    if time<0 or not 0<tolerance<1 or not 0<alpha<1:raise ValueError('invalid time, tolerance or risk')
    rho,bits=rho_upper(cap,clock)
    argument=clock*time/2;terms=100+int(argument)
    if terms>10000:raise ValueError('exponential arithmetic budget exceeded; no reconstruction claimed')
    exp_upper=exponential_bounds(argument,terms)[1]
    def directed_error(degree):
        x=exp_upper*rho**(degree+1)/(1-rho)
        scale=2**max(128,40+tolerance.denominator.bit_length())
        z=x*scale
        return Q(-((-z.numerator)//z.denominator),scale)
    degree=0
    while directed_error(degree)>tolerance/2:
        degree+=1
        if degree>max_degree:raise ValueError('polynomial degree budget exceeded; no reconstruction claimed')
    a=clock*time;c=[Q(1)]
    if degree:c.append(-a)
    for n in range(1,degree):c.append(((2*n-a)*c[n]-(n-1)*c[n-1])/(n+1))
    coeff=[sum(((-1 if j%2 else 1)*c[n]*comb(n,j) for n in range(j,degree+1)),Q(0)) for j in range(degree+1)]
    amplification=sum(map(abs,coeff))
    error=directed_error(degree)
    moment_error=tolerance/(2*amplification)
    ell=log_bounds(Q(2*(degree+1))/alpha,120)[1]
    required=2*ell/(moment_error*moment_error)
    starts=-((-required.numerator)//required.denominator)
    return {'cap':str(cap),'clock_rate':str(clock),'physical_time':str(time),
            'tolerance':str(tolerance),'alpha':str(alpha),'degree':degree,
            'polynomial_coefficients':list(map(str,coeff)),
            'operator_error_upper':str(error),'operator_error_preview':float(error),
            'moment_amplification':str(amplification),'moment_amplification_preview':float(amplification),
            'required_each_moment_error':str(moment_error),
            'sufficient_independent_preparations':starts,
            'sufficient_binary_readouts':starts*(degree+1),
            'expected_model_duration':str(Q(starts*degree)/clock),
            'rho_upper':str(rho),'rho_precision_bits':bits,
            'budget_scope':'sufficient Hoeffding budget for this inversion, not a lower bound or a single-record mixing claim',
            'physical_resources_acquired':False}


def reconstruct(plan,moments,moment_error=0):
    coeff=list(map(Q,plan['polynomial_coefficients']));moments=list(map(Q,moments));delta=Q(moment_error)
    if len(moments)!=len(coeff) or delta<0:raise ValueError('supply moments0..degree and a nonnegative valid error')
    center=sum((a*c for a,c in zip(coeff,moments)),Q(0))
    radius=Q(plan['operator_error_upper'])+delta*Q(plan['moment_amplification'])
    return {'center':str(center),'lower':str(center-radius),'upper':str(center+radius),
            'lower_preview':float(center-radius),'upper_preview':float(center+radius),
            'input_contract':'valid uniform moment error and supplied hidden kinetic cap'}


def erlang_plan(cap,time,tolerance=Q(1,1000),alpha=Q(1,40)):
    cap,time,tolerance,alpha=map(Q,(cap,time,tolerance,alpha))
    target=(4*cap*time/tolerance)**2
    k=max(1,-((-target.numerator)//target.denominator))
    ell=log_bounds(2/alpha,120)[1];required=8*ell/(tolerance*tolerance)
    starts=-((-required.numerator)//required.denominator)
    return {'clock_rate':str(Q(k)/time),'intervals_per_preparation':k,
            'sufficient_independent_preparations':starts,'binary_readouts':starts*(k+1),
            'expected_model_duration':str(starts*time),
            'scope':'ordinary positive-coefficient Erlang averaging; high observation bandwidth charged'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cap',required=True);p.add_argument('--clock',required=True);p.add_argument('--time',required=True)
    p.add_argument('--tolerance',default='1/1000');p.add_argument('--alpha',default='1/40');p.add_argument('--max-degree',type=int,default=512)
    p.add_argument('--moments',type=Path);p.add_argument('--moment-error',default='0')
    args=p.parse_args();result=plan(args.cap,args.clock,args.time,args.tolerance,args.alpha,args.max_degree)
    if args.moments:result['reconstruction']=reconstruct(result,json.loads(args.moments.read_text()),args.moment_error)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
