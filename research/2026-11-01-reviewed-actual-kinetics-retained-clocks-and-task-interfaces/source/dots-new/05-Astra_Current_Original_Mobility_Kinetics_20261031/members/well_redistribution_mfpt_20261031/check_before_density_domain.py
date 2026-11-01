from fractions import Fraction as F
from copy import deepcopy
from pathlib import Path
import json,random,math
import sympy as sp
import receive_mfpt as c
checks=0;categories={}
def ok(x,label):
 global checks
 assert x,label
 checks+=1;categories[label]=categories.get(label,0)+1

def unknown(fn,label):
 try:fn()
 except c.Unknown:ok(True,label)
 else:raise AssertionError('unexpected admission: '+label)

# Full-state conditional transport, constant-SPD Lyapunov and moment algebra.
y,z1,z2,beta,kappa,mu=sp.symbols('y z1 z2 beta kappa mu',positive=True)
v=1+kappa*(1-y*y)**2;vp=sp.diff(v,y);U=z1**4+z2**4+17*z1*z1*z2*z2
alpha=sp.Rational(1,2);w=[-vp*z1/(4*v),-vp*z2/(4*v)]
continuity=alpha*vp/v-beta*vp*U
for zi,wi in zip([z1,z2],w):continuity+=sp.diff(wi,zi)-beta*v*wi*sp.diff(U,zi)
ok(sp.simplify(continuity)==0,'full-z conditional continuity, no energy closure')
aa,dm=sp.symbols('alpha dmin',positive=True)
C=sp.sqrt(aa/(beta*(dm/(4*aa))))/(16*mu)
ok(sp.simplify(C-aa/(8*mu*sp.sqrt(beta*dm)))==0,'quartic moment bound exact dimension cancellation')
a=1+sp.Rational(9,16)*kappa
ok(sp.simplify(4*kappa*C/(aa*a**sp.Rational(3,2))-kappa/(2*mu*sp.sqrt(beta*dm)*a**sp.Rational(3,2)))==0,'slab correction symbolic constants')
ok(sp.simplify((kappa/(2*mu*sp.sqrt(beta*dm)*a**sp.Rational(3,2))).subs({kappa:1,beta:1,dm:1})-sp.Rational(32,125)/mu)==0,'ordinary unit-parameter slab constant')
t=sp.symbols('t',nonnegative=True)
for j in range(81):
 tt=F(j,9)
 for kk in [F(1,5),F(1),F(7)]:
  vv=1+kk*(1-tt)**2
  ok(4*kk*tt*(tt-1)+(4+kk)*vv>=4,'ordinary constant-SPD nonexplosion drift inequality')
# Neither Euclidean energy covariance nor drift is constant on an energy level.
a0=2**(-sp.Rational(1,4));U0=z1**4+z2**4
G2=sum(sp.diff(U0,z)**2 for z in [z1,z2]);lap=sum(sp.diff(U0,z,2)for z in [z1,z2])
ok(sp.simplify(U0.subs({z1:1,z2:0})-U0.subs({z1:a0,z2:a0}))==0,'matched exact energy level for nonclosure witness')
ok(sp.simplify(G2.subs({z1:1,z2:0})-G2.subs({z1:a0,z2:a0}))!=0,'ordinary energy covariance genuinely nonclosing')
ok(sp.simplify(lap.subs({z1:1,z2:0})-lap.subs({z1:a0,z2:a0}))!=0,'ordinary energy drift genuinely nonclosing')
H=sp.hessian(U,(z1,z2)).subs({z1:1,z2:1});qvec=sp.Matrix([1,-1])
ok((qvec.T*H*qvec)[0]<0,'admitted positive quartic can be nonconvex')
# Independent exact representatives of global quartic correction and coercivity.
for i in range(161):
 yy=F(i,16)
 for kk in [F(1,10),F(1,2),F(1),F(3),F(10)]:
  vv=1+kk*(1-yy*yy)**2;dd=4*kk*yy*(yy*yy-1)
  ok(dd**4<=1024*max(kk,F(1))**2*vv**5,'global transport power bound, exact squared comparison')
