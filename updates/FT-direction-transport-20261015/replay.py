#!/usr/bin/env python3
"""FT bounded copy-first replay; bounded execution statuses retain each source and theorem scope."""
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

BASE = 'b7cada92d2eb304578be5ed974f1e44b10a89928'
PREFIX = 'updates/FT-direction-transport-20261015/'
KNOWN_REPO = '/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-direction-transport-20261015'
DEFAULT_PYTHON = '/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-direction-transport-v1/.venv/bin/python'
# Selection authorized by root. No exploratory/search/probe verifier is selected.
STEP_SPECS = [('incoming_direction', 'package/direction/verify_direction_obstruction.py', [], 'package/direction/verification.json'), ('incoming_closure', 'package/closure/closure_experiment.py', [], 'package/closure/synthetic_results.json'), ('incoming_empirical', 'package/closure/empirical_analysis.py', [], 'package/closure/empirical_results.json'), ('incoming_transport', 'package/transport/astra_transport_checks.py', ['--output', '{WORK}/synthesis/transport_damage/source_replay_results.json'], 'synthesis/transport_damage/source_replay_results.json'), ('cartesian', 'synthesis/cartesian_elimination/check_cartesian_development.py', [], 'synthesis/cartesian_elimination/CHECK_RECEIPT.json'), ('scalar_schur', 'synthesis/direction_rigidity/verify_scalar_schur_countermodel.py', [], 'synthesis/direction_rigidity/exact_countermodel_checks.json'), ('G_heat', 'synthesis/nonlinear_qc/verify_G_heat.py', [], 'synthesis/nonlinear_qc/G_HEAT_VERIFICATION.json'), ('orbit_soft', 'synthesis/nonlinear_qc/verify_orbit_and_soft.py', [], 'synthesis/nonlinear_qc/ORBIT_AND_SOFT_VERIFICATION.json'), ('port_completion', 'synthesis/port_completion/check.py', [], 'synthesis/port_completion/check_results.json'), ('load_task', 'synthesis/external_interfaces/verify_load_task_quotient.py', [], 'synthesis/external_interfaces/verification.json'), ('accessible_clamps', 'synthesis/accessible_clamps/check_accessible_clamps.py', ['--output', '{WORK}/synthesis/accessible_clamps/CHECK_RESULTS.json'], 'synthesis/accessible_clamps/CHECK_RESULTS.json'), ('transport_damage', 'synthesis/transport_damage/check_transport.py', [], 'synthesis/transport_damage/results.json'), ('connections', 'synthesis/capital_connections/verify_connections.py', [], 'synthesis/capital_connections/CONNECTION_VERIFICATION.json'), ('adversarial_operation', 'synthesis/adversarial_operation/verify_adversarial_operation.py', [], 'synthesis/adversarial_operation/EXACT_CHECKS.json'), ('G_adversarial', 'synthesis/adversarial_operation/verify_G_certificate_adversarial.py', [], 'synthesis/adversarial_operation/G_ADVERSARIAL_CHECKS.json'), ('task_complete', 'root/verify_task_complete.py', [], 'root/TASK_COMPLETE_CHECK.json'), ('G_independent', 'root/verify_G_heat_independently.py', [], 'root/G_HEAT_INDEPENDENT_CHECK.json'), ('G_lifted_law', 'root/verify_G_lifted_law.py', [], 'root/G_LIFTED_LAW_CHECK.json'), ('empirical_prefix_audit', 'root/audit_empirical_transcription_v2.py', [], 'root/EMPIRICAL_TRANSCRIPTION_AUDIT.json')]

REQUIRED_BASE_REFERENCES = ['updates/FS-phase-closure-20261015/synthesis/phase_geometry/TRANSLATION_GAUGE_AND_SOFT_OPERATOR.md', 'updates/FR-capital-mining-20261015/synthesis/external_machinery/HEAT_TO_CRITICAL_TRACE.md']
EXCLUDED_HISTORY = ['root/audit_empirical_transcription.py', 'root/EMPIRICAL_TRANSCRIPTION_FIRST_FAILURE.json']

