"""Native forward acquisition -> constrained variational-equilibrium service.

All native probes remain on the nonnegative unit-dose simplex. The law is
nonconservative; the learner gets only responses and the supplied sector
bounds, not a potential, inverse, Jacobian, or native VI solver.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import isqrt
import json
from astra_pro3_sector_joint import vec,sub,add,mul,sq,dot,rend,phi_der,sqrt_upper,quantize
ROOT=Path(__file__).resolve().parent
M=Q(3);A=Q(1);MU=M-A

def simplex_project(y):
    # exact rational Euclidean projection onto x_i>=0, sum x_i=1
    z=sorted(y,reverse=True)
    for k in range(1,len(z)+1):
        theta=(sum(z[:k],Q(0))-1)/k
        if k==len(z) or z[k]<=theta:
            out=tuple(max(Q(0),t-theta) for t in y)
            assert sum(out,Q(0))==1
            return out
    raise RuntimeError('projection failure')

def feasible(x):return all(t>=0 for t in x) and sum(x,Q(0))==1

def nonlinear_nonconservative_3(x):
    assert feasible(x),'native source only accepts nonnegative fixed-dose inputs'
    # F=3x+0.5 Jx + weak nonpolynomial gradient, globally A-Lipschitz <=15/16.
    # diag(phi''/8): <=1/4; common all-ones rank one phi''/32: <=3/16;
    # planar skew op norm=1/2 => <=15/16<1.
    t=sum(x,Q(0))
    g=vec(*(phi_der(v)/8+phi_der(t)/32 for v in x))
    return add(add(mul(M,x),g),vec(-x[1]/2,x[0]/2,0))

class Record:
 def __init__(self):self.jets=[]
 def acquire(self,x):
  assert feasible(x)
  p=nonlinear_nonconservative_3(x)
  self.jets.append((x,p))
  return p
 def assert_compatible(self):
  for i in range(len(self.jets)):
   for j in range(i):
    x,p=self.jets[i];y,r=self.jets[j]
    assert sq(sub(sub(p,r),mul(M,sub(x,y))))<=A*A*sq(sub(x,y))
  return True
 def prior_ball(self,force,i):
  # VI test against observed x_i and strong monotonicity mu=m-a.
  x,f=self.jets[i]
  center=add(x,mul(Q(1,2)/MU,sub(force,f)))
  r2=sq(sub(force,f))/(4*MU*MU)
  return center,r2
 def initial_guess(self,force):
  best=None
  for i in range(len(self.jets)):
   center,rsq=self.prior_ball(force,i)
   r=sqrt_upper(rsq)
   trial=simplex_project(center)
   if best is None or r<best[1]:best=(trial,r,i)
  assert best is not None
  # independently, the simplex diameter is sqrt(2), so the starting centroid
  # has radius sqrt(2/3) in d=3. Exact rational upper bound follows.
  centroid=vec(Q(1,3),Q(1,3),Q(1,3))
  dimrad=sqrt_upper(Q(2,3))
  if dimrad<best[1]:return centroid,dimrad,'simplex_geometry'
  return best[0],best[1],f'old_site_{best[2]}'

def simplex_quantize(x,den=1<<12):
    assert feasible(x)
    raw=[a*den for a in x]
    z=[r.numerator//r.denominator for r in raw]
    remainder=den-sum(z)
    ranked=sorted(range(len(x)), key=lambda i:(raw[i]-z[i],-i),reverse=True)
    for i in ranked[:remainder]:z[i]+=1
    y=tuple(Q(a,den) for a in z)
    assert feasible(y)
    return y,sum((abs(t) for t in sub(y,x)),Q(0))

def projected_solver(history,force,xtrue,steps=5,generic=False):
    if generic:
        z=vec(Q(1,3),Q(1,3),Q(1,3));r=sqrt_upper(Q(2,3));origin='domain_only_centroid'
    else:
        z,r,origin=history.initial_guess(force)
    z,err=simplex_quantize(z);r+=err
    assert sq(sub(z,xtrue))<=r*r,(z,xtrue,r)
    path=[]
    for i in range(steps):
        assert feasible(z)
        f=history.acquire(z)
        z_unrounded=simplex_project(add(z,mul(Q(1)/M,sub(force,f))))
        z_next,rounding_error=simplex_quantize(z_unrounded)
        r_next=(A/M)*r+rounding_error
        assert sq(sub(z_next,xtrue))<=r_next*r_next
        path.append(dict(native_forward_call_index=len(history.jets),probe=z,
             next_estimate=z_next,rounding_error_upper=rounding_error,
             next_radius=r_next,true_squared_error=sq(sub(z_next,xtrue))))
        z,r=z_next,r_next
    return dict(initial_point=path[0]['probe'],
                 initial_method=origin, final_estimate=z,final_radius=r,
                 actual_error_squared=sq(sub(z,xtrue)),path=path)

def exact_vi_check(x,p):
    # For simplex, x solves VI iff x maximizes (p-F(x))·z over z in simplex.
    v=sub(p,nonlinear_nonconservative_3(x))
    score=dot(v,x)
    return all(score>=t for t in v)

def cyclic_falsifier(nseg=16):
    # Four segments around a square in two free coordinates of simplex.
    # The source's skew component makes the cyclic sum positive if sufficiently
    # many actual native readings are used. This excludes a convex gradient.
    points=[]
    for i in range(nseg):points.append(vec(Q(i,2*nseg),0,1-Q(i,2*nseg)))
    for i in range(nseg):points.append(vec(Q(1,2),Q(i,2*nseg),Q(1,2)-Q(i,2*nseg)))
    for i in range(nseg):points.append(vec(Q(1,2)-Q(i,2*nseg),Q(1,2),Q(i,2*nseg)))
    for i in range(nseg):points.append(vec(0,Q(1,2)-Q(i,2*nseg),Q(1,2)+Q(i,2*nseg)))
    assert all(feasible(x) for x in points)
    cycle=sum((dot(nonlinear_nonconservative_3(x),sub(points[(i+1)%len(points)],x))
                   for i,x in enumerate(points)),Q(0))
    assert cycle>0,cycle
    return dict(native_cycle_calls=len(points),positive_cyclic_monotonicity_violation=cycle)

def main():
    cyc=cyclic_falsifier()
    sites=Record()
    initial=(vec(1,0,0),vec(0,1,0),vec(0,0,1),vec(Q(1,3),Q(1,3),Q(1,3)))
    for x in initial:sites.acquire(x)
    assert sites.assert_compatible()
    task_data=[
      ('interior_root',vec(Q(1,5),Q(3,10),Q(1,2)),vec(0,0,0)),
      ('boundary_vertex',vec(1,0,0),vec(5,0,0)),
      ('boundary_edge',vec(Q(1,3),Q(2,3),0),vec(0,0,-3)),
      ('interior_second',vec(Q(2,5),Q(1,5),Q(2,5)),vec(0,0,0))]
    rows=[]
    for label,true_x,normal in task_data:
       force=add(nonlinear_nonconservative_3(true_x),normal)
       assert exact_vi_check(true_x,force)
       # Each task gets a fresh copy of exactly the common four retained sources,
       # then runs its own native forward actions. No hidden reuse of another
       # task's calls is assumed or omitted from total task cost.
       h=Record();h.jets=sites.jets.copy()
       x0,r0,_=h.initial_guess(force)
       for center,rsq in (h.prior_ball(force,i) for i in range(len(h.jets))):
           assert sq(sub(true_x,center))<=rsq
       result=projected_solver(h,force,true_x,steps=5)
       equal_budget_baseline=Record();equal_budget_baseline.jets=sites.jets.copy()
       generic_result=projected_solver(equal_budget_baseline,force,true_x,steps=5,generic=True)
       rows.append(dict(label=label,force=force,exact_true_variational_equilibrium=true_x,
           target_is_native_inverse=(normal==vec(0,0,0)),
           initial_certified_radius=r0,retained_call_count=len(sites.jets),
           new_native_calls=len(h.jets)-len(sites.jets),solver=result,
           same_budget_domain_only_baseline=generic_result,
           baseline_calls=len(equal_budget_baseline.jets)-len(sites.jets)))
    result=dict(source_contract=dict(m=M,a=A,strong_monotonicity_lower=MU,
           nonlinear_gradient_Lipschitz=Q(7,16),skew_Lipschitz=Q(1,2),
           source_residual_Lipschitz_at_most=Q(15,16)),
       cyclic_monotonicity_falsification=cyc,
       physically_admissible_input_set='three-component nonnegative mixtures with total dose one',
       common_initial_native_calls=len(sites.jets),tasks=rows,
       total_native_calls=len(sites.jets)+sum(r['new_native_calls'] for r in rows),
       independent_reference_source_aware_forward_calls=len(task_data),
       result_scope='Exact fixed-dose nonconservative forward readings and variational-equilibrium certificates; separate future tasks receive independent action budgets.',
       caveat='An inverse ball from unconstrained sector Kirszbraun does NOT remain sharp for simplex VI. The provided prior balls are safe outer enclosures and projection gives a/m convergence.')
    (ROOT/'astra_pro3_sector_constrained_vi_results.json').write_text(json.dumps(rend(result),indent=2)+'\n')
    print('cycle',float(cyc['positive_cyclic_monotonicity_violation']),'calls',cyc['native_cycle_calls'])
    for row in rows:print(row['label'],'new calls',row['new_native_calls'],'radius',float(row['solver']['final_radius']), 'domain-only',float(row['same_budget_domain_only_baseline']['final_radius']))
    return result

if __name__=='__main__':main()
