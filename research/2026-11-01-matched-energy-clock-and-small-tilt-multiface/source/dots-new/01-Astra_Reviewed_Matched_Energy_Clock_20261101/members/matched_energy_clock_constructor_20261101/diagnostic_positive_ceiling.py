"""FLOAT diagnostic of conservative grid formulas, NOT an interval certificate."""
import numpy as np
from scipy.special import gammainc,gammaincc,gamma
from math import factorial
from scipy.integrate import quad
import json,time

def run(nt=1024,ny=256,alpha=128,beta=1.,kappa=1.,L=32.,T=400.):
 start=time.perf_counter();vstar=1+kappa;b=.5;h=b/ny
 ys=np.linspace(0,b,ny+1);tt=np.linspace(L,T,nt+1)
 phi=kappa*(2*ys**2-ys**4);pp=4*kappa*ys*(1-ys**2);pp2=4*kappa*(1-3*ys**2)
 f=np.exp(-tt[:,None]*phi[None,:]/vstar);aa=tt[:,None]/vstar
 # Local trapezoid SECOND DERIVATIVE remainder, not a value-only quadrature.
 ferr=f[:,:-1]*(aa**2*pp[None,1:]**2+aa*pp2[None,:-1])*h**3/12
 gerr=f[:,:-1]*(pp2[None,:-1]+2*aa*pp[None,1:]**2+phi[None,1:]*(aa**2*pp[None,1:]**2+aa*pp2[None,:-1]))*h**3/12
 ftrap=(f[:,:-1]+f[:,1:])*h/2;gtrap=(phi[None,:-1]*f[:,:-1]+phi[None,1:]*f[:,1:])*h/2
 flo=np.maximum(0,ftrap-ferr);fhi=ftrap+ferr;glo=np.maximum(0,gtrap-gerr);ghi=gtrap+gerr
 def pref(a):return np.concatenate([np.zeros((nt+1,1)),np.cumsum(a,axis=1)],axis=1)
 def suff(a):return np.concatenate([np.cumsum(a[:,::-1],axis=1)[:,::-1],np.zeros((nt+1,1))],axis=1)
 A0hi=pref(fhi);AphiLo=pref(glo);B0lo=suff(flo);BphiHi=suff(ghi)
 Jlo=flo.sum(axis=1);Jhi=fhi.sum(axis=1)
 # A positive Taylor LOWER bound alone suffices: no asymptotic/remainder oracle.
 at=2*kappa/vstar*tt;xx=b*b*at;gam=vstar/(4*kappa);jclosed=np.zeros_like(tt)
 for kk in range(4):
  ss=2*kk+.5;den=1-max(ss-1,0)/xx
  tail=np.where(den>0,np.exp(-xx)*xx**(ss-1)/np.maximum(den,1e-300),gamma(ss))
  moment=np.maximum(0,gamma(ss)-tail)
  jclosed+=(gam/tt)**kk/factorial(kk)*moment
 jclosed/=np.sqrt(at)
 Jlo=np.maximum(Jlo,jclosed/2)
 # Future exact integer-Gamma bin masses; present scipy values are diagnostic.
 masses=gammaincc(alpha,tt[:-1])-gammaincc(alpha,tt[1:])
 frozen=np.sum(masses/(2*Jlo[1:]))
 # 1/J_full <= 2sqrt(1+t) <=2(1+t) controls omitted tails.
 frozen_tail=2*(gammainc(alpha,L)+alpha*gammainc(alpha+1,L)+gammaincc(alpha,T)+alpha*gammaincc(alpha+1,T))
 frozen+=frozen_tail
 # D is a positive double integral and decreases in t. These left/right
 # cumulatives are separately summed, never total-minus-prefix near a tail.
 Dhi=np.maximum(0,A0hi[:-1,1:]*BphiHi[:-1,:-1]-AphiLo[:-1,:-1]*B0lo[:-1,1:])
 trans_inner=2*h*np.sum((Dhi/(2*Jlo[1:,None]**2))**2/f[1:,1:],axis=1)
 Etrans=np.sum(masses*tt[1:]**1.5*trans_inner)
 m=4*alpha;normc=np.sqrt(2*52.**2+(m-2)*92.**2);coefficient=normc*np.sqrt(beta)/(alpha+.5)/vstar**1.5
 # |h_u|<=beta*osc(v)/4; t^1.5<=(t+t^2)/2.
 rho=1-phi[-1]/vstar;osc=phi[-1]
 def weighted_tail(k):
  fac=(alpha if k==1 else alpha*(alpha+1))*rho**(-alpha-k)
  return fac*(gammainc(alpha+k,rho*L)+gammaincc(alpha+k,rho*T))
 trans_tail=(osc**2/16)*.5*(weighted_tail(1)+weighted_tail(2))
 trans=coefficient*(Etrans+trans_tail)
 a0=vstar*(1-1/(2*alpha));profile=lambda y:((a0*a0/(2*a0-(1+kappa*(1-y*y)**2)))/vstar)**alpha
 Ra_scaled=2*quad(profile,0,b,epsabs=1e-13,epsrel=1e-13)[0]
 R_scaled=2*quad(lambda y:((1+kappa*(1-y*y)**2)/vstar)**alpha,0,b,epsabs=1e-13,epsrel=1e-13)[0]
 eps=(frozen+trans)*Ra_scaled-1;G=.5*np.sqrt(eps*(1+eps))+.375*eps
 record=np.sqrt(10*G*G/(1-np.exp(-4)))
 return {'status':'FLOAT_DIAGNOSTIC_OF_CONSERVATIVE_FORMULAS_NOT_CERTIFIED','nt':nt,'ny':ny,'scalar_nodes':(nt+1)*(ny+1),'L':L,'T':T,'frozen_price_over_C0_upper_diagnostic':frozen*R_scaled,'transverse_price_over_C0_upper_diagnostic':trans*R_scaled,'frozen_tail_scaled':frozen_tail,'transverse_tail_scaled':coefficient*trans_tail,'slab_product_excess_diagnostic':eps,'ideal_rate_ten_record_bound_diagnostic':record,'seconds':time.perf_counter()-start,'not_paid':['floating roundoff','exact Gamma masses','full shifted-well source join','actual mass/rate enclosure','raw derivative-coefficient receiving']}
if __name__=='__main__':
 rows=[]
 for nt,ny in [(512,128),(1024,128),(1024,256),(2048,256),(2048,512)]:
  q=run(nt,ny);rows.append(q);print(json.dumps(q),flush=True)
 open('diagnostic_positive_ceiling_results.json','w').write(json.dumps(rows,indent=2)+'\n')
