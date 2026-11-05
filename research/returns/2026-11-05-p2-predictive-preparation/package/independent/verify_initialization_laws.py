"""Diagnostic checks for the analytic initialization theorems.

Floating quadrature/ODE results are diagnostics, not interval certificates.
The formulas and inequalities in the two proof files carry the general claims.
"""
from pathlib import Path
import json
import math

import numpy as np
from scipy.integrate import quad, solve_ivp


def impulse(t, a, B, mu):
    c = a + mu + B
    disc = math.sqrt(c * c - 4 * a * mu)
    slow, fast = (c-disc)/2, (c+disc)/2
    return math.sqrt(2*B*a) * (np.exp(-slow*t)-np.exp(-fast*t))/disc


def h2_closed(T, a, B, mu):
    c = a + mu + B
    disc = math.sqrt(c*c-4*a*mu)
    slow, fast = (c-disc)/2, (c+disc)/2
    integ = (-math.expm1(-2*slow*T)/(2*slow)
             -math.expm1(-2*fast*T)/(2*fast)
             +2*math.expm1(-c*T)/c)
    return 2*B*a*integ/(disc*disc)


def main():
    a, B, mu, E = 1.3, .7, 1.1, .4
    minimax = []
    for T in (.03, .2, 1., 4.):
        h2 = h2_closed(T,a,B,mu)
        numerical = quad(lambda t: impulse(t,a,B,mu)**2,0,T,
                         epsabs=1e-13,epsrel=1e-12)[0]
        norm = math.sqrt(h2)
        w = lambda s: math.sqrt(2*E)*impulse(T-s,a,B,mu)/norm
        energy = quad(lambda s: w(s)**2/2,0,T,
                      epsabs=1e-12,epsrel=1e-12)[0]
        endpoint = quad(lambda s: impulse(T-s,a,B,mu)*w(s),0,T,
                        epsabs=1e-12,epsrel=1e-12)[0]
        assert abs(numerical-h2) < 1e-11
        assert abs(energy-E) < 1e-10
        assert abs(endpoint-math.sqrt(2*E)*norm) < 1e-10
        minimax.append(dict(T=T,h2_closed=h2,h2_quadrature=numerical,
                            extremizer_energy=energy,attained_radius=endpoint))

    # H^1 pulse: exact time-domain energy and independent spectral quadrature.
    A, pulse_T = .3, 1.7
    time_energy = A*A*(math.pi**2/(2*pulse_T)+3*a*a*pulse_T/8)/(4*B*a)
    def box_ft(omega):
        return pulse_T*np.exp(-1j*omega*pulse_T/2)*np.sinc(omega*pulse_T/(2*np.pi))
    def pulse_ft(omega,H):
        k=2*np.pi/pulse_T
        return A*np.exp(-1j*omega*H)*(.5*box_ft(omega)-.25*box_ft(omega-k)-.25*box_ft(omega+k))
    W=500.
    spectral=[]
    for H in (0.,1000.):
        val=quad(lambda om:(a*a+om*om)*abs(pulse_ft(om,H))**2,
                 0,W,epsabs=1e-10,limit=1200)[0]/(4*np.pi*B*a)
        assert abs(val-time_energy)<2e-8
        spectral.append(dict(delay=H,spectral_energy_to_cutoff=val))

    # Random-window experiment from a fixed incoming waveform. The exact
    # continuum plant has this compressed observable ODE with an incoming port.
    a=B=mu=1.
    horizon,b,kap,N=1.,.2,.01,128
    D=horizon+b+2*kap
    end=N*D
    centers=np.array([8.,24.,61.,103.])
    amplitudes=np.array([.6,-.4,.7,-.5])
    width=.6
    def incoming(t):
        s=(t-centers)/width
        active=np.abs(s)<1
        return float(np.sum(amplitudes[active]*np.cos(np.pi*s[active]/2)**2))
    # Each disjoint cos^2 pulse has integral w^2 = amplitude^2*(3width/4).
    incoming_energy=.5*float(np.sum(amplitudes**2))*3*width/4
    def rhs(t,state):
        x,z,g,spent=state
        v=-mu*x-z+g
        return [v,-a*z+B*v,-a*g+math.sqrt(2*B*a)*incoming(t),v*v]
    sol=solve_ivp(rhs,(0,end),[0,0,0,0],rtol=2e-10,atol=1e-12,
                  max_step=.025,dense_output=True)
    spent=float(sol.y[3,-1])
    assert spent <= incoming_energy*(1+1e-7)
    delta=.1
    bad=0
    maximum_ratio=0.
    for j in range(N):
        # Fixed admissible timing offset, within the declared clock envelope.
        tau=j*D+b+kap + .7*kap*math.sin(j)
        baseline=quad(lambda t:float(sol.sol(t)[0]),tau-b,tau,
                      epsabs=1e-10)[0]/b
        grid=np.linspace(tau,tau+horizon,601)
        deviation=float(np.max(np.abs(sol.sol(grid)[0]-baseline)))
        block_spent=float(sol.sol((j+1)*D)[3]-sol.sol(j*D)[3])
        bound=math.sqrt(max(0.,(horizon+b)*block_spent))
        # Numerical integration has tiny errors in nearly flat blocks.
        assert deviation <= bound+3e-8
        if bound>1e-7:
            maximum_ratio=max(maximum_ratio,deviation/bound)
        if deviation>delta:
            bad+=1
    probability_bound=min(1.,incoming_energy*(horizon+b)/(N*delta*delta))
    assert bad/N <= probability_bound+1e-12

    result={
        'status':'floating diagnostics for analytic theorems; not a physical experiment',
        'minimax_radius_checks':minimax,
        'spectral_energy_check':{
            'exact_time_energy':time_energy,'frequency_cutoff':W,'values':spectral},
        'finite_clock_example':{
            'N':N,'horizon':horizon,'position_window':b,'clock_bound':kap,
            'block_length':D,'maximum_elapsed_time':end,
            'initial_incoming_energy':incoming_energy,
            'observed_dissipation_to_end':spent,
            'delta':delta,'bad_blocks':bad,'actual_grid_bad_fraction':bad/N,
            'energy_probability_upper_bound':probability_bound,
            'largest_sampled_motion_to_block_bound_ratio':maximum_ratio},
        'limits':[
            'No raw physical meter samples were acquired.',
            'No claim of optimal randomized waiting scaling is made.',
            'The fixed-deadline minimax identity is analytic and sharp.',
            'Randomized selection assumes the initial state precedes the private seed.']}
    out=Path(__file__).with_name('initialization_law_checks.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
