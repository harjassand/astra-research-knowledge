from pathlib import Path
import json,math,time,numpy as np
from fractions import Fraction
p=str(Path(__file__).resolve().parent)+'/'
c=json.load(open(p+'mixture_certificate.json'));W=int(c['weight_denominator']);D=int(c['root_denominator']);n=c['n'];mass=0;rows=[]
for row in c['intervals']:
 rows.append(row);mass+=int(row['weight_lower_numerator'])
 residual=Fraction(1)-Fraction(1,2**n)-Fraction(mass,W)
 if residual<Fraction(1,2000000):break
rate_relative=max(Fraction(int(r['upper_numerator'])-int(r['lower_numerator']),int(r['lower_numerator'])) for r in rows)
# Keep exact q; place residual on the first positive component.
probs=[int(r['weight_lower_numerator'])*2**(n-80) for r in rows];probs[0]+=(2**n-1)-sum(probs)
shift=json.load(open(p+'dyadic128_exact.json'))['shift'];rates=[Fraction(int(r['lower_numerator'])+int(r['upper_numerator']),2*D*2**shift) for r in rows]
law=dict(atom_numerator=1,probability_denominator=str(2**n),rates=[{'numerator':str(r.numerator),'denominator':str(r.denominator)} for r in rates],positive_probability_numerators=[str(v) for v in probs],coupling_failure_upper={'numerator':str(residual.numerator),'denominator':str(residual.denominator)},root_relative_bound=float(rate_relative),rounding_relative_bound=(1+2**-12)**129-1)
total_bound=(1+Fraction(1,2**12))**129*(1+rate_relative)-1
law['total_relative_error_bound']={'numerator':str(total_bound.numerator),'denominator':str(total_bound.denominator)}
json.dump(law,open(p+'compact_law.json','w'),indent=2)
# Floating sampler benchmark, deliberately not the finite-bit sampler certificate.
rng=np.random.default_rng(20261015);cdf=np.cumsum(np.array(probs,dtype=float)/2.**n);rr=np.array([float(r) for r in rates]);t=time.perf_counter();N=1000000;v=rng.exponential(size=N)/rr[np.searchsorted(cdf,rng.random(N))];elapsed=time.perf_counter()-t
x=np.load(p+'dyadic128_float.npz');mean=np.dot(x['w'],1/x['x'])/2.**(-n);scale=float(Fraction(int(json.load(open(p+'dyadic128_exact.json'))['rates'][0]),2**shift));mean/=scale
zs=[.1,.3,1,3,10];mc=[dict(z=z,value=float(np.exp(-z*v/mean).mean()),SE=float(np.exp(-z*v/mean).std()/N**.5)) for z in zs]
# Mark-compression ideal expected exposed marks for eps=.05, delta=1e-6.
r=[5.**(-i)*(1+i/(10*n)) for i in range(n)];h=.05/2.05;marks=0;cats=0
for i in range(n):
 kap=1+sum(r[i+1:])/(2*r[i]);M=math.ceil(6*kap/h**2*math.log(4*n/1e-6));a=2.**(n-i-1);em=-a*math.expm1(-M/a);marks+=em;cats+=em*(n-i-1)
out=dict(components=len(rows),certified_residual=float(residual),root_relative_bound=float(rate_relative),exact_atom=2.**-n,one_million_float_draw_seconds=elapsed,empirical_transforms=mc,original_sampler_expected_marks=marks,original_sampler_expected_nontrivial_categorical_draws=cats)
json.dump(out,open(p+'benchmark.json','w'),indent=2);print(out)
