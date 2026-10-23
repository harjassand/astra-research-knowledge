#!/usr/bin/env python3
"""Exact, portable metadata-only design obstruction check; Python stdlib only.

Reads DESIGN_MAP.json bytes/metadata, never h5ad/RNA/outcome files. The Fraction
elimination preserves the earlier bounded rank calculation and adds lower/upper
rank certificates, source-null/target-nonnull witnesses, and an explicit J=A*T
interaction/implementation incidence alias. Does not alter frozen inputs/source.
"""
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MAP_SHA256 = '793e85498a1359fa39ca28b5321b95dd5d86093ef8c6ad387d7ec395a548388d'


def rref(matrix):
    """Exact rational elimination; return RREF and pivot column indices."""
    a = [[Fraction(x) for x in row] for row in matrix]
    if not a:
        return a, []
    pivots = []
    rr = 0
    for c in range(len(a[0])):
        chosen = next((i for i in range(rr, len(a)) if a[i][c]), None)
        if chosen is None:
            continue
        a[rr], a[chosen] = a[chosen], a[rr]
        scale = a[rr][c]
        a[rr] = [x / scale for x in a[rr]]
        for i in range(len(a)):
            if i != rr and a[i][c]:
                scale = a[i][c]
                a[i] = [x - scale*y for x, y in zip(a[i], a[rr])]
        pivots.append(c)
        rr += 1
        if rr == len(a):
            break
    return a, pivots


def transpose(a):
    return [list(col) for col in zip(*a)]


def determinant(a):
    a = [[Fraction(x) for x in row] for row in a]
    sign = 1
    answer = Fraction(1)
    for j in range(len(a)):
        chosen = next((i for i in range(j, len(a)) if a[i][j]), None)
        if chosen is None:
            return Fraction(0)
        if chosen != j:
            a[j], a[chosen] = a[chosen], a[j]
            sign *= -1
        pivot = a[j][j]
        answer *= pivot
        for i in range(j+1, len(a)):
            if a[i][j]:
                scale = a[i][j] / pivot
                a[i] = [x-scale*y for x, y in zip(a[i], a[j])]
    return sign * answer


def dot(a, v):
    return [sum((Fraction(x)*y for x, y in zip(row, v)), Fraction(0)) for row in a]


