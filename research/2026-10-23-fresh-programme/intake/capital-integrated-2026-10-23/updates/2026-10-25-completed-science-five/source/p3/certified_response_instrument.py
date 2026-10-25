"""An obtained bounded-error response interface for local balance software.

New work, 2026-10-25. The instrument checks strict row diagonal dominance of
its supplied rational balance operator A. It computes a floating Gauss-Seidel
proposal y and then the exact residual r=f-A*y. The returned enclosure
||A^{-1}f-y||_infinity <= ||r||_infinity/mu is proved from the checked margin mu.
The learner sees queries and enclosures, not A or its transpose. A source-code
incumbent may inspect A and bypass learning; no physical calibration is claimed.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import json
import random

import numpy as np

from acquired_inverse_relations import (ForwardBalanceSource, SparseElimination,
    bits, dense, dot, encode, measured, sparse_apply)


def sqrt_upper(x, bits=64):
    """Exact upward dyadic square root; retained arithmetic, copied locally.

    This is the same helper used in acquired_operation_evaluator.py, included
    here so these numerical instruments do not import unrelated prior demos.
    """
    x = F(x)
    if x < 0:
        raise ValueError('negative square')
    scale = 1 << bits
    k = isqrt(x.numerator*scale*scale//x.denominator)
    if F(k*k, scale*scale) < x:
        k += 1
    return F(k, scale)


class CertifiedBalanceInstrument:
    def __init__(self, n=32, mass=F(1), parameter=F(2, 5), max_sweeps=5000):
        self.n = n
        reference = ForwardBalanceSource(n, parameter=parameter)
        self._rows = reference.reference_rows()
        for i, row in enumerate(self._rows):
            row[i] = F(mass)+sum((abs(v) for j, v in row.items() if j != i), F(0))
        self.margin = min(row[i]-sum((abs(v) for j, v in row.items() if j != i), F(0))
                          for i, row in enumerate(self._rows))
        if self.margin <= 0:
            raise ValueError('This residual enclosure constructor needs positive row dominance.')
        self._float_rows = [{j: float(v) for j, v in row.items()} for row in self._rows]
        self.max_sweeps = max_sweeps
        self.counts = Counter()
        self.max_input_bits = self.max_output_bits = 0
        self.records = []

    def query(self, f, requested_error=F(1, 10**5)):
        f = [F(v) for v in f]
        assert len(f) == self.n and requested_error > 0
        self.counts['forward_queries'] += 1
        self.max_input_bits = max(self.max_input_bits, bits(f))
        ff = [float(v) for v in f]
        y = [0.0]*self.n
        target_residual = float(self.margin*requested_error)/2
        sweeps = 0
        for sweeps in range(1, self.max_sweeps+1):
            for i, row in enumerate(self._float_rows):
                value = ff[i]
                for j, a in row.items():
                    if j != i:
                        value -= a*y[j]
                        self.counts['float_multiply'] += 1
                        self.counts['float_add_subtract'] += 1
                y[i] = value/row[i]
                self.counts['float_divide'] += 1
            residual_max = 0.0
            for i, row in enumerate(self._float_rows):
                value = ff[i]
                for j, a in row.items():
                    value -= a*y[j]
                    self.counts['float_multiply'] += 1
                    self.counts['float_add_subtract'] += 1
                residual_max = max(residual_max, abs(value))
            if residual_max <= target_residual:
                break
        self.counts['Gauss_Seidel_sweeps'] += sweeps
        # A floating stopping test is never the certificate.
        rational_y = [F(v) for v in y]
        residual = [a-b for a, b in zip(f, sparse_apply(self._rows, rational_y))]
        enclosure = max(map(abs, residual), default=F(0))/self.margin
        self.counts['exact_residual_certificates'] += 1
        self.max_output_bits = max(self.max_output_bits, bits(rational_y))
        record = dict(input=f, response=rational_y, requested_error=requested_error,
                      coordinate_error_bound=enclosure, exact_residual=residual,
                      checked_dominance_margin=self.margin,
                      sweeps=sweeps, requested_accuracy_met=enclosure <= requested_error,
                      certificate='Every exact response coordinate lies in response +/- coordinate_error_bound.')
        self.records.append(record)
        return record

    def cost(self):
        return dict(counts=dict(self.counts), input_width=self.n, output_width=self.n,
                    returned_response_scalars=self.n*self.counts['forward_queries'],
                    maximum_input_rational_bit_length=self.max_input_bits,
                    maximum_response_rational_bit_length=self.max_output_bits,
                    native_transpose_queries=0)


def dyadic(value, precision=26):
    return F(round(float(value)*(1 << precision)), 1 << precision)


def fit_from_intervals(source, old_support_rows, training_queries=6,
                       requested_error=F(1, 10**4), seed=5101, precision=26):
    """A numerical proposal on retained supports, with no claim of exact zeros.

    Least squares uses noisy response centers. Its proposed rational matrix is
    subsequently calibrated on fresh experiments. Past support is a search
    choice, never an asserted invariant of the new source.
    """
    rng = random.Random(seed)
    records = []
    for _ in range(training_queries):
        f = [F(rng.randrange(65536)*2+1-65536, 65536) for _ in range(source.n)]
        records.append(source.query(f, requested_error))
    responses = np.array([[float(v) for v in r['response']] for r in records])
    forcings = np.array([[float(v) for v in r['input']] for r in records])
    rows, fit_controls = [], []
    for i, old in enumerate(old_support_rows):
        support = sorted(old)
        design = responses[:, support]
        coefficients, _, rank, singular = np.linalg.lstsq(design, forcings[:, i], rcond=None)
        rows.append({j: dyadic(a, precision) for j, a in zip(support, coefficients) if dyadic(a, precision)})
        fit_controls.append(dict(row=i, support=support, observed_design_rank=int(rank),
                                 observed_smallest_singular_value=float(singular[-1]),
                                 numerical_condition=float(singular[0]/singular[-1])))
    factor = SparseElimination(rows)
    return dict(rows=rows, training_records=records, fit_controls=fit_controls,
                coefficient_rounding_bits=precision,
                source_cost=source.cost(), factor=factor.artifact(),
                interpretation='Approximate operational proposal. Neither exact support nor exact coefficients are inferred from interval data.'), rows, factor


def calibrate_with_enclosures(source, rows, probes=16, alphabet=65536,
                              tau=F(1, 4), requested_error=F(1, 10**4), seed=5201):
    rng = random.Random(seed)
    maximum = F(0)
    records = []
    absolute_row_sums = [sum(map(abs, row.values()), F(0)) for row in rows]
    for _ in range(probes):
        x = [F(2*rng.randrange(alphabet)+1-alphabet, alphabet) for _ in range(source.n)]
        observation = source.query(x, requested_error)
        center = [a-b for a, b in zip(sparse_apply(rows, observation['response']), x)]
        eta = observation['coordinate_error_bound']
        propagated = [s*eta for s in absolute_row_sums]
        upper = sqrt_upper(dot(center, center))+sqrt_upper(dot(propagated, propagated))
        maximum = max(maximum, upper)
        records.append(dict(observation=observation, residual_center=center,
                            propagated_coordinate_error=propagated, probe_residual_norm_upper=upper))
    root_n = isqrt(source.n)
    root_n += root_n*root_n < source.n
    one_failure = min(F(1), F(3, 2)*(tau+F(root_n, alphabet)))
    rho = maximum/tau
    return dict(rho=rho, rho_float=float(rho), failure_probability_bound=one_failure**probes,
                probes=probes, alphabet=alphabet, tau=tau, records=records,
                source_cost=source.cost(),
                statement='With the stated probability, ||B H-I||_2 <= rho for every input. All per-query solver errors were enclosed deterministically.',
                source_contract='Fixed linear exact response beneath the tolerance-controlled numerical instrument; coefficients unavailable to the learner.')


def run():
    root = Path(__file__).resolve().parent
    old = json.loads((root/'acquired_inverse_relations_results.json').read_text())
    support_rows = [{int(j): F(v) for j, v in row.items()} for row in old['acquisition']['rows']]
    cases = []
    for mass in (F(1), F(1, 100)):
        instrument = CertifiedBalanceInstrument(mass=mass)
        (proposal, rows, factor), fit_ops = measured(lambda: fit_from_intervals(instrument, support_rows))
        certificate, calibration_ops = measured(lambda: calibrate_with_enclosures(instrument, rows))
        # Separate source-aware control of every returned enclosure.
        reference_factor = SparseElimination(instrument._rows)
        maximum_error = F(0)
        for record in instrument.records:
            truth = reference_factor.solve(record['input'])
            error = max((abs(a-b) for a, b in zip(truth, record['response'])), default=F(0))
            assert error <= record['coordinate_error_bound']
            maximum_error = max(maximum_error, error)
        all_records = proposal['training_records']+[r['observation'] for r in certificate['records']]
        assert len(all_records) == instrument.counts['forward_queries']
        cases.append(dict(mass=mass, proposed_model=proposal, calibration=certificate,
                          fit_exact_arithmetic=fit_ops, calibration_exact_arithmetic=calibration_ops,
                          all_observations=all_records, instrument_cost=instrument.cost(),
                          full_source_controls=dict(all_enclosures_hold=True,
                                                    maximum_actual_response_error=maximum_error,
                                                    actual_rows=instrument._rows),
                          source_aware_incumbent='May use the actual rows and residual enclosure directly, without model acquisition.'))
    # A strict positivity/conditioning requirement is checked, not inferred.
    rejected_nonpositive_margin = False
    try:
        CertifiedBalanceInstrument(mass=F(0))
    except ValueError:
        rejected_nonpositive_margin = True
    assert rejected_nonpositive_margin
    result = dict(construction='An auditable bounded-error instrument, approximate semantic proposal, and all-input residual calibration',
                  preselected_cases=cases, nonpositive_margin_rejected=True,
                  distinctions=['Instrument calibration follows from checked supplied software coefficients; it is not calibration of an unknown physical apparatus.',
                                'Noisy centers are used to propose approximate equations, never to certify exact absent couplings.',
                                'All acquisition and calibration responses, error bounds and failed accuracy requests are retained.'])
    (root/'certified_response_instrument_results.json').write_text(json.dumps(encode(result), indent=2))
    print(json.dumps([dict(mass=str(c['mass']), rho=c['calibration']['rho_float'],
                           calls=c['instrument_cost']['counts']['forward_queries'],
                           sweeps=c['instrument_cost']['counts']['Gauss_Seidel_sweeps'],
                           maximum_fit_condition=max(r['numerical_condition'] for r in c['proposed_model']['fit_controls']),
                           all_accuracies_met=all(r['requested_accuracy_met'] for r in c['all_observations']),
                           actual_max_error=float(c['full_source_controls']['maximum_actual_response_error'])) for c in cases], indent=2))
    return result


if __name__ == '__main__':
    run()
