#!/usr/bin/env python3
"""Audit exact published PNA source inputs; not a ribosome kinetic simulation.

Run: python stage1_biochemical/audit_pna_sources.py
The original source is preserved untouched. Its small pure functions are loaded
via AST, avoiding author-specific paths and the top-level cryo-EM workflow.
"""
from pathlib import Path
import ast
import hashlib
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'public_code' / 'PNA_50S'
provenance = json.loads((SOURCE / 'PROVENANCE.json').read_text())
checks = []
for item in provenance['files']:
    data = (SOURCE / item['path']).read_bytes()
    digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert digest == item['git_blob_sha1'], item['path']
    checks.append({'path': item['path'], 'bytes': len(data), 'git_blob_sha1': digest})

source_text = (SOURCE / 'all_seg_occ_bi.py').read_text()
tree = ast.parse(source_text)
function_names = {'get_contact_seg', 'get_contact_blocks', 'solve_uull'}
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in function_names]
namespace = {'np': np}
exec(compile(ast.Module(body=functions, type_ignores=[]), str(SOURCE / 'all_seg_occ_bi.py'), 'exec'), namespace)

matrix = pd.read_csv(SOURCE / 'contact_chimerax' / 'contact_matrix.csv', index_col=0)
values = matrix.to_numpy()
assert matrix.index.tolist() == matrix.columns.tolist()
assert values.shape == (158, 158)
assert np.array_equal(values, values.T)
assert np.all(values >= 0) and np.all(values == values.astype(int))
assert np.all(np.diag(values) == 1)
edges = []
for i, a in enumerate(matrix.index):
    for b in matrix.index[i + 1:]:
        if values[i, matrix.index.get_loc(b)] > 0:
            edges.append({'a': a, 'b': b, 'contacts': int(matrix.loc[a, b])})
assert len(edges) == 622

targets = ['h1', 'h26', 'h32b', 'h32s', 'h33b', 'h33t', 'h34b', 'h34t', 'h35', 'uL22', 'uL24']
neighborhoods = {
    a: {b: int(matrix.loc[a, b]) for b in matrix.index if b != a and matrix.loc[a, b] > 0}
    for a in targets
}
core = {
    'H2-H4,H24': ['h2', 'h3', 'h4', 'h24'],
    'H18-H20': ['h18', 'h19', 'h20'],
    'H7': ['h7'], 'uL22': ['uL22'], 'uL24': ['uL24']
}
core_contacts = []
for i, a in enumerate(core):
    for b in list(core)[i + 1:]:
        number, contacts = namespace['get_contact_blocks'](matrix, core[a], core[b])
        core_contacts.append({'a': a, 'b': b, 'segment_pairs': number, 'pairs': contacts})

# A discriminating limit of occupancy dependency: identical binary support
# gives the same inferred order under the released quadrant-count operation,
# but leaves residence times arbitrary. These are constructed examples, not data.
occupancy = np.array([[0, 0], [1, 0], [1, 1]])
quadrants = namespace['solve_uull'](occupancy[:, 0], occupancy[:, 1], occupancy[:, 0], occupancy[:, 1], 0, 1)
assert tuple(quadrants) == (0, 1, 1, 0, 1, 1)
models = [
    {'example': 'A', 'forward_rates': [1.0, 1.0], 'mean_completion_time': 2.0},
    {'example': 'B', 'forward_rates': [0.001, 20.0], 'mean_completion_time': 1000.05},
]
for model in models:
    assert np.isclose(sum(1 / k for k in model['forward_rates']), model['mean_completion_time'])

report = {
    'provenance_verified': checks,
    'contact_matrix': {'shape': list(values.shape), 'symmetric': True, 'off_diagonal_edges': len(edges),
                       'interpretation': 'Mature-structure contact counts. Not occupancy probabilities, free energies or rates.'},
    'target_neighborhoods': neighborhoods,
    'early_core_mature_contacts': core_contacts,
    'occupancy_order_nonidentifiability': {'binary_support': occupancy.tolist(), 'quadrant_counts': list(map(int, quadrants)),
                                          'same_support_different_rates': models},
    'reproduction_limits': [
        'The repository does not contain raw_occ.csv, all_seg_occ_bi.csv, tr_all_seg.csv or block_list_ann_2.csv used by the analysis.',
        'The released main script depends on author-specific map/mask directories and is not an end-to-end executable workflow from repository contents alone.',
        'RA20-B-c1 and RA20-B-c2 are explicitly removed before occupancy dependency inference.',
        'Contact generation script currently contains num_mol = 6, while deposited matrix contains 158 segments; regeneration needs original segmentation and session state.',
        'No complete cryo-EM reconstruction or published occupancy dependency graph is claimed as reproduced.'
    ]
}
(ROOT / 'pna_source_audit.json').write_text(json.dumps(report, indent=2) + '\n')
(ROOT / 'mature_contact_edges.json').write_text(json.dumps(edges, indent=2) + '\n')
print(json.dumps({'verified_files': len(checks), 'segments': len(matrix), 'edges': len(edges),
                  'H1_neighbors': neighborhoods['h1'],
                  'occupancy_graph_does_not_identify_timing': True}, indent=2))
