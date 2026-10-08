#!/usr/bin/env python3
"""Exact finite-binned decoder evidence for the N66 regular-sensor codec.

This is a finite interface: an eight-bit input bin per coordinate is mapped
to a short archive label and then to an eight-bit output bin. All transition
probabilities and reported TV certificates are exact Fractions. The example
does not claim TV closeness to an unbinned continuous law.
"""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import math
import random
import struct
from fractions import Fraction as Q
from math import ceil, isqrt, log2
from typing import Callable, Iterable, Sequence


def ceil_sqrt_fraction(x: Q) -> int:
    if x <= 0:
        return 0
    q = isqrt(x.numerator // x.denominator)
    return q if q * q * x.denominator == x.numerator else q + 1


def make_nodes(j_count: int, family: str) -> list[Q]:
    if family == "graded":
        # x_j = -1 + 6(j/J)^2 - 4(j/J)^3, all nodes rational.
        return [
            Q(-1) + Q(6 * j * j, j_count * j_count)
            - Q(4 * j**3, j_count**3)
            for j in range(j_count + 1)
        ]
    if family == "uniform":
        return [Q(-1) + Q(2 * j, j_count) for j in range(j_count + 1)]
    raise ValueError(f"unknown node family: {family}")


def integrate_hat(a: Q, b: Q, nodes: Sequence[Q], label: int) -> Q:
    """Exact integral of a nodal linear hat over [a,b]."""
    total = Q(0)
    for i, (left, right) in enumerate(zip(nodes, nodes[1:])):
        lo = max(a, left)
        hi = min(b, right)
        if lo >= hi:
            continue
        gap = right - left
        if label == i:
            value_lo = (right - lo) / gap
            value_hi = (right - hi) / gap
        elif label == i + 1:
            value_lo = (lo - left) / gap
            value_hi = (hi - left) / gap
        else:
            continue
        # The hat is linear on this segment, so the trapezoid rule is exact.
        total += (value_lo + value_hi) * (hi - lo) / 2
    return total


def make_bins(k_count: int) -> list[tuple[Q, Q]]:
    return [
        (Q(-1) + Q(2 * k, k_count), Q(-1) + Q(2 * (k + 1), k_count))
        for k in range(k_count)
    ]


def make_transitions(
    k_count: int, j_count: int, family: str
) -> tuple[list[list[Q]], list[list[Q]], list[Q]]:
    """Return encoder A[input_bin,label], decoder B[label,output_bin]."""
    nodes = make_nodes(j_count, family)
    bins = make_bins(k_count)
    labels = j_count + 1

    # Uniform-reference probability of each hat within the given input bin.
    # Since every input bin has reference mass 1/K, A[k,j] = K int phi_j dmu.
    encoder = [
        [Q(k_count, 2) * integrate_hat(a, b, nodes, j) for j in range(labels)]
        for a, b in bins
    ]
    hat_masses = [Q(1, 2) * integrate_hat(Q(-1), Q(1), nodes, j) for j in range(labels)]
    decoder = [
        [Q(1, 2) * integrate_hat(a, b, nodes, j) / hat_masses[j] for a, b in bins]
        for j in range(labels)
    ]
    assert all(sum(row, Q(0)) == 1 for row in encoder)
    assert all(sum(row, Q(0)) == 1 for row in decoder)
    assert sum(hat_masses, Q(0)) == 1
    return encoder, decoder, nodes


def h_antiderivative(x: Q) -> Q:
    # h(x)=x/3+x^3/6, so H(x)=x^2/6+x^4/24.
    return x * x / 6 + x**4 / 24


def signal_slope(k_count: int) -> list[Q]:
    """s[k] such that P_theta(bin k)=1/K + theta*s[k]."""
    return [
        (h_antiderivative(b) - h_antiderivative(a)) / 2
        for a, b in make_bins(k_count)
    ]


def tv_from_signed_masses(left: Sequence[Q], right: Sequence[Q]) -> Q:
    return sum((abs(a - b) for a, b in zip(left, right)), Q(0)) / 2


def apply_kernel_to_slope(slope: Sequence[Q], encoder: Sequence[Sequence[Q]],
                          decoder: Sequence[Sequence[Q]]) -> list[Q]:
    label_slope = [
        sum((slope[k] * encoder[k][j] for k in range(len(encoder))), Q(0))
        for j in range(len(decoder))
    ]
    return [
        sum((label_slope[j] * decoder[j][k] for j in range(len(decoder))), Q(0))
        for k in range(len(decoder[0]))
    ]


def apply_reference(encoder: Sequence[Sequence[Q]],
                    decoder: Sequence[Sequence[Q]]) -> list[Q]:
    k_count = len(encoder)
    return apply_kernel_to_slope([Q(1, k_count)] * k_count, encoder, decoder)


def integer_row(probabilities: Sequence[Q]) -> tuple[list[int], list[int], int]:
    support = [i for i, p in enumerate(probabilities) if p]
    common = math.lcm(*(probabilities[i].denominator for i in support))
    weights = [probabilities[i].numerator * (common // probabilities[i].denominator)
               for i in support]
    assert sum(weights) == common
    cumulative: list[int] = []
    running = 0
    for weight in weights:
        running += weight
        cumulative.append(running)
    return support, cumulative, common


def compile_rows(rows: Sequence[Sequence[Q]]) -> list[tuple[list[int], list[int], int]]:
    return [integer_row(row) for row in rows]


def sample_row(row: tuple[list[int], list[int], int],
               randbelow: Callable[[int], int]) -> int:
    support, cumulative, total = row
    draw = randbelow(total)
    return support[bisect.bisect_right(cumulative, draw)]


def pack_mixed_radix(labels: Sequence[int], radices: Sequence[int]) -> tuple[bytes, int]:
    if len(labels) != len(radices):
        raise ValueError("label and radix counts differ")
    rank = 0
    for label, radix in zip(labels, radices):
        if radix <= 0 or label < 0 or label >= radix:
            raise ValueError("label is outside its mixed-radix digit range")
        rank = rank * radix + label
    state_count = math.prod(radices)
    bit_count = max(1, (state_count - 1).bit_length())
    byte_count = (bit_count + 7) // 8
    return rank.to_bytes(byte_count, "big"), bit_count


def unpack_mixed_digit(packed: bytes, bit_count: int,
                       radices: Sequence[int], slot: int) -> int:
    if not 0 <= slot < len(radices):
        raise IndexError(slot)
    value = int.from_bytes(packed, "big")
    padding = len(packed) * 8 - bit_count
    rank = value >> padding
    suffix = math.prod(radices[slot + 1:])
    return (rank // suffix) % radices[slot]


def encode_vector(input_bins: Sequence[int], active_modes: Sequence[int],
                  encoder_by_mode: dict[int, list], radices: Sequence[int],
                  randbelow: Callable[[int], int]) -> tuple[bytes, int]:
    labels = [
        sample_row(encoder_by_mode[mode][input_bins[mode - 1]], randbelow)
        for mode in active_modes
    ]
    return pack_mixed_radix(labels, radices)


def decode_coordinate(packed: bytes, bit_count: int, mode: int,
                      active_modes: Sequence[int], radices: Sequence[int],
                      decoder_by_mode: dict[int, list], k_count: int,
                      randbelow: Callable[[int], int]) -> int:
    if mode not in active_modes:
        return randbelow(k_count)
    slot = active_modes.index(mode)
    label = unpack_mixed_digit(packed, bit_count, radices, slot)
    return sample_row(decoder_by_mode[mode][label], randbelow)


def decode_vector(packed: bytes, bit_count: int, dimension: int,
                  active_modes: Sequence[int], radices: Sequence[int],
                  decoder_by_mode: dict[int, list], k_count: int,
                  randbelow: Callable[[int], int]) -> list[int]:
    return [
        decode_coordinate(packed, bit_count, mode, active_modes, radices,
                          decoder_by_mode, k_count, randbelow)
        for mode in range(1, dimension + 1)
    ]


def varint_bytes(n: int) -> int:
    """Bytes in the standard unsigned base-128 variable-length encoding."""
    if n == 0:
        return 1
    return (n.bit_length() + 6) // 7


def encode_varint(n: int) -> bytes:
    if n < 0:
        raise ValueError("unsigned varint cannot encode a negative integer")
    out = bytearray()
    while n >= 0x80:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    out.append(n)
    return bytes(out)


def decode_varint(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while True:
        byte = data[offset]
        offset += 1
        value |= (byte & 0x7F) << shift
        if byte < 0x80:
            return value, offset
        shift += 7


def serialize_rows(rows: Sequence[tuple[list[int], list[int], int]],
                   id_count: int) -> bytes:
    id_bytes = max(1, (max(0, id_count - 1).bit_length() + 7) // 8)
    body = bytearray()
    offsets = [0]
    for support, cumulative, _ in rows:
        for output_id, value in zip(support, cumulative):
            body.extend(output_id.to_bytes(id_bytes, "big"))
            body.extend(encode_varint(value))
        offsets.append(len(body))
    header = b"".join(struct.pack(">I", offset) for offset in offsets)
    return header + bytes(body)


def parse_rows(data: bytes, row_count: int, id_count: int
               ) -> list[tuple[list[int], list[int], int]]:
    id_bytes = max(1, (max(0, id_count - 1).bit_length() + 7) // 8)
    header_bytes = 4 * (row_count + 1)
    offsets = [struct.unpack_from(">I", data, 4 * i)[0]
               for i in range(row_count + 1)]
    body = data[header_bytes:]
    result = []
    for row_index in range(row_count):
        pos, stop = offsets[row_index], offsets[row_index + 1]
        support: list[int] = []
        cumulative: list[int] = []
        while pos < stop:
            output_id = int.from_bytes(body[pos:pos + id_bytes], "big")
            pos += id_bytes
            value, pos = decode_varint(body, pos)
            support.append(output_id)
            cumulative.append(value)
        if pos != stop or not cumulative:
            raise ValueError("malformed sparse probability row")
        result.append((support, cumulative, cumulative[-1]))
    if offsets[0] != 0 or offsets[-1] != len(body):
        raise ValueError("malformed row-offset table")
    return result


def table_storage(rows: Sequence[tuple[list[int], list[int], int]],
                  id_count: int) -> dict[str, int]:
    # Declared wire layout: (row_count+1) uint32 offsets, then each supported
    # output ID in the minimum whole-byte width, followed by its cumulative
    # weight as an unsigned base-128 varint. The final cumulative weight is
    # the row denominator; no separate denominator field is stored.
    id_bytes = max(1, (max(0, id_count - 1).bit_length() + 7) // 8)
    entries = sum(len(row[0]) for row in rows)
    payload = 4 * (len(rows) + 1)
    payload += sum(
        id_bytes * len(cumulative) + sum(varint_bytes(v) for v in cumulative)
        for _, cumulative, _ in rows
    )
    return {
        "rows": len(rows),
        "nonzero_entries": entries,
        "max_support": max((len(row[0]) for row in rows), default=0),
        "id_bytes_per_entry": id_bytes,
        "payload_bytes": payload,
        "payload_bits": 8 * payload,
        "max_denominator_bits": max((row[2].bit_length() for row in rows), default=0),
        "max_draw_bits": max((max(0, (row[2] - 1).bit_length()) for row in rows), default=0),
    }


def codec_summary(k_count: int, j_count: int, family: str) -> dict:
    encoder, decoder, nodes = make_transitions(k_count, j_count, family)
    slope = signal_slope(k_count)
    slope_out = apply_kernel_to_slope(slope, encoder, decoder)
    reference_out = apply_reference(encoder, decoder)
    assert reference_out == [Q(1, k_count)] * k_count
    archive_slope_tv = tv_from_signed_masses(slope_out, slope)
    inactive_slope_tv = tv_from_signed_masses(slope, [Q(0)] * k_count)
    compiled_encoder = compile_rows(encoder)
    compiled_decoder = compile_rows(decoder)
    encoder_bytes = serialize_rows(compiled_encoder, j_count + 1)
    decoder_bytes = serialize_rows(compiled_decoder, k_count)
    assert parse_rows(encoder_bytes, k_count, j_count + 1) == compiled_encoder
    assert parse_rows(decoder_bytes, j_count + 1, k_count) == compiled_decoder
    assert len(encoder_bytes) == table_storage(compiled_encoder, j_count + 1)["payload_bytes"]
    assert len(decoder_bytes) == table_storage(compiled_decoder, k_count)["payload_bytes"]
    encoder_stats = table_storage(compiled_encoder, j_count + 1)
    decoder_stats = table_storage(compiled_decoder, k_count)

    # Exercise the actual table lookup path with deterministic PRNG draws.
    rng = random.Random(0xA57A + j_count + (0 if family == "graded" else 1))
    one_encoded = sample_row(compiled_encoder[k_count // 2], rng.randrange)
    one_decoded = sample_row(compiled_decoder[one_encoded], rng.randrange)

    return {
        "family": family,
        "J": j_count,
        "labels": j_count + 1,
        "fixed_label_bits": (j_count + 1 - 1).bit_length(),
        "ideal_label_bits": math.log2(j_count + 1),
        "max_node_denominator_bits": max(node.denominator.bit_length() for node in nodes),
        "encoder_table": {
            **encoder_stats,
            "serialized_bytes": len(encoder_bytes),
            "serialized_sha256": hashlib.sha256(encoder_bytes).hexdigest(),
        },
        "decoder_table": {
            **decoder_stats,
            "serialized_bytes": len(decoder_bytes),
            "serialized_sha256": hashlib.sha256(decoder_bytes).hexdigest(),
        },
        "offline_compiler_segment_intersection_checks": (2 * k_count * (j_count + 1) + j_count + 1) * j_count,
        "encoder_cdf_comparison_upper": math.ceil(math.log2(encoder_stats["max_support"] + 1)),
        "decoder_cdf_comparison_upper": math.ceil(math.log2(decoder_stats["max_support"] + 1)),
        "encoder_expected_rng_bits_upper_per_draw": 2 * encoder_stats["max_draw_bits"],
        "decoder_expected_rng_bits_upper_per_draw": 2 * decoder_stats["max_draw_bits"],
        "max_expected_rng_bit_bound_per_exact_draw": 2 * max(
            (max(0, (row[2] - 1).bit_length()) for row in compiled_encoder + compiled_decoder),
            default=0,
        ),
        "coordinate_codec_tv_slope": str(archive_slope_tv),
        "coordinate_codec_tv_slope_decimal": float(archive_slope_tv),
        "coordinate_reference_tv_exact": str(tv_from_signed_masses(reference_out, [Q(1, k_count)] * k_count)),
        "inactive_reference_decoder_tv_slope": str(inactive_slope_tv),
        "sample_path": {"input_bin": k_count // 2, "label": one_encoded, "output_bin": one_decoded},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="write JSON certificate to this path")
    args = parser.parse_args()

    k_count = 256
    epsilon = Q(1, 10)
    radii = [Q(1, 2**i) for i in range(1, 9)]

    # For rho=1/2, h=x/3+x^3/6: m=M=1/2, L=0, c=1/3,
    # H1=5/6, H2=1. N66 gives C0=215/24, C1=25/4 and
    # C*=.5 exp(1/8) sqrt(C0^2+C1^2) < (4/7)*11 < 7.
    c0 = Q(215, 24)
    c1 = Q(25, 4)
    assert c0 * c0 + c1 * c1 < 121
    c_star_upper = 7

    active = [(i, r) for i, r in enumerate(radii, start=1) if r > epsilon]
    inactive = [(i, r) for i, r in enumerate(radii, start=1) if r <= epsilon]
    mode_specs = []
    for i, r in active:
        j_count = ceil_sqrt_fraction(Q(2 * c_star_upper) * r / epsilon)
        mode_specs.append((i, r, j_count))

    results = {"graded": [], "uniform": []}
    for family in results:
        for i, r, j_count in mode_specs:
            record = codec_summary(k_count, j_count, family)
            record["mode_i"] = i
            record["radius_r"] = str(r)
            record["input_bits"] = k_count.bit_length() - 1
            record["output_bits"] = k_count.bit_length() - 1
            results[family].append(record)

    sigma = Q(results["graded"][0]["inactive_reference_decoder_tv_slope"])
    # Archive reference preservation is exact for both compilers. Since the
    # family is affine in theta and coordinates are independent, TV tensorizes
    # by a hybrid bound. Cauchy-Schwarz uses sum_i v_i^2 <= 1.
    global_bounds = {}
    for family in results:
        active_sq = sum(
            (r * Q(record["coordinate_codec_tv_slope"])) ** 2
            for (_, r, _), record in zip(mode_specs, results[family])
        )
        inactive_sq = sum((r * sigma) ** 2 for _, r in inactive)
        bound_sq = active_sq + inactive_sq
        global_bounds[family] = {
            "squared_rational": str(bound_sq),
            "tv_bound_decimal": math.sqrt(float(bound_sq)),
            "meets_epsilon": bound_sq <= epsilon * epsilon,
        }

    labels = [j + 1 for _, _, j in mode_specs]
    ideal_archive_bits = sum(math.log2(size) for size in labels)
    mixed_radix_bits = (math.prod(labels) - 1).bit_length()
    field_archive_bits = sum((size - 1).bit_length() for size in labels)
    total_public_bytes = {
        family: sum(r["encoder_table"]["payload_bytes"] + r["decoder_table"]["payload_bytes"]
                    for r in results[family])
        for family in results
    }
    graded_encoder_rng_bound = sum(
        record["encoder_expected_rng_bits_upper_per_draw"] for record in results["graded"]
    )
    graded_decoder_rng_bound = sum(
        record["decoder_expected_rng_bits_upper_per_draw"] for record in results["graded"]
    )
    inactive_output_rng_bits = len(inactive) * (k_count.bit_length() - 1)
    compiler_checks_per_family = sum(
        record["offline_compiler_segment_intersection_checks"] for record in results["graded"]
    )

    # Exercise the full encode/store/post-storage-query/decode path on the
    # compiled graded tables. A fixed PRNG seed makes this path replayable;
    # only the exact rational transition matrices are the certificate.
    graded_encoder_by_mode: dict[int, list] = {}
    graded_decoder_by_mode: dict[int, list] = {}
    for i, _, j_count in mode_specs:
        encoder, decoder, _ = make_transitions(k_count, j_count, "graded")
        enc_raw = serialize_rows(compile_rows(encoder), j_count + 1)
        dec_raw = serialize_rows(compile_rows(decoder), k_count)
        graded_encoder_by_mode[i] = parse_rows(enc_raw, k_count, j_count + 1)
        graded_decoder_by_mode[i] = parse_rows(dec_raw, j_count + 1, k_count)
    active_modes = [i for i, _, _ in mode_specs]
    radices = [j_count + 1 for _, _, j_count in mode_specs]
    demo_rng = random.Random(0xDEC0DE)
    demo_input = [k_count // 2] * len(radii)
    demo_archive, demo_archive_bits = encode_vector(
        demo_input, active_modes, graded_encoder_by_mode, radices, demo_rng.randrange
    )
    demo_query = decode_coordinate(
        demo_archive, demo_archive_bits, 2, active_modes, radices,
        graded_decoder_by_mode, k_count, demo_rng.randrange
    )
    demo_output = decode_vector(
        demo_archive, demo_archive_bits, len(radii), active_modes, radices,
        graded_decoder_by_mode, k_count, demo_rng.randrange
    )

    output = {
        "status": "exact finite-binned executable certificate; not continuous-output TV validation",
        "contract": {
            "model": "8 independent regular affine sensors with diagonal inverse radii r_i=2^-i",
            "dimension": len(radii),
            "reference": "independent Uniform[-1,1] coordinates",
            "score": "h(x)=x/3+x^3/6; C2, mean zero, |h|<=1/2, h'>=1/3",
            "parameter": "sum_i v_i^2<=1; density dP_v/dmu=product_i(1+r_i v_i h(x_i))",
            "observation": f"each source coordinate is supplied as one of {k_count} exact equal-width bins ({k_count.bit_length()-1} bits)",
            "target": "fresh vector of output-bin indices; total variation is measured on the finite product alphabet",
            "encoder": "knows the input bins and public reference tables, not v; no parameter-dependent state",
            "query": "one coordinate may be selected after archive formation; its label and decoder row are read directly",
            "error": "sup over the declared ellipsoid of finite-alphabet product TV",
            "epsilon": str(epsilon),
            "radii": [str(r) for r in radii],
            "active_modes": [i for i, _, _ in mode_specs],
            "inactive_modes": [i for i, _ in inactive],
            "J_by_active_mode": {str(i): j for i, _, j in mode_specs},
        },
        "theorem_constant": {
            "C0": str(c0),
            "C1": str(c1),
            "certified_upper_for_Cstar": c_star_upper,
            "J_rule": "ceil(sqrt(2*7*r_i/epsilon)) for r_i>epsilon",
        },
        "archive": {
            "label_counts": labels,
            "ideal_bits": ideal_archive_bits,
            "mixed_radix_payload_bits": mixed_radix_bits,
            "concatenated_field_bits": field_archive_bits,
            "byte_aligned_archive_bytes": (mixed_radix_bits + 7) // 8,
            "byte_aligned_archive_allocated_bits": 8 * ((mixed_radix_bits + 7) // 8),
            "archive_layout": "mixed-radix rank z=(((j1*L2)+j2)*L3+...), stored in the minimum fixed-length bit string; unused rank values are invalid; inactive coordinates need no stored state",
            "product_total_if_packed_as_mixed_radix": math.prod(labels),
            "public_transition_table_bytes_in_declared_layout": total_public_bytes,
            "public_transition_table_layout": "per-row uint32 offsets; each sparse entry is an output ID plus cumulative unsigned base-128 integer; the final cumulative integer is the denominator",
            "input_bits_per_vector": len(radii) * (k_count.bit_length() - 1),
            "output_bits_per_vector": len(radii) * (k_count.bit_length() - 1),
        },
        "runtime_costs": {
            "graded_offline_compiler_segment_intersection_checks": compiler_checks_per_family,
            "graded_table_generation": "exact Fraction arithmetic; O(K*J_i^2) with this deliberately simple full-segment integration loop; sparse stored tables have O(K+J_i) nonzero entries per coordinate",
            "encoder": "direct input-bin row lookup; at most 2 binary-search comparisons because encoder row support <=3; one exact randbelow draw per active coordinate",
            "decoder_active": "one mixed-radix digit extraction and table-row lookup; at most 8 binary-search comparisons in this instance; one exact randbelow draw per active coordinate",
            "decoder_inactive": "one exact randbelow(256), exactly 8 fair random bits per reference output bin",
            "active_encoder_expected_rng_bits_upper_per_vector": graded_encoder_rng_bound,
            "active_decoder_expected_rng_bits_upper_per_vector": graded_decoder_rng_bound,
            "inactive_decoder_rng_bits_per_vector": inactive_output_rng_bits,
            "all_encode_and_fresh_vector_decode_expected_rng_bits_upper": graded_encoder_rng_bound + graded_decoder_rng_bound + inactive_output_rng_bits,
            "mode_2_post_storage_query_expected_rng_bits_upper": next(r["decoder_expected_rng_bits_upper_per_draw"] for r in results["graded"] if r["mode_i"] == 2),
            "mode_2_post_storage_query_cdf_comparisons_upper": next(r["decoder_cdf_comparison_upper"] for r in results["graded"] if r["mode_i"] == 2),
            "mixed_radix_digit_extraction": "two integer quotient/remainder operations on the 9-bit rank; one-byte query table row ID",
            "random_bit_bound": "randbelow(W) via fair-bit rejection, b=ceil(log2 W)=(W-1).bit_length, uses <2b expected bits; worst-case has no finite bound",
        },
        "costs_by_mode": {family: records for family, records in results.items()},
        "product_tv_certificate": global_bounds,
        "replayed_full_codec_path": {
            "input_bins": demo_input,
            "archive_hex": demo_archive.hex(),
            "archive_payload_bits": demo_archive_bits,
            "mode_2_post_storage_query_bin": demo_query,
            "fresh_output_vector_bins": demo_output,
            "randomness": "deterministic Python PRNG for replay only; exact ideal sampler uses randbelow(total) with fair-bit rejection",
        },
        "falsifier": "Any failed exact row-normalization/reference-preservation assertion or product_tv_certificate.meets_epsilon=false falsifies this finite-binned certificate. A comparison reversal (uniform bound <= graded bound) falsifies only the example-specific practical advantage, not N66.",
        "limitations": [
            "The bins define the source and target contract; this does not establish unbinned continuous-law TV error.",
            "The example supplies the exact uniform reference, cubic score, inverse radii, and binning. Acquiring an unknown density/operator is outside the contract.",
            "The public table byte counts include transition tables only; runtime/library, model metadata, RNG state, and calibration data are separate.",
            "Uniform hats share the exact finite input/output alphabet, model, reference, archive label count, and randomness interface; they are an equally informed baseline, not a dimension-free theorem candidate.",
        ],
    }
    assert all(v["meets_epsilon"] for v in global_bounds.values())

    text = json.dumps(output, indent=2, sort_keys=True)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
