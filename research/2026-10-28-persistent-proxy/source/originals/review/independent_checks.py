"""Independent exact source-pair and approximate-competitor certificates."""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import json

def matmul(a,b):
    return [[sum((a[i][j]*b[j][k] for j in range(len(b))),F(0))
             for k in range(len(b[0]))] for i in range(len(a))]

def val(x): return {'exact':str(x),'float':float(x)}

def main():
    ell=[[F(2,3) if i==j else F(1,6) for j in range(3)] for i in range(3)]
    first=[F(2,15),F(49,120),F(49,120)]
    target=[first,[(1-v)/2 for v in first],[(1-v)/2 for v in first]]
    u=[[F(0),F(2,5),F(2,5)],
       [F(37,80),F(21,80),F(21,80)],
       [F(37,80),F(21,80),F(21,80)]]
    no_read=matmul(u,ell)
    residual=[[target[i][x]-no_read[i][x] for x in range(3)] for i in range(3)]
    assert all(z>=0 for row in residual for z in row)
    raw=[sum((residual[i][x] for i in range(3)),F(0)) for x in range(3)]
    assert raw==[F(3,40)]*3
    outputs=[]
    for x in range(3):
        zero=F(0)
        for z1 in range(3):
            for z2 in range(3):
                count=int(z1==0)+int(z2==0)
                zero+=ell[z1][x]*ell[z2][x]*(F(13,25),F(17,100),F(0))[count]
        outputs.append(zero)
    assert outputs==first
    common=sum((min(row) for row in target),F(0))
    assert 1-common==F(11,40)
    gap=F(1,4)-F(1,600)
    bounds=[]
    for n in (101,102):
        exponent=2*n*gap*gap
        # Positive Taylor sum lower-bounds exp(exponent), giving an exact
        # rational upper bound on the Hoeffding output-TV certificate.
        lower=sum((exponent**j/F(factorial(j)) for j in range(81)),F(0))
        upper=F(11,40)/lower
        bounds.append({'cheap_calls':n,'exponent':val(exponent),'TV_upper':val(upper)})
    assert bounds[1]['TV_upper']['float']<1e-6
    out={'scope':__doc__,'one_query_raw':list(map(val,raw)),
         'two_copy_output_zero':list(map(val,outputs)),
         'common_mass_raw':val(1-common),'approximate_bounds':bounds,
         'boundary':'Rational source model only. Point-calibrated two-copy operation requires persistent X and iid cheap calls. Approximate comparator uses separated per-call conditional biases. No physical service or novelty inferred.'}
    Path(__file__).with_name('INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'one_query_raw':str(raw[0]),'two_copy':list(map(str,outputs)),
                      'common_raw':str(1-common),'approximate_TV_bounds':[(r['cheap_calls'],r['TV_upper']['float']) for r in bounds]}))

if __name__=='__main__': main()
