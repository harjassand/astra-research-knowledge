#!/usr/bin/env python3
"""Audit acquired source predictions, not an independent dynamical simulation.

Requires numpy. Inputs are pinned GitHub data acquired in sources/
serial3ded_acquisition.json. No simulation, diffraction integration, atomic model
solution or experimental chirality validation is represented as performed here.
"""
from pathlib import Path
import collections
import json
import math
import time
import xml.etree.ElementTree as ET
import zipfile

import numpy as np

BASE = Path(__file__).resolve().parent
DATA = BASE / 'data/serial3ded/DemoData/Cinchonine/simu'
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def workbook(path):
    """Read numeric source-export tables without a spreadsheet runtime."""
    result = {}
    with zipfile.ZipFile(path) as z:
        sheets = ET.fromstring(z.read('xl/workbook.xml')).findall('m:sheets/m:sheet', NS)
        for idx, sheet in enumerate(sheets, 1):
            root = ET.fromstring(z.read(f'xl/worksheets/sheet{idx}.xml'))
            rows = root.findall('m:sheetData/m:row', NS)
            header = [''.join(c.itertext()) for c in rows[0]]
            a = [[float(c.find('m:v', NS).text) for c in r] for r in rows[1:]]
            result[sheet.get('name')] = (header, np.asarray(a))
    return result


def weighted_l1_scale(x, y):
    """Exact nonnegative scale minimizing sum(abs(y-scale*x))."""
    valid = x > 0
    ratio, weight = y[valid] / x[valid], x[valid]
    order = np.argsort(ratio)
    return max(0., float(ratio[order][np.searchsorted(np.cumsum(weight[order]), .5 * weight.sum())]))


def fit(pred, obs, sigma, mask):
    x, y, s = pred[mask], obs[mask], sigma[mask]
    scale = max(0., float(np.dot(x / s, y / s) / np.dot(x / s, x / s)))
    chi2 = float(np.sum(((y - scale * x) / s) ** 2))
    fa, fb = np.sqrt(x), np.sqrt(y)
    amp_scale = weighted_l1_scale(fa, fb)
    r1 = float(np.abs(fb - amp_scale * fa).sum() / fb.sum())
    return {'scale_intensity': scale, 'chi2': chi2, 'n': int(mask.sum()),
            'r1_amplitude_l1': r1, 'scale_amplitude': amp_scale}


