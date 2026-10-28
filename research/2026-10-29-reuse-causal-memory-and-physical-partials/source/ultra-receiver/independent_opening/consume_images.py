#!/usr/bin/env python3
"""Finite-record, finite-bit harmonic query; not a hydrodynamic estimator claim.

Run with bundled Python (NumPy and Pillow). Inputs are the public H015 ZIP and
the declared pole/scale below. No particle identities, velocity fields, PSF
fit, displacement bounds, iid assumption or physical truth enters this code.
"""
from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path
import hashlib
import io
import json
import math
import time
import zipfile

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
BITS = 32
SCALE = 1 << BITS
NAMES = ['A1r', 'A1i', 'A2r', 'A2i', 'B1r', 'B1i', 'B2r', 'B2i']


def rounded(num: int, den: int) -> int:
    """Nearest integer, ties upwards; exact half-unit error bound."""
    assert den > 0
    return (2 * num + den) // (2 * den)


def compile_weights(width: int, height: int):
    side = 1 << (max(width, height) - 1).bit_length()
    den = 2 * side
    assert SCALE % (den * den) == 0
    # Pixel centers, pole one 'side' to the left of the image. All coordinates
    # are in units of 'side' pixels. No inner circular wall is inferred.
    rows = [[] for _ in NAMES]
    max_quant_error = F(0)
    for r in range(height):
        Y = 2 * r + 1 - height
        for c in range(width):
            X = 2 * c + 1 + 2 * side
            D = X * X + Y * Y
            pairs = [
                (SCALE * den * X, D),
                (-SCALE * den * Y, D),
                (SCALE * den * den * (X * X - Y * Y), D * D),
                (-2 * SCALE * den * den * X * Y, D * D),
                (SCALE * X, den),
                (SCALE * Y, den),
                (SCALE * (X * X - Y * Y), den * den),
                (2 * SCALE * X * Y, den * den),
            ]
            for j, (num, div) in enumerate(pairs):
                q = rounded(num, div)
                # Check every actual compiled weight using integers.
                assert 2 * abs(q * div - num) <= div
                if j >= 4:
                    assert q * div == num
                rows[j].append(q)
    bank = np.array(rows, dtype=np.int64)
    return bank, side


