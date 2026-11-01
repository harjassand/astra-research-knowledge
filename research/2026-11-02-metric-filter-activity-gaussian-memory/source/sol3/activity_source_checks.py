#!/usr/bin/env python3
"""Check the new bounded-filter and weighted-clock source, including rapid scaling.

Every full matrix is a finite diagnostic. Scalable gates are the constructions
in ACTIVITY_COMPILER.md and the source-bound acquired scalar bridge, not these
CPU exponentials/permanents.
"""
from pathlib import Path
import sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'stage2'))
from loss_clock import CoupledBath,annihilators,gamma,expm,norm,dyadic_cells
from metric_checks import pospow,minimum,model,dg,sx
import numpy as np
import math,json

K=2;M=2
base=CoupledBath(40,K)
Pmet=3*np.array([[1,1/(2*math.sqrt(40))],[1/(2*math.sqrt(40)),.5]],complex)
pmax=4.;gapbase=.5;kappabase=gapbase/(2*K*pmax)
Z=np.eye(M)+Pmet/(K*pmax);Zh=pospow(Z,.5);Zi=pospow(Z,-.5)
Sb=gamma(Zh,K);Si=gamma(Zi,K);S=np.kron(np.eye(2),Sb);Sinv=np.kron(np.eye(2),Si)
a2=float(np.linalg.norm(base.c)**2)
tau=kappabase/(256*a2*(K+1))
# Shifted weighted-CDF Lyapunov equation, independent of overall rapid scale.
Awbase=base.A+kappabase/4*np.eye(M)
op=np.kron(np.eye(M),Awbase.conj().T)+np.kron(Awbase.T,np.eye(M))
X=np.linalg.solve(op,-(base.E@base.E.conj().T).reshape(-1,order='F')).reshape(M,M,order='F');X=(X+X.conj().T)/2

class Source:
 def __init__(self,rho):
  self.rho=rho;self.A=rho*base.A;self.E=math.sqrt(rho)*base.E;self.c=math.sqrt(rho)*base.c
  self.kappa=rho*kappabase;self.a=math.sqrt(rho*a2)
  self.g=max(float(np.linalg.norm(self.c@Zh)),float(np.linalg.norm(self.c@Zi)))
  self.mod=model(self.A,self.E,Pmet,rho*gapbase,[self.c],[sx],K)
  self.G=self.mod['G'];self.L=self.mod['Ls'][0];self.D=self.mod['G']-np.kron(np.eye(2),self.mod['G0'])
  self.Hs=.5*np.array([[0,-1j],[1j,0]])+.3*np.diag([1.,-1.])
  self.V=1j*self.D-np.kron(self.Hs,np.eye(base.d))
  self.d=2*self.a*math.sqrt(K+1)
  self.C=Zh@self.A@Zi+self.kappa/2*np.eye(M)
  self.Cfull=np.kron(np.eye(2),dg(self.C,self.mod['bs']))-1j*np.kron(self.Hs,np.eye(base.d))
  # Independently assemble the non-Hermitian transformed drive from its two
  # actual coefficient directions, rather than defining it by similarity.
  low=sum((self.c@Zi)[i]*self.mod['bs'][i] for i in range(M))
  raise_=sum((self.c@Zh)[i].conjugate()*self.mod['bs'][i].conj().T for i in range(M))
  self.Gtilde_formula=np.kron(np.eye(2),dg(Zh@self.A@Zi,self.mod['bs']))-1j*(np.kron(self.Hs,np.eye(base.d))+np.kron(sx,low+raise_))
  self.A0=2**math.ceil(math.log2(math.sqrt(16+5*K*M)))
 def F(self,t):return base.F(self.rho*t)
 def B(self,t):return np.kron(expm(-1j*self.Hs*t),gamma(self.F(t),K))
 def K0(self,t):return expm(self.G*t)
 def f(self,t):return float(np.linalg.norm(self.E.conj().T@self.F(t)))
 def J(self,t):
  f=self.F(t);return max(0.,float(M-np.trace(f.conj().T@f).real))
 def Fw(self,t):
  # Analytic two-pole formula with shifted negative exponents; no growing exp.
  u=self.rho*t;slow=-2/(1+math.sqrt(1-4/40));fast=-40-slow
  return (math.exp((slow+kappabase/4)*u)*(base.A-fast*np.eye(M))-math.exp((fast+kappabase/4)*u)*(base.A-slow*np.eye(M)))/(slow-fast)
 def Jw(self,t):
  f=self.Fw(t);return max(0.,float(np.trace(X-f.conj().T@X@f).real))
 def Iw_mass(self,a,b):
  return (2/self.kappa)*math.exp(-self.kappa*a/2)*(-math.expm1(-self.kappa*(b-a)/2))
 def event_cdf(self,t):return 2*K*self.J(t)+768*self.a**2*K*(K+1)*M*t/self.kappa
 def w(self,t):return math.sqrt(2*K*self.f(t)**2+768*self.a**2*K*(K+1)*M/self.kappa)

def scalar_kernel(g,kappa,t):
 x=kappa*t/2
 alpha=g*t*(-math.expm1(-x)/x)
 if abs(x)<1e-4:cc=g*g*t*t*(.5-x/6+x*x/24-x**3/120)
 else:cc=g*g*t*t*(x+math.expm1(-x))/(x*x)
 out=np.zeros((K+1,K+1))
 for m in range(K+1):
  for n in range(K+1):
   out[m,n]=math.exp(cc)*math.sqrt(math.factorial(m)*math.factorial(n))*sum(alpha**(m+n-2*l)*math.exp(-x*l)/(math.factorial(m-l)*math.factorial(n-l)*math.factorial(l)) for l in range(min(m,n)+1))
 return out

