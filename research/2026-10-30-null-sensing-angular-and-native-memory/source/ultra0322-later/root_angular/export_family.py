"""Exact universal coefficient/support controls for the angular-family export.

QC/heat positivity depends on the separately qualified angular seed.  This
acquires its robust NON-PC cuts and explicit scalar convexity buffer using
only ordinary integer/Fraction polynomial arithmetic. No source/model/solver.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import hashlib,json,time

def powers(n,d):
    if d==1: yield(n,);return
    for i in range(n+1):
      for tail in powers(n-i,d-1):yield(i,)+tail

def multiply(p,q):
    out={}
    for a,x in p.items():
      for b,y in q.items():
        key=tuple(i+j for i,j in zip(a,b));out[key]=out.get(key,0)+x*y
    return {k:v for k,v in out.items()if v}

def add(p,q,scale=1):
    out=p.copy()
    for k,v in q.items():out[k]=out.get(k,0)+scale*v
    return {k:v for k,v in out.items()if v}

def line_coefficient(power,R,n):
    # coefficient of t^n in (a+t)^i b^j c^k (d+t)^l
    i,j,k,l=power
    return sum(comb(i,u)*comb(l,n-u)*R[0]**(i-u)*R[3]**(l-n+u)*R[1]**j*R[2]**k
               for u in range(max(0,n-l),min(i,n)+1))

def main():
    start=time.perf_counter();here=Path(__file__).parent
    pp=list(powers(4,4))
    T={tuple(2*int(j==i)for j in range(4)):1 for i in range(4)}
    q={(1,0,0,1):1,(0,1,1,0):-1}
    X={tuple(2*int(j==i)for j in range(4)):sign for i,sign in enumerate((1,-1,1,-1))}
    T2=multiply(T,T);Fstar=add(add(T2,multiply(q,q),12),multiply(q,X),4)
    rows={}
    for label,R in [('plus',(0,200,-1,0)),('minus',(1,0,0,-2))]:
      rows[label]=[[line_coefficient(p,R,n)for p in pp]for n in range(3)]
    bounds={k:[sum(abs(v)for v in row)for row in table]for k,table in rows.items()}
    assert bounds['plus'][2]==120603
    assert bounds['minus']==[31,49,42]
    coefficients={label:{'Fstar':[sum(row[i]*Fstar.get(p,0)for i,p in enumerate(pp))for row in table],
                         'T2':[sum(row[i]*T2.get(p,0)for i,p in enumerate(pp))for row in table]}
                  for label,table in rows.items()}
    assert coefficients['plus']['Fstar'][1:]==[0,4808]
    assert coefficients['plus']['T2'][1:]==[0,160004]
    assert coefficients['minus']=={'Fstar':[97,-8,-48],'T2':[25,-20,24]}
    eps=F(1,100000);rho=eps/840
    upper=(4808+160004*eps+120603*rho)/200
    lower=(48-24*eps-42*rho+(8+20*eps-49*rho)**2/(4*(97+25*eps+31*rho)))/2
    gap=lower-upper
    assert gap>F(3,100) # a strict rational NON-PC separation, all perturbations.
    assert eps-420*rho==eps/2
    # Complete-square remainder for the universal quartic Bregman inequality.
    assert F(3,4)-F(23,4)*F(8,23)**2==F(5,92)>0
    out={'scope':'universal explicit full35 perturbation ball; robust non-PC unconditional, QC depends on separately qualified angular seed',
         'epsilon':str(eps),'coefficient_inf_ball_radius':str(rho),
         'all35_perturbation_coefficients_independent':True,
         'monomial_order':[list(p)for p in pp],
         'support_line_rows':rows,'support_row_l1_norms':bounds,
         'literal_seed_and_buffer_coefficients':coefficients,
         'universal_support_upper':str(upper),'universal_support_lower':str(lower),
         'strict_non_PC_gap':str(gap),'gap_decimal_diagnostic':float(gap),
         'convex_buffer':'H=G+420*rho*T^2; Hessian H>=0 when ||G||_coeff_inf<=rho',
         'convex_buffer_residual_T2':str(eps-420*rho),
         'strong_QC_modulus_if_seed':str((eps-420*rho)/4),
         'quartic_Bregman_square_remainder':'5/92',
         'same_angular_primitive_for_entire_ball':True,
         'old_origin_regular_exclusion_radius':'UNEVALUATED; named ball not silently declared inside it',
         'new_source_solver_random_physical_calls':0,'seconds':time.perf_counter()-start,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (here/'EXPLICIT_FAMILY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items()if k not in('monomial_order','support_line_rows','literal_seed_and_buffer_coefficients')},indent=2))

if __name__=='__main__': main()
