import sympy as s,json,time
from pathlib import Path
root=Path(__file__).parent;j=json.load(open(root/'critical_chart_result.json'));x,y,z=s.symbols('x y z');pp=[s.Poly(s.sympify(a),x,y,z) for a in j['lex_basis']]
uni=s.Poly(pp[-1].as_expr(),z);st=time.time();intervals=s.polys.polytools.intervals(uni,eps=s.Rational(1,10**30));print('isolated',len(intervals),'seconds',time.time()-st,flush=True)
rows=[]
for (a,b),mult in intervals:rows.append(dict(a=str(a),b=str(b),multiplicity=mult,midpoint=float((a+b)/2)))
for poly in pp[:2]:
 co=[c for mon,c in poly.terms() if mon[0]==0 and mon[1]==0];print('coefffloatlog10',max(abs(float(s.log(abs(c),10))) for c in co if c),flush=True)
(root/'critical_chart_isolation.json').write_text(json.dumps(dict(seconds=time.time()-st,real_intervals=rows,scope='Exact univariate root intervals; missing-chart and objective bounds still required.'),indent=2)+'\n')
