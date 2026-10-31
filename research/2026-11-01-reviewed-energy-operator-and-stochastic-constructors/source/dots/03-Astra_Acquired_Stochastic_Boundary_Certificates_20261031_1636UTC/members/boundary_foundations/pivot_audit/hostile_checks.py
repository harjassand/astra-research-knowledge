#!/usr/bin/env python3
"""Independent challenges of frozen pivot-star implementation; no simulations."""
import importlib.util, pathlib, hashlib, json
from fractions import Fraction as F
from math import prod
import sympy as S
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('frozen_pivot',HERE/'pivot_lift.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

def independently_verify_tail(rec,cert):
    if cert['finite_shells']:return True
    a,z=S.symbols('a z');num=S.sympify(cert['tail_numerator']);den=S.sympify(cert['tail_denominator'])
    H=S.sympify(cert['H']);R=cert['R']
    assert S.cancel(num/den-H-1)==0
    nc=S.Poly(num.subs(a,z+R),z).all_coeffs();dc=S.Poly(den.subs(a,z+R),z).all_coeffs()
    assert list(map(str,nc))==cert['shifted_numerator_coeffs']
    assert list(map(str,dc))==cert['shifted_denominator_coeffs']
    assert all(q<=0 for q in nc) and any(q<0 for q in nc)
    assert all(q>=0 for q in dc) and dc[-1]>0
    assert R>=max(2,cert['M']+1)
    # Bind the rational-function identity to actual integer generator values.
    pi=rec['pivot'];n=len(rec['species'])
    for av in [R,R+1,2*R,3*R+1]:
        x=[0]*n;x[pi]=av;V,LV=p.exact_generator(rec,cert,tuple(x))
        assert S.Rational(LV.numerator,LV.denominator)/S.Rational(V.numerator,V.denominator)==H.subs(a,av)
    return True

def check_case(name,species,raw,t=F(2)):
    rec=p.recognize(species,raw);assert rec['accepted'],(name,rec)
    cert=p.construct(rec,t);independently_verify_tail(rec,cert)
    if cert['finite_shells']:
        assert all(sum(s)==sum(u) for s,u,k in rec['reactions'])
        return {'name':name,'finite_shells':True}
    states=0;pi=rec['pivot'];n=len(species)
    # Corner and layer checks, including a=0 and exact B threshold endpoints.
    for av in range(cert['R']+3):
        for totalb in [0,1,2,7,31,100]:
            if n==1 and totalb:continue
            allocations=[([totalb]+[0]*(n-2))] if n>=2 else [[]]
            if n>=3:allocations += [[0]*(n-2)+[totalb],[totalb//2,totalb-totalb//2]+[0]*(n-3)]
            for bs in allocations:
                x=[];bi=iter(bs)
                for i in range(n):x.append(av if i==pi else next(bi))
                V,LV=p.exact_generator(rec,cert,tuple(x));states+=1
                if av==0 and cert['zero_face_conservative']:
                    assert LV==0
                    continue
                assert LV<=-cert['epsilon']*V+cert['foster_C'],(name,x,cert)
    for row in cert['exceptions']:
        if n==1:continue
        av=row['a'];B=row['B']
        for bsum in [max(0,B),max(0,B+1),max(0,B+20)]:
            x=[0]*n;x[pi]=av;j=next(i for i in range(n) if i!=pi);x[j]=bsum
            V,LV=p.exact_generator(rec,cert,tuple(x));states+=1
            assert LV/V<=row['H']-row['b_slope_min']*bsum
            if bsum>B:assert LV/V<=-cert['epsilon']
    return {'name':name,'finite_shells':False,'R':cert['R'],'radius_trials':cert['radius_trials'],
            'exact_corner_layer_states':states,'epsilon':str(cert['epsilon']),
            'C_numerator_bits':cert['foster_C'].numerator.bit_length()}

def main():
    original=json.loads((HERE/'pivot_lift_results.json').read_text())
    raw=[(tuple(s),tuple(u),F(k)) for s,u,k in original['example_reactions']]
    rec=p.recognize(original['example_species'],raw);cert=p.construct(rec)
    assert json.loads(json.dumps(cert,default=p.encode))==original['certificate']
    cases=[]
    cases.append(check_case('frozen_three_species_non_CB',original['example_species'],raw))
    # No zero complex; a=0 supports a genuinely moving finite B/C shell.
    r=[((2,0,0),(4,0,0),F(3,5)),((4,0,0),(2,0,0),F(5,7)),
       ((2,0,0),(1,1,0),F(2,3)),((1,1,0),(2,0,0),F(4,5)),
       ((2,0,0),(1,0,1),F(1,2)),((1,0,1),(2,0,0),F(7,8)),
       ((0,1,0),(0,0,1),F(3,4)),((0,0,1),(0,1,0),F(5,6))]
    cases.append(check_case('no_zero_core_nonabsorbing_extinction_face',['A','B','C'],r,F(3,2)))
    rr=p.recognize(['A','B','C'],r);cc=p.construct(rr,F(3,2))
    assert any(s[0]==u[0]==0 and s!=u for s,u,k in rr['reactions'])
    assert p.exact_generator(rr,cc,(0,20,10))[1]==0
    r=[((0,0,0),(4,0,0),F(2,3)),((4,0,0),(0,0,0),F(3,7)),
       ((2,0,0),(1,1,0),F(5,4)),((1,1,0),(2,0,0),F(2,5)),
       ((2,0,0),(1,0,1),F(3,2)),((1,0,1),(2,0,0),F(4,7)),
       ((0,5,2),(0,4,3),F(8,9)),((0,4,3),(0,5,2),F(11,10))]
    cases.append(check_case('four_particle_core_seventh_order_neutral',['A','B','C'],r,F(3,2)))
    r=[((0,0),(1,0),F(3,5)),((1,0),(0,0),F(2,3)),
       ((2,0),(1,1),F(2,5)),((1,1),(2,0),F(3,7))]
    cases.append(check_case('linear_core_fractional_c',['A','B'],r,F(4,3)))
    cases.append(check_case('one_species_no_star',['A'],[((0,),(5,),F(2,3)),((5,),(0,),F(4,7))],F(3,2)))
    cases.append(check_case('empty_core_finite_shells',['A','B'],[((2,0),(1,1),1),((1,1),(2,0),2)]))
    # Preserve full weak reversibility but remove B's direct star reverse.
    missing=[r for r in raw if not(r[0]==(1,1,0) and r[1]==(2,0,0))]
    missing.append(((1,1,0),(1,0,1),1))
    assert p.weak_reversible([(s,u) for s,u,k in missing])
    assert not p.recognize(['A','B','C'],missing)['accepted']
    # Preserve N but change A by a non-star rule; must fail raw acquisition.
    nonneutral=raw+[((1,1,0),(0,2,0),1),((0,2,0),(1,1,0),1)]
    assert not p.recognize(['A','B','C'],nonneutral)['accepted']
    print(json.dumps({'frozen_source_sha256':hashlib.sha256((HERE/'pivot_lift.py').read_bytes()).hexdigest(),
      'frozen_theorem_sha256':hashlib.sha256((HERE/'PIVOT_STAR_THEOREM.md').read_bytes()).hexdigest(),
      'original_certificate_exactly_reproduced':True,'cases':cases,
      'missing_direct_reverse_despite_global_WR_rejected':True,
      'N_conserving_but_pivot_changing_extra_rejected':True,
      'finite_checks_are_challenges_not_proof':True},indent=2))
if __name__=='__main__':main()
