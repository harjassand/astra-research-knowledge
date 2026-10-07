"""Finite diagnostics for rare-herald multiplicative stability.

No matching FPRAS is implemented here. Fock coefficients are directly enumerated
on small, low-energy three-mode inputs. The exact additive-noise counterexample
uses rational formulas; finite Fock checks do not certify the general theorem.
"""
from __future__ import annotations
import itertools
import json
import math
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
import numpy as np


def tuples_of_degree(m: int, degree: int):
    if m == 1:
        yield (degree,)
        return
    for x in range(degree + 1):
        for rest in tuples_of_degree(m - 1, degree - x):
            yield (x,) + rest


def coefficients(a, g, cutoff):
    m = len(g)
    coeff = {(0,) * m: 1.0 + 0.0j}
    for degree in range(1, cutoff + 1):
        for n in tuples_of_degree(m, degree):
            i = next(i for i, x in enumerate(n) if x)
            prev = list(n)
            prev[i] -= 1
            val = g[i] * coeff[tuple(prev)]
            for j in range(m):
                if prev[j]:
                    prev[j] -= 1
                    val += a[i, j] * coeff[tuple(prev)]
                    prev[j] += 1
            coeff[n] = val / n[i]
    return coeff


def pure_reference_energy(a, g):
    ident = np.eye(len(g))
    covariance_energy = np.trace(a @ a @ np.linalg.inv(ident - a @ a))
    alpha = np.linalg.solve(ident - a, g)
    return float(covariance_energy + alpha @ alpha)


def conditional_vector(coeff, herald):
    out = {}
    for n, value in coeff.items():
        if n[0] == herald:
            out[n[1:]] = value * math.sqrt(math.prod(math.factorial(x) for x in n))
    return out


def derivative_function(kernel, linear, zero):
    """Wick derivative, allowing either rational or complex entries."""
    @lru_cache(None)
    def value(n):
        if not any(n):
            return zero + 1
        i = next(i for i, x in enumerate(n) if x)
        prev = list(n)
        prev[i] -= 1
        out = linear[i] * value(tuple(prev))
        for j, multiplicity in enumerate(prev):
            if multiplicity:
                prev[j] -= 1
                out += multiplicity * kernel[i][j] * value(tuple(prev))
                prev[j] += 1
        return out
    return value


