#!/usr/bin/env python3
"""Package own constructions and selected attributed inputs; no scientific runs.
Default: read-only plan. Build only after the final report is ready: --build.
Scientific files are copied byte-for-byte and never edited by this script.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
import zipfile

ENSEMBLES = [
    'GlobMean_dD_iterations.xlsx',
    'GlobMean_dD_iterations_DasguptaCal.xlsx',
    'GlobMean_dD_iterations_DasguptaCal_noBUDS.xlsx',
    'GlobMean_dD_iterations_OGINSTAARCal.xlsx',
    'GlobMean_dD_iterations_UmezawaCal.xlsx',
    'GlobMean_dD_iterations_UmezawaCal_noBUDS.xlsx',
]
ENSEMBLE_DIR = Path('next_science/observation/dD_GlobMean/') / \
    'Riddell-Young_2025_dD_GlobMean/output'
OWN_EXT = {'.py', '.txt', '.md', '.json', '.csv', '.svg'}
OBS_TEXT = {'INITIAL_CONSTRUCTION.txt', 'TRANSFER_CHALLENGE_AND_REPAIR.txt',
            'execution_log.txt', 'methane_annual.txt', 'methane_growth.txt',
            'methane_monthly.txt'}
OBS2_TEXT = {'CONSTRUCTION_CHECKPOINT.txt', 'SOURCE_AND_RESULT_MANIFEST.txt',
             'WHOLE_CYCLE_RESULT.txt', 'vcet_SI.txt'}
CAT_TEXT = {'POISSON_AND_ACCESS_NOTES.txt', 'THERMAL_COMPETITION_AND_SCOPE.txt',
            'THERMAL_PROJECTION_COMPLETION.txt', 'THERMAL_PROJECTION_THEOREM.txt',
            'calculation_log.txt', 'variational_bound_log.txt'}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def classify(rel: Path):
    """Return category and exclusion reason from the inventoried source tree."""
    p = rel.parts
    name, ext = rel.name, rel.suffix.lower()
    if '__pycache__' in p or ext in {'.pyc', '.pyo'}:
        return None, 'Compiled/interpreter cache; not a scientific source.'
    if not p:
        return None, 'Not a file.'
    if 'primary' in p:
        if ext == '.json' and 'manifest' in name.lower():
            return 'source_url_hash_manifest', None
        return None, 'Downloaded full paper or raw governing-source copy; provenance retained in notes/manifests.'
    if len(p) == 1:
        if ext in OWN_EXT:
            return 'own_report_notes_or_packaging', None
        return None, 'Not a selected root construction.'
    branch = p[0]
    if branch in {'transfer', 'invention'}:
        if ext in OWN_EXT:
            return 'own_construction_code_result_or_negative_result', None
        return None, 'Downloaded/nonselected binary outside explicit measurement inputs.'
    if branch == 'observation':
        if p[1:4] == ('dD_GlobMean', 'Riddell-Young_2025_dD_GlobMean', 'output') and name in ENSEMBLES:
            return 'licensed_archived_methane_ensemble_CC_BY_4', None
        if len(p) == 2:
            if name in {f'isotope_source_{i}.xlsx' for i in range(4, 8)}:
                return 'published_isotope_source_data_CC_BY_4', None
            if ext in {'.py', '.json', '.csv'} or name in OBS_TEXT:
                category = 'NOAA_measurement_snapshot' if name.startswith('methane_') and ext == '.txt' else 'own_observation_analysis_or_provenance'
                return category, None
        return None, 'Full paper, upstream author archive/code or redundant author intermediate; selected inputs retained.'
    if branch == 'observation2':
        if name == 'ja5c15936_si_001.pdf' or name == 'vcet_SI.txt' or (name.startswith('si-') and ext == '.png'):
            return 'official_catalysis_SI_or_render_CC_BY_NC_4', None
        if len(p) == 2 and (ext in {'.py', '.json', '.csv'} or name in OBS2_TEXT):
            return 'own_catalysis_analysis_or_provenance', None
        return None, 'Downloaded paper/full text or nonselected external material.'
    if branch == 'root_construction':
        if p[1] == 'feedback_data':
            if ext == '.json' and 'manifest' in name:
                return 'optional_external_comparator_provenance', None
            return None, 'Optional SKIPPER author code/data; not required by own executable constructions.'
        if p[1] == 'catalysis':
            if ext in {'.py', '.json', '.png', '.svg'} or name in CAT_TEXT or name == 'thermal_competition.pdf':
                category = 'official_catalysis_SI_render_CC_BY_NC_4' if name.startswith('si-') else 'own_root_catalysis_construction_or_figure'
                return category, None
            return None, 'Downloaded paper/full text; governing references retained in own notes and source manifests.'
        if len(p) == 2 and ext in OWN_EXT:
            return 'own_root_construction', None
        return None, 'Not a selected construction or measurement input.'
    return None, 'Outside explicitly selected own constructions and attributed input sets.'


def select(workspace: Path):
    ns = workspace / 'next_science'
    included, excluded = {}, []
    for path in sorted(ns.rglob('*')):
        if not path.is_file():
            continue
        source = path.relative_to(workspace).as_posix()
        if path.is_symlink():
            excluded.append({'source': source, 'reason': 'Symlink excluded; archive contains only regular files.'})
            continue
        category, reason = classify(path.relative_to(ns))
        if category:
            included[source] = (path, category)
        else:
            excluded.append({'source': source, 'bytes': path.stat().st_size, 'reason': reason})
    provenance = json.loads((ns / 'research_provenance.json').read_text())
    prior_expected = {Path(x['path']).name: x for x in provenance['preserved_prior']}
    for name in ('clocked_grid_research.txt', 'clocked_grid_research.zip'):
        candidates = (workspace / name, workspace / 'prior_clocked_grid' / name)
        src = next((p for p in candidates if p.is_file()), None)
        if src is None:
            raise FileNotFoundError(f'Required unchanged prior artifact missing: {name}')
        got = digest(src)
        if got != prior_expected[name]['sha256']:
            raise ValueError(f'Prior artifact SHA256 changed: {name}; refusing to describe it as unchanged.')
        included[f'prior_clocked_grid/{name}'] = (src, 'unchanged_prior_clocked_grid_artifact')
    optional = [workspace / 'research_report.txt',
                workspace / 'output/pdf/autonomous_catalysis_research.pdf']
    for src in optional:
        if src.is_file():
            included[src.relative_to(workspace).as_posix()] = (src, 'final_scientific_report')
    missing_optional = [p.relative_to(workspace).as_posix() for p in optional if not p.is_file()]
    # The root report may instead be stored in next_science; preserve either exact location.
    if (ns / 'research_report.txt').is_file():
        missing_optional = [p for p in missing_optional if p != 'research_report.txt']
    required = [ENSEMBLE_DIR / name for name in ENSEMBLES]
    required += [Path(f'next_science/observation/isotope_source_{i}.xlsx') for i in range(4, 8)]
    required += [Path(f'next_science/observation/methane_{name}.txt') for name in ('annual', 'growth', 'monthly')]
    required += [Path('next_science/PACKAGE_README.txt'), Path('next_science/observation2/ja5c15936_si_001.pdf'),
                 Path('next_science/root_construction/catalysis/full_cycle_evidence.png')]
    for rel in required:
        if rel.as_posix() not in included:
            raise FileNotFoundError(f'Required selected input/construction missing: {rel}')
    return included, excluded, missing_optional

ATTRIBUTIONS = '''THIRD-PARTY MEASUREMENT ATTRIBUTIONS AND REUSE CONDITIONS

1. Benjamin Riddell-Young (2025), Code for "Microbial driver of 2006–2023
CH4 growth indicated by trends in atmospheric deltaD-CH4 and delta13C-CH4".
Zenodo DOI10.5281/zenodo.17238656, https://zenodo.org/records/17238656.
License: CC BY4.0, https://creativecommons.org/licenses/by/4.0/.
Six GlobMean_dD_iterations*.xlsx members were extracted without modification
from Riddell-Young_2025_dD_GlobMean.zip. The upstream record and individual
input SHA256 values are retained in observation/*manifest.json and
observation/dual_isotope_input_hashes.json. Our covariance/GLS CSV and JSON
files are new analyses, not revised measurements or an upstream rerun.

2. Youmi Oh, Lori Bruhwiler, Xin Lan and coauthors (2026), "Isotopic constraints
in methane inversions reveal larger trends in wetland emissions with improved
linkage to terrestrial water storage", Nature Communications,
DOI10.1038/s41467-026-74777-4. Source spreadsheets4–7 are unchanged.
License: CC BY4.0, https://creativecommons.org/licenses/by/4.0/.
Article license notice was verified in the locally retrieved primary article;
its URL/hash and the spreadsheet URLs/hashes are retained in the manifests.
The full article is excluded from this archive.

3. NOAA Global Monitoring Laboratory methane annual, monthly and growth
records. The files retain original public-use/citation headers. Source URLs
and snapshot hashes are in observation/retrieved_manifest.json. Use the
original provider citation in scientific reuse; current live data may change.

4. Chenjia Liang, Jun Yao, Xiaoxia Hou, Liang Li, NingZe Gao, Haoyu Lu, Ruiyao
Zhao, Xiangke Guo, Nianhua Xue, Luming Peng, Xuefeng Guo, Yan Zhu and Weiping
Ding (2026), Supporting Information for "Dynamic Vibration-Coupled Energy
Transfer for Boosting ORR Catalysts in Fuel Cells".
DOI10.1021/jacs.5c15936.s001; ACS Figshare article31199023,
https://acs.figshare.com/articles/journal_contribution/31199023.
License in the official record: CC BY-NC4.0,
https://creativecommons.org/licenses/by-nc/4.0/.
PDF ja5c15936_si_001.pdf is unchanged. vcet_SI.txt is a text extraction;
si-*.png are page renderings. Our digitization/results/plots are derivative
analyses; geometric digitization uncertainty is not author experimental
uncertainty. No endorsement by the authors is implied.

5. Prior clocked-grid TXT/ZIP are preserved unchanged with their original
contents/notices; this package does not alter or replace their reuse terms.

No blanket license is asserted for all archive contents. In particular the
CC BY-NC materials retain their noncommercial condition. Optional SKIPPER
provenance refers to CC BY4.0 data/code but those author files are not bundled.
Raw Astra repository sources are not bundled without an established reuse
license; pinned locations and governing conditions remain in our own notes.
'''


def environment():
    packages = {}
    for name in ('numpy', 'scipy', 'mpmath', 'openpyxl', 'matplotlib', 'Pillow', 'reportlab'):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    return {'python': sys.version, 'platform': platform.platform(), 'packages': packages,
            'scientific_calculations_rerun_during_packaging': False,
            'note': 'Build environment record, not a pinned environment or a promise of identical floating-point output.'}


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def zip_info(name):
    zi = zipfile.ZipInfo(name, date_time=(2026, 11, 4, 0, 0, 0))
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = 0o644 << 16
    return zi


def build(workspace, target, included, excluded, missing_optional):
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=target.stem + '.', suffix='.partial', dir=target.parent)
    os.close(fd)
    hashes, contents = {}, []
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED,
                             compresslevel=6, allowZip64=True) as archive:
            for name, (src, category) in sorted(included.items()):
                before = src.stat()
                sha = hashlib.sha256()
                size = 0
                with src.open('rb') as f, archive.open(zip_info(name), 'w') as dest:
                    for chunk in iter(lambda: f.read(1024 * 1024), b''):
                        dest.write(chunk)
                        sha.update(chunk)
                        size += len(chunk)
                after = src.stat()
                if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                    raise RuntimeError(f'Source changed while packaging: {src}; rerun after work completes.')
                hashes[name] = sha.hexdigest()
                contents.append({'archive_path': name, 'source_relative_path': src.relative_to(workspace).as_posix(),
                                 'bytes': size, 'sha256': hashes[name], 'category': category})
            generated = {
                'README.txt': b'Start with next_science/PACKAGE_README.txt and the final research report.\nVerify MANIFEST.sha256 before rerunning scripts that overwrite saved outputs.\n',
                'THIRD_PARTY_ATTRIBUTIONS.txt': ATTRIBUTIONS.encode('utf-8'),
                'BUILD_ENVIRONMENT.json': json_bytes(environment()),
                'PACKAGE_CONTENTS.json': json_bytes({
                    'package': 'autonomous_catalysis_research',
                    'astra_revision': 'd5ac5437c8f953fc515f931fbcb1ef80b4e96dd7',
                    'scientific_source_files_modified': False,
                    'included_source_files': contents,
                    'excluded_source_files': excluded,
                    'optional_final_outputs_not_present': missing_optional,
                    'hash_scope': 'MANIFEST.sha256 hashes every other ZIP member, including generated metadata; no self-hash.'}),
            }
            for name, data in sorted(generated.items()):
                archive.writestr(zip_info(name), data)
                hashes[name] = hashlib.sha256(data).hexdigest()
            manifest = ''.join(f'{sha}  {name}\n' for name, sha in sorted(hashes.items())).encode('utf-8')
            archive.writestr(zip_info('MANIFEST.sha256'), manifest)
        os.replace(temporary, target)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise
    archive_sha = digest(target)
    target.with_suffix(target.suffix + '.sha256').write_text(f'{archive_sha}  {target.name}\n')
    print(json.dumps({'archive': str(target), 'bytes': target.stat().st_size,
                      'sha256': archive_sha, 'source_files': len(contents),
                      'archive_members': len(contents) + 5,
                      'excluded_files': len(excluded),
                      'missing_optional_final_outputs': missing_optional}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--output', type=Path, help='Default: WORKSPACE/output/autonomous_catalysis_research.zip')
    parser.add_argument('--build', action='store_true', help='Build now; use after the final report is ready.')
    parser.add_argument('--require-report', action='store_true', help='Require both final report TXT and final PDF.')
    parser.add_argument('--list', action='store_true', help='Print every selected archive member.')
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    target = args.output.resolve() if args.output else workspace / 'output/autonomous_catalysis_research.zip'
    included, excluded, missing = select(workspace)
    if args.require_report and missing:
        parser.error('Final report outputs missing: ' + ', '.join(missing))
    if args.list:
        for name, (_, category) in sorted(included.items()):
            print(f'{name}\t{category}')
    if args.build:
        build(workspace, target, included, excluded, missing)
    else:
        print(json.dumps({'mode': 'read-only plan; archive not built', 'target': str(target),
                          'selected_files': len(included),
                          'selected_uncompressed_bytes': sum(p.stat().st_size for p, _ in included.values()),
                          'excluded_files': len(excluded),
                          'missing_optional_final_outputs': missing,
                          'next_command_after_report_ready': 'python next_science/package_research.py --build --require-report'}, indent=2))


if __name__ == '__main__':
    main()