def rank_certificate(a, row_names, column_names):
    reduced, pivots = rref(a)
    _, independent_rows = rref(transpose(a))
    rank = len(pivots)
    assert len(independent_rows) == rank
    minor = [[a[i][j] for j in pivots] for i in independent_rows]
    det = determinant(minor)
    assert det != 0
    free = [j for j in range(len(column_names)) if j not in pivots]
    null_basis = []
    for j in free:
        v = [Fraction(0)] * len(column_names)
        v[j] = Fraction(1)
        for i, p in enumerate(pivots):
            v[p] = -reduced[i][j]
        assert not any(dot(a, v))
        null_basis.append(v)
    assert all(not any(row) for row in reduced[rank:])
    return {
        'rows': len(a), 'columns': len(column_names), 'rank': rank,
        'rank_method': 'exact fractions.Fraction RREF; nonzero minor lower bound; null basis upper bound',
        'pivot_columns': [column_names[j] for j in pivots],
        'minor_row_indices_0based': independent_rows,
        'minor_rows': [row_names[i] for i in independent_rows],
        'minor_column_indices_0based': pivots,
        'minor_determinant_exact': str(det),
        'nullity': len(null_basis),
        'null_basis_exact': [[str(x) for x in v] for v in null_basis],
    }, null_basis


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--map', type=Path, default=ROOT/'results/DESIGN_MAP.json')
    parser.add_argument('--output', type=Path, default=ROOT/'results/DESIGN_OBSTRUCTION_CHECK.json')
    args = parser.parse_args()
    content = args.map.read_bytes()
    actual_hash = hashlib.sha256(content).hexdigest()
    assert actual_hash == EXPECTED_MAP_SHA256, 'frozen metadata map changed'
    design = json.loads(content)
    assert design['metadata_only'] is True
    families = [f for f in design['families'] if f['eligible']]
    assert len(families) == 105 and len(design['excluded_pairs']) == 53
    assert design['matching_control'] == 'NT_g1:NT_g2'
    assert design['matching_control_n'] == 7
    for f in families:
        a, b = f['a'], f['b']
        assert a < b
        expected = [f'{a}_g1:{b}_g2', f'{b}_g1:{a}_g2',
                    f'{a}_g1:NT_g2', f'NT_g1:{b}_g2',
                    f'{b}_g1:NT_g2', f'NT_g1:{a}_g2', 'NT_g1:NT_g2']
        assert f['arms'] == expected
        assert all(f['counts'][arm] >= 5 for arm in expected)
        spacers = {design['array_map'][arm][key]
                   for arm in expected[:2] for key in ('sequence1', 'sequence2')}
        assert len(spacers) == 4
    names = [f['pair'] for f in families]
    targets = sorted({f[k] for f in families for k in ('a', 'b')})
    guides = sorted({q for f in families for k in ('construction1', 'construction2')
                     for q in f[k].split(':')})
    x = [[int(t in (f['a'], f['b'])) for t in targets] for f in families]
    ds = [[[int(q in f[f'construction{direction}'].split(':')) for q in guides]
           for f in families] for direction in (1, 2)]
    cert_x, _ = rank_certificate(x, names, targets)
    cert_d1, null1 = rank_certificate(ds[0], names, guides)
    cert_d2, null2 = rank_certificate(ds[1], names, guides)
    stacked_names = ['C1:'+n for n in names] + ['C2:'+n for n in names]
    cert_stack, _ = rank_certificate(ds[0]+ds[1], stacked_names, guides)
    assert [cert_x['rank'], cert_d1['rank'], cert_d2['rank'], cert_stack['rank']] == [22, 38, 38, 43]
    source_witnesses = []
    for source, null_basis in enumerate((null1, null2)):
        target = 1-source
        images = [dot(ds[target], v) for v in null_basis]
        image_rank = len(rref(transpose(images))[1])
        assert image_rank == 5
        absent = [q for j, q in enumerate(guides) if not any(row[j] for row in ds[source])]
        q = absent[0]
        v = [Fraction(int(guide == q)) for guide in guides]
        source_image = dot(ds[source], v)
        target_image = dot(ds[target], v)
        assert not any(source_image) and any(target_image)
        source_witnesses.append({
            'source_construction': source+1, 'target_construction': target+1,
            'absent_source_guides': absent,
            'counterpart_relevant_dimension_of_source_nullspace': image_rank,
            'explicit_witness_guide': q,
            'source_image_identically_zero': True,
            'target_image_nonzero_rows': [names[i] for i, value in enumerate(target_image) if value],
            'witness_values_exact': [str(x) for x in v],
        })
    slot_gauge = [Fraction(1 if design['guides'][q]['slots'] == [1] else -1) for q in guides]
    assert all(design['guides'][q]['slots'] in ([1], [2]) for q in guides)
    assert not any(dot(ds[0]+ds[1], slot_gauge))
    # Standard principal convention: A is the cell-to-delivered-array onehot
    # (30707x367), T is delivered-array-to-eligible-family incidence (367x105),
    # and J=A*T is cell-to-eligible-family interaction incidence. Certify at
    # array level via I367 instead of constructing a large cell-level matrix.
    arrays = sorted(design['delivered_counts'])
    counts = [design['delivered_counts'][array] for array in arrays]
    assert len(arrays) == 367 and all(n > 0 for n in counts)
    assert sum(counts) == 30707
    t = [[int(array in (f['construction1'], f['construction2'])) for f in families]
         for array in arrays]
    assert all(sum(row) <= 1 for row in t)
    identity_witness_rows = [arrays.index(f['construction1']) for f in families]
    assert [[t[i][k] for k in range(len(families))] for i in identity_witness_rows] == [
        [int(i == k) for k in range(len(families))] for i in range(len(families))]
    # Every delivered array has at least one cell, so A has an I367 row minor.
    # [I367,T] has the displayed I367 column minor and only367 rows. Thus its
    # rank is exactly367; multiplying by full-column-rank A preserves that rank.
    sequence_slots = {}
    for q in guides:
        sequence_slots.setdefault(design['guides'][q]['sequence'], set()).update(design['guides'][q]['slots'])
    assert all(len(slots) == 1 for slots in sequence_slots.values())
    alias = {
        'definitions': {
            'A': '30707x367 cell-to-delivered-array onehot matrix',
            'T': '367x105 delivered-array-to-eligible-family incidence;1 on both paired arrays,0 on references/other arrays',
            'J': '30707x105 cell-to-eligible-family interaction incidence; J=A*T',
        },
        'delivered_array_order': arrays, 'delivered_array_counts': counts,
        'family_order': names,
        'T_nonzero_rows': [
            {'array_row_0based': i, 'array': arrays[i], 'family_column_0based': k, 'family': names[k]}
            for i, row in enumerate(t) for k, value in enumerate(row) if value],
        'J_equals_A_times_T_exact': True,
        'A_full_column_rank_reason': 'each of367 delivered arrays has at least1 cell; one witness cell per array yields I367',
        'rank_A': len(arrays), 'rank_T': len(families), 'rank_J': len(families),
        'rank_array_level_I_T': len(arrays),
        'rank_concatenated_A_J': len(arrays),
        'interaction_rank_increment_after_array_effects': 0,
        'array_level_identity_minor_row_indices_0based': list(range(len(arrays))),
        'array_level_identity_minor_column_indices_0based': list(range(len(arrays))),
        'array_level_identity_minor_determinant_exact': '1',
        'T_identity_minor_row_indices_0based': identity_witness_rows,
        'T_identity_minor_arrays': [arrays[i] for i in identity_witness_rows],
        'T_identity_minor_determinant_exact': '1',
        'coefficient_null_witness_rule': 'for any105-vector d: array_effects -= T*d; interaction_effects += d',
        'scope': 'unrestricted array-implementation alias; does not assert restricted scalar-potency/target-main-effect model spans arbitrary J',
    }
    result = {
        'status': 'EXACT_METADATA_OBSTRUCTION_VERIFIED',
        'metadata_only': True, 'RNA_files_opened': False,
        'design_map_sha256': actual_hash,
        'input_h5ad_sha256_from_metadata_only': design['identity']['h5ad_sha256'],
        'eligible_families': len(families), 'excluded_families': len(design['excluded_pairs']),
        'eligible_pair_arrays': 2*len(families), 'targets': targets, 'guides': guides,
        'matching_control_n': 7,
        'eligible_physical_sequence_slot_crossings': 0,
        'eligible_unique_targeting_sequences': len(sequence_slots),
        'target_incidence': cert_x, 'guide_C1': cert_d1, 'guide_C2': cert_d2,
        'guide_stacked': cert_stack,
        'source_null_target_nonnull_witnesses': source_witnesses,
        'global_slot_gauge_exact': [str(x) for x in slot_gauge],
        'interaction_implementation_alias': alias,
        'limits': 'no RNA outcome/statistical-power claim; guide/slot and mechanism alias are distinct from absolute-RNA scale ambiguity',
        'checker_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({
        'status': result['status'], 'eligible_families': len(families),
        'rank_X': cert_x['rank'], 'rank_D1': cert_d1['rank'],
        'rank_D2': cert_d2['rank'], 'rank_Dstack': cert_stack['rank'],
        'counterpart_relevant_null_dimensions': [r['counterpart_relevant_dimension_of_source_nullspace'] for r in source_witnesses],
        'J_equals_A_times_T': True, 'interaction_rank_increment': 0,
        'output': str(args.output),
    }, indent=2))


if __name__ == '__main__':
    main()
