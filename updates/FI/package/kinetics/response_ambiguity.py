"""Exact finite positive-frequency response ambiguity.
Finitely many perfect regularized responses do not bound the zero-frequency mean
unless global model structure excludes hidden near-zero rates.
"""
from fractions import Fraction as F
import sympy as sp
import json
from pathlib import Path

def main():
    shifts=[F(1),F(2),F(4)];nodes=[F(1),F(2),F(3),F(4)];weights=[F(1,4)]*4
    A=sp.Matrix([[1]*4]+[[sp.Rational(1,x+s) for x in nodes] for s in shifts]);delta=F(1,1000);results=[];checks=0
    responses=[sum(w/(x+s) for x,w in zip(nodes,weights)) for s in shifts]
    baseline=sum(w/x for x,w in zip(nodes,weights))
    for eps in [F(1,100),F(1,10000),F(1,10**8),F(1,10**12)]:
        f=sp.Matrix([1]+[sp.Rational(1,eps+s) for s in shifts]);a=A.inv()*f
        new=[weights[j]-delta*F(a[j]) for j in range(4)]
        assert all(w>0 for w in new);checks+=4
        assert sum(new)+delta==1;checks+=1
        for s,resp in zip(shifts,responses):assert sum(w/(x+s) for x,w in zip(nodes,new))+delta/(eps+s)==resp;checks+=1
        mean=sum(w/x for x,w in zip(nodes,new))+delta/eps
        results.append({'hidden_rate':str(eps),'hidden_mass':str(delta),'adjusted_weights':list(map(str,new)),'mean':str(mean),'mean_float':float(mean),'baseline_mean':str(baseline),'response_values':list(map(str,responses))})
    out={'exact_assertions':checks,'results':results,'scope':'exact family of reversible killed mixtures; not a theorem for fully identified finite-dimensional physical laws'}
    json.dump(out,open(Path(__file__).with_suffix('.json'),'w'),indent=2)
    print(json.dumps({'checks':checks,'baseline':float(baseline),'means':[x['mean_float'] for x in results],'same_responses':list(map(str,responses))},indent=2))
if __name__=='__main__':main()
