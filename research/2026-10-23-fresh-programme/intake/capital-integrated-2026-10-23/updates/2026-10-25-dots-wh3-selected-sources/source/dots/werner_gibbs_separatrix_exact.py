import sympy as s,json
x=s.symbols('x',positive=True);star=1+s.sqrt(3)
phi=(x**4+8*x)/(3*(x*x+2)**2)
assert s.simplify(phi.subs(x,star)-s.sqrt(3)/6)==0
assert s.simplify(s.diff(phi,x).subs(x,star))==0
assert s.simplify(s.diff(phi,x,2).subs(x,star))>0
assert s.factor(x**3-3*x*x+2)==(x-1)*(x*x-2*x-2)
assert s.simplify((s.sqrt((x**3+2)/3)).subs(x,star)-star)==0
out={'fixedpoint':'1+sqrt(3)','objective':'sqrt(3)/6','objective_second_derivative':str(s.simplify(s.diff(phi,x,2).subs(x,star))),'update_multiplier':'(1+sqrt(3))/2','full_stationarity':'follows exact self-consistency X=W3(Y), not only scalar derivative','scope':'Exact Werner invariant family; global upper bound remains open.'}
print(json.dumps(out,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(out,indent=2)+'\n')
