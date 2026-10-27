"""Read only actual public copies. Original provenance paths are never opened."""
from pathlib import Path
import ast
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent

def verify():
    record = json.loads((BASE / 'PUBLIC_SOURCE_CORRESPONDENCE.json').read_text())
    copies = record['public_derivatives']
    assert len(copies) == 14
    markers = (b'/' + b'Users' + b'/', b'file' + b':/' + b'/')
    for item in copies:
        original = Path(item['original_path'])  # Lexical identity only.
        assert not original.is_absolute() and '..' not in original.parts
        assert len(item['original_sha256']) == 64
        path = ROOT / item['path']
        data = path.read_bytes()
        assert len(data) == item['bytes']
        assert hashlib.sha256(data).hexdigest() == item['sha256']
        assert not any(marker in data for marker in markers), item['path']
        if path.suffix == '.py':
            text = data.decode()
            ast.parse(text)
            assert '.write_text(' not in text and '.write_bytes(' not in text
            assert ".open('x'" in text
    method = ROOT / 'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-method-tranche-originals'
    rows = json.loads((method / 'source/selected/pilot_numeric_records_public.json').read_text())['records']
    assert len(rows) == 12
    for row in rows:
        assert len(row['tools_observed']) == 1
        assert row['tools_observed'][0]['input'].startswith('[Original local tool-input string omitted')
    hopping = ROOT / 'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-28-conditional-hopping-and-heat-obstruction/source/originals'
    required = [hopping / 'principal/EXACT_HEAT_SEPARATOR.json',
                hopping / 'transport/CENTRAL_HOPPING_NORM_BOUNDS.json',
                ROOT / 'updates/EX/package/frontier_residual/recovered/astra_frontier_residual_response/results/fresh/witness.json',
                ROOT / 'updates/EX/package/frontier_residual/recovered/astra_frontier_residual_response/results/anchors/V1half.npz']
    assert all(path.is_file() for path in required)
    return {'passed': True, 'explicit_public_derivatives': 14,
            'excluded_unneeded_manifests': 2,
            'numeric_rows_with_explicit_tool_input_omission': 12,
            'private_originals_opened': 0,
            'scientific_programs_executed': 0,
            'scope': 'Public-copy bytes, literal local-locator omission, numeric metadata shape, static syntax/exclusive outputs and public input presence only. Not a comprehensive privacy/secret audit, numerical replay or proof re-audit. Earlier public commits may remain reachable.'}

if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