def run():
    rng = np.random.default_rng(2026100742)
    cases = []
    max_state_scaled = max_count_scaled = max_amplitude_ratio = 0.0
    cutoff = 28
    for fixture in range(30):
        a = rng.uniform(0.015, 0.08, (3, 3))
        a = (a + a.T) / 2
        g = rng.uniform(0.01, 0.10, 3)
        energy = pure_reference_energy(a, g)
        reference = coefficients(a, g, cutoff)
        for h in (0, 1, 2, 4):
            eta = [1e-6, 1e-4, 1e-3][fixture % 3] / ((h + 1) * (1 + energy))
            real = rng.uniform(-1.0, 1.0, (3, 3))
            imag = rng.uniform(-1.0, 1.0, (3, 3))
            perturb = real + 1j * imag
            perturb = (perturb + perturb.T) / 2
            perturb /= max(1, np.max(np.abs(perturb)))
            gp = rng.uniform(-1, 1, 3) + 1j * rng.uniform(-1, 1, 3)
            gp /= max(1, np.max(np.abs(gp)))
            b = a * (1 + eta * perturb)
            f = g * (1 + eta * gp)
            assert np.linalg.norm(b, 2) < 1
            perturbed = coefficients(b, f, cutoff)
            va = conditional_vector(reference, h)
            vb = conditional_vector(perturbed, h)
            na = sum(abs(x)**2 for x in va.values())
            nb = sum(abs(x)**2 for x in vb.values())
            overlap = sum(va[n].conjugate() * vb[n] for n in va) / math.sqrt(na * nb)
            state_distance = math.sqrt(max(0.0, 1 - abs(overlap)**2))
            count_distance = sum(abs(abs(va[n])**2 / na - abs(vb[n])**2 / nb) for n in va) / 2
            scale = eta * (h + 1) * (1 + energy)
            max_state_scaled = max(max_state_scaled, state_distance / scale)
            max_count_scaled = max(max_count_scaled, count_distance / scale)
            for n in va:
                if abs(va[n]) > 1e-200:
                    degree = h + sum(n)
                    if degree:
                        relative = abs(vb[n] / va[n] - 1)
                        ceiling = math.expm1(eta * degree)
                        max_amplitude_ratio = max(max_amplitude_ratio, relative / ceiling)
                        assert relative <= ceiling * 1.00001 + 1e-12
            pure_bound = 20 * scale
            assert state_distance <= pure_bound + 2e-8
            # The theorem uses exact infinite-state moments. Here we record the
            # finite boundary mass to make the truncation explicit.
            boundary = sum(abs(v)**2 for n, v in va.items() if sum(n) >= cutoff - h - 2) / na
            cases.append({'fixture': fixture, 'h': h, 'eta': eta, 'energy': energy,
                          'state_distance_truncated': state_distance,
                          'count_tv_truncated': count_distance,
                          'pure_bound': pure_bound,
                          'reference_boundary_mass': boundary})

    mixed_cases = []
    for fixture in range(12):
        c = np.array([[0.045 + 0.02 * rng.random(), 0.008],
                      [0.008, 0.03 + 0.02 * rng.random()]])
        g = rng.uniform(0.01, 0.09, 2)
        alpha = np.linalg.solve(np.eye(2) - c, g)
        energy = float(np.trace(c @ np.linalg.inv(np.eye(2) - c)) + alpha @ alpha)
        ka = np.block([[np.zeros((2, 2)), c], [c.T, np.zeros((2, 2))]])
        la = np.concatenate([g, g])
        da = derivative_function(ka, la, 0j)
        for h in (0, 1, 3):
            eta = 1e-3 / ((h + 1) * (1 + energy))
            q = np.array([[rng.uniform(-1, 1), 0.4 + 0.7j],
                          [0.4 - 0.7j, rng.uniform(-1, 1)]])
            cp = c * (1 + eta * q)
            gp = rng.uniform(-0.5, 0.5, 2) + 0.5j * rng.uniform(-1, 1, 2)
            f = g * (1 + eta * gp)
            eigenvalues = np.linalg.eigvalsh(cp)
            assert min(eigenvalues) > 0 and max(eigenvalues) < 1
            kb = np.block([[np.zeros((2, 2)), cp], [cp.T, np.zeros((2, 2))]])
            lb = np.concatenate([f, f.conjugate()])
            db = derivative_function(kb, lb, 0j)
            wa, wb = [], []
            for n in range(24):
                occupation = (h, n, h, n)
                va = da(occupation) / (math.factorial(h) * math.factorial(n))
                vb = db(occupation) / (math.factorial(h) * math.factorial(n))
                assert abs(va.imag) < 1e-12 and abs(vb.imag) < 1e-12
                assert va.real > 0 and vb.real > 0
                ceiling = math.expm1(2 * eta * (h + n))
                assert abs(vb.real / va.real - 1) <= ceiling * 1.00001 + 1e-12
                wa.append(va.real)
                wb.append(vb.real)
            pa, pb = np.array(wa) / sum(wa), np.array(wb) / sum(wb)
            tv = float(sum(abs(pa - pb)) / 2)
            x = 24 * eta * (1 + 2 * energy)
            d_bound = math.expm1(2 * eta * h - ((h + 1) / 2) * math.log1p(-x))
            tv_bound = d_bound / (1 - d_bound)
            assert tv <= tv_bound + 1e-10
            mixed_cases.append({'fixture': fixture, 'h': h, 'eta': eta,
                                'energy': energy, 'count_tv_truncated': tv,
                                'count_tv_bound': tv_bound,
                                'reference_boundary_mass': float(sum(pa[-3:]))})

    exact = []
    for denominator in (4, 10, 100, 1000, 10000):
        delta = Fraction(1, denominator)
        r2 = delta**2 + delta**4
        energy = 2 * r2 / (1 - r2)
        herald_probability = (1 - r2) * r2
        conditional_tv = (1 - delta**2) / (1 + delta**2)
        input_fidelity = ((1 - r2) / (1 - 2 * delta**3))**2
        # In the two conditional pure states all h=1 photons occupy retained
        # supermodes (delta,delta^2) and (delta^2,delta), respectively.
        overlap = 2 * delta / (1 + delta**2)
        assert 1 - overlap**2 == conditional_tv**2
        assert 0 < r2 < 1 and 0 < herald_probability < 1
        assert 0 < input_fidelity < 1
        exact.append({'delta': str(delta), 'energy': str(energy),
                      'herald_probability': str(herald_probability),
                      'conditional_tv': str(conditional_tv),
                      'conditional_trace_distance': str(conditional_tv),
                      'input_fidelity': str(input_fidelity),
                      'matrix_difference_squared_op_norm': str(2 * (delta - delta**2)**2)})

    phase_exact = []
    for denominator in (4, 10, 100, 1000):
        r = Fraction(1, denominator)
        zero = Fraction(0)
        a = [[zero, r, r, zero], [r, zero, zero, r],
             [r, zero, zero, r], [zero, r, r, zero]]
        b = [row[:] for row in a]
        b[1][3] = b[3][1] = -r
        g = [r, zero, zero, zero]
        da = derivative_function(a, g, zero)
        db = derivative_function(b, g, zero)
        for remaining in range(8):
            coefficient_a = da((1, 1, 1, remaining)) / math.factorial(remaining)
            coefficient_b = db((1, 1, 1, remaining)) / math.factorial(remaining)
            target_a = 2 * r**2 if remaining == 1 else r**3 if remaining == 2 else zero
            target_b = -r**3 if remaining == 2 else zero
            assert coefficient_a == target_a and coefficient_b == target_b
        energy_a = (9 * r**2 - 34 * r**4 + 8 * r**6) / (1 - 4 * r**2)**2
        energy_b = (9 * r**2 - 14 * r**4) / (1 - 2 * r**2)**2
        prefactor = (1 - 4 * r**2) / (1 - 2 * r**2)**2
        exponent = -4 * r**6 / ((1 - 2 * r**2) * (1 - 4 * r**2))
        unconditional_acceptance = float(prefactor) * math.exp(float(exponent))
        tv = 2 / (2 + r**2)
        herald_acceptance = r**2 / (2 + r**2)
        assert tv + herald_acceptance == 1
        phase_exact.append({'r': str(r), 'reference_energy': str(energy_a),
                            'phased_energy': str(energy_b),
                            'conditional_count_tv': str(tv),
                            'conditional_phase_acceptance': str(herald_acceptance),
                            'unconditional_phase_acceptance_prefactor': str(prefactor),
                            'unconditional_phase_acceptance_exponent': str(exponent),
                            'unconditional_phase_acceptance_float': unconditional_acceptance,
                            'global_phase_cost_nu_float': -math.log(unconditional_acceptance)})

    result = {'status': 'finite diagnostics only, no FPRAS and no general proof certificate',
              'pure_fock_cases': len(cases), 'total_fock_cutoff': cutoff,
              'max_state_distance_divided_by_eta_scale': max_state_scaled,
              'max_count_tv_divided_by_eta_scale': max_count_scaled,
              'max_per_coefficient_ratio_to_product_ceiling': max_amplitude_ratio,
              'max_reference_boundary_mass': max(x['reference_boundary_mass'] for x in cases),
              'exact_additive_noise_counterexamples': exact,
              'mixed_fock_cases': len(mixed_cases),
              'max_mixed_reference_boundary_mass': max(x['reference_boundary_mass'] for x in mixed_cases),
              'exact_low_negativity_phase_counterexamples': phase_exact,
              'cases': cases, 'mixed_cases': mixed_cases}
    destination = Path(__file__).with_name('gaussian_photonic_checks.json')
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key not in ('cases', 'mixed_cases')}, indent=2))


if __name__ == '__main__':
    run()
