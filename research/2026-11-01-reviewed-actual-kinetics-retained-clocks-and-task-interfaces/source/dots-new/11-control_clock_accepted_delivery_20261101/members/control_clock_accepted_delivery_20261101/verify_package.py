"""Nonmutating package verifier. --full adds 214 simulated source calls."""
from pathlib import Path
import hashlib, importlib.util, json, sys

ROOT = Path(__file__).resolve().parent
FREEZE = 'control_effect_clock_20261031/REVIEW_FREEZE_MANIFEST_20261031_2348UTC.json'
REVIEW = 'control_effect_clock_20261031/reviewer_0006/INDEPENDENT_WHOLE_CLOCK_REVIEW.md'
PINS = {FREEZE: '245ef5fdb6fee5dd55ae8eaa33c6839ae3176cd28585be7d485eced517e7151d',
        REVIEW: '482fb75fe98598c79bb56516684555733ee2af1a97d9f562529ad684fc806f12'}

def need(value, message):
    if not value:
        raise ValueError(message)

def hash_checks():
    manifest = json.loads((ROOT/'PACKAGE_MANIFEST.json').read_text())
    listed = set()
    for item in manifest['files']:
        name = item['path']; path = ROOT/name
        need(not Path(name).is_absolute() and '..' not in Path(name).parts and not path.is_symlink(), 'unsafe manifest path')
        need(name not in listed, 'duplicate manifest path'); listed.add(name)
        raw = path.read_bytes()
        need(len(raw) == item['bytes'] and hashlib.sha256(raw).hexdigest() == item['sha256'], 'package hash: '+name)
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    need(actual == listed | {'PACKAGE_MANIFEST.json'}, 'unlisted or missing package files; use python -B')
    for name, pin in PINS.items():
        need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == pin, 'controlling source pin: '+name)
    frozen = json.loads((ROOT/FREEZE).read_text())
    for item in frozen['files'] + frozen['dependencies']:
        raw = (ROOT/item['path']).read_bytes()
        need(len(raw) == item['bytes'] and hashlib.sha256(raw).hexdigest() == item['sha256'], 'freeze hash: '+item['path'])
    return len(listed), len(frozen['files']) + len(frozen['dependencies'])

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

def run(full=False):
    need(sys.dont_write_bytecode, 'run with python -B to preserve a clean package')
    count, frozen_count = hash_checks()
    sys.path.insert(0, str(ROOT/'control_effect_clock_20261031'))
    replay = load('package_clock_replay', 'control_effect_clock_20261031/replay.py')
    result = replay.run(saved_only=not full)
    need(result['status'] == 'PASS' and result['verified_files'] == 23, 'clock replay')
    need(result['saved']['received_admission']['status'] == 'UNKNOWN_ALL_GOAL_DIRECT_CANONICAL_ADMISSION', 'do not relabel actual acquisition')
    need(result['saved']['retained_source_calls'] == 2142, 'retained source calls')
    if full:
        need(result['harness']['checks'] == 707 and result['harness']['refusals'] == 14 and result['new_source_calls'] == 214, 'full harness totals')
        need(result['harness']['failed_search']['status'] == 'UNKNOWN_SEARCH_BUDGET' and result['harness']['failed_search']['attempts'] == 6 and result['harness']['failed_search']['source_calls'] == 100, 'failed search retained')
    else:
        need(result['new_source_calls'] == 0, 'saved replay must use zero calls')
    extra = load('package_independent_checks', 'control_effect_clock_20261031/reviewer_0006/extra_checks.py').run()
    need(extra == json.loads((ROOT/'control_effect_clock_20261031/reviewer_0006/extra_checks.json').read_text()), 'independent check result')
    counter = load('package_gap_counterexample', 'resolvent_direct_canonical_admission_20261031/check_gap_objective_counterexample.py').run()
    need(counter == json.loads((ROOT/'resolvent_direct_canonical_admission_20261031/gap_objective_counterexample.json').read_text()), 'gap correction result')
    module_locations = {}
    expected = {
        'clock_response': 'control_effect_clock_20261031/clock_response.py',
        'check_clock_response': 'control_effect_clock_20261031/check_clock_response.py',
        'ordinary_coupled_geometric': 'control_effect_clock_20261031/ordinary_coupled_geometric.py',
        'direct': 'resolvent_direct_canonical_admission_20261031/direct.py',
        'control': 'resolvent_control_reuse_20261031/control.py'}
    for name, path in expected.items():
        actual = Path(sys.modules[name].__file__).resolve()
        need(actual == (ROOT/path).resolve(), 'module outside package: '+name)
        module_locations[name] = path
    need(hash_checks() == (count, frozen_count), 'post-replay hashes')
    import sympy
    return dict(status='PASS_PACKAGE_REPLAY', packaged_files_verified=count, manifest_self_excluded=True,
                original_freeze_entries_verified=frozen_count, clock=result, independent=extra,
                gap_counterexample=counter, packaged_module_locations=module_locations,
                new_simulated_source_calls=result['new_source_calls'], scientific_sources_unchanged=True,
                runtime=dict(python=sys.version.split()[0],sympy=sympy.__version__),
                scope='Byte consistency, receiving and algebra only; actual acquisition remains UNKNOWN.')

if __name__ == '__main__':
    need(sys.argv[1:] in ([], ['--full']), 'usage: python -B verify_package.py [--full]')
    print(json.dumps(run('--full' in sys.argv), indent=2))