# Exact global tail identities after x=1+t; all displayed coefficients nonnegative.
x=1+t;vx=1+kappa*(1-x*x)**2;dx=sp.diff(1+kappa*(1-y*y)**2,y).subs(y,x)
ok(sp.expand(dx-8*kappa*t-4*kappa*t*t*(t+3))==0,'global derivative lower tail bound')
ok(sp.expand(sp.diff(v,y,2).subs(y,x)-4*kappa*(2+6*t+3*t*t))==0,'convex profile on complete right tail')
for aa in range(4,150):
 d=F(1,aa);a=F(25,16);vd=1+(1-(1+d)**2)**2
 ok(vd<=a,'near-well maximum receives all alpha>=4 examples')
 ok((1+d)*((1+d)**2-1)<=1,'near-well derivative bound')
# Independent finite reversible-chain analogue checks the actual source-to-mean join.
rng=random.Random(1932)
for n in range(2,9):
 for _ in range(12):
  mass=[sp.Rational(rng.randint(1,7),rng.randint(1,7))for i in range(n)];conduct=[sp.Rational(rng.randint(1,7),rng.randint(1,7))for i in range(n)]
  H=sp.zeros(n)
  for i in range(n):
   H[i,i]+=conduct[i]
   if i<n-1:H[i+1,i+1]+=conduct[i];H[i,i+1]-=conduct[i];H[i+1,i]-=conduct[i]
  split=rng.randrange(1,n);fa=sp.Matrix(mass[:split]+[0]*(n-split));fs=sp.Matrix([0]*split+mass[split:]);M=sum(mass[:split]);MS=sum(mass[split:]);inv=H.inv()
  QA=(fa.T*inv*fa)[0];QS=(fs.T*inv*fs)[0];QAS=(fa.T*inv*fs)[0];TA=(QA+QAS)/M
  ja=sp.Rational(0);js=sp.Rational(0);DA=DS=sp.Rational(0)
  for i in range(n):ja+=fa[i];js+=fs[i];DA+=ja*ja/conduct[i];DS+=js*js/conduct[i]
  ok(QA==DA and QS==DS,'source current equals exact 1D Poisson dual')
  ok(QAS>=0 and QAS*QAS<=QA*QS,'positive zero-resolvent cross Cauchy')
  ok(DS<=(MS/M)**2*DA,'source-S current comparison')
  ok(QA/M<=TA<=(1+MS/M)*DA/M,'actual conditional mean sandwich, not capacity')
# Fixed-point integer powers against exact Fractions.
for _ in range(500):
 aa=rng.randrange(4,40);kap=F(rng.randrange(1,10),rng.randrange(1,10));ii=c.Scalar(aa,kap,rng.randrange(32,200),10000,100000,100000)
 b=F(rng.randrange(1,100),rng.randrange(1,100));n=rng.randrange(0,50);lo,hi=ii.power(b,n)
 ok(F(lo,ii.S)<=b**n<=F(hi,ii.S),'outward integer power exact reference')
# Independent rational refined Darboux bounds for every monotone region.
for aa in [4,7,16]:
 for kap in [F(1,3),F(1),F(7,2)]:
  ii=c.Scalar(aa,kap,384,10000,1000000,100000)
  for left,right,kind in [(F(1,2),F(1),'q'),(F(1),F(2),'q'),(F(0),F(1,2),'r')]:
   lo,hi=ii.integrate(left,right,64,kind);h=(right-left)/128;vals=[]
   for j in range(129):
    yy=left+j*h;vv=1+kap*(1-yy*yy)**2;vals.append(vv**(-aa if kind=='q' else aa))
   rl=h*sum((min(vals[j],vals[j+1])for j in range(128)),F(0));rh=h*sum((max(vals[j],vals[j+1])for j in range(128)),F(0))
   ok(lo<=rl<=rh<=hi,'outward quadrature contains exact refined Darboux')
   if kind=='q' and left==1:
    T=F(2);exact=T/(4*aa-1)/(kap*(T*T-1)**2)**aa
    ok(ii.tail(T)>=exact,'full infinite tail rounded upward')
