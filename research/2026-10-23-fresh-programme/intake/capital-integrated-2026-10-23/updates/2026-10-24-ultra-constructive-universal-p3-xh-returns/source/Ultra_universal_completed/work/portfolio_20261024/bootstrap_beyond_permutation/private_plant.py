#!/usr/bin/env python3
"""Private statistical fixture, never imported by reset_learner.py.

Designer-chosen two-state HMM. Counts, not these parameters or hidden states,
cross the acquisition interface. PRNG simulation is not a physical entropy,
constant-time controller or erasure implementation.
"""
from fractions import Fraction
from random import Random


PREPARATIONS = {"initial": (), "a": ("a",), "b": ("b",)}
MACROS = {"none": (), "a": ("a",), "b": ("b",)}
PROGRAMS = ("three_a_then_sense", "b_a_b_then_sense", "feedback")
LEGACY_CONTROL_PROGRAMS = ("sense", "two_a_then_sense", "feedback")


class Plant:
    def __init__(self, seed):
        self.rng = Random(seed)
        self.state = 1
        self.initializers = 0
        self.steps = 0
        self.produced_readouts = 0

    def initialize(self):
        self.initializers += 1
        self.state = int(self.rng.randrange(20) < 19)

    def step(self, action):
        if action == "a":
            self.state ^= int(self.rng.randrange(20) < 1)
        elif action == "b":
            self.state ^= int(self.rng.randrange(10) < 9)
        elif action != "s":
            raise ValueError(action)
        self.steps += 1
        self.produced_readouts += 1
        return int(self.rng.randrange(20) < (19 if self.state else 1))

    def run_program(self, program):
        if program == "sense":
            return self.step("s")
        if program == "two_a_then_sense":
            self.step("a")
            self.step("a")
            return self.step("s")
        if program == "three_a_then_sense":
            self.step("a")
            self.step("a")
            self.step("a")
            return self.step("s")
        if program == "b_a_b_then_sense":
            self.step("b")
            self.step("a")
            self.step("b")
            return self.step("s")
        if program == "feedback":
            first = self.step("s")
            self.step("a" if first else "b")
            return self.step("s")
        raise ValueError(program)


def calibration_counts(seed, shots=50_000):
    if shots != 50_000:
        raise ValueError("Budget was fixed before observing counts")
    plant = Plant(seed)
    cells = []
    for prep in PREPARATIONS:
        for macro in MACROS:
            word = PREPARATIONS[prep] + MACROS[macro] + ("s",)
            ones = 0
            for _ in range(shots):
                plant.initialize()
                for action in word:
                    observed = plant.step(action)
                ones += observed
            cells.append({"preparation": prep, "macro": macro,
                          "test": "sense_one", "trials": shots, "ones": ones,
                          "primitive_actions_per_trial": len(word)})
    return {"interface": {
                "full_controlled_hankel_rank_upper_bound": 2,
                "rank_bound_provenance": "supplied finite architecture promise",
                "primitive_control_names": ["s", "a", "b"],
                "preparation_library": {k: list(v) for k, v in PREPARATIONS.items()},
                "test_event": "output one from one s control",
                "reset_control_durations": {"a": 1, "b": 1}},
            "calibration": {"samples_per_setting": shots, "error_width": [1, 100],
                            "settings": cells,
                            "paid_initializers": plant.initializers,
                            "paid_primitive_actions": plant.steps,
                            "paid_produced_readouts": plant.produced_readouts},
            "statistical_fixture_only": True}


