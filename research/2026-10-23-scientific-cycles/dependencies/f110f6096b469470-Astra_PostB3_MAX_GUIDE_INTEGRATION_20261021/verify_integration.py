#!/usr/bin/env python3
"""Bounded receipt verification only. Never fits RNA models or resumes draws.

Python standard library. The exact producer ZIP is retained unchanged. Optional
--common streams and hashes the already supplied input, without extracting it.
Reported floating arithmetic is checked to tolerance, not certified as an exact
population effect. Producer rank certificates are received, not regenerated here.
"""
import argparse
import ast
import csv
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import platform
import re
import resource
import stat
import struct
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parent
PRODUCER_NAME = 'Astra_PostB3_ULTRA_GUIDE_RESULT_20261021'
PRODUCER_SHA = '2a064407a4b4ff875f71f7631ae30e4309cb625d5cb3b5cbff3f03f40dac7953'
COMMON_SHA = 'cb89eb8ff17ef2f35131d5058a294181eac927cdd2d131003205b974e2f3f968'
INPUT_SHA = '5da0485aed81b23bda57b4a7b4510a394682d54911416db89b4846ff6dd34732'
CONTRACT_SHA = 'b2a8fbb8a408bdda718f78528f156ab25c84470794df3178a089da4b5ba82fbd'
SOURCE_SHA = 'a2ddf21711499bae08d7504235103d0913bb5dcd24782a19cc11ee2ed3e26ef4'
MAP_SHA = '793e85498a1359fa39ca28b5321b95dd5d86093ef8c6ad387d7ec395a548388d'
DOTS_NAME = 'Astra_PostB3_DOTS_GUIDE_CHECK_20261021'
DOTS_SHA = '20dbda0f9fb02a1e55553af61c5be8511f71ba7ae22dbf51f7be7a3eddb37156'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest_stream(stream):
    h = hashlib.sha256()
    size = 0
    for block in iter(lambda: stream.read(1024 * 1024), b''):
        h.update(block)
        size += len(block)
    return size, h.hexdigest()


def identity(path):
    with path.open('rb') as f:
        return digest_stream(f)


def read_json(path):
    return json.loads(path.read_text())


def close(a, b):
    require(math.isfinite(a) and math.isfinite(b), 'Nonfinite reported arithmetic')
    require(math.isclose(a, b, rel_tol=2e-12, abs_tol=2e-12), f'Arithmetic mismatch: {a}, {b}')


def verify_manifest(root):
    envelope = read_json(root / 'MANIFEST.json')
    m = envelope.get('files', envelope)
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(actual == set(m) | {'MANIFEST.json'}, 'Manifest does not enumerate exact payload')
    for name, record in m.items():
        p = PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts, 'Unsafe manifest path')
        require(identity(root / name) == (record['bytes'], record['sha256']), f'Manifest mismatch: {name}')
    return len(m)


def npz_shapes(path):
    """Read NPY headers only; no scientific calculation on partial draws."""
    shapes = {}
    with zipfile.ZipFile(path) as z:
        require(len(z.namelist()) == len(set(z.namelist())), 'Duplicate NPZ member')
        for member in z.infolist():
            with z.open(member) as f:
                require(f.read(6) == b'\x93NUMPY', 'Invalid NPY magic')
                version = tuple(f.read(2))
                require(version in {(1, 0), (2, 0), (3, 0)}, 'Unexpected NPY version')
                fmt = '<H' if version == (1, 0) else '<I'
                length = struct.unpack(fmt, f.read(struct.calcsize(fmt)))[0]
                require(length <= 16384, 'Oversized NPY header')
                header = ast.literal_eval(f.read(length).decode('utf-8' if version == (3, 0) else 'latin1'))
                dtype = re.fullmatch(r'[<>|=][fiu]([1248])', header['descr'])
                require(dtype is not None, 'Unexpected NPY dtype')
                shape = header['shape']
                require(all(isinstance(n, int) and n >= 0 for n in shape), 'Invalid NPY dimensions')
                require(member.file_size - f.tell() == math.prod(shape) * int(dtype[1]), 'NPY payload size mismatch')
                shapes[member.filename] = list(shape)
    expected = {'gains.npy': [7, 2, 2, 105], 'null_gain.npy': [7, 2, 2],
                'lambda_index.npy': [7, 2, 2], 'null_lambda_index.npy': [7, 2, 2],
                'control_weights.npy': [7, 7], 'technical_ranks.npy': [7, 2]}
    require(shapes == expected, 'Partial-draw execution differs from reported 7 draws')
    return shapes


