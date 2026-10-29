"""Genus-one adapter of saved rounded-section experiment; NOT certified numerics.
Exact rational kernel, polynomial gcd/isolation, and reduced quotient sheet.
Independent Abel quadrature and scalar ODE check; exact multiplicity regressions.
"""
from pathlib import Path
import json,hashlib,time
import sympy as s
import mpmath as mp
from scipy.integrate import solve_ivp
import rounded_relative_doubling as r
x,t=r.x,r.t
r.g=1;r.F=s.Poly((x*x-4)*(x*x-1),x,domain=s.QQ)
r.EDGES=list(map(mp.mpf,[-2,-1,1,2]));r._integral_cache.clear()
r.PERIODS=mp.matrix(1,1);r.PERIODS[:,0]=r.abel_period(0)

def section_zeros(A,B,bits):
    C=s.gcd(A,B).monic();Ar=A.exquo(C);Br=B.exquo(C)
    R=Ar*Ar-r.F*Br*Br;zeros=[]
    def add(xx,yy,m,kind):
        zeros.extend(dict(x=xx,y=yy,infinity=False,kind=kind) for _ in range(m))
    for fac,m in C.sqf_list()[1]:
        branch=s.gcd(fac,r.F);ordinary=fac.exquo(branch)
        for xx,mr in r.exact_roots(branch,bits):add(xx,mp.mpf(0),2*m*mr,'common_branch')
        for xx,mr in r.exact_roots(ordinary,bits):
            yy=mp.sqrt(r.polyvalue(r.F,xx));add(xx,yy,m*mr,'common_plus');add(xx,-yy,m*mr,'common_minus')
    assert s.gcd(Br,R).degree()==0 or R.degree()==0
    for xx,m in r.exact_roots(R,bits):
        yy=-r.polyvalue(Ar,xx)/r.polyvalue(Br,xx)
        add(xx,yy,m,'reduced_exact_quotient_sheet')
    rev=s.expand(t**4*r.F.as_expr().subs(x,1/t));H=s.series(s.sqrt(rev),t,0,5).removeO()
    orders=[]
    for sign in [1,-1]:
        local=s.Poly(s.expand(t**2*A.as_expr().subs(x,1/t)+sign*B.as_expr().subs(x,1/t)*H),t)
        order=next(k for k in range(5) if local.nth(k)!=0);orders.append(order)
        zeros.extend(dict(infinity=True,sheet=sign,kind='infinity') for _ in range(order))
    assert len(zeros)==4
    return zeros,dict(common_factor_degree=C.degree(),reduced_norm_degree=R.degree(),infinity_orders=orders,
      norm_coefficient_bits=r.bitmax((A*A-r.F*B*B).all_coeffs()),sheet_method='exact coprime quotient, not sqrt sign comparison')
r.section_zeros=section_zeros

def exact_cases():
    records=[]
    for name,A,B in [('origin',x*x,0),('conjugate_triple',2-s.Rational(5,4)*x*x,1),('infinity_cancellation',x*x,1),('branch_common',x-1,0)]:
        A=s.Poly(A,x);B=s.Poly(B,x);zs,meta=section_zeros(A,B,160)
        records.append(dict(name=name,A=str(A.as_expr()),B=str(B.as_expr()),norm=str((A*A-r.F*B*B).as_expr()),metadata=meta,
          zeros=[{k:(r.outnum(v) if k in ['x','y'] else v) for k,v in z.items()} for z in zs]))
    return records

def independent_phase(theta):
    # F is fixed: dA/dtheta=-1/sqrt(4-cos(theta)^2).
    return -mp.quad(lambda u:1/mp.sqrt(4-mp.cos(u)**2),[0,mp.pi,theta] if theta>mp.pi else [0,theta])

def ode_target(theta):
    a0=independent_phase(mp.pi/2);a=independent_phase(theta)
    # dA/dtau=1; signed time a-a0 moves input to relative double.
    dt=float(a-a0)
    sol=solve_ivp(lambda tt,z:[-float(mp.sqrt(4-mp.cos(float(z[0]))**2))],(0,dt),[float(theta)],rtol=2.3e-14,atol=1e-14,method='DOP853')
    assert sol.success
    return mp.mpf(float(sol.y[0,-1]))%(2*mp.pi)

def main():
    start=time.perf_counter();path=Path(__file__).with_suffix('.json')
    data=dict(warning='Noncertified analytic evaluation, matching and projection. Exact rational algebra and rational root isolation only.',
      F=str(r.F.as_expr()),origin={'x':0,'y':2,'theta':'pi/2'},source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      reused_source_sha256=hashlib.sha256(Path(r.__file__).read_bytes()).hexdigest(),exact=exact_cases(),results=[])
    cases={'origin':mp.pi/2,'exact_conjugate':3*mp.pi/2,'near_conjugate_40':3*mp.pi/2+mp.mpf(2)**-40,
      'near_conjugate_100':3*mp.pi/2+mp.mpf(2)**-100,'branch_right':mp.mpf(0),'branch_left':mp.pi,'generic':mp.mpf('1.3')}
    period=independent_phase(2*mp.pi)
    for name,theta in cases.items():
      ref=ode_target(theta)
      for epsbits,qbits in [(12,32),(12,96),(24,64),(24,160)]:
        rec=r.run_case(name,[mp.pi/2],[theta],qbits,epsbits,True)
        if 'projected_output_angles' in rec:
          out=mp.mpf(rec['projected_output_angles'][0]);delta=independent_phase(out)-2*independent_phase(theta)+independent_phase(mp.pi/2)
          rec['independent_abel_error']=r.outnum(abs(delta-mp.nint(delta/period)*period))
          rec['independent_float64_ode_angle_error']=r.outnum(r.circular_distance(out,ref))
        rec['admitted']=bool(rec.get('matching_below_quarter_input_separation') and rec.get('output_one_point_per_gap'))
        if not rec['admitted']:rec['status']='ADMISSION_FAILED'
        data['results'].append(rec);data['seconds']=time.perf_counter()-start;path.write_text(json.dumps(data,indent=2))
        print(json.dumps({k:rec.get(k) for k in ['name','qbits','epsbits','status','matching_below_quarter_input_separation','independent_abel_error','independent_float64_ode_angle_error']}),flush=True)
if __name__=='__main__':main()
