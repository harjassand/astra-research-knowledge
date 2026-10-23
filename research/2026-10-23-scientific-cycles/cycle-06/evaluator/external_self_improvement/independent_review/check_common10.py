#!/usr/bin/env python3
"""Independent, standard-library reconstruction. Does not import root's analysis.

Only released observations are read. Missing task results remain None. A verified
gain means that the child's lowest compatible score exceeds the parent's highest
compatible score. This is an observation rule, not a probability estimate.
"""
import ast
import collections
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
READ_FILES = set()


def read(path):
    READ_FILES.add(path)
    return path.read_text()


def documents(path):
    """Independent brace lexer for the multiline concatenated JSON documents."""
    s = read(path)
    depth, start, quoted, escape = 0, None, False, False
    for i, char in enumerate(s):
        if quoted:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == '{':
            if depth == 0:
                start = i
            depth += 1
        elif char == '}':
            depth -= 1
            assert depth >= 0
            if depth == 0:
                yield json.loads(s[start:i+1])
                start = None
        elif depth == 0:
            assert char.isspace(), (path, i, char)
    assert depth == 0 and start is None and not quoted


SMALL = json.loads(read(BASE / 'official_repository/swe_bench/subsets/small.json'))
assert len(SMALL) == len(set(SMALL)) == 10


def statuses(meta):
    perf = meta.get('overall_performance') or {}
    good = set(perf.get('total_resolved_ids', []))
    bad = set(perf.get('total_unresolved_ids', []))
    empty = set(perf.get('total_emptypatch_ids', []))
    assert not good.intersection(bad | empty)
    return {task: 1 if task in good else 0 if task in bad | empty else None
            for task in SMALL}


def interval(values):
    known_success = sum(v == 1 for v in values.values())
    return known_success, known_success + sum(v is None for v in values.values())


def summarize(rows):
    complete = [r for r in rows if r['complete']]
    gains = [r for r in rows if r['child_interval'][0] > r['parent_interval'][1]]
    losses = [r for r in rows if r['child_interval'][1] < r['parent_interval'][0]]
    return {
        'attempts': len(rows),
        'native_archive_admissions': sum(r['admitted'] for r in rows),
        'child_performance_metadata_available': sum(r['performance_present'] for r in rows),
        'fully_observed_parent_child_pairs_10': len(complete),
        'verified_improving_children_10': len(gains),
        'definitely_worse_children_10': len(losses),
        'ties_in_complete_pairs_10': sum(r['net'] == 0 for r in complete),
        'no_observed_verified_gain_10': len(rows)-len(gains),
        'unknown_child_outcome_pairs_10': len(rows)-len(complete),
        'new_success_events_complete_pairs_10': sum(len(r['gained_tasks']) for r in complete),
        'lost_success_events_complete_pairs_10': sum(len(r['lost_tasks']) for r in complete),
        'sum_net_success_events_complete_pairs_10': sum(r['net'] for r in complete),
        'complete_gains': sum(r['net'] > 0 for r in complete),
        'complete_losses': sum(r['net'] < 0 for r in complete),
        'verified_partial_gains': [r['child'] for r in gains if not r['complete']],
        'verified_partial_losses': [r['child'] for r in losses if not r['complete']],
    }


