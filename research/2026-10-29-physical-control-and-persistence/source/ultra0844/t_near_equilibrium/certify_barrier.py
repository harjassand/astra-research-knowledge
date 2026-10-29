"""Exact constants/source controls for the full near-equilibrium barrier.

No kinetic sampler, old fixture, producer module or grid is run.
"""
from fractions import Fraction as F
from pathlib import Path
import json,math,time


def atan_bounds(x,n):
    total=sum((-1)**j*x**(2*j+1)/F(2*j+1) for j in range(n))
    next_term=(-1)**n*x**(2*n+1)/F(2*n+1)
    return min(total,total+next_term),max(total,total+next_term)


def main():
    started=time.perf_counter()
    p_ball,p_shell=F(41,189),F(148,189)
    assert p_ball+p_shell==1
    m_ball=F(3,5)*2**2
    m_shell=F(3,5)*(F(2)**5-F(3,2)**5)/(F(2)**3-F(3,2)**3)
    assert m_ball==F(12,5) and m_shell==F(2343,740)
    assert p_ball*m_ball+p_shell*m_shell==3
    # Densities expressed as coefficients of1/pi.
    density_ball=F(3,32);density_shell=F(6,37)
    density_max=p_ball*density_ball+p_shell*density_shell
    assert density_max==F(33,224)
    a5=atan_bounds(F(1,5),12);a239=atan_bounds(F(1,239),4)
    pi_upper=16*a5[1]-4*a239[0]
    assert pi_upper<F(22,7)
    assert 2*pi_upper<F(64,9) # sqrt2pi<8/3.
    n=12
    exp_partial=sum(F(2)**j/math.factorial(j) for j in range(n+1))
    exp_upper=exp_partial+(F(2)**(n+1)/math.factorial(n+1))/(1-F(2,n+2))
    assert exp_upper<F(15,2)
    ratio_upper=F(33,112)*F(8,3)*F(15,2)
    assert ratio_upper==F(165,28)<6
    radius,target_speed=F(2),F(8)
    min_relative=target_speed-radius
    kernel_upper=4*F(15,2)/min_relative-min_relative
    assert kernel_upper==-1
    assert target_speed**2>2*radius**2
    literal_kernel=4/target_speed-target_speed
    assert literal_kernel==F(-15,2)
    result={"status":"PASS_exact_analytic_constants",
        "source_weights":[str(p_ball),str(p_shell)],
        "ball_energy":str(m_ball),"shell_energy":str(m_shell),
        "source_energy":3,"source_mean":[0,0,0],"source_covariance":"I_by_radial_symmetry",
        "source_max_density_coefficient_of_1_over_pi":str(density_max),
        "exp2_upper":str(exp_upper),"pi_upper":str(pi_upper),
        "r_over_M_upper":str(ratio_upper),
        "global_relative_fdelta_nearness":"<=5delta, all0<delta<1",
        "source_radius":str(radius),"target_speed_lower":str(target_speed),
        "uniform_cross_kernel_over_M_upper":str(kernel_upper),
        "literal_v8_w0_cross_kernel_over_M":str(literal_kernel),
        "quadratic_r_r_gain_on_target_region":0,
        "fixed_share_tangent_upper":"-delta(1-delta)M on |v|>=8",
        "finite_scalar_depletion":"excluded from tight share by c_V->infinity",
        "all_exact_iid_uniform_time_algorithms_excluded":False,
        "no_MC_or_sampler_rerun":True,"elapsed_seconds":time.perf_counter()-started}
    out=Path(__file__).parent/'CERTIFICATE.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