def moments(image, bank):
    flat = image.ravel().astype(np.int64)
    peak = int(flat.max())
    out = []
    maxw = max(int(np.max(np.abs(w))) for w in bank)
    # Every individual dot sum has absolute sum strictly below 2^62.
    chunk = min(flat.size, max(1, ((1 << 62) - 1) // max(1, maxw * peak)))
    for weights in bank:
        total = 0
        for start in range(0, flat.size, chunk):
            stop = min(start + chunk, flat.size)
            total += int(np.dot(flat[start:stop], weights[start:stop]))
        out.append(total)
    return out + [int(flat.sum())], chunk


def cov(A, B):
    n = len(A)
    assert n == len(B) and n > 1
    return F(n * sum(a * b for a, b in zip(A, B)) - sum(A) * sum(B),
             n * (n - 1))


def cov_quant(A, B, mass):
    """Covariance of one rounded Laurent sum and one EXACT polynomial sum.

    Integers A,B represent image sums times 2^BITS; Laurent rounding error
    per image is <= mass/(2*2^BITS), with mass nonnegative. For difference
    images it is the actual L1 pixel difference, not a free cancellation.
    """
    n = len(A)
    SB = sum(B)
    center = cov(A, B) / (SCALE * SCALE)
    radius = F(sum(m * abs(n * b - SB) for m, b in zip(mass, B)),
               2 * n * (n - 1) * SCALE * SCALE)
    return center, radius


def query(left, right, mass):
    # beta=1. q(left,right) = -Im Cov(A2,B2)+2 Im Cov(A1,B1).
    center = F(0)
    radius = F(0)
    for ai, bi, coefficient in [(2, 7, -1), (3, 6, -1),
                                 (0, 5, 2), (1, 4, 2)]:
        value, err = cov_quant([v[ai] for v in left],
                               [v[bi] for v in right], mass)
        center += coefficient * value
        radius += abs(coefficient) * err
    return center, radius


def as_json(center, radius=F(0)):
    return {'center': float(center), 'radius_arithmetic_only': float(radius),
            'lower_fraction': str(center - radius),
            'upper_fraction': str(center + radius),
            'numerator_bits': max((center - radius).numerator.bit_length(),
                                  (center + radius).numerator.bit_length()),
            'denominator_bits': max((center - radius).denominator.bit_length(),
                                    (center + radius).denominator.bit_length())}


def summarize(records):
    left = [r['left'] for r in records]
    right = [r['right'] for r in records]
    diff = [[b - a for a, b in zip(x, y)] for x, y in zip(left, right)]
    fwd = query(left, right, [r['left'][8] for r in records])
    rev = query(right, left, [r['right'][8] for r in records])
    self0 = query(left, left, [r['left'][8] for r in records])
    self1 = query(right, right, [r['right'][8] for r in records])
    qdiff, ediff = query(diff, diff, [r['L1_difference'] for r in records])
    controlled = (-qdiff / 2, ediff / 2)
    # Literal algebra holds at the rounded-weight level; this is not a
    # stochastic validity assertion for the dataset.
    assert controlled[0] == (fwd[0] + rev[0] - self0[0] - self1[0]) / 2
    normalizer = cov([r['left'][8] for r in records],
                     [r['right'][8] for r in records])
    out = {'record_pairs': len(records),
           'forward': as_json(*fwd), 'reverse': as_json(*rev),
           'self_start_expected_zero_only_under_model': as_json(*self0),
           'self_end_expected_zero_only_under_model': as_json(*self1),
           'symmetric_difference_control': as_json(*controlled),
           'normalizer_empirical': as_json(normalizer),
           'normalizer_positive': normalizer > 0}
    if normalizer > 0:
        for name, value in [('forward', fwd), ('symmetric_difference_control', controlled)]:
            out[name + '_normalized_empirical'] = as_json(value[0] / normalizer,
                                                         value[1] / normalizer)
    return out


def main():
    started = time.perf_counter()
    path = ROOT / 'data' / 'MS_Images_H015.zip'
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    assert sha == '2a1e5b41f44e57c315f1e62ad56e44e6dc6c76eb03171c4cf30735b16562c00c'
    hash_done = time.perf_counter()
    records = []
    decode_seconds = weighted_seconds = 0.
    max_pixel = 0
    chunks = []
    bank = None
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        assert names == [f'B{i:05}.tif' for i in range(1, 501)]
        for k in range(0, len(names), 2):
            arrays = []
            ms = []
            for name in names[k:k+2]:
                t = time.perf_counter()
                # ZipFile.read checks each member CRC. No TIFF re-encoding.
                arr = np.array(Image.open(io.BytesIO(archive.read(name))))
                assert arr.dtype == np.uint16
                decode_seconds += time.perf_counter() - t
                if bank is None:
                    height, width = arr.shape
                    t = time.perf_counter()
                    bank, side = compile_weights(width, height)
                    compile_seconds = time.perf_counter() - t
                assert arr.shape == (height, width)
                max_pixel = max(max_pixel, int(arr.max()))
                t = time.perf_counter()
                moment, chunk = moments(arr, bank)
                weighted_seconds += time.perf_counter() - t
                arrays.append(arr)
                ms.append(moment)
                chunks.append(chunk)
            l1 = int(np.abs(arrays[1].astype(np.int64) - arrays[0].astype(np.int64)).sum())
            records.append({'members': names[k:k+2], 'left': ms[0], 'right': ms[1],
                            'L1_difference': l1})
    stats_start = time.perf_counter()
    summary = summarize(records)
    blocks = [summarize(records[k:k+25]) for k in range(0, len(records), 25)]
    # No confidence claim: TR-PIV pairs are not declared iid.
    summary.update({
        'source_zip_sha256': sha,
        'source_contract': 'experimental rectangular turbulent jet; not annular torque data',
        'frames': 500, 'shape': [height, width], 'pixel_type': 'uint16',
        'actual_max_pixel': max_pixel, 'weight_bits': BITS,
        'coordinate_rule': 'z=((c+.5)+side)/side + i*((r+.5)-height/2)/side',
        'side_pixels': side, 'beta': 1,
        'pole': [-side, height / 2],
        'all_compiled_weight_integer_half_ulp_checks': height * width * 8,
        'polynomial_weights_exact': True,
        'signed_dot_absolute_bound': 'strictly below 2^62 for each chunk',
        'smallest_dot_chunk_pixels': min(chunks),
        'weight_bank_bytes': bank.nbytes,
        'source_pixels_read': 500 * height * width,
        'weighted_scalar_multiplications': 500 * height * width * 8,
        'weighted_real_sums_per_frame': 8,
        'total_intensity_sums_per_frame': 1,
        'finite_record_only': True,
        'population_confidence': 'NOT_ACQUIRED: temporal dependence/model gates unpaid',
        'physical_torque': 'NOT_ACQUIRED',
        'conditional_radial_PSF_support_tail_contract': 'NOT_ACQUIRED from these images',
        'cost_seconds': {
            'zip_hash': hash_done - started,
            'weight_compile': compile_seconds,
            'decode_and_crc': decode_seconds,
            'weighted_moments': weighted_seconds,
            'statistics': time.perf_counter() - stats_start,
            'total_after_imports': time.perf_counter() - started,
        },
        'ten_contiguous_block_diagnostics_no_iid_confidence': blocks,
    })
    (ROOT / 'DATA_RECEIPT.json').write_text(json.dumps(summary, indent=2) + '\n')
    (ROOT / 'DATA_MOMENTS.json').write_text(json.dumps({
        'moment_scale': SCALE, 'names': NAMES + ['total_unscaled'],
        'records': records,
    }, indent=2) + '\n')
    display = ['record_pairs', 'normalizer_empirical', 'normalizer_positive',
               'cost_seconds', 'physical_torque']
    display += [k for k in ['forward_normalized_empirical',
                            'symmetric_difference_control_normalized_empirical']
                if k in summary]
    print(json.dumps({k: summary[k] for k in display}, indent=2))


if __name__ == '__main__':
    main()
