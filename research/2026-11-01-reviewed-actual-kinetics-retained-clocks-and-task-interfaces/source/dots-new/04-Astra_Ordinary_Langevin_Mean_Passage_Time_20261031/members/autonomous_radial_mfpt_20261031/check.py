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

# Exact conditional-transport continuity and current-resistance algebra.
y,u,alpha,beta,kappa,gamma=sp.symbols('y u alpha beta kappa gamma',positive=True)
v=1+kappa*(1-y*y)**2;vp=sp.diff(v,y);w=-vp*u/v
log_py=alpha*vp/v-beta*vp*u;log_pu=(alpha-1)/u-beta*v
ok(sp.simplify(log_py+sp.diff(w,u)+w*log_pu)==0,'Gamma conditional continuity equation')
ok(sp.simplify((vp/v)**2*(alpha/(beta*v))/gamma-alpha*vp**2/(beta*gamma*v**3))==0,'current energy beta/gamma factor')
J,Jp,q,f=sp.symbols('J Jp q f')
ok(sp.simplify(Jp+J*log_py+J*(sp.diff(w,u)+w*log_pu)-Jp)==0,'full divergence reduces to source cumulative derivative')
# Radial gain global Lyapunov coefficient is not a free time rescaling.
t=sp.symbols('t',nonnegative=True);cc=1+2*kappa/gamma
coef=8*kappa*t*(t-1)+(gamma+2*kappa)*(1+kappa*(1-t)**2)
ok(sp.expand(coef-(gamma+2*kappa)*(1+kappa*(1-t)**2)-8*kappa*t*(t-1))==0,'gain Lyapunov exact coefficient')
for j in range(81):
 tt=F(j,9)
 for kk in [F(1,5),F(1),F(7)]:
  for gg in [F(1,2),F(1),F(512)]:
   vv=1+kk*(1-tt)**2;d=8*kk*tt*(tt-1)+(gg+2*kk)*vv
   ok(d>=gg,'global gain nonexplosion drift inequality')
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
 rr=deepcopy(raw);rr['radial_gain']=value;unknown(lambda rr=rr:c.certify(rr,**task),'actual radial-gain input gate')
for key,value in [('max_dimension',1),('max_terms',1),('max_coefficient_bits',1),('max_exponent_entries',1),('max_total_coefficient_bits',1),('max_grid',32),('max_points',1),('max_cutoff',1),('max_precision',1),('max_operations',1),('max_integer_bits',1)]:
 tt=dict(task);tt[key]=value;unknown(lambda tt=tt:c.certify(raw,**tt),'finite budget UNKNOWN')
rr=c.fixture(16,gamma=F(1));unknown(lambda:c.certify(rr),'declared gain insufficient for sufficient-width certificate')
rr=c.fixture(64);unknown(lambda:c.certify(rr),'finite alpha misses requested TOTAL width')
rr=c.fixture(12);unknown(lambda:c.certify(rr,**task),'alpha below finite backend scope')
rr=c.fixture(17);unknown(lambda:c.certify(rr,**task),'noninteger alpha backend scope')
for mutation in ['negative_energy','missing_gain','extra_field','wrong_actual_program','duplicate','bool_dimension']:
 rr=deepcopy(raw)
 if mutation=='negative_energy':rr['energy_terms'][-1]['coefficient']='-20'
 elif mutation=='missing_gain':del rr['radial_gain']
 elif mutation=='extra_field':rr['claimed_initialization']='point source'
 elif mutation=='wrong_actual_program':rr['tangent_program']['kind']='constant_identity'
 elif mutation=='duplicate':rr['energy_terms'].append(deepcopy(rr['energy_terms'][0]))
 else:rr['dimension']=True
 unknown(lambda rr=rr:c.certify(rr,**task),'raw actual model rejection: '+mutation)
for mutation in ['gain','modelhash','typed_m','initialization','observable','component','mean_endpoint','mass_endpoint','constant','task','N','proof_method']:
 cc=deepcopy(cert)
 if mutation=='gain':cc['acquisition']['radial_gain']='1'
 elif mutation=='modelhash':cc['acquisition']['raw_sha256']='0'*64
 elif mutation=='typed_m':cc['acquisition']['m']=16.0
 elif mutation=='initialization':cc['initialization']='arbitrary point start'
 elif mutation=='observable':cc['observable']='cap/mass'
 elif mutation=='component':cc['upper_components']['basin_far_radial']='0'
 elif mutation=='mean_endpoint':cc['mean_hitting_time']['upper']='1'
 elif mutation=='mass_endpoint':cc['basin_mass']['lower']='1'
 elif mutation=='constant':cc['constants']['d']='0'
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
 fi=row['fixture'];rr=c.fixture(fi['m'],F(fi['coupling']),F(fi['tangent']),F(fi['radial_gain']));cc=row['certificate'];target=F(11,10)if fi['m']==64 else F(101,100)
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
ok(rows[-1]['certificate']['mean_hitting_time']==rows[-2]['certificate']['mean_hitting_time'],'exact autonomous mean independence on strongly different angular models')
# Equally informed ordinary Gaussian comparator gets identical scalar operation at matched alpha.
q=c.certify(c.fixture(16,p=4),**task);g=c.certify(c.fixture(8,p=2),**task)
ok(q['mean_hitting_time']==g['mean_hitting_time'],'strong ordinary Gaussian comparator receives identical scalar engine')
report={'status':'PASS','checks':checks,'categories':categories,'saved_cases_recomputed':len(rows),'independent_exact_resistance':'all saved cases','floating_mass_checks':'diagnostic only, no certificate premise','diagnostics':diagnostics}
Path('check_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
