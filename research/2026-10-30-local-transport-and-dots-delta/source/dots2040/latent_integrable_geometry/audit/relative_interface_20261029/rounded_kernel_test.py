import sympy as S, mpmath as mp, json
from pathlib import Path
mp.mp.dps=160
x=S.symbols('x'); q=256; h=mp.mpf(2)**-10
F=(x*x-4)*(x*x-1)
def circ(t):
 c=mp.cos(t);return c,mp.sin(t)*mp.sqrt(4-c*c)
def dist(a,b):return abs(mp.e**(1j*a)-mp.e**(1j*b))
def roundq(v):return S.Rational(int(mp.nint(v*2**q)),2**q)
records=[]
for label,t,t0 in [('near_conjugate_60',-mp.pi/2+mp.mpf(2)**-60,mp.pi/2),('exact_conjugate',-mp.pi/2,mp.pi/2),('branch_edge',mp.mpf(0),mp.mpf(0)),('opposite_edge',mp.pi,mp.mpf(0))]:
 selected=[]
 for a in [t,t,-t0]:
  for k in range(3):
   b=a+8*k*h
   if all(dist(b,c)>2*h for c in selected):selected.append(b);break
  else:raise AssertionError('candidate exhaustion')
 rows=[]
 for a in selected:
  xx,yy=circ(a); rows.append([S.Integer(1),roundq(xx),roundq(xx*xx),roundq(yy)])
 mat=S.Matrix(rows);v=mat.nullspace()[0];v=v/max(abs(z) for z in v)
 A=v[0]+v[1]*x+v[2]*x*x; B=v[3];P=S.Poly(A*A-F*B*B,x)
 roots=S.polys.polytools.intervals(P,eps=S.Rational(1,2**100),all=True)
 # nroots is a numerical diagnostic only; exact interval isolation above certifies multiplicities.
 rr=S.nroots(P,n=95,maxsteps=2000)
 pts=[]
 for r in rr:
  xx=mp.mpc(str(S.re(r)),str(S.im(r)));yy=-(mp.mpf(str(S.N(v[0],155)))+mp.mpf(str(S.N(v[1],155)))*xx+mp.mpf(str(S.N(v[2],155)))*xx*xx)/mp.mpf(str(S.N(B,155)))
  pts.append((xx,yy))
 assigned=[];errors=[]
 for a in selected:
  xx,yy=circ(a);j=min((j for j in range(4) if j not in assigned),key=lambda j:abs(pts[j][0]-xx)+abs(pts[j][1]-yy));assigned.append(j);errors.append(abs(pts[j][0]-xx)+abs(pts[j][1]-yy))
 residual=[]
 vv=[mp.mpf(str(S.N(z,155))) for z in v]
 for a in selected:
  xx,yy=circ(a);residual.append(abs(vv[0]+vv[1]*xx+vv[2]*xx*xx+vv[3]*yy))
 records.append(dict(case=label,rank=mat.rank(),coefficient_bits=max(max(abs(int(z.p)).bit_length(),int(z.q).bit_length()) for z in v),min_input_chord=float(min(dist(a,b) for j,a in enumerate(selected) for b in selected[j+1:])),max_residual=str(max(residual)),max_selected_curve_error=str(max(errors)),finite_degree=P.degree(),root_multiplicities=[m for _,m in roots[0]]+[m for _,m in roots[1]],remaining_root_index=list(set(range(4))-set(assigned))[0]))
 assert max(errors)<mp.mpf(2)**-60
out={'scope':'Exact rational rounded kernel and certified polynomial isolation; numerical same-sheet matching diagnostics, not full arbitrary-genus arithmetic implementation','q':q,'separation_h':str(h),'cases':records}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