def select_steps(packet):
    selected = list(STEP_SPECS)
    additions = packet / 'REPLAY_ADDITIONS.json'
    if additions.is_file():
        document = json.loads(additions.read_text())
        need(document.get('schema') == 'astra.ft-bounded-replay-additions.v1', 'unsupported optional replay selection')
        for item in document['steps']:
            script = item['script']; name = item['name']
            need((script.startswith(('root/', 'synthesis/nonlinear_qc/')) or script in ('synthesis/cartesian_elimination/check_G_storage_scope.py', 'synthesis/adversarial_operation/verify_storage_compatibility_supplement.py')) and script.endswith('.py'), 'optional checker outside approved G storage roles')
            need('storage' in Path(script).name.lower() and not any(x in Path(script).name.lower() for x in ['search', 'acquire']), 'only explicitly selected bounded G storage additions permitted')
            need(isinstance(item.get('scope'), str) and item['scope'].strip(), 'optional checker needs exact scope')
            selected.append((name, script, item.get('args', []), item['output']))
    need(len({x[0] for x in selected}) == len(selected), 'duplicate bounded replay step')
    for name, script, args, output in selected:
        need(local(packet, script).is_file(), 'selected checker absent: ' + script)
        local(packet, output)
        need(all(isinstance(x, str) for x in args), 'non-string checker argument')
        need(script not in EXCLUDED_HISTORY and not any(x in Path(script).name.lower() for x in ['search', 'acquire']), 'historical failure/search/acquisition must not enter routine PASS selection')
    return selected

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
    adapters = []
    for name, target in [('sources', 'package'), ('workers', 'synthesis')]:
        need(not (work / name).exists(), 'copy already has path alias: ' + name)
        (work / name).symlink_to(target, target_is_directory=True)
        adapters.append({'kind': 'copy_only_path_alias', 'path': name, 'target': target,
                         'scope': 'Preserve original source/root parent lookups; published originals unchanged.'})
    name = 'synthesis/cartesian_elimination/check_cartesian_development.py'
    before = 'assert head==PIN,(head,PIN)'
    after = "subprocess.run(['git','merge-base','--is-ancestor',PIN,'HEAD'],cwd=WORK,check=True)"
    path = local(work, name); original = path.read_bytes(); text = original.decode()
    need(text.count(before) == 1, 'unexpected Cartesian pinned HEAD adapter shape')
    changed = text.replace(before, after).replace(KNOWN_REPO, str(repo)); path.write_text(changed)
    adapters.append({'kind': 'copy_only_head_and_path_adapter', 'file': name,
        'original_sha256': digest(original), 'adapted_sha256': sha(path),
        'original_assertion': before, 'replacement': after,
        'reason': 'BASE ancestry and exact prior FS source bytes checked by runner; checked descendant HEAD only.'})
    return adapters

def restore_frozen_cartesian_inventory(work, original_packet):
    """Restore frozen originals in the disposable copy after saving prior replay output."""
    folder = 'synthesis/cartesian_elimination/'
    manifest_name = folder + 'WORKER_MANIFEST.json'
    original_manifest = local(original_packet, manifest_name)
    need(sha(local(work, manifest_name)) == sha(original_manifest), 'copied frozen manifest drift')
    manifest = json.loads(original_manifest.read_text()); restored = []
    for name, record in manifest['files'].items():
        relative = folder + name
        original = local(original_packet, relative).read_bytes(); copied = local(work, relative)
        need(digest(original) == record['sha256'] and len(original) == record['bytes'], 'frozen Cartesian source inventory mismatch: ' + relative)
        before = sha(copied) if copied.is_file() else None
        copied.write_bytes(original)
        restored.append({'path': relative, 'copied_before_sha256': before,
            'restored_sha256': sha(copied), 'frozen_sha256': record['sha256'],
            'bytes': len(original), 'changed_in_copy': before != record['sha256']})
    return {'manifest_path': manifest_name, 'manifest_sha256': sha(original_manifest),
        'scope': 'Copy-only restore for the storage checker frozen-inventory assertion; earlier fresh replay outputs remain separately preserved.',
        'files': restored}

