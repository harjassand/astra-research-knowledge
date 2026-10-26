"""Astra Pro3: exact rational inverse-sector history, 26 October 2026.

No source derivatives, inverse calls, or energy law are available to learner.
This is a synthetic native-source experiment with independently proved sector constants.
"""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent

def q(v): return Q(v)
def vec(*v): return tuple(Q(t) for t in v)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def mul(t,x):return tuple(t*a for a in x)
def dot(x,y):return sum((a*b for a,b in zip(x,y)),Q(0))
def sq(x):return dot(x,x)
def sqrt_upper(v, scale=1<<40):
 if v<0: raise ValueError('negative')
 ratio=v*scale*scale
 k=(ratio.numerator+ratio.denominator-1)//ratio.denominator
 floor=isqrt(k)
 return Q(floor+(floor*floor<k),scale)

def quantize(x, scale=1<<12):
 return tuple(Q(round(t*scale),scale) for t in x)
def rend(x):
 if isinstance(x,Q):return str(x)
 if isinstance(x,tuple):return [rend(t) for t in x]
 if isinstance(x,list):return [rend(t) for t in x]
 if isinstance(x,dict):return {k:rend(v) for k,v in x.items()}
 return x

def phi_der(t):return 2*t/(1+t*t)**2

def native_nonconservative(x):
 # F=3I+A, A=0.5 Jx + weak nonlinear gradient.
 # |phi''|<=2, so Lip(A)<=.5+.25+.25=1, strictly below m=3.
 a,b=x
 v=add(mul(Q(3),x),vec(phi_der(a)/8+phi_der(a+b)/16,
                       phi_der(b)/8+phi_der(a+b)/16))
 return add(v,vec(-b/2,a/2))

M=Q(3); A=Q(1); DEN=M*M-A*A
C=M/DEN; B=A/DEN

class Data:
 def __init__(self): self.pairs=[];self.calls=0
 def acquire(self,x):
  y=native_nonconservative(x); self.calls+=1
  self.pairs.append((tuple(x),tuple(y)))
  return y
 def check(self):
  for (x,p),(y,r) in combinations(self.pairs,2):
   left=sq(sub(sub(p,r),mul(M,sub(x,y))))
   right=A*A*sq(sub(x,y))
   assert left<=right,(left,right)
  return True
 def ball(self,p,site):
  x,f=self.pairs[site]
  center=add(x,mul(C,sub(p,f)))
  r2=B*B*sq(sub(p,f))
  return center,r2
 def balls(self,p):return [self.ball(p,i) for i in range(len(self.pairs))]
 def contains(self,p,x):return all(sq(sub(x,c))<=r2 for c,r2 in self.balls(p))

def circle_points(n_per_edge=8):
 # Walk counterclockwise around square to falsify cyclic monotonicity of potential-gradient model.
 v=[]
 for i in range(n_per_edge):v.append(vec(-1+Q(2*i,n_per_edge),-1))
 for i in range(n_per_edge):v.append(vec(1,-1+Q(2*i,n_per_edge)))
 for i in range(n_per_edge):v.append(vec(1-Q(2*i,n_per_edge),1))
 for i in range(n_per_edge):v.append(vec(-1,1-Q(2*i,n_per_edge)))
 return v

def circulation():
 pts=circle_points()
 s=sum((dot(native_nonconservative(x),sub(pts[(i+1)%len(pts)],x)) for i,x in enumerate(pts)),Q(0))
 assert s>0,s
 # gradients of convex energy necessarily have cyclic sum <=0
 return dict(probe_count=len(pts),cyclic_monotonicity_violation=s)

def trace_inverse():
 true_x=vec(Q(3,2),Q(-1)); p=native_nonconservative(true_x)
 history=Data();history.acquire(vec(0,0));assert history.check()
 first_center,first_radius2=history.ball(p,0)
 z=first_center; radius=sqrt_upper(first_radius2)
 iter_rows=[]
 for i in range(5):
  assert sq(sub(z,true_x))<=radius**2
  probe=quantize(z); quantization_error=sum(map(abs,sub(probe,z)),Q(0))
  obs=history.acquire(probe);assert history.check()
  znew=add(probe,mul(Q(1)/M,sub(p,obs)))
  next_radius=(A/M)*(radius+quantization_error)
  assert sq(sub(znew,true_x))<=next_radius**2
  assert history.contains(p,true_x)
  iter_rows.append(dict(native_call=i+2,probe=probe,response=obs,next_estimate=znew,
                        probe_quantization_error_upper=quantization_error,
                        certified_error_radius=next_radius,
                        source_aware_actual_error_squared=sq(sub(znew,true_x))))
  z,radius=znew,next_radius
 # Every fresh force p is a later task; no direct inverse access.
 return history,dict(target_force=p,source_aware_true_equilibrium=true_x,
   initial_center=first_center,initial_radius_squared=first_radius2,
   iteration=iter_rows,final_certified_radius=radius,
   final_source_aware_actual_error_squared=sq(sub(z,true_x)),
   native_calls=history.calls,returned_scalars=2*history.calls)

