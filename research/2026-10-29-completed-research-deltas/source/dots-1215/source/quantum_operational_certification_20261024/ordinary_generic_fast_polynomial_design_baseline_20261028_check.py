import numpy as np,sympy as s,json,hashlib,itertools,math
from fractions import Fraction
from pathlib import Path
r=Path(__file__).resolve().parent;rng=np.random.default_rng(281014)
# Exact encoder conditioning, independent of source parameters.
rows=[]
for i in range(4):
 z=[s.Rational(0)]*10;z[i]=1;rows.append(z)
for j,(a,b) in enumerate(itertools.combinations(range(4),2)):
 z=[s.Rational(0)]*10;z[a]=z[b]=s.Rational(1,2);z[4+j]=1;rows.append(z)
E=s.Matrix(rows);W=E.T*E/10;tr_inv=s.trace(W.inv());assert tr_inv<4000
exact=0
for dc in [4,13,28,49,100,301]:
 assert Fraction(1,dc*(32*dc-31))>=Fraction(1,33*dc*dc)
 D=10*dc
 assert Fraction(1,4000*33*dc*dc*19)>=Fraction(1,2**22*D*D);exact+=1
assert Fraction(3,256)+Fraction(17,24)<Fraction(3,4)
# Determinant/LDL/coordinate approximation diagnostics on continuous polytopes.
# All maximizations below are exact vertex maximizations for these test bodies,
# not a substitute for the full-CPTP SDP oracle required in the manuscript.
designs=0;updates=0;envcases=0;gridcases=0;regcases=0;maxlevratio=0.;maxregfrac=0.
for D in [2,3,5,8]:
 for rep in range(6):
  z=rng.normal(size=(12*D,D-1));z/=np.maximum(np.linalg.norm(z,axis=1,keepdims=True),1)
  z=np.vstack([np.zeros((1,D-1)),np.eye(D-1)/4,np.eye(D-1),-np.eye(D-1),z]);A=np.c_[np.ones(len(z)),z]
  direction=rng.normal(size=D-1);direction/=np.linalg.norm(direction)
  raw=z@direction;low=raw.min();hi=raw.max();theta=np.r_[(-low+.005)/(hi-low+1),direction/(hi-low+1)]
  q=A@theta;assert min(q)>0 and max(q)<1
  u=np.ones(len(A));last=None
  for tau in [.5,.125,.03125]:
   pi=np.zeros(len(A));pi[:D]=1/D;V=(A.T*(pi/u))@A;V0=V.copy();B=max(np.linalg.norm(A,axis=1));lamstar=np.linalg.eigvalsh(V0)[0]
   Tmax=math.ceil(D*math.log2(B*B/(tau*lamstar)))+1;lamlow=lamstar*(tau*lamstar/B**2)**4/4
   for it in range(Tmax+1):
    C=np.linalg.cholesky(V);ds=np.diag(C)**2;L=C/np.diag(C)[None,:];R=np.linalg.inv(L)
    assert np.linalg.norm(V-L@np.diag(ds)@L.T)<1e-10
    coords=(A@R.T)**2/(u[:,None]*ds[None,:]);flat=np.argmax(coords);idx,j=np.unravel_index(flat,coords.shape);best=coords[idx,j]
    lev=np.einsum('ij,jk,ik->i',A,np.linalg.inv(V),A)/u
    assert np.max(abs(coords.sum(axis=1)-lev))<1e-9
    assert np.linalg.eigvalsh(V)[0]>=lamlow
    # Check the scalar-grid variational identity near each selected optimum.
    ell=(R@A[idx])[j];opt=ell/(ds[j]*u[idx]);delta=1/(1+19*max(np.linalg.eigvalsh(V)))
    zg=round(opt/delta)*delta;ach=2*zg*ell-zg*zg*ds[j]*u[idx]
    assert best-ach<=1+1e-10;gridcases+=1
    if best<8*D:
     assert max(lev)<=10*D*D+1e-9;break
    old=np.linalg.slogdet(V)[1];pi*=1-1/D;pi[idx]+=1/D;V=(A.T*(pi/u))@A
    gain=np.linalg.slogdet(V)[1]-old;assert gain>math.log(2)-1e-10;updates+=1
   else:raise AssertionError('declared determinant cap exhausted')
   designs+=1;maxlevratio=max(maxlevratio,max(lev)/(10*D*D))
   n=math.ceil(2**14*D*(10*D*D)/tau);b=17;est=[]
   ni=np.ceil(n*pi).astype(np.int64)
   for batch in range(b):
    counts=rng.binomial(ni,q);y=np.divide(counts,ni,out=np.zeros(len(ni)),where=ni>0)
    tb=np.linalg.solve(V,A.T@(pi*y/u));est.append(L.T@tb)
   med=np.median(est,axis=0);that=np.linalg.solve(L.T,med)
   pred=A@that;bound=np.sqrt(tau*u)/32
   maxregfrac=max(maxregfrac,float(np.max(abs(pred-q)/bound)))
   assert np.all(abs(pred-q)<=bound+1e-12)
   # Round coefficients as in the theorem, preserving the final 1/16 bound.
   mesh=tau/(128*D*max(B,1));that=np.round(that/mesh)*mesh;pred=A@that
   assert np.all(abs(pred-q)<=np.sqrt(tau*u)/16+1e-12)
   unew=2*pred+2*tau
   assert min(unew)>=tau and max(unew)<=19
   assert np.all(unew>=q) and np.all(unew<=3*q+16*tau)
   regcases+=1;u=unew
# Worst-sign affine envelope and final root conversion, not only sampled errors.
for tau in [2.**-j for j in range(1,15)]:
 for q in [0.,tau/100,tau/2,tau,2*tau,.1,.5,1.]:
  if q>1:continue
  err=math.sqrt(tau*(3*q+32*tau))/16
  for sign in [-1,1]:
   qh=q+sign*err;unew=2*qh+2*tau
   assert unew>=q+tau-1e-14 and unew<=3*q+16*tau+1e-14
   assert abs(math.sqrt(max(qh,0))-math.sqrt(q))<=2*math.sqrt(tau)+1e-14
   envcases+=1
# Exact final risk ledger.
for gam in [Fraction(1,100),Fraction(1,4),Fraction(1)]:
 add=Fraction(3,2)*(1+gam/4)*Fraction(2,256)+Fraction(3,2)*Fraction(125,2**15)
 assert add<Fraction(1,16)
 assert add+Fraction(1,32)+Fraction(1,4)<1
out={'status':'PASS_AUTHOR_GENERIC_FAST_POLYNOMIAL_DESIGN','exact_encoder_inverse_trace':str(tr_inv),'exact_anchor_dimension_cases':exact,'continuous_polytope_design_cases':designs,'determinant_updates':updates,'fractional_quadratic_grid_cases':gridcases,'capped_coordinate_median_cases':regcases,'worst_sign_envelope_cases':envcases,'max_leverage_bound_ratio':maxlevratio,'max_regression_radius_fraction':maxregfrac,'source_sha256':hashlib.sha256((r/'ordinary_generic_fast_polynomial_design_baseline_20261028.md').read_bytes()).hexdigest(),'scope':'Exact constants plus finite-dimensional continuous-polytope design/regression diagnostics. Not a full-CPTP SDP implementation, physical acquisition execution or independent receiving.'}
(r/'ordinary_generic_fast_polynomial_design_baseline_20261028_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
