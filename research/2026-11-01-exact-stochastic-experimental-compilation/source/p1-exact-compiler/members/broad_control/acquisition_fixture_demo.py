"""Synthetic experimental validation for acquisition_dictionary.py.

The fixture is the only object that knows the response tables. The learner
sees its public CountSource methods and metadata only. The separately retained
FixtureTruth is used after learning to validate scopes and executable address
semantics; it never supplies observations to the acquisition algorithm.

NumPy draws independent binomial counts with exactly representable dyadic
parameters. These are simulation batches, and every represented Bernoulli
trial is charged in both the fixture and learner ledgers. This experiment does
not execute the enormous worst-case generic factory starting level.
"""

from dataclasses import asdict, dataclass
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random

import numpy as np

from acquisition_dictionary import JuntaDictionaryLearner


@dataclass(frozen=True)
class FixtureTruth:
    scopes: tuple[tuple[int, ...], ...]
    tables: tuple[dict[tuple[int, ...], F], ...]

    def mean(self, component: int, context: tuple[int, ...]) -> F:
        key = tuple(context[i] for i in self.scopes[component])
        return self.tables[component][key]


class SyntheticControlledSource:
    def __init__(self, input_dimension, truth: FixtureTruth, seed):
        self.input_dimension = input_dimension
        self.component_count = len(truth.scopes)
        self.__truth = truth
        self.__rng = np.random.default_rng(seed)
        self.count_batches = 0
        self.represented_bit_trials = 0
        self.trials_by_component = [0] * self.component_count

    def draw_count(self, component, context, shots):
        if len(context) != self.input_dimension or shots < 0:
            raise ValueError("invalid experiment request")
        p = self.__truth.mean(component, context)
        assert p.denominator & (p.denominator - 1) == 0
        self.count_batches += 1
        self.represented_bit_trials += shots
        self.trials_by_component[component] += shots
        return int(self.__rng.binomial(shots, float(p)))


def make_fixture(seed=20261031):
    scopes = ((1, 5), (2, 8, 13), (4, 11, 20))
    tables = (
        {c: F(1, 4) + F(1, 2) * (c[0] ^ c[1])
         for c in product((0, 1), repeat=2)},
        {c: F(1, 8) + F(3, 4) * (c[0] ^ c[1] ^ c[2])
         for c in product((0, 1), repeat=3)},
        {c: F(1, 8) + F(1, 4) * c[0] + F(1, 4) * (c[1] ^ c[2])
         for c in product((0, 1), repeat=3)},
    )
    truth = FixtureTruth(scopes, tables)
    source = SyntheticControlledSource(24, truth, seed)
    return source, truth


def run_demo(output_path=None):
    source, truth = make_fixture()
    learner = JuntaDictionaryLearner(source, d=3, gamma=F(1, 4),
                                    delta=F(1, 100),
                                    completion_rng=random.Random(891723))
    dictionary = learner.acquire()
    acquisition_trials = source.represented_bit_trials
    assert acquisition_trials == learner.stats.represented_bit_trials
    assert dictionary.scopes == truth.scopes
    max_estimation_error = max(
        abs(estimate - truth.mean(component, context))
        for (component, context), estimate in learner._estimates.items()
    )
    assert max_estimation_error <= learner.limits.estimation_radius

    # Exact semantic validation occurs outside the learner. Full-context
    # invariance follows from equality of acquired and hidden scopes; these
    # direct checks also catch address-order and canonical-context bugs.
    rng = random.Random(17832)
    context_checks = 0
    validation_entries = []
    for address in dictionary.addresses():
        canonical = dictionary.canonical_context(address)
        exact_mean = truth.mean(address.component, canonical)
        for _ in range(64):
            context = [rng.randrange(2) for _ in range(source.input_dimension)]
            for variable, value in zip(dictionary.scopes[address.component],
                                       address.assignment):
                context[variable] = value
            assert truth.mean(address.component, tuple(context)) == exact_mean
            assert dictionary.address_for_context(address.component, tuple(context)) == address
            context_checks += 1
        validation_entries.append({"address": address.label(),
                                   "scope": list(dictionary.scopes[address.component]),
                                   "assignment": list(address.assignment),
                                   "exact_mean_for_validation_only": str(exact_mean)})

    # A later context-adaptive consumer chooses addresses after observing each
    # previous output. Fresh observations go through the retained dictionary.
    # This demonstrates executable semantics, not statistical proof of them.
    addresses = dictionary.addresses()
    previous = 0
    transcript = []
    for t in range(256):
        address = addresses[(7 * t + 3 * previous) % len(addresses)]
        bit = dictionary.flip(address)
        transcript.append((address.label(), bit))
        previous = bit

    result = {
        "status": "all exact scope and address checks passed",
        "N": source.input_dimension,
        "M": source.component_count,
        "max_scope": 3,
        "minimum_promised_max_influence": "1/4",
        "scope_failure_budget": "1/100",
        "learned_scopes": [list(s) for s in dictionary.scopes],
        "hidden_scopes_validation_only": [list(s) for s in truth.scopes],
        "limits": asdict(learner.limits),
        "acquisition": asdict(learner.stats),
        "maximum_observed_mean_error_validation_only": str(max_estimation_error),
        "all_realized_mean_estimates_within_radius": True,
        "charged_acquisition_physical_bit_trials": acquisition_trials,
        "all_experiment_batches": source.count_batches,
        "all_represented_physical_bit_trials": source.represented_bit_trials,
        "trials_by_component": source.trials_by_component,
        "dictionary_entries": len(addresses),
        "exact_context_semantics_checks": context_checks,
        "adaptive_fresh_dictionary_calls": len(transcript),
        "adaptive_transcript_first_16": transcript[:16],
        "numeric_truth_is_only_a_validator": validation_entries,
        "scope_of_demonstration": (
            "Actual nonmonotone discovery and fresh address execution; independent "
            "binomial simulation counts charge all represented trials. This is "
            "not an execution of the generic large-starting-level factory, nor "
            "a claim that the sufficient discovery bill is practical or minimal."
        ),
    }
    if output_path is not None:
        Path(output_path).write_text(json.dumps(result, indent=2, default=str) + "\n")
    return dictionary, truth, result


if __name__ == "__main__":
    output = Path(__file__).with_name("acquisition_fixture_results.json")
    _, _, result = run_demo(output)
    print(json.dumps({k: result[k] for k in (
        "status", "learned_scopes", "charged_acquisition_physical_bit_trials",
        "dictionary_entries", "exact_context_semantics_checks",
        "adaptive_fresh_dictionary_calls")}, indent=2))
    print(f"Results: {output}")

