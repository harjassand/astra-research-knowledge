#!/usr/bin/env python3
"""Population checks of the real metered cell and rejected active recorder."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parent
H = np.pi/2
B = np.pi/(2*np.sqrt(2))


def cell(omega, refresh, ratio):
    # Order V,Z,R,P,zeta,xi,A,F; F is held and A initially zero.
    beta = np.arccos(refresh)/B
    a = np.zeros((8, 8))
    a[0, 1], a[1, 0] = -omega, omega
    a[0, 2], a[2, 0] = -ratio, ratio
    a[2, 3], a[3, 2] = -1, 1
    a[6, 0] = a[0, 7] = 1
    transport = expm(H*a)
    a = np.zeros((8, 8))
    a[0, 2], a[2, 0] = -ratio, ratio
    a[2, 3], a[3, 2] = -1, 1
    a[3, 4], a[4, 3] = -1, 1
    a[1, 5], a[5, 1] = -beta, beta
    a[6, 0] = a[0, 7] = 1
    full = expm(B*a)@transport
    m, noise, d = full[:4, :4], full[:4, 4:6], full[:4, 7]
    ell, out, c = full[6, :4], full[6, 4:6], full[6, 7]
    k = np.linalg.solve((np.eye(4)-m).T, ell)
    return dict(full=full, m=m, noise=noise, d=d, k=k,
                mu=c+k@d, sigma=out+k@noise, beta=beta)


def algebra():
    rows = []
    for ratio in (0., .01, .1, .25):
        for omega, refresh in ((.5, -.5), (.9, .2), (1.25, .7)):
            c = cell(omega, refresh, ratio)
            m, noise, full = c['m'], c['noise'], c['full']
            rho = float(max(abs(np.linalg.eigvals(m))))
            errors = dict(gaussian=float(np.max(abs(m@m.T+noise@noise.T-np.eye(4)))),
                fdt=float(abs(c['sigma']@c['sigma']-2*c['mu'])),
                energy_linear=float(np.max(abs(full[6, :6]-full[:6, 7]@full[:6, :6]))),
                energy_quadratic=float(abs(full[6, 7]-.5*(full[:6, 7]@full[:6, 7]))))
            assert rho < 1 and c['mu'] > 0 and max(errors.values()) < 2e-11
            rows.append(dict(ratio=ratio, omega=omega, refresh=refresh,
                spectral_radius=rho, mobility=float(c['mu']), residuals=errors))
    exact = np.array([[-1/np.sqrt(2), -.5], [0, -1/np.sqrt(2)]])
    error = float(np.max(abs(cell(.9, .2, 0.)['m'][2:4, 2:4]-exact)))
    assert error < 1e-14
    return dict(exact_probe_block_residual=error, cells=rows)


def nonlinear_meter():
    rng = np.random.default_rng(111030)
    n, stiffness, ratio, omega = 7, 4., .2, .9
    c = cell(omega, .2, ratio)
    x = np.arange(n)+rng.uniform(-.04, .04, n)
    v, z, r, p = rng.normal(size=(4, n))
    q = np.concatenate([x, v, z, r, p, ratio*x-r, np.zeros(2*n), [0.]])
    xmin, xmax, work = 1., 1., 0.
    errors = dict(cell=0., pointer=0., work=0., energy=0.)

    def gaps(x):
        return np.roll(x, -1)-x+np.r_[np.zeros(n-1), n]

    def energy(q):
        x, v, z, r, p, u, xi, ze = q[:-1].reshape(8, n)
        d = gaps(x)-1
        assert np.all(abs(d) < 1)
        return stiffness*np.sum(d*d/(2*(1-d*d)))+.5*np.sum(v*v+z*z+r*r+p*p+xi*xi+ze*ze)

    def rhs(force, phase):
        def f(_, q):
            x, v, z, r, p, u, xi, ze = q[:-1].reshape(8, n)
            d = gaps(x)-1
            edge = stiffness*d/(1-d*d)**2
            dv = edge-np.roll(edge, 1)-ratio*r+force
            dr, dp = ratio*v-p, r.copy()
            if phase == 'transport':
                dv = dv-omega*z
                dz, dxi, dze = omega*v, np.zeros(n), np.zeros(n)
            else:
                dp = dp-ze
                dz, dxi, dze = -c['beta']*xi, c['beta']*z, p
            return np.concatenate([v, dv, dz, dr, dp, p, dxi, dze, [force*np.sum(v)]])
        return f

    for j in range(12):
        force = .05*np.sin(.7*j)-.02
        start = q.copy()
        z0 = np.sum(start[:-1].reshape(8, n)[1:5], axis=1)
        fresh = rng.normal(size=(2, n))
        q[6*n:7*n], q[7*n:8*n] = fresh[0], fresh[1]
        for phase, duration in [('transport', H), ('bath', B)]:
            e0, w0 = energy(q), q[-1]
            sol = solve_ivp(rhs(force, phase), (0., duration), q,
                            method='DOP853', rtol=2e-11, atol=2e-12)
            assert sol.success
            q = sol.y[:, -1]
            errors['energy'] = max(errors['energy'], abs(energy(q)-e0-q[-1]+w0))
            for xx in sol.y[:n].T:
                gg = gaps(xx)
                xmin, xmax = min(xmin, float(min(gg))), max(xmax, float(max(gg)))
        z1 = np.sum(q[:-1].reshape(8, n)[1:5], axis=1)
        da = np.sum(q[:n]-start[:n])
        du = np.sum(q[5*n:6*n]-start[5*n:6*n])
        dr = np.sum(q[3*n:4*n]-start[3*n:4*n])
        residual = da+c['k']@(z1-z0)-n*c['mu']*force
        residual -= c['sigma']@np.array([sum(fresh[1]), sum(fresh[0])])
        errors['cell'] = max(errors['cell'], abs(residual))
        errors['pointer'] = max(errors['pointer'], abs(da-du/ratio-dr/ratio))
        errors['work'] = max(errors['work'], abs(q[-1]-start[-1]-force*da))
        work += q[-1]-start[-1]
        q[6*n:8*n] = 0.  # retired, then replaced by fresh independent sources
    assert max(errors.values()) < 2e-7
    return dict(N=n, stiffness=stiffness, ratio=ratio, cells=12,
        minimum_gap=xmin, maximum_gap=xmax, maximum_identity_residuals=errors,
        actual_signed_work=float(work), scope='Nonlinear local link, actual continuous pointer, ideal final positional readout.')


def active_cost():
    rows = []
    for n in (16, 64, 256, 1024):
        hh, tau, gamma = np.log(n+2.), .8, 1.3
        g, lam, duration = np.sqrt(hh)/n, n*n/hh, float(n*n)
        # Use Z=c/g, lambda=M*g^2; state V,Y,Z,X.
        a = np.array([[-gamma, -g, g, 0.], [g, 0., 0., 0.],
                      [-g/lam, 1/tau, -1/tau, 0.], [1., 0., 0., 0.]])
        d = np.diag([2*gamma, 0., 2/(lam*tau), 0.])
        c0 = np.diag([1., 1., 1/lam, 0.])
        op = np.zeros((20, 20))
        op[:16, :16] = np.kron(a, np.eye(4))+np.kron(np.eye(4), a)
        op[:16, 16] = d.ravel()
        op[17, 6], op[18, 0], op[19, 10] = 1., 1., 1.
        initial = np.zeros(20)
        initial[:16], initial[16] = c0.ravel(), 1.
        result = expm(duration*op)@initial
        cov = result[:16].reshape(4, 4)
        work = lam*result[17]/tau
        ediff = .5*(cov[0, 0]+cov[1, 1]+lam*cov[2, 2])-1.5
        bath = gamma*(duration-result[18])+(duration-lam*result[19])/tau
        balance = abs(ediff-work-bath)/max(1., abs(work))
        invariant = np.array([0., 1., 0., -g])
        pointer = abs(invariant@cov@invariant-1)
        m = n**4/hh**2
        deff = (gamma+tau/m)/(gamma+tau*(g*g+1/m))**2
        assert balance < 1e-6 and pointer < 2e-6
        rows.append(dict(N=n, precision_parameter=float(hh),
            total_expected_input_work=float(n*n*work),
            input_work_divided_by_N6=float(work/n**4), predicted_limit=1/(gamma*tau),
            pointer_energy_divided_by_N2H=float(.5*cov[1, 1]/hh),
            finite_time_native_diffusion=float(cov[3, 3]/(2*duration)),
            exact_asymptotic_diffusion=float(deff),
            relative_energy_balance_residual=float(balance),
            initial_pointer_offset_variance_residual=float(pointer)))
    return rows


if __name__ == '__main__':
    result = dict(schema='astra_p1.metered_cell_and_recorder.v1',
        finite_cell_algebra=algebra(), nonlinear_actual_meter=nonlinear_meter(),
        rejected_active_recorder=active_cost(),
        scope='Population algebra, ODE and exact covariance checks; no acquired end-to-end confidence or physical deployment.')
    (ROOT/'METERED_CELL_AND_RECORDER_CHECK_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
