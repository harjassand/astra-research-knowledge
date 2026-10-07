"""Exact arithmetic for the post-exposure universal delta=3/5 refinement."""
from fractions import Fraction as F
from math import factorial,comb
from pathlib import Path
import json
checks={}
def test(name,val):
    assert val,name
    checks[name]=True
test('sqrt_two_fifths_gt_five_eighths',F(5,8)**2<F(2,5))
phase=F(1024,9375)*F(27,125)*F(9,16)/(F(2,5)**3*F(5,8))
test('phase_bound',phase==F(5184,15625)<F(1,3))
test('exp6_lower250',sum(F(6**j,factorial(j)) for j in range(8))>250)
test('vertical_exponent',-F(5,3)+F(27,80)+1==-F(79,240))
test('sqrt5_gt20_over9',F(20,9)**2<5)
test('vertical_exp_bound',sum(F(79,60)**j/factorial(j) for j in range(5))>F(18,5))
test('vertical_ratio',F(27,20)/F(18,5)==F(3,8))
test('density_margin',1-F(1,3)-F(1,1000)-F(3,8)==F(109,375)>F(1,4))
test('correction_derivative',1-F(91,60)<0)
test('correction_N4_exponent',-F(20,3)+F(27,20)==-F(319,60)<-5)
test('exp5_lower128',sum(F(5**j,factorial(j)) for j in range(8))>128)
test('small_N2_positive',1/(1-F(3,10))<2)
test('small_N3_positive',1/(1-F(2,5))<3)
fixtures=0
for N in range(1,17):
    for ell in range(N+1):
        for j in range(ell+1):
            col=sum(F(comb(ell,j)*comb(N-ell,k-j),comb(N,k))
                    for k in range(N+1) if 0<=k-j<=N-ell)
            assert col==F(N+1,ell+1)
            fixtures+=1
out={'status':'EXACT_CONSTANT_CHECKS_PASS','checks':checks,
     'degree_elevation_column_fixtures':fixtures,'phase_upper_bound':str(phase),
     'scope':'Supporting rational arithmetic; proof09 supplies all-N analytic inequalities.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
