#!/usr/bin/env python3
"""Finite diagnostics for R2; the asymptotic proof is in R2.txt."""

import json
import math

A = 1e-3
BETA0 = 0.1
SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
NORM = math.sqrt(2.0 * math.pi)


def phi(x):
    return math.exp(-0.5*x*x) / NORM


def Phi(x):
    return 0.5 * (1.0 + math.erf(x/math.sqrt(2.0)))


def g(x):
    return 2.0*Phi(x)-1.0


def gpp(x):
    return -2.0*x*phi(x)


def psi2(i, x):
    k = 2.0*math.pi*i
    phase = k*Phi(x)
    return SQRT2*(-k*k*math.cos(phase)*phi(x)**2
                  + k*x*math.sin(phase)*phi(x))


def parameters(i):
    s = A*math.exp(-i)
    beta = BETA0*math.exp(-i*i)
    alpha = math.sqrt(1.0-beta*beta/3.0)
    return s, beta, alpha


def p_log_hessian_upper(x, v):
    entries = []
    for i, vi in enumerate(v, start=1):
        s, _, _ = parameters(i)
        z = s*vi
        den = 1.0+z*g(x[i-1])
        gp = 2.0*phi(x[i-1])
        entries.append(-1.0+z*gpp(x[i-1])/den-(z*gp/den)**2)
    return max(entries)


def c_log_hessian_upper(x0, xs, v):
    h = 0.0
    h00 = 0.0
    other = []
    for i, vi in enumerate(v, start=1):
        s, beta, alpha = parameters(i)
        phase = 2.0*math.pi*i*Phi(x0)
        psi = SQRT2*math.cos(phase)
        h += s*vi*(alpha*psi+beta*g(xs[i-1]))/SQRT3
        h00 += s*vi*alpha*psi2(i,x0)/SQRT3
        other.append(s*vi*beta*gpp(xs[i-1])/SQRT3)
    return -1.0 + max([h00]+other)/(1.0+h)


def hat_periodic_value(coeffs, j_count, u):
    z = j_count*u
    left = int(z) % j_count
    alpha = z-math.floor(z)
    right = (left+1) % j_count
    return (1.0-alpha)*coeffs[left]+alpha*coeffs[right]


def periodic_kernel_error(j_count, mode, grid_n=32768):
    masses = [0.0]*j_count
    vals, labels = [], []
    for k in range(grid_n):
        t = (k+0.5)/grid_n
        z = j_count*t
        left = int(z) % j_count
        alpha = z-math.floor(z)
        right = (left+1) % j_count
        val = SQRT2*math.cos(2.0*math.pi*mode*t)
        vals.append(val)
        labels.append((left,right,alpha))
        masses[left] += (1-alpha)*val/grid_n
        masses[right] += alpha*val/grid_n
    return max(abs(j_count*((1-a)*masses[l]+a*masses[r])-v)
               for v,(l,r,a) in zip(vals,labels))


def graded_mesh_bias(j_count, grid_n=20001):
    nodes = [-1.0 + 6.0*(j/j_count)**2 - 4.0*(j/j_count)**3
             for j in range(j_count+1)]
    masses = []
    means = []
    for j in range(j_count+1):
        left = nodes[j]-nodes[j-1] if j>0 else 0.0
        right = nodes[j+1]-nodes[j] if j<j_count else 0.0
        mass = (left+right)/4.0  # uniform[-1,1] base measure
        if j == 0:
            mean = nodes[0]+right/3.0
        elif j == j_count:
            mean = nodes[j]-left/3.0
        else:
            mean = nodes[j]+(right-left)/3.0
        masses.append(mass)
        means.append(mean)
    max_bias = 0.0
    for k in range(grid_n):
        u = -1.0+2.0*k/(grid_n-1)
        j = next((z for z in range(j_count)
                  if nodes[z] <= u <= nodes[z+1]), j_count-1)
        alpha = (u-nodes[j])/(nodes[j+1]-nodes[j])
        decoded_mean = (1-alpha)*means[j]+alpha*means[j+1]
        max_bias = max(max_bias, abs(decoded_mean-u))
    return max_bias