# Source chain types, task budget joining and honest failures.
raw=c.fixture(16);task=dict(quad_relative=F(1,50),full_ratio=F(1000000))
cert=c.certify(raw,**task);ok(c.verify(raw,cert,**task)['status']=='PASS','actual small complete receiving replay')
for key in ['max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits','max_grid','max_points','max_cutoff','max_precision','max_operations','max_integer_bits']:
 for alias in [True,1.0,None,0,-1]:
  tt=dict(task);tt[key]=alias;unknown(lambda tt=tt:c.certify(raw,**tt),'strict external resource types')
for key in ['beta','kappa','quad_relative','full_ratio']:
 for alias in [True,1,1.0,float('nan'),None,F(0),F(-1)]:
  tt=dict(task);tt[key]=alias;unknown(lambda tt=tt:c.certify(raw,**tt),'strict exact task rational types')
for value in ['0','-1','1/1',True,1.0,float('nan')]:
 rr=deepcopy(raw);rr['mobility_program']['value']=value;unknown(lambda rr=rr:c.certify(rr,**task),'actual positive canonical mobility gate')
for key,value in [('max_dimension',1),('max_terms',1),('max_coefficient_bits',1),('max_exponent_entries',1),('max_total_coefficient_bits',1),('max_grid',32),('max_points',1),('max_cutoff',1),('max_precision',1),('max_operations',1),('max_integer_bits',1)]:
 tt=dict(task);tt[key]=value;unknown(lambda tt=tt:c.certify(raw,**tt),'finite budget UNKNOWN')
rr=c.fixture(16,mobility=F(1,1000000000));unknown(lambda:c.certify(rr),'actual slow mobility may exhaust new sufficient full-width bound')
rr=c.fixture(64);unknown(lambda:c.certify(rr),'finite alpha misses requested TOTAL width')
rr=c.fixture(12);unknown(lambda:c.certify(rr,**task),'alpha below finite backend scope')
rr=c.fixture(17);unknown(lambda:c.certify(rr,**task),'noninteger alpha backend scope')
for mutation in ['negative_energy','missing_mobility','extra_field','wrong_actual_program','duplicate','bool_dimension','diagonal_dimension','diagonal_nonpositive','old_radial_model','quadratic']:
 rr=deepcopy(raw)
 if mutation=='negative_energy':rr['energy_terms'][-1]['coefficient']='-20'
 elif mutation=='missing_mobility':del rr['mobility_program']
 elif mutation=='extra_field':rr['claimed_initialization']='point source'
 elif mutation=='wrong_actual_program':rr['mobility_program']['kind']='radial_lift'
 elif mutation=='diagonal_dimension':rr['mobility_program']={'kind':'constant_diagonal','entries':['64']*15}
 elif mutation=='diagonal_nonpositive':rr['mobility_program']={'kind':'constant_diagonal','entries':['64']*15+['0']}
 elif mutation=='old_radial_model':rr['radial_gain']='512'
 elif mutation=='quadratic':rr['energy_terms'][0]['powers'][0]=2
 elif mutation=='duplicate':rr['energy_terms'].append(deepcopy(rr['energy_terms'][0]))
 else:rr['dimension']=True
 unknown(lambda rr=rr:c.certify(rr,**task),'raw actual model rejection: '+mutation)
for mutation in ['floor','modelhash','typed_m','initialization','observable','component','mean_endpoint','mass_endpoint','constant','task','N','proof_method']:
 cc=deepcopy(cert)
 if mutation=='floor':cc['acquisition']['mobility_floor']='2'
 elif mutation=='modelhash':cc['acquisition']['raw_sha256']='0'*64
 elif mutation=='typed_m':cc['acquisition']['m']=16.0
 elif mutation=='initialization':cc['initialization']='arbitrary point start'
 elif mutation=='observable':cc['observable']='cap/mass'
 elif mutation=='component':cc['upper_source_A_components']['far_conditional_tail']='0'
 elif mutation=='mean_endpoint':cc['mean_hitting_time']['upper']='1'
 elif mutation=='mass_endpoint':cc['basin_mass']['lower']='1'
 elif mutation=='constant':cc['constants']['delta']='0'
 elif mutation=='task':cc['task']['beta']='2'
 elif mutation=='N':cc['N']=float(cc['N'])
 else:cc['proof_method']='capacity substitution'
 unknown(lambda cc=cc:c.verify(raw,cc,**task),'certificate full conjunction binding: '+mutation)
