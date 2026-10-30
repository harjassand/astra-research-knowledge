"""Root: compact geometric representation of the literal angular candidate.

This is exact coefficient reconstruction, not positivity or a QC theorem.
No solver or scientific source/model execution.
"""
from pathlib import Path
import json,time,hashlib
import sympy as s

def main():
 start=time.perf_counter();base=Path(__file__).resolve().parent
 source=base.parent/'b_angular_repair'
 raw=(source/'ANGULAR_REDUCTION.json').read_bytes(); rr=(source/'PROFILE_CANDIDATE.json').read_bytes()
 red=json.loads(raw);case=json.loads(rr)
 a,b,c,d=s.symbols('a b c d');v=(a,b,c,d);T=a*a+b*b+c*c+d*d
 X=a*a+c*c-b*b-d*d;Y=2*(a*b+c*d);Z=2*(a*d-b*c)
 K=s.Matrix([-c,-d,a,b]);dx=s.Matrix([s.diff(X,z)for z in v]);dy=s.Matrix([s.diff(Y,z)for z in v]);dz=s.Matrix([s.diff(Z,z)for z in v])
 eta_poly=K
 form_xy=Y*dx-X*dy;form_yz=Y*dz-Z*dy
 params={s.Symbol(k):s.Rational(q)for k,q in case['parameters'].items()}
 numerator=s.Matrix([s.expand(s.sympify(q).subs(params))for q in red['primitive_numerator']])
 radial=sum(v[i]*numerator[i]for i in range(4))
 # Exact Euler gauge alpha' = alpha-d[i_A alpha/4], preserving d alpha.
 target=s.Matrix([s.expand(T*numerator[i]-(T*s.diff(radial,v[i])-radial*s.diff(T,v[i]))/4)for i in range(4)])
 assert s.expand(sum(v[i]*target[i]for i in range(4)))==0
 # T^2 times alpha: six odd x,z scalar coefficients in f, plus quadratic p,r.
 fnames=['f_x','f_z','f_xxx','f_xxz','f_xzz','f_zzz']
 fmons=[X*T*T,Z*T*T,X**3,X*X*Z,X*Z*Z,Z**3]
 names=fnames+['p_0','p_xx','p_xz','p_zz','r_0','r_xx','r_xz','r_zz']
 basis=[s.expand(m)*eta_poly for m in fmons]
 for form in(form_xy,form_yz):
  basis.extend(s.expand(m)*form for m in(T*T,X*X,X*Z,Z*Z))
 powers=set()
 for form in [target]+basis:
  for val in form:powers.update(s.Poly(val,*v).monoms())
 powers=sorted(powers)
 mat=[];rhs=[]
 polybasis=[[s.Poly(q,*v)for q in form]for form in basis];polytarget=[s.Poly(q,*v)for q in target]
 for i in range(4):
  for p in powers:
   row=[form[i].coeff_monomial(p)for form in polybasis];value=polytarget[i].coeff_monomial(p)
   if any(row)or value:mat.append(row);rhs.append(value)
 A=s.Matrix(mat);y=s.Matrix(rhs)
 sol,free=A.gauss_jordan_solve(y)
 if free.rows:
  sol=sol.subs({z:0 for z in free})
 assert A*sol==y
 reconstructed=s.zeros(4,1)
 for coeff,form in zip(sol,basis):reconstructed+=coeff*form
 assert all(s.expand(q)==0 for q in reconstructed-target)
 # Pin exact scalar geometry and both the polynomial relation and primitive.
 out={'scope':'exact geometric reconstruction of one rational P5/T angular candidate; positivity separate',
  'source_reduction_sha256':hashlib.sha256(raw).hexdigest(),'source_candidate_sha256':hashlib.sha256(rr).hexdigest(),
  'coordinates':{'T':str(T),'X':str(X),'Y':str(Y),'Z':str(Z),'sphere_identity':str(s.expand(T*T-X*X-Y*Y-Z*Z))},
  'normalization':'x=X/T,y=Y/T,z=Z/T; eta=(-c da-d db+a dc+b dd)/T',
  'alpha':'T^2 [f(x,z) eta+p(x,z)(y dx-x dy)+r(x,z)(y dz-z dy)]',
  'exact_Euler_gauge':'alpha_prime=alpha-d[(i_A alpha)/4]; denominator can become T^2; d alpha unchanged',
  'exact_coefficients':{n:str(z)for n,z in zip(names,sol)},'basis_rank':int(A.rank()),'equations':A.rows,
  'all_four_global_polynomial_identities_exact':True,'seconds':time.perf_counter()-start}
 (base/'COMPACT_HOPF.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