def main():
    started = time.perf_counter()
    raw = np.asarray([[float(v) for v in line.split()]
                      for line in (DATA / 'XDS_ASCII.HKL').read_text().splitlines()
                      if not line.startswith('!')])
    keys = [tuple(map(int, r[:3])) for r in raw]
    assert len(set(keys)) == len(keys), 'Do not silently merge dynamic intensities'
    tables = [workbook(DATA / name) for name in ['Intensity.xlsx', 'Intensity_inv.xlsx']]
    thicknesses = list(tables[0])
    assert list(tables[1]) == thicknesses
    sim_keys = [tuple(map(int, r[:3])) for r in tables[0][thicknesses[0]][1]]
    assert len(set(sim_keys)) == len(sim_keys)
    lookup = {k: i for i, k in enumerate(sim_keys)}
    common = np.array([i for i, key in enumerate(keys) if key in lookup], dtype=int)
    observed = raw[common]
    indices = [lookup[keys[i]] for i in common]
    predictions = np.empty((2, len(thicknesses), len(common)))
    for hand, wb in enumerate(tables):
        for ti, thick in enumerate(thicknesses):
            a = wb[thick][1]
            assert [tuple(map(int, r[:3])) for r in a] == sim_keys
            predictions[hand, ti] = a[indices, 3]
    intensity, signed_sigma = observed[:, 3], observed[:, 4]
    sigma = np.abs(signed_sigma)
    assert np.all(sigma > 0) and np.all(predictions > 0)
    # Negative sigma is an XDS MISFIT flag, not a negative uncertainty.
    # Dynamical symmetry breaking may itself generate such flags, so neither
    # automatic inclusion nor automatic exclusion is independent validation.
    strong = (intensity > 2 * sigma) & (signed_sigma > 0)
    source_compatible = (intensity > 0) & (intensity > 2 * signed_sigma)
    all_fits = []
    for hand in range(2):
        for ti, thick in enumerate(thicknesses):
            all_fits.append({'hand': hand, 'thickness_grid_A': int(thick[:-1]),
                             **fit(predictions[hand, ti], intensity, sigma, strong)})

    source_selection_fits = []
    for hand in range(2):
        for ti, thick in enumerate(thicknesses):
            source_selection_fits.append({'hand': hand, 'thickness_grid_A': int(thick[:-1]),
                                         **fit(predictions[hand, ti], intensity, sigma, source_compatible)})
    # Source coordinates and orientations already used all diffraction data.
    # These folds validate only hand/thickness/scale scoring, not full pipeline.
    angle_coordinate = observed[:, 7]
    cutpoints = np.quantile(angle_coordinate[strong], np.linspace(0, 1, 6))
    blocks = np.clip(np.digitize(angle_coordinate, cutpoints[1:-1]), 0, 4)
    folds = []
    for fold in range(5):
        train, test = strong & (blocks != fold), strong & (blocks == fold)
        hands = []
        for hand in range(2):
            candidates = [fit(p, intensity, sigma, train) for p in predictions[hand]]
            ti = min(range(len(candidates)), key=lambda j: candidates[j]['chi2'])
            chosen = candidates[ti]
            residual = (intensity[test] - chosen['scale_intensity'] * predictions[hand, ti, test]) / sigma[test]
            hands.append({'hand': hand, 'train_thickness_grid_A': int(thicknesses[ti][:-1]),
                          'train_scale': chosen['scale_intensity'],
                          'test_chi2': float(np.dot(residual, residual)), 'test_n': int(test.sum())})
        folds.append({'block': fold, 'ZD_range': [float(angle_coordinate[test].min()),
                                                float(angle_coordinate[test].max())],
                      'hand_fits': hands})

    # Finite-grid contrast separation in real acquired prediction tables.
    obs_lookup = {tuple(map(int, r[:3])): i for i, r in enumerate(observed)}
    pairs = []
    for key, i in obs_lookup.items():
        opposite = tuple(-x for x in key)
        if opposite not in obs_lookup or key <= opposite:
            continue
        j = obs_lookup[opposite]
        if not (strong[i] and strong[j]):
            continue
        sums = predictions[:, :, i] + predictions[:, :, j]
        contrasts = (predictions[:, :, i] - predictions[:, :, j]) / sums
        intervals = [[float(row.min()), float(row.max())] for row in contrasts]
        gap = max(intervals[0][0] - intervals[1][1], intervals[1][0] - intervals[0][1])
        measured = (intensity[i] - intensity[j]) / (intensity[i] + intensity[j])
        variance = (4 * intensity[j] ** 2 * sigma[i] ** 2 +
                    4 * intensity[i] ** 2 * sigma[j] ** 2) / (intensity[i] + intensity[j]) ** 4
        pairs.append({'hkl': key, 'minus_hkl': opposite, 'grid_interval_by_hand': intervals,
                      'finite_grid_gap': gap, 'observed_contrast': float(measured),
                      'observed_contrast_delta_method_sigma': float(np.sqrt(variance)),
                      'ZD_pair_separation': float(abs(angle_coordinate[i] - angle_coordinate[j])),
                      'source_intensities': [float(intensity[i]), float(intensity[j])],
                      'source_sigmas': [float(sigma[i]), float(sigma[j])]})
    pairs.sort(key=lambda p: p['finite_grid_gap'], reverse=True)
    (BASE / 'friedel_pair_grid_audit.json').write_text(json.dumps(pairs, indent=2) + '\n')

    # One isolated positive intensity is exactly nonidentifying with free gain.
    i = int(np.flatnonzero(strong)[0])
    scalar_example = {'hkl': list(map(int, observed[i, :3])), 'observed_I': float(intensity[i]),
                      'thickness_grid_A': 100,
                      'predicted_I_by_hand': predictions[:, 0, i].tolist(),
                      'exact_fit_gain_by_hand': (intensity[i] / predictions[:, 0, i]).tolist(),
                      'squared_residual_by_hand': [0., 0.]}
    source_table = workbook(DATA / 'R-factors.xlsx')
    source_header = next(iter(source_table.values()))[0]
    result = {
        'status': 'SOURCE_MODEL_DISCRIMINATION_ONLY; NO_NEW_OPERATION',
        'inputs': {'observed_rows': len(raw), 'observed_distinct_hkl': len(set(keys)),
                   'source_prediction_rows_per_hand_per_thickness': len(sim_keys),
                   'common_rows': len(common),
                   'observed_positive_intensity_rows': int((raw[:, 3] > 0).sum()),
                   'XDS_flagged_rows': int((raw[:, 4] < 0).sum()),
                   'observed_strong_unflagged_rows': int(((raw[:, 3] > 2 * np.abs(raw[:, 4])) & (raw[:, 4] > 0)).sum()),
                   'common_strong_unflagged_rows': int(strong.sum()),
                   'source_compatible_positive_I_and_I_gt_2_signed_sigma_rows': int(((raw[:, 3] > 0) & (raw[:, 3] > 2 * raw[:, 4])).sum()),
                   'source_compatible_common_rows': int(source_compatible.sum()),
                   'thickness_grid_A': list(range(100, 1001, 100)),
                   'model_space_group_from_cif': 'P 21, IT number 4',
                   'source_R_workbook_header': source_header,
                   'saved_notebook_claimed_counts': {'observed_positive_rows': 1874,
                                                    'strong_rows': 1290, 'common_strong_rows': 1271}},
        'method': 'Profile a single positive intensity scale independently for each hand and source thickness grid; exact weighted Gaussian SSE; L1 amplitude R1 is separate. No p-values inferred.',
        'full_fits_unflagged_strong': all_fits,
        'full_fits_source_count_compatible_selection': source_selection_fits,
        'held_out_angle_blocks': folds,
        'pair_summary': {'strong_measured_friedel_pairs': len(pairs),
                         'positive_gap_finite_grid_pairs': sum(p['finite_grid_gap'] > 0 for p in pairs),
                         'positive_gap_ZD_distance_le_2': sum(p['finite_grid_gap'] > 0 and p['ZD_pair_separation'] <= 2 for p in pairs),
                         'top_five_grid_separated_pairs': pairs[:5]},
        'single_intensity_gain_counterexample': scalar_example,
        'limitations': ['Atomic coordinates, orientation and indexed hkl supplied by incumbent pipeline; no independent structural solution.',
                        'Source computed intensity tables were acquired, not recomputed; compiled Windows extension used by source cannot execute in the current macOS Python runtime.',
                        'Only 10 fixed thicknesses and source orientation are considered. Between-grid thickness, orientation, shape, excitation error, absorption and detector-gain uncertainty remain untested.',
                        'Five scoring folds do not remove leakage from the previously fitted atomic coordinates and orientation.',
                        'Friedel-pair selection after seeing all predictions is not an independent dose-reduction demonstration.',
                        'XDS errors and source theory mismatch are not an independently validated error model.',
                        'Detector pattern handedness requires separately calibrated goniometer rotation and detector geometry, or a known absolute reference.',
                        'Saved notebook counts are exactly reproduced by positive I and I>2*signed_sigma selection, including XDS flagged MISFITs. The compiled code was not inspected, so matching counts do not prove the implementation predicate. The R-workbook space-group headers disagree with the monoclinic sample model.'],
        'execution_elapsed_s': time.perf_counter() - started,
        'inference_tokens': 'UNKNOWN', 'inference_energy': 'UNKNOWN', 'inference_cost': 'UNKNOWN',
    }
    (BASE / 'cinchonine_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    for hand in range(2):
        rows = [r for r in all_fits if r['hand'] == hand]
        best = min(rows, key=lambda r: r['chi2'])
        print('hand', hand, 'best_chi2', best)
    print('pair_summary', result['pair_summary'])
    print('folds', folds)
    print('elapsed_s', result['execution_elapsed_s'])


if __name__ == '__main__':
    main()
