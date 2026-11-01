"""Outward positive scalar prices for the energy-sensitive trial.
Not a full model receiver by itself. No angular integration/sampling oracle.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,hashlib,time
PARENT=Path(__file__).resolve().parent.parent/'retained_state_renewal_clock_20261101'/'receive_clock.py'
PARENT_SHA='6ab77089b94b0052f458644b7c64895f0c7a4fed53c43c2dc5510be770124cac'
if hashlib.sha256(PARENT.read_bytes()).hexdigest()!=PARENT_SHA:raise RuntimeError('accepted retained-clock runtime hash mismatch')
spec=importlib.util.spec_from_file_location('retained_clock_for_matched_scalar',PARENT);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
base=old.base;Unknown=base.Unknown;Roots=old.core.Roots;fs=base.fs

class Intervals(base.Fixed):
 def __init__(self,*args):super().__init__(*args);self.additions=0;self.divisions=0;self.max_stored_bits=0
 def keep(self,a):
  size=max(abs(a[0]).bit_length(),abs(a[1]).bit_length());self.max_stored_bits=max(self.max_stored_bits,size)
  if size>self.limit:raise Unknown('stored positive interval integer bit budget')
  if not 0<=a[0]<=a[1]:raise Unknown('positive interval ordering')
  return a
 def add(self,a,b):self.additions+=1;return self.keep((a[0]+b[0],a[1]+b[1]))
 def div(self,a,b):
  self.divisions+=1
  if b[0]<=0:raise Unknown('strictly positive scalar denominator unresolved')
  lo=self.product(a[0],self.S)//b[1];num=self.product(a[1],self.S);hi=(num+b[0]-1)//b[0]
  return self.keep((lo,hi))
 def power(self,a,n):
  r=(self.S,self.S)
  while n:
   if n&1:r=self.mul(r,a)
   n//=2
   if n:a=self.mul(a,a)
  return r
 def positive_sub(self,a,b):return self.keep((max(0,a[0]-b[1]),max(0,a[1]-b[0])))

class Price:
 def __init__(self,alpha,beta,kappa,H,dmin,*,Nt=1024,Ny=256,L=F(32),T=F(400),precision_bits=512,max_nodes=2000000,max_operations=30000000,max_integer_bits=1000000,max_exp_terms=16384,max_rational_bits=1000000):
  pars=locals().copy();pars.pop('self')
  for k,v in pars.items():
   if k not in ['beta','kappa','H','dmin','L','T']:base.strict_int(v,k)
  for k in ['beta','kappa','H','dmin','T']:base.frac(pars[k],k,True)
  base.frac(L,'L')
  if not 0<=L<T or alpha<4 or precision_bits<32:raise Unknown('finite positive integration window, alpha and precision')
  if (Nt+1)*(Ny+1)>max_nodes:raise Unknown('paid tensor-node budget before array construction')
  self.alpha=alpha;self.beta=beta;self.kappa=kappa;self.H=H;self.dmin=dmin;self.Nt=Nt;self.Ny=Ny;self.L=L;self.T=T;self.ht=(T-L)/Nt;self.hy=F(1,2*Ny);self.vstar=1+kappa
  self.fx=Intervals(precision_bits,max_operations,max_integer_bits,max_exp_terms,1);self.roots=Roots(precision_bits,max_integer_bits);self.rb=base.RationalBudget(max_rational_bits)
  self.rational_powers=0;self.gamma_calls=0;self.y_rows=0;self.nodes=0
  for k in ['beta','kappa','H','dmin','L','T']:self.rb.keep(pars[k])
  if precision_bits*2>max_integer_bits:raise Unknown('fixed precision preallocation integer budget')
  self.sqrt_pi_lower=self.pi_root_lower()
  self.K=self.roots.upper(beta*H/(dmin*self.vstar**3))/(F(alpha)+F(1,2))
  # Exact coefficient formation is scalar/rational work, not hidden angular work.
  self.phi=[];self.coeffs=[];self.f_seed=[];self.f_ratio=[]
  for j in range(Ny+1):
   y=j*self.hy;phi=kappa*(2*y*y-y**4);self.phi.append(phi)
   self.f_seed.append(self.fx.expminus(L*phi/self.vstar));self.f_ratio.append(self.fx.expminus(self.ht*phi/self.vstar))
  self.phi_fx=[self.fx.rat(x)for x in self.phi]
  for j in range(Ny):
   l=j*self.hy;r=(j+1)*self.hy;pp=4*kappa*r*(1-r*r);p2=4*kappa*(1-3*l*l);q=self.hy**3/12
   self.coeffs.append([self.fx.rat(self.rb.keep(x))for x in [q*pp*pp/self.vstar**2,q*p2/self.vstar,q*self.phi[j+1]*pp*pp/self.vstar**2,q*(2*pp*pp+self.phi[j+1]*p2)/self.vstar,q*p2]])
 def ratpow(self,q,n):
  if max(q.numerator.bit_length(),q.denominator.bit_length())*max(1,n)>self.rb.bits:raise Unknown('rational power precheck bit budget')
  self.rational_powers+=1;return self.rb.keep(q**n)
 def pi_root_lower(self):
  def atan(n):
   total=F(0)
   for j in range(32):
    term=F(1,(2*j+1)*n**(2*j+1));total=self.rb.add(total,term if j%2==0 else -term)
   return total,total+F(1,65*n**65)
  al,ah=atan(5);bl,bh=atan(239);pi_lower=self.rb.keep(16*al-4*bh)
  if pi_lower<=0:raise Unknown('positive Machin pi lower bound')
  return self.roots.upper(pi_lower)-F(1,self.fx.S)
 def analytic_J_lower(self,t):
  # Returns a fixed-point LOWER for J=half the full profile integral.
  if t==0:return self.fx.S//2
  at=2*self.kappa*t/self.vstar;X=at/4;gam=self.vstar/(4*self.kappa)
  root_hi=self.roots.upper(at);root_lo=root_hi-F(1,self.fx.S)
  if root_lo<=0:return 0
  ex=self.fx.expminus(X);total=0;half_gamma=F(1);coef=F(1)
  for k in range(4):
   s=F(4*k+1,2);den=1-max(s-1,F(0))/X
   if den>0:
    # X^(s-1)=X^(2k)/sqrt(X), sqrt(X)>=root_lo/2.
    tail=self.fx.times(ex,self.ratpow(X,2*k)*2/(root_lo*den))[1]
    full_lo=self.fx.rat(half_gamma*self.sqrt_pi_lower)[0]
    mom=max(0,full_lo-tail)
    total+=self.fx.times((mom,mom),coef)[0]
   half_gamma*=s*(s+1);coef*=gam/(t*(k+1))
  return self.fx.times((total,total),1/(2*root_hi))[0]
 def row(self,t,f):
  self.y_rows+=1;self.nodes+=self.Ny+1;fx=self.fx;S=fx.S;tf=fx.rat(t);t2=fx.mul(tf,tf)
  g=[fx.mul(p,v)for p,v in zip(self.phi_fx,f)]
  flo=[];fhi=[];glo=[];ghi=[]
  for j,(A,B,C,D,E)in enumerate(self.coeffs):
   fe=fx.mul(f[j],fx.add(fx.mul(A,t2),fx.mul(B,tf)))[1]
   ge=fx.mul(f[j],fx.add(fx.add(fx.mul(C,t2),fx.mul(D,tf)),E))[1]
   ft=fx.times(fx.add(f[j],f[j+1]),self.hy/2);gt=fx.times(fx.add(g[j],g[j+1]),self.hy/2)
   flo.append(max(0,ft[0]-fe));fhi.append(ft[1]+fe);glo.append(max(0,gt[0]-ge));ghi.append(gt[1]+ge)
  A0=[0];Aphi=[0]
  for f0,g0 in zip(fhi,glo):A0.append(A0[-1]+f0);Aphi.append(Aphi[-1]+g0)
  B0=[0]*(self.Ny+1);Bphi=[0]*(self.Ny+1)
  for j in range(self.Ny-1,-1,-1):B0[j]=B0[j+1]+flo[j];Bphi[j]=Bphi[j+1]+ghi[j]
  jl=max(sum(flo),self.analytic_J_lower(t));fx.keep((0,max(A0[-1],Aphi[-1],B0[0],Bphi[0],jl)))
  if jl<=0:raise Unknown('positive J lower unresolved')
  return {'A0hi':A0,'AphiLo':Aphi,'B0lo':B0,'BphiHi':Bphi,'Jlo':jl,'f':f}
 def gamma_survival(self,n,x):
  self.gamma_calls+=1;fx=self.fx;term=fx.expminus(x);total=term
  for j in range(1,n):term=fx.times(term,x/j);total=fx.add(total,term)
  return max(0,total[0]),min(fx.S,total[1])
 def gamma_cdf(self,n,x):
  lo,hi=self.gamma_survival(n,x);return self.fx.S-hi,self.fx.S-lo
 def tails(self):
  fx=self.fx;a=self.alpha;S=fx.S;L=self.L;T=self.T
  # Only upper endpoints are accumulated; shape constants remain exact.
  pf=2*(self.gamma_cdf(a,L)[1]+a*self.gamma_cdf(a+1,L)[1]+self.gamma_survival(a,T)[1]+a*self.gamma_survival(a+1,T)[1])
  rho=(1+F(9,16)*self.kappa)/self.vstar;osc=F(7,16)*self.kappa;z=0
  for k,rising in [(1,F(a)),(2,F(a*(a+1)))]:
   tail=self.gamma_cdf(a+k,rho*L)[1]+self.gamma_survival(a+k,rho*T)[1]
   z+=fx.times((tail,tail),rising/self.ratpow(rho,a+k))[1]
  pz=fx.times((z,z),self.K*osc*osc/32)[1]
  return pf,pz
 def run(self):
  start=time.perf_counter();fx=self.fx;S=fx.S;f=self.f_seed;prev=self.row(self.L,f);surv=self.gamma_survival(self.alpha,self.L);pf=pz0=0
  for i in range(self.Nt):
   t=self.L+(i+1)*self.ht;f=[fx.mul(x,r)for x,r in zip(f,self.f_ratio)];cur=self.row(t,f);new_surv=self.gamma_survival(self.alpha,t)
   W=fx.positive_sub(surv,new_surv);surv=new_surv
   pf+=fx.div((W[1],W[1]),(2*cur['Jlo'],2*cur['Jlo']))[1]
   J4lo=fx.power((cur['Jlo'],cur['Jlo']),4)[0]
   inner=0
   for j in range(self.Ny):
    term1=fx.mul((prev['A0hi'][j+1],)*2,(prev['BphiHi'][j],)*2)[1]
    term2=fx.mul((prev['AphiLo'][j],)*2,(prev['B0lo'][j+1],)*2)[0]
    Dhi=max(0,term1-term2);num=fx.mul((Dhi,Dhi),(Dhi,Dhi))[1]
    den=4*fx.mul((J4lo,J4lo),(f[j+1][0],f[j+1][0]))[0]
    if den<=0:raise Unknown('positive transverse cell denominator unresolved')
    inner+=fx.div((num,num),(den,den))[1]
   t32=t*self.roots.upper(t) if t else F(0)
   inner_hi=fx.times((inner,inner),2*self.hy*t32)[1]
   pz0+=fx.mul((W[1],W[1]),(inner_hi,inner_hi))[1]
   fx.keep((0,max(pf,pz0)));prev=cur
  pf_tail,pz_tail=self.tails();pz=fx.times((pz0,pz0),self.K)[1]+pz_tail;pf+=pf_tail
  return {'P_frozen_upper':F(pf,S),'P_transverse_upper':F(pz,S),'P_total_upper':F(pf+pz,S),'P_frozen_tail_upper':F(pf_tail,S),'P_transverse_tail_upper':F(pz_tail,S),'K_upper':self.K,
   'work':{'tensor_nodes':self.nodes,'rows':self.y_rows,'fixed_operations':fx.operations,'interval_additions':fx.additions,'interval_divisions':fx.divisions,'exponential_calls':fx.exp_calls,'exponential_Taylor_terms':fx.exp_terms,'gamma_survival_calls':self.gamma_calls,'root_calls':self.roots.calls,'largest_root_operand_bound_bits':self.roots.max_bits,'largest_guarded_product_bits':fx.max_guarded_bits,'max_stored_interval_integer_bits':fx.max_stored_bits,'rational_power_calls':self.rational_powers,'pi_rational_operations':self.rb.operations,'max_rational_bits_proxy':self.rb.max_stored_bits},'seconds':time.perf_counter()-start}

if __name__=='__main__':
 import json,sys
 nt=int(sys.argv[1])if len(sys.argv)>1 else 1024;ny=int(sys.argv[2])if len(sys.argv)>2 else 256
 p=Price(128,F(1),F(1),F(4322048),F(1),Nt=nt,Ny=ny)
 r=p.run();out={k:fs(v)if type(v)is F else v for k,v in r.items()}
 Path(f'positive_prices_{nt}_{ny}.json').write_text(json.dumps(out,indent=2)+'\n')
 print({k:base.show(v)if type(v)is F else v for k,v in r.items()},flush=True)
