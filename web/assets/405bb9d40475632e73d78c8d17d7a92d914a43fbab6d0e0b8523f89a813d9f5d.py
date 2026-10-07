"""Exact penalty sharpness for two self-complementary partition matroids."""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json


def coefficients(n):
    assert n>=2 and n%2==0
    red=[(i,i+1) for i in range(0,n,2)]
    blue=[((i+1)%n,(i+2)%n) for i in range(0,n,2)]
    observed=[0]*(n//2+1)
    for s_choices in product((0,1),repeat=n//2):
        s=set(red[i][c] for i,c in enumerate(s_choices))
        for t_choices in product((0,1),repeat=n//2):
            t=set(blue[i][c] for i,c in enumerate(t_choices))
            observed[len(s&t)]+=1
    expected=[2*comb(n,2*j) for j in range(n//2+1)]
    assert observed==expected
    return observed


def checks():
    records=[{"n":n,"soft_coefficients":coefficients(n)} for n in (2,4,6,8,10)]
    illustrative=[]
    for n in (20,100,1000):
        for penalty in (F(1,64*n*n),F(1,64*n)):
            z=sum((2*comb(n,2*j)*penalty**j for j in range(n//2+1)),F(0))
            illustrative.append({"n":n,"penalty":str(penalty),"hard_probability_float":float(2/z)})
    return {"status":"PASS","scope":"exact finite coefficient checks plus exact closed-form evaluation; asymptotic statement proved separately",
            "records":records,"illustrations":illustrative}


if __name__=="__main__":
    result=checks()
    Path(__file__).with_name('balanced_cycle_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
