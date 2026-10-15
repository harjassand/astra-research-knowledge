#!/usr/bin/env python3
"""FS bounded copy-first replay; execution success never means general positivity."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

BASE = '846f185763ed3a27310fad4ce9471ba324d1e5f4'
PREFIX = 'updates/FS-phase-closure-20261015/'
KNOWN_REPO = '/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-phase-closure-20261015'
DEFAULT_PYTHON = '/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-phase-closure-v1/.venv/bin/python'
# Selection authorized by root. No exploratory/search/probe verifier is selected.
STEP_SPECS = [
    ('phase_exact', 'package/phase_density/verify_directional_density.py', [], 'package/phase_density/directional_density_verification.json'),
    ('phase_adaptive', 'package/phase_density/certify_adaptive_dual.py', [], 'package/phase_density/adaptive_continuum_certificate.json'),
    ('phase_integral512', 'package/phase_density/certify_phase_density.py', ['512'], 'package/phase_density/phase_density_intervals_512.json'),
    ('closure', 'package/closure/closure_audit.py', ['--output-dir', '{WORK}/package/closure/replay_results'], 'package/closure/replay_results/results.json'),
    ('radial', 'synthesis/radial_analysis/check_radial_extensions.py', [], 'synthesis/radial_analysis/EXACT_CHECK_RECEIPT.json'),
    ('external_duality', 'synthesis/external_duality/verify_external_duality.py', [], 'synthesis/external_duality/verification.json'),
    ('shear', 'synthesis/global_compatibility/verify_shear_density.py', [], 'synthesis/global_compatibility/exact_shear_checks.json'),
    ('general_phase', 'synthesis/global_compatibility/verify_general_phase.py', [], 'synthesis/global_compatibility/general_phase_checks.json'),
    ('phase_geometry', 'synthesis/phase_geometry/verify_phase_geometry.py', [], 'synthesis/phase_geometry/exact_checks.json'),
    ('late_resonance', 'synthesis/phase_geometry/verify_late_resonance.py', [], 'synthesis/phase_geometry/late_exact_checks.json'),
    ('decision', 'synthesis/decision_closure/calculate.py', [], 'synthesis/decision_closure/calculation_results.json'),
    ('passive_networks', 'synthesis/passive_networks/verify_passive_networks.py', [], 'synthesis/passive_networks/CHECK_RESULTS.json'),
    ('material', 'synthesis/material_physics/calculate.py', [], 'synthesis/material_physics/results.json'),
    ('connections', 'synthesis/capital_connections/verify_connections.py', [], 'synthesis/capital_connections/CONNECTION_VERIFICATION.json'),
    ('adversarial_response', 'synthesis/adversarial_closure/verify_response_closure.py', [], 'synthesis/adversarial_closure/EXACT_CHECKS.json'),
    ('terminal', 'synthesis/root/verify_terminal_calibration.py', [], 'synthesis/root/TERMINAL_CALIBRATION_CHECK.json'),
]

def need(value, message):
    if not value: raise ValueError(message)
def digest(data): return hashlib.sha256(data).hexdigest()
def sha(path): return digest(path.read_bytes())
def encoded(value): return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()
def local(root, name):
    need(isinstance(name, str) and not Path(name).is_absolute() and '..' not in Path(name).parts, 'unsafe path: ' + str(name))
    p = (root / name).resolve(); need(p.is_relative_to(root.resolve()), 'outside root: ' + name); return p
def git(repo, *args): return subprocess.check_output(['git', '-C', str(repo), *args])
def packet_hashes(packet):
    return {str(p.relative_to(packet)): sha(p) for p in sorted(packet.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
def publication_hashes(repo):
    names = git(repo, 'ls-files', '-z', '--cached', '--others', '--exclude-standard').decode().split('\0')
    return {name: sha(repo / name) if (repo / name).is_file() else None for name in sorted(set(names)) if name and '__pycache__' not in Path(name).parts}

def pinned_dependencies(repo, curation):
    """Pin older evidence bytes at BASE; no original verifier is executed."""
    result = {}
    for ref in curation['evidence'].values():
        recovered = False
        for name in dict.fromkeys([ref['path'], ref.get('read_path', ref['path'])]):
            p = local(repo, name)
            if not p.is_file(): continue
            data = p.read_bytes()
            if digest(data) == ref['sha256']: recovered = True
            elif p.suffix == '.html':
                recovered |= any(digest(html.unescape(b).encode()) == ref['sha256'] for b in re.findall(r'<pre(?:\s[^>]*)?>(.*?)</pre>', data.decode(), re.S))
            if name.startswith(PREFIX): continue
            baseline = git(repo, 'show', BASE + ':' + name)
            need(data == baseline, 'pinned underlying reference changed: ' + name)
            result[name] = {'path': name, 'sha256': digest(data), 'bytes': len(data), 'source_revision': BASE}
        need(recovered, 'selected evidence hash unavailable: ' + ref['path'])
    return list(result.values())

def adapt_copy(work, repo):
    need(not (work / 'sources').exists(), 'copy already has a sources path; inspect mapping')
    (work / 'sources').symlink_to('package', target_is_directory=True)
    adapters = [{'kind': 'copy_only_path_alias', 'path': 'sources', 'target': 'package',
                 'scope': 'Radial SOURCE lookup only; published originals unchanged.'}]
    specs = [
        ('synthesis/radial_analysis/check_radial_extensions.py', 'assert head==PIN, (head,PIN)',
         "subprocess.run(['git','merge-base','--is-ancestor',PIN,'HEAD'],cwd=REPO,check=True)"),
        ('synthesis/external_duality/verify_external_duality.py', 'assert actual==PIN',
         "subprocess.run(['git','merge-base','--is-ancestor',PIN,'HEAD'],cwd=ASTRA,check=True)"),
    ]
    for name, before, after in specs:
        p = local(work, name); original = p.read_bytes(); text = original.decode()
        need(text.count(before) == 1, 'unexpected pinned HEAD adapter shape: ' + name)
        changed = text.replace(before, after).replace(KNOWN_REPO, str(repo))
        p.write_text(changed)
        adapters.append({'kind': 'copy_only_head_and_path_adapter', 'file': name,
            'original_sha256': digest(original), 'adapted_sha256': sha(p),
            'original_assertion': before, 'replacement': after,
            'reason': 'Outer runner verifies BASE ancestry and exact older dependency bytes; permit checked descendant HEAD only.'})
    return adapters

def execute_steps(work, out, python, timeout, specs=STEP_SPECS, originals=None):
    checks = []; inconclusive = []
    (out / 'results').mkdir(exist_ok=True)
    for name, relative, arguments, output in specs:
        script = local(work, relative); result_path = local(work, output)
        prior_result = sha(result_path) if result_path.is_file() else None
        result_path.unlink(missing_ok=True)  # Only the disposable copy; forbid stale PASS reuse.
        command = [str(python), '-B', str(script)] + [a.format(WORK=str(work)) for a in arguments]
        start = time.monotonic(); error = None
        try:
            run = subprocess.run(command, cwd=script.parent, capture_output=True, text=True, timeout=timeout)
            code, stdout, stderr = run.returncode, run.stdout, run.stderr
        except subprocess.TimeoutExpired as exc:
            code = 124; stdout = exc.stdout or ''; stderr = exc.stderr or ''
            if isinstance(stdout, bytes): stdout = stdout.decode(errors='replace')
            if isinstance(stderr, bytes): stderr = stderr.decode(errors='replace')
            stderr += '\nTIMEOUT: ' + str(timeout) + ' seconds'
        log = out / (name + '.log'); log.write_text(stdout + '\nSTDERR:\n' + stderr)
        output_info = None; classification = 'bounded_execution_only'
        try:
            need(code == 0, 'subprocess exit ' + str(code))
            need(result_path.is_file(), 'fresh declared result JSON absent')
            data = json.loads(result_path.read_text())
            need(str(data.get('status', '')).upper() not in ('FAIL', 'ERROR'), 'source result reports failure')
            target = out / 'results' / (name + '.json'); shutil.copyfile(result_path, target)
            output_info = {'path': str(target.relative_to(out)), 'sha256': sha(target),
                           'source_reported_status': data.get('status', 'not_reported')}
            if name == 'phase_integral512':
                need(data.get('N') == 512 and data.get('status') == 'inconclusive interval bound', 'integral512 must retain its expected inconclusive scope')
                classification = 'expected_inconclusive_interval_bound'
                inconclusive.append({'name': name, **output_info, 'meaning': 'Successful bounded reproduction of an inconclusive interval; not an all-positivity certificate.'})
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            error = str(exc)
        checks.append({'name': name, 'script': relative, 'command': command, 'exit_code': code,
            'wall_seconds': time.monotonic() - start, 'log': log.name, 'log_sha256': sha(log),
            'original_script_sha256': originals.get(relative) if originals else None,
            'executed_script_sha256': sha(script), 'copied_prior_result_sha256': prior_result,
            'fresh_output': output_info, 'result_classification': classification,
            'execution_check': 'PASS' if error is None else 'FAIL', 'error': error})
        print(name + ': ' + checks[-1]['execution_check'] + ' (' + classification + ')', flush=True)
    return checks, inconclusive

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--python', type=Path, default=Path(DEFAULT_PYTHON))
    parser.add_argument('--timeout-seconds', type=int, default=240)
    args = parser.parse_args(); repo = args.repo.resolve(); packet = repo / PREFIX; out = args.output_dir.resolve()
    need(packet.is_dir() and not out.exists() and not out.is_relative_to(repo), 'use a new output directory outside the publication checkout')
    need(args.python.is_file() and args.timeout_seconds > 0, 'missing scientific runtime or invalid timeout')
    subprocess.run(['git', '-C', str(repo), 'merge-base', '--is-ancestor', BASE, 'HEAD'], check=True)
    curation = json.loads((packet / 'CURATION_INPUT.json').read_text())
    need(curation['base_revision'] == BASE and curation['intake_id'] == 'FS', 'finalized curation pin/scope mismatch')
    before = publication_hashes(repo); packet_before = packet_hashes(packet)
    deps = pinned_dependencies(repo, curation)
    out.mkdir(parents=True); work = out / 'work'; shutil.copytree(packet, work, ignore=shutil.ignore_patterns('__pycache__'))
    input_manifest = out / 'PUBLISHED_INPUTS.json'; input_manifest.write_bytes(encoded(before))
    packet_manifest = out / 'PACKET_INPUTS.json'; packet_manifest.write_bytes(encoded(packet_before))
    adapters = adapt_copy(work, repo)
    runtime = json.loads(subprocess.check_output([str(args.python), '-B', '-c',
        'import sys,json,numpy,scipy,sympy;print(json.dumps(dict(python=sys.version,executable=sys.executable,numpy=numpy.__version__,scipy=scipy.__version__,sympy=sympy.__version__)))'], text=True))
    checks, inconclusive = execute_steps(work, out, args.python, args.timeout_seconds, originals=packet_before)
    after = publication_hashes(repo); changed = [name for name in sorted(set(before) | set(after)) if before.get(name) != after.get(name)]
    unchanged = not changed and packet_before == packet_hashes(packet)
    receipt = {'schema': 'astra.fs-copy-first-replay.v1', 'status': 'PASS' if unchanged and all(x['execution_check'] == 'PASS' for x in checks) else 'FAIL',
        'base_revision': BASE, 'observed_head': git(repo, 'rev-parse', 'HEAD').decode().strip(),
        'scope': 'Bounded exact/numerical reproduction only; analytic proofs, interval implementation, general positivity, novelty and physical acquisition remain separately scoped.',
        'runtime': runtime, 'checks': checks, 'total_steps': len(checks), 'selected_steps': [x[0] for x in STEP_SPECS],
        'runtime_adapters': adapters, 'pinned_dependencies': deps,
        'published_input_files': len(before), 'published_inputs_hash_unchanged': unchanged, 'changed_published_paths': changed,
        'published_input_manifest': {'path': input_manifest.name, 'sha256': sha(input_manifest)},
        'packet_input_manifest': {'path': packet_manifest.name, 'sha256': sha(packet_manifest)},
        'inconclusive_results': inconclusive, 'all_positivity_certified': False,
        'generator_sha256': sha(Path(__file__)), 'timeout_seconds_per_step': args.timeout_seconds}
    (out / 'RECEIPT.json').write_bytes(encoded(receipt))
    print(json.dumps({k: v for k, v in receipt.items() if k not in ('checks', 'runtime_adapters', 'pinned_dependencies')}, indent=2))
    return 0 if receipt['status'] == 'PASS' else 1

if __name__ == '__main__': raise SystemExit(main())