results = {}
for name in ['swe_dgm', 'swe_dgm_noselfimprove', 'swe_dgm_nodarwin']:
    directory = BASE / 'released_metadata' / name
    metadata = {p.parent.name: json.loads(read(p))
                for p in sorted(directory.glob('*/metadata.json'))}
    groups = list(documents(directory / 'dgm_metadata.jsonl'))
    ordered_children, rows = [], []
    archive = {'initial'}
    for group in groups:
        pairs = collections.Counter(tuple(x) for x in group['selfimprove_entries'])
        children = group['children']
        assert len(children) == sum(pairs.values())
        actual_pairs = []
        for child in children:
            meta = metadata[child]
            parent = meta['parent_commit']
            assert parent in archive
            actual_pairs.append((parent, meta['entry']))
            a, b = statuses(metadata[parent]), statuses(meta)
            ia, ib = interval(a), interval(b)
            complete = all(x is not None for x in [*a.values(), *b.values()])
            gained = [t for t in SMALL if a[t] == 0 and b[t] == 1]
            lost = [t for t in SMALL if a[t] == 1 and b[t] == 0]
            rows.append({'child': child, 'parent': parent, 'generation': group['generation'],
                'admitted': child in group['children_compiled'],
                'performance_present': bool(meta.get('overall_performance')),
                'parent_interval': ia, 'child_interval': ib,
                'complete': complete, 'net': ib[0]-ia[0] if complete else None,
                'gained_tasks': gained, 'lost_tasks': lost})
        assert collections.Counter(actual_pairs) == pairs
        ordered_children.extend(children)
        archive.update(group['children_compiled'])
        assert set(group['archive']) == archive
    assert len(ordered_children) == len(set(ordered_children))
    assert set(ordered_children) == set(metadata)-{'initial'}
    results[name] = {'all_attempts': summarize(rows), 'first_80_attempts': summarize(rows[:80]),
                     'rows': rows}

# Root's results are opened only after the independent reconstruction above.
root = json.loads(read(BASE / 'ROOT_LINEAGE_RESULTS.json'))
comparisons = []
for name, run in results.items():
    for which in ['all_attempts', 'first_80_attempts']:
        for key, value in run[which].items():
            if key in root['runs'][name][which]:
                assert value == root['runs'][name][which][key], (name, which, key, value)
                comparisons.append([name, which, key])

# Independent inspection of the released child trace, not the producer summary.
baseline = BASE / 'released_metadata/swe_dgm_noselfimprove'
child = '20250408_005738_095636'
parent = '20250407_212519_184190'
meta = json.loads(read(baseline / child / 'metadata.json'))
assert meta['parent_commit'] == parent
patch = read(baseline / parent / 'model_patch.diff')
assert '+def edit_range_in_file(' in patch
assert '+                    "enum": ["view", "create", "edit", "edit_range"],' in patch
trace = ast.literal_eval(read(baseline / child / 'self_evo.md'))
initial_reads = []
for i, msg in enumerate(trace):
    for part in msg.get('content', []):
        text = part.get('text', '')
        if msg.get('role') == 'user' and "result of running `cat -n` on /dgm/tools/edit.py:" in text:
            initial_reads.append((i, text))
assert initial_reads
i, tool_result = initial_reads[0]
assert 'No partial/line-range edits or partial viewing are supported.' in tool_result
assert '"enum": ["view", "create", "edit"]' in tool_result
assert 'edit_range' not in tool_result
source = read(BASE / 'official_repository/self_improve_step.py')
assert "if run_baseline not in ['no_selfimprove']:" in source
source_constants = [node.value for node in ast.walk(ast.parse(source))
                    if isinstance(node, ast.Constant)]
assert '/dgm/coding_agent.py' in source_constants
assert '--git_dir' in source_constants and '/dgm/' in source_constants
workspace = {
    'child': child, 'declared_parent': parent,
    'parent_patch_adds_edit_range': True,
    'child_first_editor_read_message_index': i,
    'child_editor_read_lacks_parent_feature': True,
    'official_source_skips_parent_patch_application_in_baseline': True,
    'producer_executes_from_target_tree': '/dgm/',
    'scope': 'One actual trace plus released source semantics. No effect-size or all-attempt attribution.'}

bindings = [{'path': str(p.relative_to(BASE)), 'bytes': p.stat().st_size,
             'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(READ_FILES)]
out = {'scope': 'Independent reconstruction of released metadata, no new agent executions.',
       'common_tasks': SMALL, 'runs': results,
       'matching_root_summary_fields': len(comparisons),
       'baseline_workspace_evidence': workspace, 'source_bindings': bindings}
(HERE / 'COMMON10_RESULTS.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({'status': 'PASS', 'matching_root_summary_fields': len(comparisons),
                 'runs': {k: v['all_attempts'] for k, v in results.items()},
                 'baseline_workspace_evidence': workspace}, indent=2))
