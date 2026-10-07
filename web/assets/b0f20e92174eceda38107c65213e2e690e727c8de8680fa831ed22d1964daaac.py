"""Actual capped hard trace sampler; no counting or field-descent call.

Conditional on Chen--Liu Lemma5.5, positive LC local gates, and independent
fair coin input. Pseudorandom seed is recorded for reproducible local execution.
"""
from fractions import Fraction as F
from xxz_quadratic_gates import compile_quadratic_trace
from xxz_local_chain import CoinTape, LocalExchange, TapeAbort, ceil_log2_fraction, mixing_steps
from nofield_counter import acquired_complement_ratio, ResourceRefusal


def trace_sample_plan(instance, tv=F(1, 4), *, allow_bounded_bias=False):
    tv = F(tv)
    if not 0 < tv <= F(1, 4):
        raise ValueError("TV target in (0,1/4] required")
    if not allow_bounded_bias and not instance.complement_symmetric():
        raise ValueError("complement symmetry required unless numeric bias is admitted")
    ratio = acquired_complement_ratio(instance)
    n = instance.n
    if n < 1:
        return {"n":0,"total_steps":0,"tv":tv,"trivial":True}
    t = F(1, 256 * n * n) / ratio
    repetitions = max(1, ceil_log2_fraction(4 / tv))
    sample_tv = tv / (4 * repetitions)
    steps = mixing_steps(instance, t, [F(1)] * n, sample_tv)
    height = max(1, (n - 1).bit_length())
    choices = repetitions * steps * (2 * height + 2) + instance.inactive_qubits
    coin_bits = max(1, ceil_log2_fraction(4 * choices / tv))
    return {"n":n,"tv":tv,"t":t,"complement_ratio":ratio,"trivial":False,
            "repetitions":repetitions,"soft_tv":sample_tv,"steps_per_sample":steps,
            "total_steps":repetitions * steps,"choice_cap":choices,
            "bits_per_choice":coin_bits,"random_bits_cap":choices * coin_bits,
            "hard_rejection_failure_bound":F(1, 4 ** repetitions)}


def sample_trace(qubits, gates, tv=F(1,4), *, max_steps=10000000, seed=20261007,
                 allow_bounded_bias=False):
    instance = compile_quadratic_trace(qubits, gates)
    plan = trace_sample_plan(instance, tv, allow_bounded_bias=allow_bounded_bias)
    if plan["total_steps"] > max_steps:
        raise ResourceRefusal(plan)
    first_rows = {}
    for j, (kind, vertices, _, _, _) in enumerate(gates):
        for local, vertex in enumerate(vertices):
            first_rows.setdefault(vertex, 4 * j + local if kind == "edge" else 4 * j)
    if plan["trivial"]:
        tape = CoinTape(seed, 1, max(1, qubits))
        return {"bits":[int(tape.bernoulli(F(1,2))) for _ in range(qubits)],
                "accepted":True,"aborted":False,"plan":plan,
                "steps":0,"attempts":0,"coin_bits":tape.bits,"coin_choices":tape.choices}
    tape = CoinTape(seed, plan["bits_per_choice"], plan["choice_cap"])
    attempts = steps = 0
    try:
        for _ in range(plan["repetitions"]):
            attempts += 1
            chain = LocalExchange(instance, t=plan["t"])
            for _ in range(plan["steps_per_sample"]):
                chain.step(tape)
                steps += 1
            if not chain.S.isdisjoint(chain.T):
                continue
            bits = [int(first_rows[v] in chain.S) if v in first_rows else int(tape.bernoulli(F(1,2)))
                    for v in range(qubits)]
            return {"bits":bits,"accepted":True,"aborted":False,"plan":plan,
                    "steps":steps,"attempts":attempts,"coin_bits":tape.bits,
                    "coin_choices":tape.choices,"S":sorted(chain.S),"T":sorted(chain.T)}
        return {"bits":[0]*qubits,"accepted":False,"aborted":False,
                "plan":plan,"steps":steps,"attempts":attempts,"coin_bits":tape.bits,
                "coin_choices":tape.choices,"fallback_reason":"rejection cap"}
    except TapeAbort as error:
        return {"bits":[0]*qubits,"accepted":False,"aborted":True,
                "plan":plan,"steps":steps,"attempts":attempts,"coin_bits":tape.bits,
                "coin_choices":tape.choices,"fallback_reason":str(error)}
