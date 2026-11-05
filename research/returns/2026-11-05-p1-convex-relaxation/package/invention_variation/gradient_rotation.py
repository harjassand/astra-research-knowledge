"""Exact-model construction for bounded, symmetric restoring forces in 2D.

No experiments. The underlying SL(2,R) geometry is established prior art.
This script checks the explicit reachability formula and a thermal-noise
ordering deduction. Contraction is NOT heat or actuator work.
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent
J = np.array([[0., -1.], [1., 0.]])
E = np.diag([1., -1.])


def rotation(angle):
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s], [s, c]])


def shape_distance(N):
    """SL2 distance and a minimizing rotating-strain program.

    The formula is an elementary, monotone scalar root, not a distance oracle.
    The near-rotation branch uses a rescaled chart so that subtracting a
    barely resolved delta from pi cannot corrupt the endpoint. This is still
    floating arithmetic, not a certified all-scale interval implementation.
    """
    N = np.asarray(N, dtype=float)
    if N.shape != (2, 2) or abs(np.linalg.det(N)-1.) > 2e-8:
        raise ValueError('N must have determinant one')
    u = complex((N[0,0]+N[1,1])/2, (N[1,0]-N[0,1])/2)
    v = complex((N[0,0]-N[1,1])/2, (N[0,1]+N[1,0])/2)
    q = abs(v)
    theta = math.atan2(u.imag, u.real)
    target = abs(theta)
    sign = 1. if theta >= 0 else -1.
    if q == 0:
        if target == 0:
            return dict(distance=0., w=0., alpha=0., q=q, theta=theta, branch='identity')
        d = math.sqrt(target*target + 2*math.pi*target)
        return dict(distance=d, w=sign*(math.pi+target), alpha=0., q=q,
                    theta=theta, branch='rotation')
    r = math.asinh(q)
    h = q-math.atan(q)
    if target < 1e-14:
        d, w, branch = r, 0., 'straight strain'
    elif target <= h:
        def f(z):
            if z == 0:
                return h-target
            t = math.sinh(z)
            b = math.sqrt(max(0., q*q-t*t))
            return z*b/t - math.atan2(b, math.cosh(z))-target
        z = brentq(f, 0., r, xtol=1e-14, rtol=1e-14)
        if z < 1e-12:
            d, w = q, sign*q
        else:
            t = math.sinh(z)
            d = q*z/t
            w = sign*z*math.sqrt(max(0., q*q-t*t))/t
        branch = 'hyperbolic'
    elif q < .01*math.sqrt(target*target+2*math.pi*target):
        # Near a rotation, pi-delta is O(q). Solve for its scaled value
        # z=(pi-delta)/q; never evaluate sin(pi-small) or divide q by an
        # unresolved distance to pi. The old direct-delta branch failed
        # badly at q~1e-12 despite well-scaled target matrix entries.
        rotation_distance=math.sqrt(target*target+2*math.pi*target)
        def chart(z):
            epsilon=q*z
            if epsilon >= math.pi:
                return h-target
            t=z*np.sinc(epsilon/math.pi) # sin(qz)/q, stably
            dd=(math.pi-epsilon)/t
            ww=dd*math.hypot(1.,t)
            phi=math.atan2(q*math.hypot(1.,t),-math.cos(epsilon))
            return ww-phi-target
        guess=math.pi/rotation_distance
        lo,hi=guess/2,guess*2
        while chart(lo)<0:
            lo/=2
        while chart(hi)>0:
            hi=min(hi*2,math.pi/q)
        z=brentq(chart,lo,hi,xtol=1e-14,rtol=1e-14)
        epsilon=q*z
        t=z*np.sinc(epsilon/math.pi)
        d=(math.pi-epsilon)/t
        w=sign*d*math.hypot(1.,t)
        branch='elliptic near-rotation stable chart'
    else:
        def f(delta):
            if delta == 0:
                return h-target
            t = math.sin(delta)
            b = math.sqrt(q*q+t*t)
            return delta*b/t-math.atan2(b, math.cos(delta))-target
        delta = brentq(f, 0., np.nextafter(math.pi, 0.), xtol=1e-14, rtol=1e-14)
        t = math.sin(delta)
        d = q*delta/t
        w = sign*delta*math.sqrt(q*q+t*t)/t
        branch = 'elliptic'
    alpha = (math.atan2(v.imag, v.real)-w-math.pi)/2
    return dict(distance=d, w=w, alpha=alpha, q=q, theta=theta, branch=branch)


def compile_target(M, cap=1.):
    """Exact minimum-time mean-map program when the target is reachable."""
    M = np.asarray(M, dtype=float)
    det = float(np.linalg.det(M))
    if cap <= 0 or det <= 0:
        raise ValueError('Positive cap and positive target determinant required')
    s = -.5*math.log(det)
    N = M/math.sqrt(det)
    geo = shape_distance(N)
    d = geo['distance']
    if s < d-1e-10:
        return dict(reachable=False, s=s, N=N.tolist(), **geo)
    T = (s+d)/cap
    if T == 0:
        return dict(reachable=True, s=s, T=0., a=0., k=0., omega=0., cap=cap, **geo)
    return dict(reachable=True, s=s, T=T, a=s/T, k=d/T,
                omega=geo['w']/T, cap=cap, **geo)


def closed_mean(program):
    T, a, k, omega, alpha = [program[x] for x in ('T','a','k','omega','alpha')]
    return math.exp(-a*T)*rotation(alpha+omega*T)@expm(-(k*E+omega*J)*T)@rotation(-alpha)


def gaussian_protocol(a, k, omega, alpha, T, diffusion=1., drag=1., initial_second=None):
    """Full Gaussian mean/noise map and continuous actuator work in this model.

    Work is integral (drag/2) tr(A_dot E[xx^T]) dt. Initial/final changes
    of the trap, initial state preparation and real actuator losses are extra.
    """
    if initial_second is None:
        initial_second = np.eye(2)
    B = a*np.eye(2)+k*E+omega*J
    F = np.block([[-B, 2*diffusion*np.eye(2)], [np.zeros((2,2)), B.T]])
    ef = expm(F*T)
    eb = ef[:2,:2]
    Qbody = ef[:2,2:]@eb.T
    R0, RT = rotation(alpha), rotation(alpha+omega*T)
    M = RT@eb@R0.T
    Q = RT@Qbody@RT.T
    Q = (Q+Q.T)/2
    C0 = R0.T@np.asarray(initial_second)@R0
    W = np.zeros((5,5))
    W[:3,:3] = [[-2*(a+k), 2*omega, 0],
                 [-omega, -2*a, omega],
                 [0, -2*omega, -2*(a-k)]]
    W[:3,3] = [2*diffusion, 0, 2*diffusion]
    W[4,1] = 2*drag*omega*k
    moment = expm(W*T)@np.array([C0[0,0],C0[0,1],C0[1,1],1.,0.])
    return dict(M=M, Q=Q, continuous_actuator_work=float(moment[4]))


def fastest_shape_then_cool(program, diffusion=1., initial_second=None, drag=1.):
    """Minimum added noise for this minimizing shape, among minimum-time maps."""
    d, s, cap = [program[x] for x in ('distance','s','cap')]
    surplus = max(0., s-d)
    if d < 1e-14:
        return dict(M=math.exp(-s)*np.eye(2),
                    Q=(diffusion/cap)*(1-math.exp(-2*s))*np.eye(2),
                    geometric_time=0., cooling_time=s/cap,
                    net_work_with_endpoint_quenches=0.,
                    predicted_net_work=0.)
    tg = 2*d/cap
    g = gaussian_protocol(cap/2, cap/2, program['w']/tg, program['alpha'], tg,
                          diffusion=diffusion, initial_second=initial_second, drag=drag)
    if initial_second is None:
        initial_second=np.eye(2)
    C0=np.asarray(initial_second)
    Cg=g['M']@C0@g['M'].T+g['Q']
    R0=rotation(program['alpha'])
    Rg=rotation(program['alpha']+program['w'])
    A0=cap/2*(np.eye(2)+R0@E@R0.T)
    Ag=cap/2*(np.eye(2)+Rg@E@Rg.T)
    begin_quench=drag/2*np.trace((A0-cap*np.eye(2))@C0)
    end_quench=drag/2*np.trace((cap*np.eye(2)-Ag)@Cg)
    total_work=begin_quench+g['continuous_actuator_work']+end_quench
    b = math.exp(-surplus)
    return dict(M=b*g['M'],
                Q=b*b*g['Q']+(diffusion/cap)*(1-b*b)*np.eye(2),
                geometric_time=tg, cooling_time=surplus/cap,
                geometric_continuous_actuator_work=g['continuous_actuator_work'],
                begin_quench_work=float(begin_quench),end_quench_work=float(end_quench),
                net_work_with_endpoint_quenches=float(total_work),
                predicted_net_work=2*drag*diffusion*d)


def radial_tail(radius, eigenvalues):
    """Exact quadrature for ||N(0,Q)||; orientation does not enter."""
    lo,hi=sorted(map(float,eigenvalues))
    if hi == 0:
        return float(radius < 0)
    def integrand(phi):
        variance=lo*math.cos(phi)**2+hi*math.sin(phi)**2
        return math.exp(-radius*radius/(2*variance)) if variance else 0.
    return 2/math.pi*quad(integrand,0,math.pi/2,epsabs=1e-12,epsrel=1e-12)[0]


def radial_quantile(probability,eigenvalues):
    if not 0 < probability < 1:
        raise ValueError('Probability must be between zero and one')
    hi=max(eigenvalues)
    if hi == 0:
        return 0.
    bound=math.sqrt(2*hi*math.log(1/(1-probability)))*1.001
    return brentq(lambda r:radial_tail(r,eigenvalues)-(1-probability),0,bound,
                  xtol=1e-12,rtol=1e-12)


def numerical_ode(program, diffusion=1.):
    T, a, k, omega, alpha = [program[x] for x in ('T','a','k','omega','alpha')]
    def rhs(t,y):
        R = rotation(alpha+omega*t)
        A = a*np.eye(2)+k*R@E@R.T
        M = y[:4].reshape(2,2)
        Q = y[4:].reshape(2,2)
        return np.r_[(-A@M).ravel(), (-A@Q-Q@A+2*diffusion*np.eye(2)).ravel()]
    out = solve_ivp(rhs,(0,T),np.r_[np.eye(2).ravel(),np.zeros(4)],
                    rtol=1e-11,atol=1e-12,max_step=max(T/150,1e-6))
    if not out.success:
        raise RuntimeError(out.message)
    return out.y[:4,-1].reshape(2,2), out.y[4:,-1].reshape(2,2)


def main():
    rng=np.random.default_rng(581037)
    tests=[]
    shapes=[rotation(x) for x in [0.,.01,.2,math.pi/2,math.pi,-.7]]
    shapes.extend([rotation(float(rng.uniform(-math.pi,math.pi)))@
                   np.diag(np.exp([r,-r]))@rotation(float(rng.uniform(-math.pi,math.pi)))
                   for r in rng.uniform(.02,2.5,30)])
    for j,N in enumerate(shapes):
        geo=shape_distance(N)
        s=geo['distance']+(.7 if j%2 else .05)
        target=math.exp(-s)*N
        p=compile_target(target)
        analytic=gaussian_protocol(p['a'],p['k'],p['omega'],p['alpha'],p['T'])
        measured,Qnum=numerical_ode(p)
        Z=rng.normal(size=(2,2));C0=Z@Z.T
        cool=fastest_shape_then_cool(p,initial_second=C0)
        excess=analytic['Q']-(np.eye(2)-analytic['M']@analytic['M'].T)
        row={'case':j,'branch':p['branch'],'s':s,'distance':p['distance'],'T':p['T'],
             'mean_closed_error':float(np.linalg.norm(analytic['M']-target)),
             'mean_ODE_error':float(np.linalg.norm(measured-target)),
             'noise_closed_ODE_error':float(np.linalg.norm(Qnum-analytic['Q'])),
             'cool_last_mean_error':float(np.linalg.norm(cool['M']-target)),
             'cool_last_covariance_improvement_min_eigenvalue':float(np.linalg.eigvalsh(analytic['Q']-cool['Q'])[0]),
             'bath_floor_excess_min_eigenvalue':float(np.linalg.eigvalsh(excess)[0])}
        row['net_work_with_endpoint_quenches']=cool['net_work_with_endpoint_quenches']
        row['net_work_identity_error']=abs(cool['net_work_with_endpoint_quenches']-cool['predicted_net_work'])
        assert row['mean_closed_error']<1e-9,row
        assert row['mean_ODE_error']<1e-9,row
        assert row['noise_closed_ODE_error']<2e-8,row
        assert row['cool_last_mean_error']<1e-9,row
        assert row['cool_last_covariance_improvement_min_eigenvalue']>-1e-8,row
        assert row['bath_floor_excess_min_eigenvalue']>-1e-8,row
        assert row['net_work_identity_error']<1e-8,row
        tests.append(row)
    rows=[]
    for degrees in [1,10,45,90,180]:
        th=math.radians(degrees);ell=math.sqrt(th*th+2*math.pi*th)
        ratio=ell/(math.pi+th);f=-math.expm1(-2*ell)
        Q=2*f*np.array([[1.,ratio],[ratio,1+2*ratio*ratio]])
        p=compile_target(math.exp(-ell)*rotation(th))
        analytic=gaussian_protocol(p['a'],p['k'],p['omega'],p['alpha'],p['T'])
        R=rotation(math.pi+th)
        assert np.linalg.norm(analytic['Q']-R@Q@R.T)<1e-9
        randomised=(analytic['Q']+rotation(math.pi/2)@analytic['Q']@rotation(-math.pi/2))/2
        assert np.linalg.norm(randomised-np.trace(analytic['Q'])/2*np.eye(2))<1e-12
        rows.append({'angle_degrees':degrees,'minimal_log_attenuation':ell,
                     'amplitude_retained':math.exp(-ell),'minimal_time_times_cap':2*ell,
                     'added_noise_eigenvalues_in_D_over_cap':np.linalg.eigvalsh(Q).tolist(),
                     'randomized_worst_direction_variance_in_D_over_cap':float(np.trace(Q)/2),
                     'optimal_radius_95_in_sqrt_D_over_cap':radial_quantile(.95,np.linalg.eigvalsh(Q)),
                     'net_work_in_kBT':2*ell})
    out={'status':'Synthetic verification of an exact controlled-OU model; no experiment or new physical law',
         'scope':'Deterministic time-dependent 2D symmetric PSD drift, cap I; D=1 in tests. Randomized orientation is separately labeled.',
         'prior_art_status':'The SL2 sub-Riemannian geometry and gradient-flow holonomy are established; novelty of the stochastic scheduling consequence requires literature audit.',
         'cases':tests,'rotation_table':rows}
    (HERE/'gradient_rotation_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({'cases':len(tests),'max_mean_error':max(z['mean_ODE_error'] for z in tests),
                      'max_noise_error':max(z['noise_closed_ODE_error'] for z in tests),
                      'rotation_table':rows},indent=2))


if __name__=='__main__':
    main()