cc=deepcopy(cert);cc['seconds']='non-proof';cc['work']={'nonsense':True};cc['mean_hitting_time']['display']=[]
ok(c.verify(raw,cc,**task)['status']=='PASS','diagnostics not silently proof-bearing')
# Extremely large time scale does not turn optional display conversion into a failure.
big=c.certify(raw,beta=F(1<<2000),**task)
ok(big['mean_hitting_time']['display']==[None,None],'large exact time scale has optional safe displays')
# The scalar bound may refuse due to fixed precision/total width; it never loops forever.
unknown(lambda:c.certify(raw,quad_relative=F(1,10**10),full_ratio=F(1000000),max_grid=64),'finite numerical refinement exhaustion')
# Source-bound saved actual cases. External task reconstructed literally.
rows=json.loads(Path('results.json').read_text());diagnostics=[]
import mpmath as mp
mp.mp.dps=80
for row in rows:
 fi=row['fixture'];rr=c.fixture(fi['m'],F(fi['coupling']),F(fi['mobility']),fi['diagonal']);cc=row['certificate'];target=F(11,10)if fi['m']==128 else F(103,100)if fi['m']==256 else F(101,100)
 tt=dict(beta=F(1),kappa=F(1),quad_relative=F(1,1000),full_ratio=target)
 ok(c.verify(rr,cc,**tt)['status']=='PASS','all saved autonomous cases actually recomputed')
 lo,hi=F(cc['mean_hitting_time']['lower']),F(cc['mean_hitting_time']['upper']);ok(hi/lo<=target,'external TOTAL MFPT ratio conjunction')
 # Entire resistance is a polynomial, giving an independent exact rational integral.
 aa=fi['m']//4;t=sp.Symbol('t');poly=sp.Poly((2-2*t+t*t)**aa,t);exact=F(0)
 for (j,),coef in poly.terms():exact+=F(int(coef))*2*F(1,2)**(2*j+1)/(2*j+1)
 ok(F(cc['slab_resistance']['lower'])<=exact<=F(cc['slab_resistance']['upper']),'full resistance independent exact polynomial integral')
 mass=mp.quad(lambda x:(1+(1-x*x)**2)**(-aa),[mp.mpf('.5'),1,mp.mpf('1.25'),2,mp.inf])
 ok(mp.mpf(cc['basin_mass']['lower'].split('/')[0])/mp.mpf(cc['basin_mass']['lower'].split('/')[1])<=mass<=mp.mpf(cc['basin_mass']['upper'].split('/')[0])/mp.mpf(cc['basin_mass']['upper'].split('/')[1]),'high-precision mass diagnostic, not proof')
 diagnostics.append({'m':fi['m'],'mass_display':float(mass),'total_ratio_display':float(hi/lo)})
ok(rows[-1]['certificate']['mean_hitting_time']==rows[-2]['certificate']['mean_hitting_time'],'same certified outer endpoints for distinct angular and diagonal kinetic models, not equal actual means')
# Outward roots compared to exact squared inequalities; no floating oracle.
for _ in range(1200):
 q=F(rng.randrange(1,10**20),rng.randrange(1,10**20));P=rng.randrange(16,160);rt=c.Roots(P,10000);h=rt.upper(q)
 ok(h*h>=q and (h-F(1,1<<P))**2<=q if h>=F(1,1<<P) else h*h>=q,'outward positive root against exact rational square')
for j in range(1,90):
 q=F(j,j+1);rt=c.Roots(32,10000);ok(rt.upper(q*q)==q,'perfect rational square detected exactly')
