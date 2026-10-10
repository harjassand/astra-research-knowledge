"""Directed-interval certificate for a Gaussian complete-RE countertest.
Uses mpmath.iv at 90 decimal digits; finite convergent Gibbs-matrix series
with an analytic positive-semidefinite tail bound. No numerical eigensolver.
"""
import mpmath as mp,json
iv=mp.iv;iv.dps=90

def f(n,d=1):return iv.mpf(n)/d

def ident(n):return [[f(int(i==j)) for j in range(n)] for i in range(n)]
def add(A,B):return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def scale(A,s):return [[x*s for x in row] for row in A]
def mul(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),f(0)) for j in range(len(B[0]))] for i in range(len(A))]
def inv(A):
 n=len(A);W=[list(A[i])+ident(n)[i] for i in range(n)]
 for j in range(n):
  p=W[j][j]
  assert bool(p.a>0) or bool(p.b<0),'pivot interval contains zero'
  W[j]=[x/p for x in W[j]]
  for i in range(n):
   if i==j:continue
   a=W[i][j];W[i]=[W[i][k]-a*W[j][k] for k in range(2*n)]
 return [row[n:] for row in W]
def quad(A,d):return sum((d[i]*A[i][j]*d[j] for i in range(len(d)) for j in range(len(d))),f(0))
def tr(A):return sum((A[i][i] for i in range(len(A))),f(0))
def series_quadratic(Q,P,d,K=48,rho=f(1,3)):
 # Gibbs p-block = P^-1 sum_{k>=0} (Q^-1 P^-1/4)^k/(2k+1).
 A=inv(P);B=scale(mul(inv(Q),A),f(1,4));power=ident(len(P));s=f(0)
 for k in range(K+1):
  s+=quad(mul(A,power),d)/(2*k+1)
  power=mul(power,B)
 power8=ident(len(P))
 for _ in range(8):power8=mul(power8,B)
 trace8=tr(power8)
 # B is similar to an SPD matrix, so lambda_max(B)^8 <= Tr(B^8).
 assert bool(trace8.b<(rho**8).a),'spectral-radius bound failed'
 tail=quad(A,d)*rho**(K+1)/((2*K+3)*(1-rho))
 assert bool(tail.a>0)
 return s,tail,trace8

def certify(eta_num,eta_den,u,w,t_num,t_den,sa,score_num,score_den):
 eta=f(eta_num,eta_den);u=f(u);w=f(w);t=f(t_num,t_den);sa=f(sa)
 ch=(1+t*t)/(1-t*t);sh=2*t/(1-t*t)
 r=u*ch*ch+w*sh*sh;a=w*ch*ch+u*sh*sh;c=(u+w)*ch*sh
 v=f(3,2);ce=iv.sqrt(f(2));se=iv.sqrt(eta);sl=iv.sqrt(1-eta)
 Qb=[[r,se*c*sa],[se*c*sa,eta*a*sa*sa+(1-eta)*v]]
 Pb=[[r,-se*c/sa],[-se*c/sa,eta*a/sa/sa+(1-eta)*v]]
 Qe=[[r,-sl*c*sa,f(0)],[-sl*c*sa,(1-eta)*a*sa*sa+eta*v,se*ce],[f(0),se*ce,v]]
 Pe=[[r,sl*c/sa,f(0)],[sl*c/sa,(1-eta)*a/sa/sa+eta*v,-se*ce],[f(0),-se*ce,v]]
 d=[f(score_num,score_den),f(-1)]
 db=[d[0],se*d[1]];de=[d[0],-sl*d[1],f(0)]
 sb,tb,trb=series_quadratic(Qb,Pb,db)
 se0,te,tre=series_quadratic(Qe,Pe,de)
 # True gap lies in (se0 - sb) + [0,te] - [0,tb].
 partial=se0-sb
 enclosure=iv.mpf([(partial.a-tb.b).a,(partial.b+te.b).b])
 assert bool(enclosure.b<0),'no certified negative gap'
 return {'eta_rational':f'{eta_num}/{eta_den}','eta_interval':str(eta),
  'thermal_seed_variances_u_w':[str(u),str(w)],'squeezing_tanh_half_r':f'{t_num}/{t_den}',
  'input_local_q_squeeze':str(sa),'input_mean_direction_p_R_p_A':[f'{score_num}/{score_den}','-1'],
  'twice_relative_entropy_gap_E_minus_B_per_unit_mean_squared':str(enclosure),
  'B_series':str(sb),'E_series':str(se0),'B_tail_upper_interval':str(tb),
  'E_tail_upper_interval':str(te),'trace_B_power8':str(trb),'trace_E_power8':str(tre),
  'verified_spectral_radius_upper':'1/3','series_last_k':48,'iv_decimal_precision':iv.dps,
  'status':'negative interval verified by convergent analytic series; relies on Gaussian Gibbs identity'}

if __name__=='__main__':
 out={'convention':'vacuum covariance I/2; natural logarithms; mu=1 means finite physical displacement',
      'certificates':[certify(3803,5000,5.5,1000000,1,1800,140,3377,4000),
                      certify(761,1000,2,1000,3,200,10,933,1000),
                      certify(5433561,7123561,1,1000,1,200,10,9,10)]}
 print(json.dumps(out,indent=2))
 with open('work/continuation_03/reports/e4_zero_support/interval_reference_certificate.json','w') as ff:json.dump(out,ff,indent=2)