def joint_pair():
 # Task p2 differs minimally from p1. The exact joint posterior is much tighter
 # than independently intersecting marginal intervals.
 p1=vec(2,0);p2=vec(2,Q(1,50)); dp=sub(p2,p1)
 cc=mul(C,dp);rr=B*B*sq(dp)
 assert cc[0]==0 and rr==Q(1,160000),rr
 rad=Q(1,400)
 assert rad**2==rr
 lo=cc[1]-rad;hi=cc[1]+rad
 # Two *globally sector admissible affine* sources realizing extremes.
 # A_plus(x,y)=(0,+y), A_minus(x,y)=(0,-y)
 # Each agrees with native old measurement F(0)=0.
 x1=vec(Q(2,3),0)
 x2plus=vec(Q(2,3),Q(1,200))
 x2minus=vec(Q(2,3),Q(1,100))
 assert x2plus[1]-x1[1]==lo and x2minus[1]-x1[1]==hi
 # Marginal e_y intervals for each p separately from one datum at 0.
 # Their summed half widths >= (|p1|+|p2|)/8 ~= 0.5000,
 # while relative task half width is 1/400 =0.0025.
 # Safe rational lower on unrelated marginal interval width by ||p2||>=2.
 independent_width_lower=2*B*(Q(2)+Q(2))
 joint_width=hi-lo
 assert independent_width_lower/joint_width==200
 return dict(relative_equilibrium_y_interval=(lo,hi),
    sharp_joint_width=joint_width,independent_marginal_width_at_least=independent_width_lower,
    factor_at_least=independent_width_lower/joint_width,
    witness_source_plus='F(x,y)=(3x,4y)',witness_source_minus='F(x,y)=(3x,2y)',
    two_compatible_equilibrium_differences=(x2plus[1]-x1[1],x2minus[1]-x1[1]))

def coherent_portfolio(history):
 # Short general task compiler emits rational dual/edge certificates for
 # linear combinations of x*(p) while retaining source coherence.
 # Each observed pair is a native anchor (force, equilibrium).
 force0=history.pairs[0][1]
 x0=history.pairs[0][0]
 p1=vec(Q(7,2),Q(1,2));p2=vec(Q(7,2),Q(51,100)); delta=sub(p2,p1)
 v=vec(0,1)
 # Each inverse position x(p)=C p+u(p), Lip u <= B.
 c=dot(v,mul(C,delta))
 r2=B*B*sq(delta)
 assert r2==Q(1,640000),r2
 r=Q(1,800)
 lo,hi=c-r,c+r
 # Compare with two independent one-anchor predictions in y direction.
 # Need no square roots for valid looser bound r_ind: ||p-force0|| <= |dx|+|dy|
 def r_simple(p):return B*sum((abs(a) for a in sub(p,force0)),Q(0))
 r_ind=r_simple(p1)+r_simple(p2)
 # Independent (loose) scalar interval width 2*r_ind.
 return dict(p1=p1,p2=p2,component='y',joint_interval=(lo,hi),
       joint_radius=r,independent_valid_radius=r_ind,
       independent_to_joint_radius_ratio=r_ind/r,
       algebraic_dual_certificate='one edge linking the two future forces; force-shifted inverse residual is B-Lipschitz')

