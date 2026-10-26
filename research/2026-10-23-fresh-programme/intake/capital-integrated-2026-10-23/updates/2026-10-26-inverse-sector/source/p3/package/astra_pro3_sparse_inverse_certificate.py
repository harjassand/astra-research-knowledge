"""Astra Pro3: two-history rational future-inverse certificates.

Optimization proposes convex weights, while soundness follows from a short
completed-square identity with exact Fraction arithmetic and outward sqrt.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
from math import sqrt
import json
from scipy.optimize import minimize_scalar
from astra_pro3_sector_joint import (Data, vec,native_nonconservative,trace_inverse,add,sub,mul,
    sq,dot,sqrt_upper,rend)
ROOT=Path(__file__).resolve().parent


def certify_weighted_ball(centers, squared_radii, indices, weights, direction):
    assert len(indices)==len(weights) in (1,2)
    assert all(0<=w<=1 for w in weights) and sum(weights,Q(0))==1
    c=vec(*([0]*len(direction)))
    for i,w in zip(indices,weights):c=add(c,mul(w,centers[i]))
    rr=sum((w*(squared_radii[i]-sq(sub(centers[i],c))) for i,w in zip(indices,weights)),Q(0))
    assert rr>=0,rr
    ub=dot(direction,c)+sqrt_upper(sq(direction)*rr)
    return dict(upper=ub,selected=indices,weights=weights,ball_center=c,
                ball_radius_squared=rr,upper_sqrt_outward_precision_bits=40)


def best_rational_two_ball_certificate(history,p,direction,allow_two=True):
    balls=history.balls(p);cs=[a for a,r in balls];r2=[r for a,r in balls]
    all_candidates=[]
    for i in range(len(cs)):
        all_candidates.append(certify_weighted_ball(cs,r2,(i,),(Q(1),),direction))
    if allow_two:
        for i,j in combinations(range(len(cs)),2):
            ci,cj=cs[i],cs[j]
            c0=[float(a) for a in ci];c1=[float(a) for a in cj]
            ri=float(r2[i]);rj=float(r2[j]);dist2=float(sq(sub(ci,cj)))
            dd=[float(a) for a in direction]
            norm2=float(sq(direction))
            def upper(w):
                rsq=w*ri+(1-w)*rj-w*(1-w)*dist2
                return sum(d*(w*x+(1-w)*y) for d,x,y in zip(dd,c0,c1))+sqrt(max(0,rsq)*norm2)
            proposal=minimize_scalar(upper,bounds=(0,1),method='bounded',options={'maxiter':80,'xatol':1e-7})
            quantized=Q(max(0,min(1<<14,round(float(proposal.x)*(1<<14)))),1<<14)
            # Crucially, numerical optimization cannot invalidate the certificate.
            all_candidates.append(certify_weighted_ball(cs,r2,(i,j),(quantized,1-quantized),direction))
    best=min(all_candidates,key=lambda x:x['upper'])
    # All certificates are independently exact-rational algebra after choosing weights.
    assert best==certify_weighted_ball(cs,r2,best['selected'],best['weights'],direction)
    return dict(**best,checked_candidates=len(all_candidates),
                max_integer_bits=max(max(z.numerator.bit_length(),z.denominator.bit_length())
                                     for z in (best['upper'],*best['weights'],best['ball_radius_squared'])))


def task_bounds(history,p,v):
    low=-best_rational_two_ball_certificate(history,p,mul(Q(-1),v))['upper']
    up=best_rational_two_ball_certificate(history,p,v)['upper']
    oldlo=-best_rational_two_ball_certificate(history,p,mul(Q(-1),v),False)['upper']
    oldup=best_rational_two_ball_certificate(history,p,v,False)['upper']
    assert low<=up and oldlo<=low<=up<=oldup
    return dict(lower=low,upper=up,width=up-low,
                best_single_ball_width=oldup-oldlo,
                improvement=(oldup-oldlo)/(up-low) if up>low else 'infinite',
                lower_certificate=best_rational_two_ball_certificate(history,p,mul(Q(-1),v)),
                upper_certificate=best_rational_two_ball_certificate(history,p,v))


def execute():
    history,transfer=trace_inverse()
    xref=vec(Q(3,2),Q(-1));force=native_nonconservative(xref)
    focused=[]
    for direction in (vec(1,0),vec(0,1),vec(1,1),vec(1,-1)):
        cert=task_bounds(history,force,direction)
        assert cert['lower']<=dot(direction,xref)<=cert['upper']
        focused.append(dict(direction=direction,source_aware_true_answer=dot(direction,xref),certificate=cert))
    spatial=Data()
    for x in (vec(0,0),vec(1,0),vec(-1,0),vec(0,1),vec(0,-1),vec(1,1)):
        spatial.acquire(x)
    assert spatial.check()
    controls=[]
    for x in (vec(Q(1,3),Q(1,4)),vec(Q(-1,4),Q(1,3)),vec(Q(1,2),Q(1,2))):
        p=native_nonconservative(x)
        for v in (vec(1,0),vec(0,1)):
            result=task_bounds(spatial,p,v)
            assert result['lower']<=dot(v,x)<=result['upper']
            controls.append(dict(true_x=x,p=p,direction=v,
               two_source_width=result['width'],single_source_width=result['best_single_ball_width'],
               improvement=result['improvement'],
               support_upper_sites=result['upper_certificate']['selected'],
               support_lower_sites=result['lower_certificate']['selected'],
               max_certificate_bits=max(result['upper_certificate']['max_integer_bits'],result['lower_certificate']['max_integer_bits'])))
    out=dict(focused_task_native_calls=history.calls,focused_tasks=focused,
        spatial_bank_native_calls=spatial.calls,spatial_bank_tasks=controls,
        proof='Convex weighted sum of at most two squared ball inequalities plus exact outward square-root supports every returned bound. Numerical search influences only tightness.',
        scope='All bounds outer and universally sound; theorem ensures existence of a sharp at-most-d-active dual under Slater, but selected dyadic certificates may not be sharp.')
    (ROOT/'astra_pro3_sparse_inverse_certificate_results.json').write_text(json.dumps(rend(out),indent=2)+'\n')
    print('focused gains:',[round(float(r['certificate']['improvement']),4) for r in focused])
    print('spatial gains:',[round(float(r['improvement']),4) for r in controls])
    print('max integer bits:',max(r['max_certificate_bits'] for r in controls))
    return out
if __name__=='__main__':execute()