def execute_steps(work, out, python, timeout, specs=STEP_SPECS, originals=None, original_packet=None):
    checks = []; scoped_results = []
    (out / 'results').mkdir(exist_ok=True)
    for name, relative, arguments, output in specs:
        restorations = None
        if relative == 'synthesis/cartesian_elimination/check_G_storage_scope.py':
            need(original_packet is not None, 'storage replay needs original frozen packet')
            restorations = restore_frozen_cartesian_inventory(work, original_packet)
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
            need(isinstance(data, dict), 'expected fresh structured result object')
            target = out / 'results' / (name + '.json'); shutil.copyfile(result_path, target)
            output_info = {'path': str(target.relative_to(out)), 'sha256': sha(target),
                           'source_reported_status': data.get('status', 'not_reported')}
            output_info['source_reported_scope'] = data.get('scope', data.get('limits', data.get('finite_scope', 'not_reported')))
            if name == 'incoming_empirical':
                classification = 'producer_transcribed_prefix_reanalysis'
                need(len(data['objective_traces']['Invisibility']) == 39, 'producer-prefix scope changed')
                scoped_results.append({'name': name, **output_info, 'meaning': 'Producer39-row invisibility prefix; proposed port completion not experimentally validated.'})
            if relative == 'synthesis/cartesian_elimination/check_G_storage_scope.py':
                classification = 'four_exact_storage_groups_with_separate_analytic_proof'
                need(data.get('groups') == 4 and data.get('frozen_inventory_unchanged') is True, 'storage four-group/frozen-source scope changed')
                need(isinstance(data.get('analytic_scope'), str) and isinstance(data.get('heat_scope'), str), 'storage analytic/heat premise scope absent')
                scoped_results.append({'name': name, **output_info, 'analytic_scope': data['analytic_scope'], 'heat_scope': data['heat_scope'],
                    'meaning': 'Four exact checks retained; universal supplied heat/QC premise and analytic required-supply/continuity arguments remain separately proved and reviewed.'})
            if relative == 'synthesis/adversarial_operation/verify_storage_compatibility_supplement.py':
                classification = 'five_exact_storage_law_groups_with_separate_analytic_proof'
                need(data.get('groups') == 5 and isinstance(data.get('scope'), str), 'storage-law five-group scope changed')
                scoped_results.append({'name': name, **output_info, 'meaning': 'Five exact constants and finite identity groups; analytic storage, trace-compactness and law-limit arguments remain separately proved and reviewed.'})
            if name == 'empirical_prefix_audit':
                classification = 'raw_prefix_match_with_omitted_final_row'
                files = {x['objective']: x for x in data['files']}
                need(set(files) == {'CPA', 'TMT', 'Invisibility'}, 'raw audit needs all three CSVs')
                invis = files['Invisibility']
                need(invis['raw_rows'] == 40 and invis['transcribed_rows'] == 39 and invis['omitted_final_values'] == [1.7068097484292658e-5], 'omitted raw endpoint scope lost')
                for ref in files.values():
                    need(sha(local(work, ref['path'])) == ref['sha256'], 'raw CSV audit hash mismatch')
                scoped_results.append({'name': name, **output_info, 'meaning': 'Three primary CSV hashes checked; full invisibility log has40 rows, producer transcribed39, omitted endpoint retained.'})
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            error = str(exc)
        checks.append({'name': name, 'script': relative, 'command': command, 'exit_code': code,
            'wall_seconds': time.monotonic() - start, 'log': log.name, 'log_sha256': sha(log),
            'original_script_sha256': originals.get(relative) if originals else None,
            'executed_script_sha256': sha(script), 'copied_prior_result_sha256': prior_result,
            'fresh_output': output_info, 'result_classification': classification,
            'copy_frozen_inventory_restoration': restorations,
            'execution_check': 'PASS' if error is None else 'FAIL', 'error': error})
        print(name + ': ' + checks[-1]['execution_check'] + ' (' + classification + ')', flush=True)
    return checks, scoped_results

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
    need(curation['base_revision'] == BASE and curation['intake_id'] == 'FT', 'finalized curation pin/scope mismatch')
    before = publication_hashes(repo); packet_before = packet_hashes(packet)
    deps = pinned_dependencies(repo, curation)
    for name in REQUIRED_BASE_REFERENCES:
        raw = local(repo, name).read_bytes(); need(raw == git(repo, 'show', BASE + ':' + name), 'pinned checker dependency drift: ' + name)
        if name not in {x['path'] for x in deps}: deps.append({'path': name, 'sha256': digest(raw), 'bytes': len(raw), 'source_revision': BASE})
    selected = select_steps(packet)
    excluded = [{'path': name, 'sha256': sha(local(packet, name)), 'reason': 'Retained failed exact-full-record empirical assertion/history; not routine PASS selection.'} for name in EXCLUDED_HISTORY]
    out.mkdir(parents=True); work = out / 'work'; shutil.copytree(packet, work, ignore=shutil.ignore_patterns('__pycache__'))
    input_manifest = out / 'PUBLISHED_INPUTS.json'; input_manifest.write_bytes(encoded(before))
    packet_manifest = out / 'PACKET_INPUTS.json'; packet_manifest.write_bytes(encoded(packet_before))
    adapters = adapt_copy(work, repo)
    runtime = json.loads(subprocess.check_output([str(args.python), '-B', '-c',
        'import sys,json,numpy,scipy,sympy;print(json.dumps(dict(python=sys.version,executable=sys.executable,numpy=numpy.__version__,scipy=scipy.__version__,sympy=sympy.__version__)))'], text=True))
    checks, scoped_results = execute_steps(work, out, args.python, args.timeout_seconds, specs=selected, originals=packet_before, original_packet=packet)
    after = publication_hashes(repo); changed = [name for name in sorted(set(before) | set(after)) if before.get(name) != after.get(name)]
    unchanged = not changed and packet_before == packet_hashes(packet)
    receipt = {'schema': 'astra.ft-copy-first-replay.v1', 'tooling_version': '0003', 'status': 'PASS' if unchanged and all(x['execution_check'] == 'PASS' for x in checks) else 'FAIL',
        'base_revision': BASE, 'observed_head': git(repo, 'rev-parse', 'HEAD').decode().strip(),
        'scope': 'Bounded exact/numerical reproduction only; universal G/translation/Schur claims are separately proved/reviewed in source texts; execution does not establish external correctness, novelty or physical acquisition.',
        'runtime': runtime, 'checks': checks, 'total_steps': len(checks), 'selected_steps': [x[0] for x in selected], 'selection_specs': selected,
        'runtime_adapters': adapters, 'pinned_dependencies': deps,
        'published_input_files': len(before), 'published_inputs_hash_unchanged': unchanged, 'changed_published_paths': changed,
        'published_input_manifest': {'path': input_manifest.name, 'sha256': sha(input_manifest)},
        'packet_input_manifest': {'path': packet_manifest.name, 'sha256': sha(packet_manifest)},
        'scoped_results': scoped_results, 'excluded_historical_checks': excluded,
        'generator_sha256': sha(Path(__file__)), 'timeout_seconds_per_step': args.timeout_seconds}
    (out / 'RECEIPT.json').write_bytes(encoded(receipt))
    print(json.dumps({k: v for k, v in receipt.items() if k not in ('checks', 'runtime_adapters', 'pinned_dependencies')}, indent=2))
    return 0 if receipt['status'] == 'PASS' else 1

if __name__ == '__main__': raise SystemExit(main())