def verify_saved_output(root):
    require(identity(root / 'FROZEN_CONTRACT.txt')[1] == CONTRACT_SHA, 'Contract pin differs')
    require(identity(root / 'src/run_guide_experiment.py')[1] == SOURCE_SHA, 'Frozen source pin differs')
    require(identity(root / 'results/DESIGN_MAP.json')[1] == MAP_SHA, 'Design pin differs')
    freeze = read_json(root / 'FREEZE.json')
    require((freeze['contract_sha256'], freeze['analysis_source_sha256'], freeze['design_map_sha256']) ==
            (CONTRACT_SHA, SOURCE_SHA, MAP_SHA), 'Freeze/source binding mismatch')
    require(freeze['historically_untouched'] is False, 'Historical exposure scope changed')
    point = read_json(root / 'results/POINT_RESULT.json')
    result = read_json(root / 'results/RESULT.json')
    design = read_json(root / 'results/DESIGN_MAP.json')
    body = read_json(root / 'results/RESOURCE_RECEIPT.json')
    outer = read_json(root / 'results/OUTER_RESOURCE_RECEIPT.json')
    require(point['input_sha256'] == INPUT_SHA == body['input_sha256'] == design['identity']['h5ad_sha256'], 'Scientific input mismatch')
    require(point['contract_sha256'] == CONTRACT_SHA, 'Point contract binding mismatch')
    require(len(design['eligible_pairs']) == 105 and len(design['excluded_pairs']) == 53, 'Admission/exclusions changed')
    require(design['matching_control_n'] == 7 and design['matching_control'] == 'NT_g1:NT_g2', 'Matching control changed')
    require(point['families'] == design['eligible_pairs'] and len(set(point['families'])) == 105, 'Family order differs')
    require(result['status'] == 'STOP_RESOURCE_CAP_NO_ROBUST_GUIDE_SIGNAL_ESTABLISHED', 'Scientific status changed')
    require(result['bootstrap_completed'] == body['completed'] == 7 and result['bootstrap_requested'] == body['requested'] == 399, 'Draw status changed')
    require(result['inference_status'].startswith('NOT_COMPUTED') and result['leave_one_control_out_status'].startswith('NOT_PERFORMED'), 'Unperformed inference was promoted')
    require(outer['returncode'] == 1 and body['peak_rss_bytes'] > 3 * 2**30, 'Resource failure receipt differs')
    require(body['peak_rss_bytes'] == outer['child_peak_rss_bytes'], 'Peak RSS receipts disagree')
    require('RuntimeError: frozen3GiB RSS resource cap' in (root / 'results/ANALYSIS_STDERR.txt').read_text(), 'Missing preserved stop traceback')
    require(result['resource_body'] == body and result['resource_entire_command'] == outer, 'Final result detached from execution receipts')
    require(not any(k in json.dumps(result) for k in ['simulated_p', 'basic_interval']), 'Completed inference asserted')
    csv_rows = list(csv.DictReader((root / 'results/ALL_FAMILY_SCORES.csv').open()))
    require(len(csv_rows) == 420, 'Family CSV row count differs')
    rows = {(r['representation'], r['direction'], r['family']): r for r in csv_rows}
    require(len(rows) == 420, 'Duplicate CSV rows')
    for summary in result['point_summary']:
        kind, direction = summary['representation'], summary['direction']
        z = int(direction[0]) - 1
        values = point['point'][kind][z]
        for key in ('gain', 'ordinary_mse', 'transfer_mse', 'additive_mse'):
            require(len(values[key]) == 105, 'Incomplete point comparison')
            close(math.fsum(values[key]) / 105, summary[key])
        for i, family in enumerate(point['families']):
            close(values['ordinary_mse'][i] - values['transfer_mse'][i], values['gain'][i])
            row = rows[(kind, direction, family)]
            for key in ('gain', 'ordinary_mse', 'transfer_mse', 'additive_mse'):
                close(float(row[key]), values[key][i])
            close(float(row['beta_A']), values['beta'][i][0])
            close(float(row['beta_B']), values['beta'][i][1])
            require(int(row['projector_span_rank']) == values['rank'][i], 'CSV projector rank differs')
            close(float(row['singleton_gram_eigen_min']), values['single_gram_eigenvalues'][i][0])
            close(float(row['singleton_gram_eigen_max']), values['single_gram_eigenvalues'][i][1])
        require(summary['positive_family_gains'] == sum(v > 0 for v in values['gain']), 'Positive counts differ')
        require(summary['source_selected_lambda'] == [.01, .1, 1, 10, 100][values['lambda_index']], 'Source lambda differs')
        close(1 - summary['ordinary_mse'] / summary['additive_mse'], summary['ordinary_error_reduction_vs_raw_additive'])
        close(summary['transfer_mse'] / summary['ordinary_mse'] - 1, summary['transfer_relative_error_change_vs_ordinary'])
        for key in ('clipped_ordinary_entries', 'clipped_transfer_entries'):
            require(summary[key] == values[key], 'Clipping report differs')
        require(summary['gain'] < 0 if kind == 'log' else summary['gain'] > 0, 'Representation disagreement changed')
    require(len(result['point_summary']) == 4, 'Not all scales/directions reported')
    return {'producer_manifest_payload_files': 74, 'family_rows_tied_to_point_json': 420,
            'point_summary': result['point_summary'], 'partial_npz_shapes': npz_shapes(root / 'results/BOOTSTRAP_DRAWS.npz'),
            'producer_resource_body': body, 'producer_resource_outer': outer,
            'completed_intervals_or_null_calibration': False, 'control_omissions_completed': 0,
            'RNA_or_model_replay': False, 'rank_check_regenerated_by_Max': False}