unknown(lambda:c.Roots(192,100).upper(F(2,3)),'finite scaled root integer budget')
unknown(lambda:c.Roots(32,100).upper(F(1<<101)),'finite root argument budget')
# Model-specific mobility and initialization cannot be changed under a retained certificate.
rr=deepcopy(raw);rr['mobility_program']['value']='65';unknown(lambda:c.verify(rr,cert,**task),'actual mobility input is source-bound')
cc=deepcopy(cert);cc['actual_full_generator']='projected CIR generator';unknown(lambda:c.verify(raw,cc,**task),'reject projected generator substitution')
cc=deepcopy(cert);cc['acquisition']['transverse_SPD_everywhere']=1;unknown(lambda:c.verify(raw,cc,**task),'strict nested bool acquisition binding')
# Isotropic and anisotropic raw programs at the same acquired floor get the same outer bound.
rdiag=c.fixture(16,diagonal=True);cdiag=c.certify(rdiag,**task)
ok(cdiag['mean_hitting_time']==cert['mean_hitting_time'],'same floor gives common enclosure, not exact dynamics')
# Non-square parameter factors exercise actual outward-root producer/receiving path.
cs=c.certify(raw,beta=F(2,3),kappa=F(3,7),**task)
ok(c.verify(raw,cs,beta=F(2,3),kappa=F(3,7),**task)['status']=='PASS','actual irrational-root endpoint path replay')
# Homogeneous density derivative earns the explicit well homotopy.
sv,ss=sp.symbols('v s',positive=True);pi=ss**sp.Rational(1,2)*sp.exp(-beta*ss*U)
hom=sp.diff(pi,ss)-sum(sp.diff(zi*pi/(4*ss),zi)for zi in [z1,z2])
ok(sp.simplify(hom)==0,'homotopy derivative equals exact full-z divergence')
pi_v=sv**sp.Rational(1,2)*sp.exp(-beta*sv*U);pi_2=(2*ss-sv)**sp.Rational(1,2)*sp.exp(-beta*(2*ss-sv)*U)
ok(sp.simplify(pi*pi/pi_v-(ss*ss/(sv*(2*ss-sv)))**sp.Rational(1,2)*pi_2)==0,'exact density ratio with unknown angular normalizer canceled')
vstar=sp.symbols('vstar',positive=True)
ok(sp.factor(sp.diff(ss*ss/(2*ss-sv),ss)-2*ss*(ss-sv)/(2*ss-sv)**2)==0,'parallel density base monotonicity in homotopy parameter')
ok(sp.simplify(sp.diff(sp.log(vstar*vstar/(sv*sv*(2*vstar-sv))),sv)-(3*sv-4*vstar)/(sv*(2*vstar-sv)))==0,'global well base decreases over admitted interval')
# Exact all-point algebra behind the mid/tail constants.
ok(F(5,4)**2<2<F(3,2)**2,'rational proof cutoffs straddle sqrt2')
for _ in range(900):
 kap=F(rng.randrange(1,100),rng.randrange(1,100));vs=1+kap;v=1+kap*F(rng.randrange(0,101),100);s=v+(vs-v)*F(rng.randrange(0,101),100)
 G1=vs*vs/(2*vs-1);ab=1+F(9,16)*kap;Gb=vs*vs/(2*vs-ab)
 ok(s*s/(v*v*(2*s-v))<=G1 and s**4*(2*s-v)>=1,'global exact homotopy norm integrand bound')
 ok(G1<vs and Gb<vs and Gb>=ab,'well density bases strictly cheaper than barrier base')
# New scalar profile receives its own monotonicity and total point budget.
for aa in [4,7,16]:
 for kap in [F(1,3),F(1),F(7,2)]:
  ii=c.Scalar(aa,kap,384,10000,1000000,100000);left=F(0);right=F(1,2);lo,hi=ii.integrate(left,right,64,'rplus');h=(right-left)/128;vals=[];vs=1+kap
  for j in range(129):
   y=left+j*h;v=1+kap*(1-y*y)**2;vals.append((vs*vs/(2*vs-v))**aa)
  rl=h*sum((min(vals[j],vals[j+1])for j in range(128)),F(0));rh=h*sum((max(vals[j],vals[j+1])for j in range(128)),F(0))
  ok(lo<=rl<=rh<=hi,'Rplus outward quadrature contains exact refined rational Darboux')
