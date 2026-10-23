"""Conditional positive-Debye continuation of the published 10 ms pulse.

This is an attack on one explicitly linear, time-invariant passive model.  It
is not a deduction of low-frequency nonlinear FE loss from that pulse.
"""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from numpy.polynomial.legendre import leggauss

HERE = Path(__file__).resolve().parent
SRC = HERE.parent
V = 23.27
N = 10
AREA = np.pi * (0.1e-3)**2
PERIOD = 0.026
SEGMENTS = [(0., V, .010), (V, V, .003),
            (V, 0., .010), (0., 0., .003)]
UNCERTAINTY_UA = 9.467455621301774e-8 * 1e6


def generic_coefficients(t, voltage, taus):
    """LP loss coefficients for any continuous periodic piecewise-linear path.

    Return J per ten-film-bank m2 for each 1 microampere step-response
    amplitude, first the DC shunt then each supplied Debye tau.  Discrete
    voltage jumps need finite transition times supplied by the circuit: this
    routine refuses duplicate time samples and unequal endpoint voltages.
    """
    t=np.asarray(t,dtype=float); voltage=np.asarray(voltage,dtype=float)
    taus=np.asarray(taus,dtype=float)
    if len(t)!=len(voltage) or len(t)<2 or np.any(np.diff(t)<=0):
        raise ValueError('Need strictly increasing time and matching voltage samples')
    if abs(voltage[-1]-voltage[0])>1e-8:
        raise ValueError('Periodic path must explicitly return to initial voltage')
    if np.any(taus<=0):raise ValueError('Positive relaxation times required')
    dt=np.diff(t); slopes=np.diff(voltage)/dt
    def evolve(x,loss=False):
        total=np.zeros_like(taus)
        for v0,h,m in zip(voltage[:-1],dt,slopes):
            z=h/taus;p=-np.expm1(-z);a=1-p;u=v0-x
            if loss:
                f=z-p-p*p/2
                small=z<.005
                zz=z[small]
                f[small]=zz**3*(1/3+zz*(-1/4+zz*(7/60+zz*(-1/24+zz*31/2520))))
                total += u*u*(p-p*p/2)+u*m*taus*p*p+(m*taus)**2*f
            x=v0+m*h-(u*a+m*taus*p)
        return x,total
    b,_=evolve(np.zeros_like(taus))
    x0=b/(-np.expm1(-(t[-1]-t[0])/taus))
    xf,energy_per_C=evolve(x0,True)
    # C=1uA*tau/V for one unit of fitted step amplitude.
    deb=energy_per_C*taus*N/AREA*1e-6/V
    intv2=float(np.sum(dt*(voltage[:-1]**2+voltage[:-1]*voltage[1:]+voltage[1:]**2)/3))
    dc=intv2*N/AREA*1e-6/V
    return np.r_[dc,deb],float(np.max(abs(xf-x0)))


def branch(tau):
    """Return periodic dissipation integral int (V-x)^2 dt and reset residual.

    Each Debye capacitor has xdot=(V-x)/tau.  The capacitor voltage x is reset
    periodically, not arbitrarily set to zero at each ramp.  A 64 point rule
    handles tau >= segment/40; the exact expression handles shorter boundary
    layers.  Both expressions are integrated on the exact analytic trajectory.
    """
    def propagate(x):
        for v0, v1, duration in SEGMENTS:
            m = (v1-v0)/duration
            r = -np.expm1(-duration/tau)
            # Exact ramp: x_end = v1 - [(v0-x)*exp(-dt/tau)+m*tau*r].
            x = v1 - ((v0-x)*(1-r)+m*tau*r)
        return x
    b = propagate(0.)
    decay = np.exp(-PERIOD/tau)
    x = b / (-np.expm1(-PERIOD/tau))
    x_initial = x
    z, w = leggauss(64)
    integral = 0.
    for v0, v1, duration in SEGMENTS:
        m = (v1-v0)/duration
        y0 = v0-x
        if duration/tau <= 40:
            tt = (z+1)*duration/2
            yy = y0*np.exp(-tt/tau) + m*tau*(-np.expm1(-tt/tau))
            integral += float(duration/2*np.dot(w, yy*yy))
        else:
            a = np.exp(-duration/tau)
            b = y0-m*tau
            integral += ((m*tau)**2*duration
                         + 2*m*tau*b*tau*(1-a)
                         + b*b*tau/2*(1-a*a))
        r = -np.expm1(-duration/tau)
        x = v1 - (y0*(1-r)+m*tau*r)
    return integral, x-x_initial


