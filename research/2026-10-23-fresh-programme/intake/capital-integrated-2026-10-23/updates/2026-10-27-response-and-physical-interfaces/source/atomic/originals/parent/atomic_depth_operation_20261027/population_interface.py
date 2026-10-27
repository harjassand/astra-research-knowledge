"""Exact mean-law ambiguity and conditional Gaussian-dose replay, not new physics."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import time

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parents[1] / 'empirical_operation_invention' / 'sources'


def value(x):
    return {'exact': str(x), 'float': float(x)}


def generator_check(n, block, a, b):
    """Unlabelled counts of independent, internally synchronized 3-state blocks."""
    m = n // block
    checked = 0
    for k0 in range(m + 1):
        for kp in range(m - k0 + 1):
            km = m - k0 - kp
            k = (k0, kp, km)
            transitions = []
            for end in (1, 2):
                if k0:
                    z = list(k); z[0] -= 1; z[end] += 1
                    transitions.append((k0 * a, z))
                if k[end]:
                    z = list(k); z[end] -= 1; z[0] += 1
                    transitions.append((k[end] * b, z))
            got = [sum((q * F(z[i] - k[i], m) for q, z in transitions), F(0))
                   for i in range(3)]
            target = [b * F(kp + km, m) - 2*a * F(k0, m),
                      a * F(k0, m) - b * F(kp, m),
                      a * F(k0, m) - b * F(km, m)]
            assert got == target
            checked += 1
    # Even blocks can instead move in balanced +/- halves and return whole.
    # This also respects delta_plus,delta_minus <= 1/2 on every trajectory.
    balanced_checked = 0
    if block % 2 == 0:
        for j in range(m + 1):
            drift = 2*a*(m-j)*F(-1, m) + b*j*F(1, m)
            assert drift == b*F(j, m) - 2*a*F(m-j, m)
            balanced_checked += 1
    return checked, balanced_checked


def main():
    started = time.monotonic()
    n = 16
    a, b = F(124, 125), F(89, 1000)
    p_eq = b / (2*a + b)
    t = 2.0
    p0 = float(p_eq) + (1-float(p_eq))*math.exp(-float(2*a+b)*t)
    models = []
    for block in (1, 2, 4, 8, 16):
        count, balanced = generator_check(n, block, a, b)
        hazard = 2*a*(n//block)
        models.append({'atoms_per_synchronized_block': block,
                       'exact_generator_states_checked': count,
                       'balanced_binary_states_checked': balanced,
                       'all_native_first_change_rate_per_second': value(hazard),
                       'no_first_change_by_2s': math.exp(-float(hazard)*t),
                       'mean_native_fraction_at_2s': p0,
                       'native_fraction_variance_at_2s': block/n*p0*(1-p0)})
    rates = {'SI': (a, b), 'pinned_repository': (F(779,1000), F(141,1250))}
    cross_sections = {label: {'forward_barn_if_flux_as_stated': value(aa/F(19,10)),
                              'return_barn_if_flux_as_stated': value(bb/F(12,5))}
                      for label, (aa, bb) in rates.items()}
    # Angstrom units, normalized Gaussian is conditional, not a measured probe.
    electrons_per_second = 20e-12/1.602176634e-19
    sigma = 0.8/(2*math.sqrt(2*math.log(2)))
    area = 2*math.pi*sigma*sigma
    phase_n = 131072
    centers = [2.385*math.cos(2*math.pi*(i+0.5)/phase_n) for i in range(phase_n)]
    time_source_centers = [2.385*math.cos(2*math.pi*500*i/999) for i in range(1000)]

    def shape(x, positions):
        return math.fsum(math.exp(-(x-z)**2/(2*sigma*sigma)) for z in positions)/len(positions)

    dose = []
    for x in (0.0, 2.385, 2.4):
        uniform = shape(x, centers)
        sampled = shape(x, time_source_centers)
        for dy in (0.1, 0.05, 0.025):
            ys = [-2+i*dy for i in range(round(4/dy))]
            unweighted_y = math.fsum(math.exp(-y*y/(2*sigma*sigma)) for y in ys)
            dose.append({'x_angstrom': x, 'y_grid_angstrom': dy,
                         'source_unweighted_y_sum_numeric': electrons_per_second*sampled*unweighted_y,
                         'source_y_sum_times_dy_numeric': electrons_per_second*sampled*unweighted_y*dy,
                         'conditional_normalized_areal_flux_e_per_A2_s': electrons_per_second*uniform/area,
                         'source_time_sampled_shape_mean': sampled,
                         'uniform_phase_shape_mean': uniform})
    hashes = {name: hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()
              for name in ('Cross_sections.ipynb', 'Dose_rate_profile.ipynb', 'supplement.pdf')}
    out = {'scope': __doc__, 'source_sha256': hashes,
           'population_scope': 'Exact alternative generators with identical mean law; none fitted as physical layer dynamics.',
           'SI_a': value(a), 'SI_b': value(b), 'native_equilibrium': value(p_eq),
           'models': models, 'cross_sections': cross_sections,
           'dose_scope': 'Conditional Gaussian and source-grid dimensional replay. No calibrated physical cross section inferred.',
           'sigma_angstrom': sigma, 'gaussian_integral_A2': area,
           'electrons_per_second_at_20pA': electrons_per_second,
           'conditional_parked_peak_flux_e_per_A2_s': electrons_per_second/area,
           'dose_replay': dose, 'elapsed_seconds': time.monotonic()-started}
    (ROOT/'POPULATION_RESULTS.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'models': models, 'cross_sections': cross_sections,
                      'dose_replay': dose[:3], 'elapsed_seconds': out['elapsed_seconds']}, indent=2))


if __name__ == '__main__':
    main()