def checks(s,res):
 t=tau
 no=s.K0(t);blocks=[no];conv=np.zeros_like(no)
 for lo,hi in dyadic_cells(t,s.rho*40,res):
  u=(lo+hi)/2;f=s.f(u);lk=s.L@s.K0(u)
  mass=max(0.,s.event_cdf(hi)-s.event_cdf(lo));blocks.append(math.sqrt(mass)/s.w(u)*lk)
  mw=max(0.,s.Jw(hi)-s.Jw(lo));mi=s.Iw_mass(lo,hi)
  if f>0 and mw>0 and mi>0:
   # Acquired row/column weights, with their exact normalization restored.
   conv+=math.sqrt(mw*mi)/f*(s.L@s.B(u)@s.V@s.K0(t-u))
 V=np.vstack(blocks)
 G=V.conj().T@V
 return {'resolution':res,'outer_cells_for_CPU_check':len(blocks)-1,'source_Gram_error':norm(G-np.eye(len(G))),
         'weighted_cross_source_Duhamel_error':norm(s.L@s.K0(t)-s.L@s.B(t)+1j*conv)}

if __name__=='__main__':
 rows=[]
 for rho in [1.,100.,10000.,1e6,1e8]:
  s=Source(rho);Gt=S@s.G@Sinv
  no=s.K0(tau);nt=expm(Gt*tau);rest=Sinv@nt@S
  E=scalar_kernel(s.g,s.kappa,tau)
  gx,gw=np.polynomial.legendre.leggauss(24);positive_integral=0.
  for lo,hi in dyadic_cells(tau,rho*40,1):
   for x,w in zip(gx,gw):
    f=s.E.conj().T@s.Fw((lo+hi)/2+(hi-lo)*x/2)
    positive_integral+=(hi-lo)*w/2*float(np.linalg.norm(f)**2)
  # Transferred scalar majorization on every actual unequal-dimensional sector.
  index={n:[q*base.d+i for q in range(2) for i,b in enumerate(base.states) if sum(b)==n] for n in range(K+1)}
  excess=max(norm(nt[np.ix_(index[m],index[n])])-E[m,n] for m in range(K+1) for n in range(K+1))
  data={'rapid_scale':rho,'physical_passive_norm':norm(s.A),'drive_norm':s.a,'kappa':s.kappa,
   'new_max_duration':tau,'old_stage2_max_duration':1/(1+norm(s.Hs)+2*s.a*math.sqrt(K+1)),
   'filter_norm':norm(S),'filter_inverse_norm':norm(Sinv),'C_dissipativity_margin_min':minimum(-(s.C+s.C.conj().T)),
   'physical_nojump_filter_reconstruction_error':norm(rest-no),'scalar_kernel_row_col_bound':float(max(E.sum(0).max(),E.sum(1).max())),
   'transformed_direction_generator_identity_error':norm(s.Gtilde_formula-Gt),
   'weighted_CDF_vs_positive_integral_error':abs(s.Jw(tau)-positive_integral),
   'actual_sector_majorant_excess':excess,'weighted_CDF_at_tau':s.Jw(tau),'weighted_CDF_total_bound':3*M,
   'actual_outer_envelope_mass':s.event_cdf(tau),'proved_outer_envelope_bound':5*K*M,'complete_source_normalizer':s.A0,
   'candidate_immigration_mean_cap':2*s.g**2*tau/s.kappa,
   'checks':checks(s,16)}
  assert data['physical_nojump_filter_reconstruction_error']<3e-6,data
  assert data['transformed_direction_generator_identity_error']<1e-5,data
  assert data['weighted_CDF_vs_positive_integral_error']<1e-7,data
  assert data['scalar_kernel_row_col_bound']<2,data
  assert excess<3e-6,data
  assert s.Jw(tau)<3*M+1e-7
  assert s.event_cdf(tau)<=5*K*M+1e-7
  assert data['checks']['source_Gram_error']<.003,data
  assert data['checks']['weighted_cross_source_Duhamel_error']<.003,data
  rows.append(data);print(json.dumps(data),flush=True)
 ref=[];s=Source(1e6)
 for res in [8,16,32,64]:ref.append(checks(s,res))
 assert all(y['source_Gram_error']<x['source_Gram_error'] for x,y in zip(ref,ref[1:]))
 out={'scope':'Finite bounded-filter/majorant/weighted-time-source checks. Rapid drive grows as sqrt(relaxation); actual retained quantum amplitudes are compared. Not an independent audit or gate execution.',
      'metric_P':Pmet.tolist() if False else [[float(x.real) for x in row] for row in Pmet],
      'pmax':pmax,'K':K,'modes':M,'X_weighted_gramian_trace':float(np.trace(X).real),
      'rapid_scaling':rows,'refinement_at_rapid_scale_1e6':ref}
 (P/'results/activity_source_checks.json').write_text(json.dumps(out,indent=2)+'\n')
 print('PASS: bounded metric source and weighted loss clock retain constant normalization under sqrt-rate driving.',flush=True)