def solve(taus, uncertainty_scale=1., force_dc=None, waveform=None, objective_cost=None):
    d = np.genfromtxt(SRC/'source_10ms_current.csv', delimiter=',', names=True)
    take = d['time_s'] >= .001
    t = d['time_s'][take]
    y = d['source_current_A'][take] * 1e6
    # Positive step amplitudes in microampere per original source device.
    A = np.c_[np.ones(len(t)), np.exp(-t[:,None]/taus)]
    if waveform is None:
        waveform=(np.array([0.,.010,.013,.023,.026]),np.array([0.,V,V,0.,0.]))
    cost,reset_error=generic_coefficients(*waveform,taus)
    if objective_cost is not None:
        cost=np.asarray(objective_cost,dtype=float)
        if cost.shape != (len(taus)+1,):raise ValueError('Objective dimension mismatch')
    err = UNCERTAINTY_UA * uncertainty_scale
    bounds = [(0,None)]*(len(taus)+1)
    if force_dc is not None:
        bounds[0] = (force_dc, force_dc)
    result = linprog(cost, A_ub=np.r_[A,-A],
                     b_ub=np.r_[y+err,-y+err], bounds=bounds,
                     method='highs', options={'dual_feasibility_tolerance':1e-9,
                                               'primal_feasibility_tolerance':1e-9})
    if not result.success:
        return dict(success=False,message=result.message)
    x = result.x
    active = []
    for i in np.flatnonzero(x > 1e-8):
        item = dict(step_amplitude_microampere=float(x[i]),
                    loss_J_per_bank_m2=float(cost[i]*x[i]))
        if i == 0:
            item['kind'] = 'DC conductance'
            item['conductance_S_per_source_device'] = float(x[i]*1e-6/V)
        else:
            item.update(kind='Debye branch', tau_s=float(taus[i-1]),
                        C_F_per_source_device=float(x[i]*1e-6*taus[i-1]/V))
        active.append(item)
    predicted=A@x
    return dict(success=True, minimum_loss_J_per_bank_m2=float(result.fun),
                dc_loss_J_per_bank_m2=float(x[0]*cost[0]),
                absorption_loss_J_per_bank_m2=float(result.fun-x[0]*cost[0]),
                maximum_absolute_current_fit_error_A=float(np.max(abs(predicted-y))*1e-6),
                active_components=active, observed_t0_s=float(t[0]),
                tau_grid_min_s=float(taus.min()),tau_grid_max_s=float(taus.max()),
                tau_grid_size=len(taus),uncertainty_scale=uncertainty_scale,
                forced_dc_amplitude_microampere=force_dc,
                periodic_Debye_reset_max_error_V=reset_error,
                _t=t,_y=y,_predicted=predicted,_x=x,_cost=cost,_A=A,
                _dual=result.ineqlin.marginals)


def clean(result):
    return {k:v for k,v in result.items() if not k.startswith('_')}


def main():
    taus=np.geomspace(1e-6,10,1201)
    result=solve(taus)
    variants=[clean(solve(np.geomspace(1e-6,10,n))) for n in [401,801,1601]]
    variants += [clean(solve(taus, uncertainty_scale=s)) for s in [0.5,2.,4.]]
    variants += [clean(solve(taus,force_dc=0.))]
    out=dict(scope='CONDITIONAL_LINEAR_PASSIVE_STEP_RESPONSE_ATTACK',
             constitutive_assumption='I_step(t)=V*[g+sum(C_k/tau_k)*exp(-t/tau_k)], g,C_k>=0; initially uncharged Debye branches',
             source_condition='348.15 K, nominal 895 kV/cm positive voltage step; initial bump and all t<1 ms excluded',
             waveform=[dict(V0=a,V1=b,duration_s=t) for a,b,t in SEGMENTS],
             period_s=PERIOD, electrode_area_m2=AREA,
             films_per_parallel_bank=N, exact_periodic_all_Debye_states=True,
             current_uncertainty_A=UNCERTAINTY_UA*1e-6,
             result=clean(result), convergence_and_sensitivity=variants,
             claim_boundaries=[
                 'One conditioning trace does not establish this linear time-invariant constitutive law, initial state, or the proposed nonlinear engine response.',
                 'The finite positive relaxation spectrum fit can test reinterpreting a tail as recoverable absorption instead of DC leakage within that law.',
                 'These are additional transient branches, not the reversible FE envelope already counted in the candidate engine.',
                 'Each branch capacitor returns to its periodic initial voltage; no trapped-charge reset inventory is silently consumed.',
                 'Unobserved sub-millisecond modes leave no scientifically useful upper bound: their permissible amplitude grows exponentially with inverse tau.',
                 'No favorable values are assigned to hysteresis, switches, contacts, controls, or a replacement cycle.'])
    (HERE/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    if result['success']:
        np.savetxt(HERE/'minimum_fit.csv',np.c_[result['_t'],result['_y']*1e-6,
                   result['_predicted']*1e-6],delimiter=',',comments='',
                   header='time_s,source_current_A,minloss_fit_current_A')
    print(json.dumps(out,indent=2))


if __name__ == '__main__':
    main()
