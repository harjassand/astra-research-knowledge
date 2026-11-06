"""Rational certificate compiler for write, handover and retention.

Only acquired static data and warranted scalar bounds enter this module.
No native-source matrix, state or exact transfer function is used.
"""
from pathlib import Path
from fractions import Fraction as Q
import json
from exact import require, sqrt_up, exp_minus, dyadic, qbits, encode

ROOT = Path(__file__).resolve().parent


def norm(v):
    return sqrt_up(sum((x*x for x in v), Q(0)), 60)


def mv(A, x):
    return [sum((a*b for a,b in zip(row,x)), Q(0)) for row in A]


def save(path, obj):
    Path(path).write_text(json.dumps(encode(obj), indent=2, sort_keys=True)+'\n')


def maxbits(v):
    if isinstance(v,Q): return qbits(v)
    if isinstance(v,dict): return max((maxbits(x) for x in v.values()),default=0)
    if isinstance(v,(list,tuple)): return max((maxbits(x) for x in v),default=0)
    return 0


def make_plan():
    elementary={'exponential_enclosures':0,'taylor_terms':0,'squarings':0,'series_bits_max':0}
    def eupper(x):
        lo,hi,cost=exp_minus(x,96)
        elementary['exponential_enclosures']+=1
        elementary['taylor_terms']+=cost['taylor_terms']
        elementary['squarings']+=cost['squarings']
        elementary['series_bits_max']=max(elementary['series_bits_max'],cost['series_coefficient_bits_max'])
        return hi
    old=json.loads((ROOT/'inputs/PROGRAMMED_PATTERN.json').read_text())
    src=json.loads((ROOT/'inputs/ORDER_INPUTS.json').read_text())
    K=[list(map(Q,row)) for row in old['physical_K']]
    S=[list(map(Q,row)) for row in src['static_model']]
    p=list(map(Q,old['target_amplitude']))
    z=list(map(Q,old['physical_target']))
    beta=list(map(Q,old['beta'])); field=list(map(Q,old['physical_field']))
    fg=list(map(Q,old['field_in_gauge'])); sigma=old['sign_pattern']
    n=len(p); P2=sum((x*x for x in p),Q(0)); P=norm(p)
    Es=max(map(Q,src['source_errors_rounded_up']))
    # Source-only uncertainty is a subset of the retained robust 1% certificate.
    require(old['robust_one_percent_certificate']['status']=='PASS')
    require(old['robust_one_percent_certificate']['relative_radius']=='1/100')
    a=Q(1); A0=Q(2); c0=Q(1,4); Lg=Q(9,8); BH=Q(33,16)
    require(Lg*Lg>=1+c0/a**2 and BH*BH>=A0*A0+c0)
    theta=Q(1,100); box=Q(1,5); r=(box-theta)*min(p)
    m=min(f/x+b*(3*(1-box)**2-1)*x*x for f,x,b in zip(fg,p,beta))-Es
    alpha=Q(7,8)
    require(0<alpha<a and (m-alpha)*(a-alpha)>=alpha*c0/a)
    # The source-uncertain ideal retention law has a second local minimum.
    negative_radius=box*min(p)
    negative_residual=Es*P+2*norm(fg)
    require(negative_residual<m*negative_radius)
    require(Lg*(P+negative_radius)<4)

    fixed_bits=40
    scale=1<<fixed_bits
    Kd=[[dyadic(v,fixed_bits) for v in row] for row in K]
    bd=[dyadic(v,fixed_bits) for v in beta]
    hd=[dyadic(v,fixed_bits) for v in field]
    cw_exact=mv(S,z)
    require(all(v==w for v,w in zip(cw_exact,
        [v-b*x**3+f for v,b,x,f in zip(mv(K,z),beta,z,field)])))
    cw=[dyadic(v,fixed_bits) for v in cw_exact]
    write_round=norm([x-y for x,y in zip(cw,cw_exact)])
    C=norm(cw); Cexact=norm(cw_exact)
    R0=Q(4); V0=Q(4)
    nu=Q(1,1<<20)  # complete Euclidean read error, including quantization/native error
    zeta=Q(1,1<<16) # Euclidean actuator-equation error
    # Lipschitz constant on physical basin plus all admissible noisy readings.
    lows=[(1-box)*x-nu for x in p]
    highs=[(1+box)*x+nu for x in p]
    require(min(lows)>0)
    L=max(max(abs(K[i][i]-3*beta[i]*lows[i]**2),
              abs(K[i][i]-3*beta[i]*highs[i]**2))
          +sum(abs(K[i][j]) for j in range(n) if j!=i) for i in range(n))
    # Exact integer evaluation with rounded coefficients and final nearest rounding.
    errs=[sum(abs(Kd[i][j]-K[i][j])*highs[j] for j in range(n))
          +abs(bd[i]-beta[i])*highs[i]**3+abs(hd[i]-field[i])+Q(1,2*scale)
          for i in range(n)]
    eval_error=norm(errs)
    Rh=Lg*(1+theta)*P+r
    Fmax=Cexact+L*(theta*P+r+nu)
    Vh=max(V0,C+zeta,Fmax+eval_error+zeta)
    Vw=max(V0,C+zeta); Rw=max(R0,Vw/a)
    # The first retention command may use a reading taken just before handover.
    My=max(BH*Rh+Vh,BH*Rw+Vw)
    delta=Q(1,50); lifetime=Q(1)
    # Known preparation may be anywhere in ||x||<=4, ||v||<=4.
    write_time=Q(9)
    write_e=eupper(a*write_time)
    ew=(Es*P+write_round)/a
    gap=Lg*(theta*P+ew)
    candidates=[]
    for exponent in range(8,25):
        dt=Q(1,1<<exponent); tau=dt
        # Timestamp jitter +/- dt/32 and computation/communication <= dt/16.
        age=Q(9,8)*dt
        require(a*tau<=Q(1,2) and alpha*tau<=Q(1,2))
        M=R0+C/a+2*tau*(V0+C)
        xi=M*write_e+zeta/a
        actuator_tail=(V0+C)*eupper(write_time/tau)+zeta
        w0=xi+gap
        D0=actuator_tail+write_round+L*(xi+ew)
        dinf=L*nu+eval_error+zeta+L*My*(age+tau)
        floor=dinf/alpha
        transient=w0+2*tau*D0
        basin_budget=transient+floor
        candidates.append({'exponent':exponent,'floor':floor,'basin_budget':basin_budget})
        if basin_budget<r and floor<delta/2:
            break
    else: raise ValueError('No selected hardware plan meets the declared margin')
    settle=Q(0)
    while transient*eupper(alpha*settle)+floor>delta:
        settle+=Q(1,8)
    settle_bound=transient*eupper(alpha*settle)+floor
    total_hold=settle+lifetime
    intervals=int(total_hold/dt)
    require(intervals*dt==total_hold)
    # At an initial zero-latency command there is one sample per hold interval.
    # Worst clock-jitter sample count includes one extra boundary sample.
    min_interval=Q(15,16)*dt
    Nworst=1+int(total_hold/min_interval)+1
    slew_write=(Vw+C+zeta)/tau
    slew_hold=(Vh+Fmax+eval_error+zeta)/tau
    source_supply_bound=Rw*Vw*write_time+Rh*Vh*total_hold
    pulse_A=Lg*(P+negative_radius)
    # Runtime bound: all sensor magnitudes <= highs, rounded coefficients <=2^b0.
    largest=max([Q(1)]+highs+[abs(v) for row in Kd for v in row]+list(map(abs,bd))+list(map(abs,hd)))
    b0=1
    while (1<<b0)<largest: b0+=1
    # Accumulated integer numerator has denominator 2^(4p).
    # A deliberately generous width also covers sum(n) and signed temporaries.
    width=4*(fixed_bits+b0)+n.bit_length()+8
    # Per sample: n^2 linear products, 3n cubic products, no arbitrary division.
    mults=n*n+3*n
    adds=n*n+6*n
    # Schoolbook bit operations, including shifts/rounding/reading integer inputs.
    bits_per_sample=(mults+1)*8*width*width+(adds+10*n)*8*width
    memory_bits=(n*n+4*n)*width
    latency=dt/16
    pre_read_bound=M*eupper(a*(write_time-latency))+zeta/a+gap
    require(pre_read_bound<r)
    negative_equilibrium_displacement=negative_residual/m
    negative_basin=negative_radius-negative_equilibrium_displacement
    negative_R=Lg*(P+negative_equilibrium_displacement)+negative_basin
    negative_F=Cexact+2*norm(fg)+L*(negative_radius+nu)
    negative_V=negative_F+eval_error+zeta
    negative_floor=(L*nu+eval_error+zeta+L*(BH*negative_R+negative_V)*(age+tau))/alpha
    source_S_bound=min(A0,max(sum(map(abs,row),Q(0)) for row in S)+Es)
    negative_equilibrium_actuator_bound=source_S_bound*(P+negative_equilibrium_displacement)
    require(negative_floor<negative_basin and negative_equilibrium_actuator_bound<V0)
    result={
      'status':'PASS','n_ports':n,'source_state_access':False,
      'source_priors':{'a':a,'A0':A0,'c0':c0,'lift_bound':Lg,'HB_bound':BH},
      'static_operator_error':Es,'target':z,'target_amplitudes':p,'signs':sigma,
      'target_norm_upper':P,'K':K,'beta':beta,'field':field,
      'source_only_equilibrium_relative_error':theta,
      'local_port_box_relative_radius':box,'local_port_hessian_lower':m,
      'full_state_local_contraction_rate':alpha,'full_state_basin_radius':r,
      'negative_attractor_certificate':{'radius_about_minus_target':negative_radius,
          'gradient_residual_upper':negative_residual,'outward_margin':m*negative_radius-negative_residual,
          'full_state_norm_upper':pulse_A,'strict_nonglobal':True,
          'equilibrium_displacement_bound':negative_equilibrium_displacement,
          'equilibrium_actuator_norm_bound':negative_equilibrium_actuator_bound,
          'retention_only_invariant_radius':negative_basin,
          'retention_only_error_floor':negative_floor,
          'retention_only_state_norm_upper':negative_R,
          'retention_only_command_norm_upper':negative_F},
      'initial_state_norm_bound':R0,'initial_actuator_norm_bound':V0,
      'measurement_error_L2':nu,'actuator_error_L2':zeta,
      'fixed_point_fraction_bits':fixed_bits,'K_fixed':Kd,'beta_fixed':bd,'field_fixed':hd,
      'control_evaluation_error_L2':eval_error,
      'write_command':cw,'write_command_norm_upper':C,'write_command_rounding_error':write_round,
      'write_duration':write_time,'write_state_radius_upper':Rw,'write_force_bound':Vw,
      'write_error_about_own_equilibrium':xi,'write_to_target_equilibrium_gap':gap,
      'state_error_at_switch':w0,'actuator_tracking_error_at_switch':D0,
      'sample_interval':dt,'actuator_time_constant':tau,'clock_jitter_each_timestamp':dt/32,
      'maximum_compute_and_communication_latency':latency,'maximum_reading_age':age,
      'state_error_at_first_possible_pre_switch_read':pre_read_bound,
      'minimum_sample_interval':min_interval,
      'local_feedback_Lipschitz':L,'retention_state_norm_upper':Rh,
      'retention_ideal_command_norm_upper':Fmax,'retention_actuator_norm_upper':Vh,
      'output_time_derivative_bound':My,'continuing_actuator_tracking_error':dinf,
      'retention_error_floor':floor,'handover_transient_coefficient':transient,
      'invariant_basin_budget':basin_budget,'invariant_basin_slack':r-basin_budget,
      'settling_time_after_switch':settle,'certified_error_after_settling':settle_bound,
      'retention_radius_about_true_equilibrium':delta,'retention_duration_after_settling':lifetime,
      'total_retention_law_duration':total_hold,
      'port_relative_error_after_settling':theta+delta/min(p),
      'executed_schedule_intervals':intervals,'worst_clock_sample_count':Nworst,
      'write_slew_bound':slew_write,'retention_slew_bound':slew_hold,
      'source_absolute_supply_integral_bound':source_supply_bound,
      'source_power_bound_write':Rw*Vw,'source_power_bound_retention':Rh*Vh,
      'source_steady_pattern_supply_lower':a*(1-theta)**2*P2,
      'controller_integer_width_bound':width,'controller_multiplications_per_sample':mults,
      'controller_additions_per_sample_bound':adds,'controller_bit_operations_per_sample_bound':bits_per_sample,
      'controller_working_bits_bound':memory_bits,'required_bit_operations_per_time_bound':Q(bits_per_sample)/latency,
      'planner_elementary_cost':elementary,
      'planner_encoded_input_bytes':sum((ROOT/path).stat().st_size for path in ['inputs/PROGRAMMED_PATTERN.json','inputs/ORDER_INPUTS.json']),
      'candidate_sample_plans':candidates,
      'model':'first-order actual actuator; sampled noisy reader; programmed force switch',
      'execution_scope':'native finite-source software; no laboratory or real-time hardware execution',
    }
    result['certificate_rational_bits_max']=maxbits(result)
    return result


if __name__=='__main__':
    plan=make_plan();save(ROOT/'results/PLAN.json',plan)
    keys=['static_operator_error','local_port_hessian_lower','full_state_local_contraction_rate',
          'local_feedback_Lipschitz','sample_interval','state_error_at_switch','actuator_tracking_error_at_switch',
          'retention_error_floor','invariant_basin_budget','full_state_basin_radius',
          'settling_time_after_switch','executed_schedule_intervals','source_absolute_supply_integral_bound',
          'required_bit_operations_per_time_bound']
    print(json.dumps({k:float(plan[k]) for k in keys},indent=2))
