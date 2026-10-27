#!/usr/bin/env python3
"""Exact truth tables proving the smooth quotient-height threshold is sharp.

Uses H=X^2 Z+Y^3+Z^3+XYZ over F2[t]/t^e.  Input polynomials are
manufactured directly from coefficient convolution, independently of the
stationary compiler and its acquired coordinates.
"""
import itertools
import json
from pathlib import Path
import numpy as np


def toggle(poly, monomial):
    if monomial in poly: poly.remove(monomial)
    else: poly.add(monomial)


def polynomial(e):
    result=set()
    for i in range(e):
        j=e-1-2*i
        if 0<=j<e:
            toggle(result,(1<<i)|(1<<(2*e+j)))
            toggle(result,(1<<(e+i))|(1<<(e+j)))
            toggle(result,(1<<(2*e+i))|(1<<(2*e+j)))
        for j in range(e):
            k=e-1-i-j
            if 0<=k<e: toggle(result,(1<<i)|(1<<(e+j))|(1<<(2*e+k)))
    return result


def signed_sum(poly,n):
    table=np.zeros(1<<n,dtype=np.uint8)
    table[list(poly)]=1
    for i in range(n):
        view=table.reshape(-1,2,1<<i)
        view[:,1,:]^=view[:,0,:]
    return (1<<n)-2*int(table.sum())


def run():
    records=[]
    for e in range(1,9):
        h=(e+1)//3;n=3*e
        base=polynomial(e)
        # The new digit is index h, so this noise needs quotient height h+1.
        variables=(0,2) if e%3==1 else (0,1)
        extra=(1<<(variables[0]*e+h))|(1<<(variables[1]*e+h))
        perturbed=base.copy();toggle(perturbed,extra)
        z=signed_sum(base,n);w=signed_sum(perturbed,n)
        expected=1<<(2*e-int(e%3!=0))
        expected_w=expected//2 if e%3==0 else -expected if e%3==1 else 2*expected
        assert (z,w)==(expected,expected_w),(e,z,w,expected,expected_w)
        records.append(dict(e=e,n=n,allowed_quotient_height=h,
            perturbation_quotient_height=h+1,perturbation_polar_rank=2,
            perturbation_variables=list(variables),perturbation_coefficient_index=h,
            signed_base=z,signed_perturbed=w,enumerated_assignments_per_phase=1<<n,
            base_anf=sorted(base),perturbation_anf=[extra]))
    gradient=[]
    for x,y,z in itertools.product([0,1],repeat=3):
        gradient.append(dict(point=[x,y,z],gradient=[y*z,y^(x*z),x^z^(x*y)]))
    assert sum(row['gradient']==[0,0,0] for row in gradient)==1
    assert sum(row['gradient']==[1,0,0] for row in gradient)==0
    output=dict(status='all assertions passed',cases=records,gradient_table=gradient,
        total_truth_assignments=2*sum(1<<(3*e) for e in range(1,9)),
        practical_speed_claim=False)
    Path(__file__).with_name('quotient_height_boundary_results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ['status','total_truth_assignments']}))
    print(json.dumps([{k:r[k] for k in ['e','n','signed_base','signed_perturbed']} for r in records]))


if __name__=='__main__':run()
