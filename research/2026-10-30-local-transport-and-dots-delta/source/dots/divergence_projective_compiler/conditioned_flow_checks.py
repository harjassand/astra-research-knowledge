"""Large-time evaluation of the ACTUALLY acquired/normalized n=16 chart.

Read acquired artifacts; do not call the hidden-family constructor. This is
supplemental numerical evidence, not a proof of the all-time analytic bounds.
"""
from pathlib import Path
import json,hashlib
import sympy as s
import mpmath as mp
from strong_decoder import strong_decoder

root=Path(__file__).parent
record=json.loads((root/'quadratic_circuit_results.json').read_text())['runs'][-1]
n=record['dimension']-1;x=s.symbols('x0:'+str(n))
chart=s.Matrix([s.sympify(v) for v in record['chart']]);A=s.Matrix(record['matrix'])
offset=chart.subs(dict.fromkeys(x,0));J=chart.jacobian(x).subs(dict.fromkeys(x,0))
F=(J.inv()*(chart-offset)).applyfunc(s.expand)
R=s.eye(n+1);R[1:,0]=offset;R[1:,1:]=J;M=R.inv()*A*R
assert M==s.Matrix(record['normalized_matrix'])
B=M[1:,1:];c=M[0,1:];row=c*B.inv()
for i in range(0,n,2):
    w=B[i+1,i]
    assert B[i,i]==B[i+1,i+1]==0 and B[i,i+1]==-w and w>0
    assert all(B[j,k]==0 for j in (i,i+1) for k in range(n) if k not in (i,i+1))
inv=strong_decoder(F,x);dag=inv['dag'];roots=inv['roots']
x0=s.Matrix([s.Rational(1,128*n)]*n)
y0=F.subs(dict(zip(x,x0)))
assert sum(v*v for v in y0)<=s.Rational(1,32)**2

def run(t,dps):
    with mp.workdps(dps):
        cv=lambda z:mp.mpf(str(s.numer(z)))/mp.mpf(str(s.denom(z)))
        tt=cv(t);yp=[]
        for j in range(0,n,2):
            theta=cv(B[j+1,j])*tt;co,si=mp.cos(theta),mp.sin(theta)
            a,b=cv(y0[j]),cv(y0[j+1]);yp += [co*a-si*b,si*a+co*b]
        den=1+sum(cv(row[j])*(yp[j]-cv(y0[j])) for j in range(n))
        latent=[v/den for v in yp];values={}
        for i in dag.reachable(roots):
            op,*a=dag.nodes[i]
            if op=='var':v=latent[a[0]]
            elif op=='const':v=mp.mpf(a[0].numerator)/a[0].denominator
            elif op=='add':v=values[a[0]]+values[a[1]]
            else:v=values[a[0]]*values[a[1]]
            values[i]=v
        return [values[r] for r in roots],den

rows=[]
for t in [s.Integer(0),s.Integer(1),s.Integer(10**12),s.Integer(-10**12),s.Integer(10**30)+s.Rational(1,3)]:
    low,d=run(t,80);truth,_=run(t,160);bad,_=run(t,20)
    with mp.workdps(170):
        error=max(abs(a-b) for a,b in zip(low,truth));baderr=max(abs(a-b) for a,b in zip(bad,truth))
        assert error<mp.mpf('1e-40');assert d>=mp.mpf(7)/8;assert max(abs(v) for v in truth)<mp.mpf(1)/8
        rows.append({'rational_time':str(t),'working_decimal_digits':80,'reference_digits':160,
                     'max_absolute_error':str(error),'denominator':str(d),
                     'max_state_absolute_value':str(max(abs(v) for v in truth)),
                     'underprecise_20_digit_error':str(baderr)})
out={'n':n,'checks':rows,'admission':'Numerical supplemental checks; analytic theorem supplies all-time bounds.',
     'source_hashes':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in
                      ['quadratic_circuit_results.json','strong_decoder.py','conditioned_flow_checks.py']}}
(root/'conditioned_flow_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