def retained_evaluation(acquisition, seed, trials=20_000, programs=PROGRAMS):
    if acquisition["status"] != "CERTIFIED":
        return {"status": "NOT_RUN", "reason": "No usable acquired preparation"}
    plant = Plant(seed+1)
    # Starting state is deliberately not externally initialized. It is a
    # private fixture condition, not information supplied to the learner.
    bits = acquisition["precision_bits_per_reset"]
    threshold = acquisition["dyadic_selection"]["a_threshold"]
    selection_rng = Random(seed)
    start_steps = plant.steps
    blocks = []
    for program in programs:
        ones = 0
        steps_before = plant.steps
        for _ in range(trials):
            # Fixed bit budget, equal-duration actual controls. Neither this
            # key nor reset outcome is retained in returned evaluation data.
            selection = selection_rng.getrandbits(bits)
            plant.step("a" if selection < threshold else "b")
            del selection
            ones += plant.run_program(program)
        blocks.append({"evaluation_program": program,
                       "trials": trials, "ones": ones,
                       "sample_mean": float(Fraction(ones, trials)),
                       "paid_primitive_actions": plant.steps-steps_before})
    return {"status": "EXECUTED", "blocks": blocks,
            "paid_initializers": plant.initializers,
            "paid_primitive_actions": plant.steps-start_steps,
            "paid_produced_readouts": plant.produced_readouts,
            "fresh_selection_bits": len(programs)*trials*bits,
            "reset_invocations": len(programs)*trials,
            "selection_words_exposed": False,
            "reset_outputs_exposed": False,
            "private_rng_state_exposed": False,
            "private_prng_state_persists_inside_simulator": True,
            "physical_fresh_entropy_or_state_erasure_proven": False,
            "public_reset_duration": 1,
            "physical_isolation_or_erasure_validated": False}


# The following truth routines are evaluation-only. They are called only
# after count-only acquisition and retained-state execution have completed.
def hidden_p_after(action, p):
    if action == "a":
        return Fraction(1, 20)+Fraction(9, 10)*p
    if action == "b":
        return Fraction(9, 10)-Fraction(4, 5)*p
    if action == "s":
        return p
    raise ValueError(action)


def sensor_probability(p):
    return Fraction(1, 20)+Fraction(9, 10)*p


def program_probability(program, p):
    if program == "sense":
        return sensor_probability(p)
    if program == "two_a_then_sense":
        return sensor_probability(hidden_p_after("a", hidden_p_after("a", p)))
    if program == "three_a_then_sense":
        return sensor_probability(hidden_p_after("a", hidden_p_after("a", hidden_p_after("a", p))))
    if program == "b_a_b_then_sense":
        return sensor_probability(hidden_p_after("b", hidden_p_after("a", hidden_p_after("b", p))))
    if program == "feedback":
        # Sum unnormalized hidden masses; no posterior division or state-ID oracle.
        answer = Fraction(0)
        for state, mass in ((0, 1-p), (1, p)):
            emit = Fraction(19 if state else 1, 20)
            for first, first_mass in ((1, emit), (0, 1-emit)):
                after = hidden_p_after("a" if first else "b", Fraction(state))
                answer += mass*first_mass*sensor_probability(after)
        return answer
    raise ValueError(program)


def post_execution_truth(acquisition, evaluation):
    weight = Fraction(acquisition["implemented_weight_a"]["numerator"],
                      acquisition["implemented_weight_a"]["denominator"])
    p0 = Fraction(19, 20)
    pstar = weight*hidden_p_after("a", p0)+(1-weight)*hidden_p_after("b", p0)
    slope = weight*Fraction(9, 10)+(1-weight)*Fraction(-4, 5)
    rows = []
    for block in evaluation["blocks"]:
        probability = program_probability(block["evaluation_program"], pstar)
        mean = Fraction(block["ones"], block["trials"])
        rows.append({"program": block["evaluation_program"],
                     "reference_event_probability": probability,
                     "absolute_error": abs(mean-probability)})
    return {"hidden_reference_probability_state_one": pstar,
            "implemented_hidden_contraction_slope": slope,
            "actual_uniform_future_tv_diameter_upper": abs(slope),
            "oracle_exact_weight_a_for_comparison_only": Fraction(8, 17),
            "original_initializer_sensor_probability": sensor_probability(p0),
            "new_reference_sensor_probability": sensor_probability(pstar),
            "evaluated_programs": rows,
            "every_fixed_nonselective_word_has_nonzero_slope": True,
            "scope": "private post-execution fixture truth, never used by learner"}
