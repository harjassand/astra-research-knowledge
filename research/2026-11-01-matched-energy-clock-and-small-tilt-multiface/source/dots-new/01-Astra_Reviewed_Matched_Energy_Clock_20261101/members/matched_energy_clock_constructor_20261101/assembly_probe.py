"""Actual scalar/current assembly probe, not the completed raw public receiver."""
from fractions import Fraction as F
from pathlib import Path
import json,time
import positive_integrals as p
import acquire_derivative as a
core=p.old.core
class Shifted(core.Scalar):
 def __init__(self,*args,abar):super().__init__(*args);self.abar=abar;self.vstar=1+self.kappa
 def point(self,y,kind):
  if kind!='shifted':return super().point(y,kind)
  key=(y,kind)
  if key in self.cache:return self.cache[key]
  if len(self.cache)>=self.max_points:raise p.Unknown('shifted scalar-point budget')
  if not 0<=y<=F(1,2):raise p.Unknown('shifted slab domain')
  v=1+self.kappa*(1-y*y)**2;den=2*self.abar-v
  if den<=0:raise p.Unknown('positive shifted-flux density denominator')
  ans=self.power(self.abar*self.abar/(self.vstar*den),self.alpha);self.cache[key]=ans;return ans
 def slab(self,N):
  h=F(1,2*N);prev=self.point(F(0),'shifted');lo=hi=0
  for j in range(1,N+1):
   cur=self.point(j*h,'shifted');lo+=min(prev[0],cur[0]);hi+=max(prev[1],cur[1]);prev=cur
  return 2*h*F(lo,self.S),2*h*F(hi,self.S)

if __name__=='__main__':
 start=time.perf_counter();raw=p.old.fixture();canonical,acq,H,dmin,alpha=a.acquire(raw)
 beta=kap=F(1);vs=1+kap;vb=1+F(9,16)*kap;abar=vs*(1-F(1,2*alpha));assert vb<=abar<=vs
 mean=core.certify(canonical,quad_relative=F(1,4000),full_ratio=F(2));Ml=F(mean['basin_mass']['lower']);Mh=F(mean['basin_mass']['upper'])
 price=json.load(open('positive_prices_1024_256.json'));Pu=F(price['P_total_upper'])
 ii=Shifted(alpha,kap,512,1000000,30000000,1000000,abar=abar);jl,jh=ii.slab(mean['N'])
 c=mean['constants'];d=F(1,alpha);E=Mh*Mh*(F(1,2)+d)*F(c['G_b_power_upper'])+(vs*vs/(128*kap*kap*(alpha-1)**2*d*d)+F(c['K_upper'])*kap*kap)*F(c['G_1_power_upper'])+(1+F(c['global_transport_correction_upper']))/(16*kap*kap*(alpha-1)**2)
 bF=(Mh/Ml)**2*jh+2*E/(Ml*Ml*vs**alpha);bR=(1/(vs*(1+kap/8)))**alpha/(4*Ml*Ml)
 roots=p.Roots(512,1000000);eps=Pu*(roots.upper(bF)+roots.upper(bR))**2-1
 eta=F(mean['slab_to_basin_mass_ratio_upper']);s=eta/(2+eta);G=roots.upper(eps*(1+eps))/2+3*eps/8;delta=G+2*roots.upper(s)
 fx=p.base.Fixed(512,100000,1000000,16384,1);e=fx.expminus(F(4));TV=roots.upper((2+eta)*10*delta*delta/(2*(1-F(e[1],fx.S))))+10*eta
 rate=Pu/(beta*Ml*vs**alpha)
 out={'status':'ACTUAL_OUTWARD_ASSEMBLY_PROBE_NOT_COMPLETE_PUBLIC_RECEIVING','raw_sha256':acq['actual_raw_sha256'],'H':p.fs(H),'mass_relative_width':p.fs(Mh/Ml-1),'shifted_resistance_scaled':{'lower':p.fs(jl),'upper':p.fs(jh)},'epsilon_upper':p.fs(eps),'ten_record_TV_upper':p.fs(TV),'reference_flip_rate':p.fs(rate),'old_mean_certificate':mean,'source_acquisition':acq,'work':{'inherited_fixed_operations':mean['work']['fixed_operations'],'new_primal_fixed_operations':price['work']['fixed_operations'],'shifted_fixed_operations':ii.fixed.operations,'total_fixed_operations_before_finite_query':mean['work']['fixed_operations']+price['work']['fixed_operations']+ii.fixed.operations,'mass_grid':mean['N'],'shifted_points':len(ii.cache)},'seconds_excluding_previously_executed_primal':time.perf_counter()-start}
 Path('assembly_probe_result.json').write_text(json.dumps(out,indent=2)+'\n')
 print('epsilon',float(eps),'ten-record TV',float(TV),'mean mass rel',float(Mh/Ml-1),'work',out['work'],'seconds',out['seconds_excluding_previously_executed_primal'],flush=True)