def unforeseen_task_bank(history):
 # Test setter independently defines later forces from held-out reference equilibria.
 # Calls by setter are charged separately and never revealed to acquisition policy.
 rows=[]
 for i in range(10):
  for j in range(5):
   true_x=vec(Q(3,2)+Q(i-5,25), Q(-1)+Q(j-2,25))
   force=native_nonconservative(true_x)
   assert history.contains(force,true_x)
   old=sqrt_upper(history.ball(force,0)[1],1<<40)
   best=min(sqrt_upper(r2,1<<40) for _,r2 in history.balls(force))
   assert best<=old
   rows.append(dict(force=force,true_equilibrium=true_x,initial_radius=old,
                    retained_bank_radius=best))
 return dict(later_tasks=len(rows),learner_new_native_calls=0,
             independent_setter_forward_calls=len(rows),
             mean_initial_radius=sum((row['initial_radius'] for row in rows),Q(0))/len(rows),
             mean_bank_radius=sum((row['retained_bank_radius'] for row in rows),Q(0))/len(rows),
             max_bank_radius=max(row['retained_bank_radius'] for row in rows),
             ratio=sum((row['initial_radius'] for row in rows),Q(0))/sum((row['retained_bank_radius'] for row in rows),Q(0)),
             rows=rows)

def noisy_control():
 # Every experiment reports mx with Euclidean error <=eps=1/1000.
 # Two sector-compatible sources F+-=mx +/-eps e1 produce same all-history reports.
 eps=Q(1,1000);p=vec(1,0)
 plus=add(mul(Q(1)/M,p),vec(-eps/M,0))
 minus=add(mul(Q(1)/M,p),vec(eps/M,0))
 assert sq(sub(plus,minus))==(2*eps/M)**2
 return dict(per_reading_error_bound=eps,
  indistinguishable_equilibrium_positions=(plus,minus),
  universal_error_floor=eps/M,
  result='No count of adversarially perturbed calls can beat eps/m in this class; systematic observation bias may persist.')

def noise_outer_ball(p,x,fhat,eps):
 # Triangle inequality with all norms Euclidean, exact squared inflation avoids sqrt
 cp=add(x,mul(C,sub(p,fhat)))
 # r <= B*||p-fhat|| + (B+C)eps. Output an exact safe squared radius,
 # using norm <= l1 (rational) for the first term.
 rad=B*sum((abs(t) for t in sub(p,fhat)),Q(0))+(B+C)*eps
 return cp,rad*rad

def execute():
 assert C==Q(3,8) and B==Q(1,8)
 cyclic=circulation()
 history,inverse=trace_inverse()
 pair=joint_pair()
 portfolio=coherent_portfolio(history)
 batch=unforeseen_task_bank(history)
 noisy=noisy_control()
 pp=vec(2,1);ep=Q(1,1000);h=vec(0,0)
 fc=native_nonconservative(h); fc_hat=add(fc,vec(ep,0))
 center,rsq=noise_outer_ball(pp,h,fc_hat,ep)
 # Verify true exact posterior center is included in inflated ball (test geometry)
 true_center=add(h,mul(C,sub(pp,fc)))
 true_rad_sq=B*B*sq(sub(pp,fc))
 # Inclusion of disks can be shown via triangle inequality; float approximation only test.
 from math import sqrt
 assert sqrt(float(sq(sub(center,true_center))))+sqrt(float(true_rad_sq))<=sqrt(float(rsq))+1e-13
 out=dict(source_contract=dict(m=M,a=A,inverse_center_multiplier=C,inverse_residual_Lipschitz=B,
        gradient_part_Lipschitz_bound=Q(1,2),skew_part_Lipschitz_bound=Q(1,2)),
        cyclic_violation=cyclic,inverse_native_transfer=inverse,
        sharp_joint_pair=pair,portfolio_certificate=portfolio,unforeseen_batch=batch,
        adversarial_noise=noisy,
        noisy_outer_test=dict(reported_force=fc_hat,uncertainty=ep,outer_center=center,outer_radius_squared=rsq),
        proof_scope='Exact finite joint posterior over global residual-Lipschitz maps; native calls from a nonconservative nonlinear source; no claims of learned physical contracts or source-aware inference.')
 (OUT/'astra_pro3_sector_joint_results.json').write_text(json.dumps(rend(out),indent=2)+'\n')
 print('nonconservative cyclic violation:',float(cyclic['cyclic_monotonicity_violation']))
 print('native inverse final radius:',float(inverse['final_certified_radius']))
 print('joint relative interval:',list(map(float,pair['relative_equilibrium_y_interval'])))
 print('relative gain >=',float(pair['factor_at_least']))
 print('50 later task bank improvement:',float(batch['ratio']))
 print('precision noise floor:',float(noisy['universal_error_floor']))
 return out

if __name__=='__main__':execute()
