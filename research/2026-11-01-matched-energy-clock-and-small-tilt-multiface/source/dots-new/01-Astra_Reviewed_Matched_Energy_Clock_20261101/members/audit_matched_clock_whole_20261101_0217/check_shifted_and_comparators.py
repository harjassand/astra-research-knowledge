from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import sys,json,random,time
A=Path(__file__).resolve().parent;S=A/'replay/matched_energy_clock_constructor_20261101';sys.path.insert(0,str(S));import receive_matched_clock as r
checks=0;cats={};rng=random.Random(11010221);start=time.perf_counter()
def ok(v,k):
 global checks
 assert v,k
 checks+=1;cats[k]=cats.get(k,0)+1

def no(fn,k):
 try:fn()
 except r.Unknown:ok(True,k)
 else:raise AssertionError(k)
N=256;mom=[]
for n in range(N+1):
 coef=F(1);v=F(1,2*n+1)
 for j in range(1,n+1):coef*=F(n-j+1,j)*F(-1,8);v+=coef/F(2*n+2*j+1)
 mom.append(F(1,2**(n+1))*v)

def shifted_ref(alpha,kappa,abar):
 den=2*abar-(1+kappa);c=abar*abar/((1+kappa)*den);b=kappa/den;coef=F(1);val=mom[0]
 for n in range(1,N+1):
  coef*=-b*F(alpha+n-1,n);val+=coef*mom[n]
  if n==N-1:lo=val
 return 2*c**alpha*lo,2*c**alpha*val
full=json.loads((A/'actual_full_recapture.json').read_text());alpha=full['raw_derivative_acquisition']['alpha'];kap=F(full['task']['kappa']);abar=F(full['shifted_current_parameter']);lo,hi=shifted_ref(alpha,kap,abar);interval=full['scaled_shifted_resistance'];ok(F(interval['lower'])<=lo<=hi<=F(interval['upper']),'production shifted resistance encloses independent exact integrated binomial reference')
reference={'lower':str(lo),'upper':str(hi)}
for a,k in [(4,F(2,5)),(5,F(1)),(16,F(7,3)),(128,F(1))]:
 ab=(1+k)*(1-F(1,2*a));obj=r.Shifted(a,k,512,1000,100000,1000000,abar=ab);l,h=obj.slab(128);x,y=shifted_ref(a,k,ab);ok(l<=x<=y<=h,'shifted endpoint/nonunit/odd-alpha exact spatial integral')
 count=1+2*((a.bit_length()-1)+a.bit_count());ok(obj.fixed.operations==129*count and len(obj.cache)==129,'all shifted positive powers and points paid')
 no(lambda obj=obj:obj.point(F(3,4),'shifted'),'shifted slab domain guard')
 no(lambda a=a,k=k,ab=ab:r.Shifted(a,k,512,128,100000,1000000,abar=ab).slab(128),'shifted exact point limit fails one below')
for i in range(500):
 a=rng.randrange(4,130);k=F(rng.randrange(1,30),rng.randrange(1,20));vs=1+k;vb=1+9*k/16;ab=vb+F(rng.randrange(101),100)*(vs-vb);y=F(rng.randrange(101),200);v=1+k*(1-y*y)**2;den=2*ab-v
 ok(den>=1+k/8 and ab*ab/den-v==(ab-v)**2/den>=0,'shifted density bound valid even where slab v exceeds a')
# Strong same-input ordinary witness comparisons, no new model solve.
mean=full['inherited_source_certificate'];ml,mh=(F(mean['basin_mass'][k])for k in ['lower','upper']);rl,rh=(F(mean['slab_resistance'][k])for k in ['lower','upper']);eta=F(full['slab_to_basin_mass_ratio_upper']);C=2+eta;s=eta/C;P=512;beta=F(full['task']['beta']);V=(1+kap)**alpha;dt=F(full['actual_physical_spacing']);n=full['task']['n'];comp=json.loads((S/'same_task_comparison.json').read_text())
def root(q):
 nn=isqrt(q.numerator);dd=isqrt(q.denominator)
 return F(nn,dd)if nn*nn==q.numerator and dd*dd==q.denominator else F(isqrt((q.numerator<<(2*P))//q.denominator)+1,1<<P)
def tvfrom(eps,rate,rate_error=F(0)):
 delta=root(eps*(1+eps))/2+3*eps/8+2*root(s)+rate_error;fx=r.base.Fixed(P,100000,1000000,16384,1);den=1-F(fx.expminus(4*rate*dt)[1],fx.S);return root(C*n*delta*delta/(2*den))+n*eta
parts={k:F(v)for k,v in mean['upper_source_A_components'].items()};bf0=(2*sum(parts.values())-parts['parallel_slab'])/(beta*ml*rl);cs=F(mean['source_S_slab_factor_upper']);eps0=(1+eta/2)*(bf0+eta*cs/2)-1;l=1/(beta*mh*rh);u=1/(beta*ml*rl);rate=(l+u)/2;d=(u-l)/(u+l)
tv0=tvfrom(eps0,rate,3*d/(8*(1-d)));ok(tv0==F(comp['older_received_record_TV_upper']) and tv0>F(1,10),'strong older witness receives SAME newly paid finer scalar information')
Pu=F(full['primal_scalar_price']['P_total_upper']);bf=F(full['normalized_odd_basin_source_inverse_upper']);br=F(full['normalized_odd_slab_residual_inverse_upper']);E=F(full['well_remainder_upper_without_beta']);bfold=(mh/ml)**2*F(mean['parallel_slab_resistance']['upper'])/V+2*E/(ml*ml*V);brscalar=eta*eta*rh*cs/(4*V)
for name,pv,bfv,brv in [('new_energy_trial_with_old_fixed_barrier_current',Pu,bfold,br),('old_scalar_trial_with_new_shifted_current',V/rl,bf,brscalar)]:
 eps=pv*(root(bfv)+root(brv))**2-1;tv=tvfrom(eps,pv/(beta*V*ml));ok(eps==F(comp[name]['epsilon_upper']) and tv==F(comp[name]['record_TV_upper']) and tv>F(1,10),'full alternative primal/dual witness error exactly reproduced '+name)
 ok(comp[name]['literal_physical_spacing']==full['actual_physical_spacing'],'comparators never retime original query')
(A/'shifted_integral_reference.json').write_text(json.dumps(reference,indent=2)+'\n');out={'status':'PASS','checks':checks,'categories':cats,'seconds':time.perf_counter()-start,'scope':'exact shifted-current scalar and paid same-input witness comparison; no independent prior or physical-floor claim'};(A/'shifted_comparator_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
