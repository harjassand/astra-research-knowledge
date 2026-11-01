"""Finite-temperature Ising modules and exact boundary-interaction tests.

Conventional background: Fisher (1959), decoration/star transformations;
Yoshioka--Akagi--Katsura PRE 99, 032113 (2019), exact many-spin-to-pairwise
compilation. The explicit Hadamard gadget is independently constructed here.
Its mathematical validity is verified; priority/novelty is NOT asserted.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.special import logsumexp


def configurations(n):
    return np.array(list(itertools.product([-1, 1], repeat=n)), dtype=float)


def log_cosh(x):
    return np.logaddexp(x, -x)-np.log(2)


H4 = np.array([[1, 1, 1, 1], [1, 1, -1, -1],
               [1, -1, 1, -1], [1, -1, -1, 1]], dtype=float)


def quartic_strength(lam):
    """The negative dimensionless quartic coupling after tracing auxiliaries."""
    return 0.5*(log_cosh(4*lam)-4*log_cosh(2*lam))


def lambda_for_quartic(magnitude):
    if magnitude <= 0:
        return 0.0
    return float(brentq(lambda x: -quartic_strength(x)-magnitude, 0, magnitude+2))


def hadamard_boundary_logweights(lam):
    visible = configurations(4)
    hidden = configurations(4)
    # H_{a i}: hidden a to visible i. Explicit sum of all 16 hidden states.
    energy_exponent = lam * visible @ H4.T @ hidden.T
    return visible, logsumexp(energy_exponent, axis=1)


def walsh_coefficients(spins, function):
    out = {}
    for mask in range(1 << spins.shape[1]):
        sites = [i for i in range(spins.shape[1]) if mask & (1 << i)]
        product = np.prod(spins[:, sites], axis=1) if sites else np.ones(len(spins))
        out[mask] = float(np.mean(function*product))
    return out


def diamond_logweights(beta):
    st = configurations(2)
    uv = configurations(2)
    output = []
    for s, t in st:
        u, v = uv[:, 0], uv[:, 1]
        exponent = beta*(s*u+u*t+s*v-0.7*v*t+0.3*u*v)
        output.append(logsumexp(exponent))
    return st, np.array(output)


def exact_quartic_tree(n_visible, target):
    """Resource construction for even n>=4, using a tree of quartic factors.

    G=(n-2)/2 quartic factors, joined by G-1 separator spins. Each factor
    is independently compiled with the four-hidden-spin Hadamard module.
    Product identity gives tanh(K_target)=product_j tanh(K_j). This routine
    reports resources and verifies the effective strength analytically.
    It does NOT establish fast physical equilibration or all-temperature
    Hamiltonian equivalence.
    """
    if n_visible < 4 or n_visible % 2:
        raise ValueError("n_visible must be even and at least four")
    g = (n_visible-2)//2
    k_local = np.arctanh(np.tanh(abs(target))**(1/g))
    lam = lambda_for_quartic(k_local)
    effective = np.arctanh(np.tanh(k_local)**g)
    return dict(visible=n_visible, target_abs_K=target, quartic_modules=g,
                separator_spins=g-1, hidden_spins=4*g, total_auxiliaries=5*g-1,
                microscopic_pair_edges=16*g, local_quartic_abs_K=float(k_local),
                microscopic_abs_dimensionless_coupling=lam,
                recovered_abs_K=float(effective))


def run():
    results = {"hadamard_gadget": [], "diamond": [], "quartic_tree": [],
               "single_star_competitor": [], "fixed_hardware_temperature_sweep": []}
    for lam in [0.01, 0.05, 0.1, 0.3, 0.7, 1.2, 2.0]:
        visible, logW = hadamard_boundary_logweights(lam)
        parity = np.prod(visible, axis=1)
        formula = np.where(parity > 0, np.log(16)+log_cosh(4*lam),
                           np.log(16)+4*log_cosh(2*lam))
        coefficients = walsh_coefficients(visible, logW)
        probabilities = np.exp(logW-logsumexp(logW))
        moments = {mask: float(np.sum(probabilities*np.prod(
            visible[:, [i for i in range(4) if mask & (1 << i)]], axis=1)))
            for mask in range(1, 16)}
        results["hadamard_gadget"].append(dict(lam=lam,
            max_logweight_formula_error=float(np.max(abs(logW-formula))),
            quartic_from_walsh=coefficients[15], quartic_formula=float(quartic_strength(lam)),
            max_forbidden_log_coupling=max(abs(coefficients[k]) for k in range(1, 15)),
            max_one_two_three_spin_moment=max(abs(moments[k]) for k in range(1, 15)),
            four_spin_moment=moments[15], four_spin_moment_formula=float(np.tanh(quartic_strength(lam))),
            quartic_over_lam=float(quartic_strength(lam)/lam)))

    # Stronger conventional quartic compiler at one chosen temperature:
    # one hidden star plus six direct terminal pair counterterms.
    visible = configurations(4)
    pair_sum = np.column_stack([visible[:, i]*visible[:, j]
        for i in range(4) for j in range(i+1, 4)]).sum(axis=1)
    for lam in [0.1, 0.3, 0.7, 1.2, 2.0]:
        jpair = -0.125*log_cosh(4*lam)
        logW = np.log(2)+log_cosh(lam*visible.sum(axis=1))+jpair*pair_sum
        coeff = walsh_coefficients(visible, logW)
        results["single_star_competitor"].append(dict(lam=lam,
            direct_pair_counterterm=float(jpair), auxiliaries=1, microscopic_bonds=10,
            quartic_from_walsh=coeff[15], expected_quartic=float(quartic_strength(lam)/4),
            largest_lower_order_coupling=max(abs(coeff[k]) for k in range(1, 15))))

    # Both physical networks calibrated to K4=-1 at beta=1. Then hold each
    # microscopic physical bond fixed and change temperature through beta.
    lambda_hadamard = lambda_for_quartic(1)
    lambda_star = lambda_for_quartic(4)
    star_pair_energy = -0.125*log_cosh(4*lambda_star)
    for beta in [0.1, 0.25, 0.5, 1, 2, 4]:
        _, logW_h = hadamard_boundary_logweights(beta*lambda_hadamard)
        logW_s = np.log(2)+log_cosh(beta*lambda_star*visible.sum(axis=1)) \
            + beta*star_pair_energy*pair_sum
        ch = walsh_coefficients(visible, logW_h)
        cs = walsh_coefficients(visible, logW_s)
        results["fixed_hardware_temperature_sweep"].append(dict(beta=beta,
            hadamard_K4=ch[15], hadamard_largest_lower_order=max(abs(ch[k]) for k in range(1,15)),
            one_star_K4=cs[15], one_star_pair_leakage=cs[3],
            one_star_higher_odd_leakage=max(abs(cs[k]) for k in [1,2,4,8,7,11,13,14])))

    for beta in [0.01, 0.1, 0.3, 1, 3, 10]:
        st, logW = diamond_logweights(beta)
        aligned = logW[0]
        opposite = logW[1]
        logC = 0.5*(aligned+opposite)
        keff = 0.5*(aligned-opposite)
        err = float(np.max(abs(logW-(logC+keff*st[:, 0]*st[:, 1]))))
        A = np.exp(aligned)
        B = np.exp(opposite)
        difference_formula = np.expm1(0.6*beta)*(np.exp(2*beta)-np.exp(-2*beta))
        results["diamond"].append(dict(beta=beta, logC=float(logC), K_eff=float(keff),
            max_logweight_error=err,
            difference_identity_relative_error=float(abs((A-B)-difference_formula)/max(1, abs(A-B)))))

    # Validate exact composition on the nonplanar K3,3 base graph.
    base = configurations(6)
    base_edges = [(i, j) for i in range(3) for j in range(3, 6)]
    beta = 1.0
    _, logW = diamond_logweights(beta)
    logC = 0.5*(logW[0]+logW[1]); keff = 0.5*(logW[0]-logW[1])
    bond_products = np.column_stack([base[:, i]*base[:, j] for i, j in base_edges])
    logZ_explicit_contracted = logsumexp(np.where(bond_products > 0, logW[0], logW[1]).sum(axis=1))
    logZ_effective = len(base_edges)*logC+logsumexp(keff*bond_products.sum(axis=1))
    results["nonplanar_decorated_graph"] = dict(base_graph="K3,3", base_sites=6,
        modules=9, physical_sites=24, physical_bonds=45, frustrated_modules=9,
        logZ_contracted=float(logZ_explicit_contracted), logZ_effective=float(logZ_effective),
        error=float(abs(logZ_effective-logZ_explicit_contracted)),
        validation="independent module contraction and effective-network evaluation; not 2^24 full enumeration")

    for n in [4, 8, 16, 64, 256, 1024]:
        results["quartic_tree"].append(exact_quartic_tree(n, 1.0))

    # Explicit 6-terminal composition: two pure quartic factors sharing z.
    v = configurations(6)
    k_local = np.arctanh(np.sqrt(np.tanh(1.0)))
    A = np.prod(v[:, :3], axis=1); B = np.prod(v[:, 3:], axis=1)
    logW6 = np.logaddexp(k_local*(A+B), -k_local*(A+B))
    coeffs = walsh_coefficients(v, logW6)
    results["six_terminal_tree_check"] = dict(extracted_six_body=coeffs[63],
        largest_other_nonconstant_coefficient=max(abs(coeffs[k]) for k in range(1, 63)))

    Path(__file__).with_name("boundary_results.json").write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    run()