ii=c.Scalar(4,F(1),192,2,100000,10000);ii.point(F(0),'r');ii.point(F(1),'q');unknown(lambda:ii.point(F(0),'rplus'),'new Rplus points share one total point budget')
for bad in [F(-1),F(3,4)]:unknown(lambda bad=bad:c.Scalar(4,F(1),192,100,10000,10000).point(bad,'rplus'),'Rplus restricted actual slab domain')
for row in rows:
 cc=row['certificate'];fi=row['fixture'];aa=fi['m']//4;Mlo=F(cc['basin_mass']['lower']);Mhi=F(cc['basin_mass']['upper']);Rlo=F(cc['slab_resistance']['lower']);Rhi=F(cc['slab_resistance']['upper']);Plo=F(cc['parallel_slab_resistance']['lower']);Phi=F(cc['parallel_slab_resistance']['upper']);eta=F(cc['slab_to_basin_mass_ratio_upper']);d=F(1,aa);K=F(aa,8);D=F(4*aa);G1=F(4,3);Gb=F(64,39);const=cc['constants'];g1=F(const['G_1_power_upper']);gb=F(const['G_b_power_upper'])
 ok(g1>=G1**aa and gb>=Gb**aa,'independent exact well density powers')
 terms={'parallel_slab':Mhi*Phi,'near_well_longitudinal':Mhi*(F(1,2)+d)*gb,'middle_well_longitudinal':4*g1/(128*(aa-1)**2*d*d*Mlo),'well_vertical_redistribution':K*g1/Mlo,'far_conditional_tail':(1+D)/(16*(aa-1)**2*Mlo)}
 ok(all(F(cc['upper_source_A_components'][k])==v for k,v in terms.items()),'every new source-A correction independently reconstructed')
 UA=sum(terms.values(),F(0));T0hi=Mhi*Rhi;Cs=F(32,125);US=eta*eta*T0hi*(1+Cs)
 ok(F(cc['source_A_inverse_per_mass_upper'])==UA and F(cc['source_S_inverse_per_mass_upper'])==US,'SEPARATE actual source-A and source-S bound fields')
 hi=(1+eta/2)*UA+(eta/2)*T0hi*(1+Cs);ok(F(cc['mean_hitting_time']['upper'])==hi,'new full mean AMGM join reconstructed, not old current ratio')
 cross=eta*(UA+T0hi*(1+Cs))/2;ok(cross*cross>=UA*US,'cross-source AMGM dominates exact squared Cauchy term')
 ok(F(cc['source_S_slab_factor_upper'])>F(101,100),'old mobility slab factor is NOT the new A-current accuracy gate')
 # High-precision Rplus check is diagnostic, the proof uses monotone exact sums.
 plus=2*mp.quad(lambda y:(4/(4-(1+(1-y*y)**2)))**aa,[0,mp.mpf('.5')])
 to_mp=lambda x:mp.mpf(x.numerator)/mp.mpf(x.denominator)
 ok(to_mp(Plo)<=plus<=to_mp(Phi),'high-precision Rplus diagnostic, not proof')
# Mutations specific to the new source split cannot inherit an old certificate.
for field in ['source_A_inverse_per_mass_upper','source_S_inverse_per_mass_upper','source_S_slab_factor_upper','source_cross_AMGM_upper']:
 cc=deepcopy(cert);cc[field]='0';unknown(lambda cc=cc:c.verify(raw,cc,**task),'new separate-current receiving field: '+field)
cc=deepcopy(cert);cc['parallel_slab_resistance']['upper']='1';unknown(lambda:c.verify(raw,cc,**task),'new actual Rplus interval bound')
report={'status':'PASS','checks':checks,'categories':categories,'saved_cases_recomputed':len(rows),'independent_exact_resistance':'all saved cases','floating_mass_checks':'diagnostic only, no certificate premise','diagnostics':diagnostics}
Path('check_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