def main():
    q = math.exp(-2.0)
    s4 = q*(1+11*q+11*q*q+q**3)/(1-q)**5
    s2 = q/(1-q)
    assert s2 < 1.0/6.0 and s4 < 1.0
    delta = A/math.sqrt(6.0)
    g2 = 2.0/math.sqrt(2.0*math.pi*math.e)
    p_h2 = A*g2
    c_h2 = max(9.0*math.sqrt(2.0/3.0)*A,
               A*BETA0*g2/math.sqrt(3.0))
    p_curv = -1.0+p_h2/(1.0-delta)
    c_curv = -1.0+c_h2/(1.0-delta)
    assert p_curv < -0.999 and c_curv < -0.99

    d=12
    v=[(-1.0)**i/math.sqrt(d) for i in range(1,d+1)]
    xs=[-3.0+6.0*k/600.0 for k in range(601)]
    p_grid=max(p_log_hessian_upper(xs, v) for _ in [0])
    c_grid=max(c_log_hessian_upper(x0, [0.25]*d, v) for x0 in xs)

    periodic=[]
    for j_count in (8,16,32):
        err=periodic_kernel_error(j_count, mode=3)
        bound=8.0*SQRT2*math.pi**2*3**2/(j_count*j_count)
        assert err <= bound + 2e-4
        periodic.append({"J":j_count,"mode":3,"grid_sup_bias":err,
                         "analytic_bound":bound})

    graded=[]
    for j_count in (2,4,8,16,32):
        err=graded_mesh_bias(j_count)
        bound=4.0/(j_count*j_count)
        assert err <= bound + 1e-8
        graded.append({"J":j_count,"grid_sup_bias":err,
                       "analytic_bound":bound})

    schedules=[]
    for L in (25.0,100.0,400.0):
        eps=math.exp(-L)
        d_chosen=math.ceil(L)
        tail_cut=SQRT3*eps/16.0
        active=[i for i in range(1,d_chosen+1)
                if parameters(i)[0]*parameters(i)[1] > tail_cut]
        k=len(active)
        c_shared=8.0*SQRT2*math.pi**2*A/SQRT3
        d0=max(5,math.ceil(math.sqrt(2.0*c_shared/eps)))
        bits=math.log2(d0)
        for i in active:
            s,beta,_=parameters(i)
            ji=max(2,math.ceil(math.sqrt(16.0*s*beta/(SQRT3*eps))) )
            bits += math.log2(ji+1)
        active_l2=eps/4.0
        q_tail=(parameters(k+1)[0]*parameters(k+1)[1]
                if k+1 <= d_chosen else 0.0)
        omitted_l2=q_tail/3.0
        schedules.append({"ln1_over_eps":L,"d_chosen":d_chosen,
                          "active_noise_coordinates":k,
                          "archive_bits_upper_from_schedule":bits,
                          "shared_density_sup_bound":eps/2.0,
                          "active_noise_density_l2_bound":active_l2,
                          "omitted_noise_density_l2_bound":omitted_l2,
                          "spectral_sum_order_scale":L*L})

    print(json.dumps({
        "scope":"finite diagnostics only; proof and asymptotic cost are in R2.txt",
        "a":A,"beta0":BETA0,"d_grid":d,
        "sum_exp_minus_2i":s2,"sum_i4_exp_minus_2i":s4,
        "uniform_abs_h_bound":delta,
        "P_log_hessian_upper_bound":p_curv,
        "C_log_hessian_upper_bound":c_curv,
        "P_grid_log_hessian_upper":p_grid,
        "C_grid_log_hessian_upper":c_grid,
        "periodic_codec":periodic,
        "graded_uniform_codec":graded,
        "memory_schedules":schedules,
        "score_covariance":"both exactly diag(s_i^2/3)",
    },indent=2))


if __name__=="__main__":
    main()
