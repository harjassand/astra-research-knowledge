#!/usr/bin/env python3
"""Exact conditional gradient/product algebra and rational envelope constants."""
from fractions import Fraction as F
from pathlib import Path
import sympy as s,json,math
P=Path(__file__).parent
A,L,E,T=s.symbols('A L E T',positive=True);B=s.Function('b');ll,ee=s.symbols('l e')
b=B(L/T,E/T**3);bl=s.diff(B(ll,ee),ll).subs({ll:L/T,ee:E/T**3});be=s.diff(B(ll,ee),ee).subs({ll:L/T,ee:E/T**3});bll=s.diff(B(ll,ee),ll,2).subs({ll:L/T,ee:E/T**3});ble=s.diff(B(ll,ee),ll,ee).subs({ll:L/T,ee:E/T**3})
f=b+A*E/T**6*bl
assert s.simplify(s.diff(f,A)-E/T**6*bl)==0
assert s.simplify(s.diff(f,L)-(bl/T+A*E/T**7*bll))==0
assert s.simplify(s.diff(f,E)-(be/T**3+A/T**6*(bl+E/T**3*ble)))==0
rows=[(1,1,0),(-1,-1,0),(-1,F(-1,2),0),(1,F(1,2),0),(-1,F(-1,2),0),(1,F(1,2),0),(-1,-1,1),(1,1,-1),(-1,0,-1),(1,0,1),(1,0,0),(-1,0,0)]
b0,b1,g0,g1=s.symbols('b0 b1 g0 g1')
for da,dl,de in rows:
 h=A*E;hp=(A+da)*(E+de);dh=E*da+A*de+da*de
 assert s.expand(hp-h-dh)==0
 assert s.expand((b1+hp*g1/T**6)-(b0+h*g0/T**6)-((b1-b0)+dh*g0/T**6+hp*(g1-g0)/T**6))==0
 assert abs(da)==1 and abs(de)<=1 and abs(dl)<=1
# Small/large l cases prove the displayed continuous derivative envelopes.
assert F(243,10**4)<F(1,25) # K_L squared relative to psi/T², T>=10, l<=1.
assert F(75,16000)<F(1,25) # large l, L/N<=1/4000.
assert F(27,10**2)<F(3,10) # K_E relative to sqrt(psi4)/T³, small l.
assert F(9,4000)<F(9,100) # squared large-l relative coefficient <(.3)^2.
assert F(243,10000**4)<F(49,10000)
assert F(75,16000)<F(49,10000) # practical K_L <=.07 sqrt(psi)/T.
R10=F(10,9)**5;Rbig=F(10000,9999)**5;Pphi=F(1000,999)**2
assert Pphi<F(101,100)
assert F(36,25)*R10<F(5,2)
assert F(107,100)**2*Rbig<F(23,20)
assert 24*Pphi<25
assert 49*8*Pphi<400
assert F(6,5)+F(9,100)<F(13,10)
assert F(107,100)+F(9,10000**2)<F(27,25)
assert F(4,100)+F(1212,17)<72
assert 3*F(5,2)==F(15,2)
assert 3*(25+400)==1275
assert F(21,20)*F(23,20)==F(483,400)
assert 2*21*(25+400)==17850
assert 1275*72==91800 and 17850*72==1285200
assert F(483,400)*F(3,2)==F(1449,800)
assert 1/F(5000)+1/F(10**5)<=1/F(4000) # all L exit endpoints.
# Startup endpoint rectangle exactly includes all enabled changes, including L'=0.
assert F(401,10000)<1
assert F(8*400**3+1,10000**3)<F(1,1000)
# Useful exact v/j values for the finite-N receiver.
examples=[]
for tt in [10000,100000]:
 v=F(1449,800*tt)+F(1285200,tt**3);j=F(27,25*tt)
 examples.append({'T':tt,'N':tt**5,'v_exact':str(v),'v_decimal':float(v),'j_exact':str(j),'j_decimal':float(j)})
out={'status':'PASS_EXACT_FULL_CORRECTED_CLOCK_BRACKET_CONDITIONAL','gradient_identities':3,'actual_product_rows_checked':12,'enabled_row_delta_bounds_checked':12,'rational_derivative_padding_cost_assertions':23,'examples':examples,'conditional_inputs':['Derivative ceilings and smooth l=0 extension on D = cone union startup rectangle','Actual regularized source budget and rate bound through original 4T','All enabled whole jump segments lie in D','Pre-stop L<=N/5000, T>=10000 for practical constants'],'scope':'No generator residual, gate admission or clearance conclusion is asserted.'}
(P/'full_corrected_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
