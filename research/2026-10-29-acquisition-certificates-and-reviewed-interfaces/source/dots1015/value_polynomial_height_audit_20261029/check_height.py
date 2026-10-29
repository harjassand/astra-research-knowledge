import sympy as s, json, math,sys,hashlib
from pathlib import Path
sys.set_int_max_str_digits(0)
r=Path('producer-workspace/quaternion_algebraic_completion_20261029');o=Path(__file__).parent
j=json.loads((r/'input.json').read_text());expected=json.loads((r/'value_polynomial_height_bound.json').read_text())
q=s.symbols('q0:4');F=sum(s.Rational(c)*s.prod(x**a for x,a in zip(q,e)) for e,c in zip(j['exponents'],j['perturbed']))
D=4*s.ilcm(*[s.Rational(c).q for c in j['perturbed']]);Q=sum(x*x for x in q)
a=[s.Poly(D*s.diff(F,x)/4,*q).as_dict() for x in q];b=[s.Poly(-D*Q*x,*q).as_dict() for x in q]
assert all(c.q==1 for d in a+b for c in d.values())
S=[sum((abs(aa.get(e,0))+abs(bb.get(e,0)))**2 for e in set(aa)|set(bb)) for aa,bb in zip(a,b)]
mons=[(i,j,k,9-i-j-k) for i in range(10) for j in range(10-i) for k in range(10-i-j)]
idx={e:i for i,e in enumerate(mons)};counts=[0]*4;M=[[0]*len(mons) for _ in mons]
for row,e in enumerate(mons):
 v=next(i for i,t in enumerate(e) if t>=3);counts[v]+=1
 shift=list(e);shift[v]-=3
 for exp,c in a[v].items():M[row][idx[tuple(x+y for x,y in zip(shift,exp))]]=int(c)
p=1000000007
from sympy.polys.matrices import DomainMatrix
det=int(DomainMatrix.from_Matrix(s.Matrix(M)).convert_to(s.GF(p)).det())%p
W=math.prod(int(x)**n for x,n in zip(S,counts));h=math.isqrt(W);h+=h*h<W;H=2**40*h
assert str(D)==expected['common_scale'];assert list(map(str,S))==expected['row_l2_squared_bounds'];assert counts==expected['row_counts'];assert str(H)==expected['primitive_coefficient_height_bound'];assert str(2*H*H)==expected['required_crt_modulus_strictly_exceeds'];assert det==expected['full_matrix_det_at_lambda0_modp']
out={'independent_row_construction':True,'dimension':len(mons),'D':int(D),'counts':counts,'S':list(map(str,S)),'full_det_modp':det,'H_bits':H.bit_length(),'threshold_bits':(2*H*H).bit_length(),'all_matches':True}
(o/'height_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