def verify_received_dots(path, tempdir, producer_summary):
    require(identity(path) == (4057493, DOTS_SHA), 'Dots ZIP does not match delivered identity')
    with zipfile.ZipFile(path) as z:
        members = z.infolist()
        require(len(members) == 29 and len({i.filename for i in members}) == 29, 'Dots ZIP member count differs')
        require(sum(i.file_size for i in members) < 64 * 1024**2, 'Unexpected Dots expansion')
        for i in members:
            p = PurePosixPath(i.filename)
            require(not p.is_absolute() and '..' not in p.parts and p.parts[0] == DOTS_NAME and not stat.S_ISLNK(i.external_attr >> 16), 'Unsafe Dots ZIP path')
        z.extractall(tempdir)
    root = Path(tempdir) / DOTS_NAME
    require(verify_manifest(root) == 28, 'Dots payload count differs')
    require(identity(root / 'source_archives' / (PRODUCER_NAME + '.zip')) == (4029706, PRODUCER_SHA), 'Dots assessed a different producer packet')
    decision = read_json(root / 'RESULT.json')
    require(decision['producer_result_sha256'] == PRODUCER_SHA and decision['decision'] == 'ACCEPT_SCOPED_NEGATIVE_AND_INCOMPLETE_RESULT_STOP', 'Dots disposition differs')
    require(decision['positive_scientific_claim_accepted'] is False and decision['uncertainty_complete'] is False, 'Dots acceptance was promoted')
    design = read_json(root / 'design_review/receipt.json')
    require(design['original_input_pins']['raw'] == INPUT_SHA and design['original_input_pins']['book'] == '64582b92edae28b71a6aff1072cb600c275969e6af454465be475c8a58a22450', 'Dots scientific input differs')
    require((design['eligible'], design['excluded'], design['control_cells']) == (105, 53, 7), 'Dots design receipt disagrees')
    point = read_json(root / 'independent_point_receipt.json')
    require(point['input_sha256'] == INPUT_SHA and point['independent_implementation'] is True and point['producer_source_imported'] is False, 'Point reconstruction scope changed')
    require(point['uncertainty_draws_executed'] == 0 and point['loco_executed'] is False, 'Receiver execution was promoted')
    summary = {(r['representation'], int(r['direction'][0])-1): r for r in producer_summary}
    require(len(point['point_rows']) == 4, 'Incomplete Dots point rows')
    clipping = []
    for row in point['point_rows']:
        reference = summary[(row['scale'], row['direction'])]
        errors = row['maximum_absolute_family_discrepancy']
        require(max(errors.values()) < 2e-7, 'Dots declared tolerance failed')
        for key, value in row['means'].items():
            require(abs(value - reference[key]) <= errors[key] + 2e-12, 'Independent mean inconsistent with discrepancy receipt')
        require(row['positive_gain_count'] == reference['positive_family_gains'], 'Independent sign count differs')
        require([.01, .1, 1, 10, 100][row['lambda_index']] == reference['source_selected_lambda'], 'Independent lambda differs')
        require(row['clipped_ordinary'] == reference['clipped_ordinary_entries'], 'Ordinary clipping differs')
        clipping.append({'scale': row['scale'], 'direction_0based': row['direction'],
                         'producer_transfer_clipped': reference['clipped_transfer_entries'],
                         'Dots_transfer_clipped': row['clipped_transfer']})
    inference = read_json(root / 'inference_review/inference_controls.json')
    require(inference['producer_source_sha256'] == SOURCE_SHA and inference['partial_inference_status_consistent'] is True, 'Dots source/failure binding differs')
    require(inference['rss_portability']['linux_counterexample_4GiB_raw_KiB_would_not_trigger'] is True, 'Linux cap finding missing')
    require(inference['rss_portability']['full_runner_executed'] is False, 'Receiver full-run scope changed')
    return {'status': 'RECEIVED_AND_BOUND_SCOPED_ACCEPTANCE', 'archive_sha256': DOTS_SHA,
            'manifest_payload_files': 28, 'scientific_decision': decision['decision'],
            'independent_point_receipt': point, 'transfer_clipping_exact_reproduction': False,
            'clipping_differences': clipping, 'Linux_producer_cap_portability': 'FAILED_UNCHANGED_RUNNER; actual Mac stop remains supported',
            'Dots_RNA_or_controls_reexecuted_by_Max': False,
            'scope': 'Actual independent Dots RNA/design/control evidence received and source/receipt bindings checked; not a Max RNA replay or completed inference'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', type=Path, default=ROOT / 'received' / (PRODUCER_NAME + '.zip'))
    ap.add_argument('--dots', type=Path, default=ROOT / 'received' / (DOTS_NAME + '.zip'))
    ap.add_argument('--common', type=Path, help='Optional existing common ZIP: hash bytes only, no RNA analysis')
    ap.add_argument('--output', type=Path, required=True, help='Write receipt outside the sealed source directory')
    args = ap.parse_args()
    start, cpu = time.perf_counter(), time.process_time()
    require(not args.output.resolve().is_relative_to(ROOT.resolve()), 'Receipt output must be outside sealed packet')
    own_manifest_count = verify_manifest(ROOT) if (ROOT / 'MANIFEST.json').exists() else None
    require(identity(args.archive) == (4029706, PRODUCER_SHA), 'Producer ZIP does not match activation identity')
    with tempfile.TemporaryDirectory(prefix='astra_max_guide_receipt_') as td:
        with zipfile.ZipFile(args.archive) as z:
            members = z.infolist()
            require(len(members) == 75 and len({i.filename for i in members}) == 75, 'Producer ZIP member count differs')
            require(sum(i.file_size for i in members) < 64 * 1024**2, 'Unexpected producer expansion')
            for i in members:
                p = PurePosixPath(i.filename)
                require(not p.is_absolute() and '..' not in p.parts and p.parts[0] == PRODUCER_NAME and not stat.S_ISLNK(i.external_attr >> 16), 'Unsafe producer ZIP path')
            z.extractall(td)
        root = Path(td) / PRODUCER_NAME
        require(verify_manifest(root) == 74, 'Producer payload count differs')
        checks = verify_saved_output(root)
        dots = verify_received_dots(args.dots, td, checks['point_summary'])
    input_check = {'scope': 'Immutable input binding received; optional independent common-byte check not requested'}
    if args.common:
        require(identity(args.common) == (215144567, COMMON_SHA), 'Common ZIP differs from supplied source')
        with zipfile.ZipFile(args.common) as z:
            name = 'Astra_PostB3_Empirical_Probe_20261021/data/WesselsSatija2023.h5ad'
            with z.open(name) as f:
                require(digest_stream(f) == (219393529, INPUT_SHA), 'Scientific input bytes differ')
        input_check = {'common_zip_sha256': COMMON_SHA, 'h5ad_sha256': INPUT_SHA,
                       'h5ad_bytes': 219393529, 'streamed_byte_identity_only': True,
                       'h5ad_decoded_or_RNA_analyzed': False}
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    receipt = {'status': 'PASS_BOUNDED_SOURCE_AND_SAVED_OUTPUT_RECEIPT',
               'producer_zip_sha256': PRODUCER_SHA, 'integration_manifest_files_verified': own_manifest_count,
               'checks': checks, 'input_check': input_check,
               'Dots_received_assessment': dots,
               'scientific_disposition': 'Preserve descriptive comparison and scoped conditional information obstruction; robust guide-distinct effect not established; allocation remains stopped',
               'Dots_acceptance': 'Actual scoped negative/incomplete acceptance received; Max agrees within DECISION.txt limits. No completed inference inferred.',
               'wall_seconds': time.perf_counter() - start, 'self_cpu_seconds': time.process_time() - cpu,
               'process_peak_rss_bytes': peak if sys.platform == 'darwin' else peak * 1024,
               'python': sys.version, 'platform': platform.platform(),
               'scope': 'Receipt/hash/saved arithmetic and partial-array header verification only; no new draw, fit, rank calculation, or biological inference'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: receipt[k] for k in ('status', 'wall_seconds', 'self_cpu_seconds', 'process_peak_rss_bytes')}))


if __name__ == '__main__':
    main()
