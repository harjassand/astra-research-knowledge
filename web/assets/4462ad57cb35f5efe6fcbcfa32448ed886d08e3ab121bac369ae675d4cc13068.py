from pathlib import Path
import os, json, hashlib, shutil, zipfile, datetime, sys

root = Path(__file__).resolve().parent.parent
name = sys.argv[1]
out = root / 'outputs' / 'research' / name
if out.exists():
    raise SystemExit('Numbered checkpoint already exists; use a new name.')
out.mkdir(parents=True)
excluded_dirs = {'vendor', 'sources', 'source_maps', 'source_text', 'downloads',
        'astra', 'astra_cards', 'astrasources', 'research_notes', '__pycache__', '.cache',
                 '.venv', 'node_modules', 'papers', 'raw'}
extensions = {'.md', '.txt', '.json', '.py', '.jl', '.sage', '.tex', '.csv', '.lean', '.sh', '.log', '.stdout', '.stderr'}
records, ledgers, parse_errors = [], [], []
source_root = root / 'work' / 'agents'
for current, dirs, files in os.walk(source_root):
    dirs[:] = [d for d in dirs if d not in excluded_dirs and not d.startswith('.')
               and not d.startswith('source') and not d.endswith('_source')
               and not d.endswith('_sources')]
    for filename in sorted(files):
        src = Path(current) / filename
        lower = filename.lower()
        if (src.suffix.lower() not in extensions and filename not in ('lean-toolchain', 'lakefile.toml')) or src.stat().st_size > 1_500_000:
            continue
        if any(term in lower for term in ('extracted', 'paper_body', 'fulltext', 'manuscript_text')):
            continue
        if src.suffix == '.tex':
            continue  # Source-body downloads stay in work; written derivations are retained.
        if src.suffix in {'.log', '.stdout', '.stderr'} and not any(term in lower for term in
                ('compile', 'audit', 'build', 'verify', 'axiom', 'assumption')):
            continue
        if src.suffix == '.txt' and not any(term in lower for term in
                ('proof', 'report', 'deriv', 'failure', 'source_log', 'sources',
                 'audit', 'claim', 'result', 'cost', 'gate', 'counterexample',
                 'readme', 'contract', 'model', 'status', 'restart', 'compile',
                 'audit', 'verify', 'axiom', 'build', 'hash', 'fingerprint', 'replay', 'run_output', '_run')):
            continue
        if src.suffix == '.json' and any(term in lower for term in
                ('preprints_tree', 'catalog', 'agent__manifest')):
            continue
        rel = src.relative_to(source_root)
        data = src.read_bytes()
        if src.suffix == '.json' and 'claim' in lower:
            try:
                value = json.loads(data)
            except Exception as error:
                parse_errors.append({'path': str(rel), 'error': str(error)})
                continue
            ledgers.append({'original': str(src.relative_to(root)),
                            'snapshot': 'evidence/' + str(rel), 'ledger': value})
        dst = out / 'evidence' / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        records.append({'original': str(src.relative_to(root)),
                        'snapshot': str(dst.relative_to(out)), 'bytes': len(data),
                        'sha256': hashlib.sha256(data).hexdigest()})
# Authored source ledgers sometimes live beside downloaded bodies. Retain only
# these explicit note filenames from otherwise excluded source directories.
retained_originals = {row['original'] for row in records}
for note_name in ('SOURCES.md', 'SOURCE_NOTES.md', 'NOTES.md', 'PRIOR_ART.md'):
    for src in source_root.rglob(note_name):
        rel = src.relative_to(source_root)
        original = str(src.relative_to(root))
        if original in retained_originals or any(p in rel.parts for p in
                ('node_modules', '.lake', '.venv', 'vendor', '.cache')):
            continue
        data = src.read_bytes()
        if len(data) > 1_500_000:
            continue
        dst = out / 'evidence' / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        records.append({'original': original, 'snapshot': str(dst.relative_to(out)),
                        'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        retained_originals.add(original)
for rel in ('work/ROOT_MANDATE.txt', 'work/CYCLE2_DIRECTIVE.txt', 'work/CYCLE3_DIRECTIVE.txt',
            'work/CYCLE4_5_DIRECTIVE.txt', 'outputs/research/RESEARCH_REPORT.txt',
            'work/CYCLE6_DIRECTIVE.txt',
            'work/CYCLE7_DIRECTIVE.txt',
            'work/CYCLE8_DIRECTIVE.txt',
            'work/CYCLE9_DIRECTIVE.txt',
            'work/CYCLE10_DIRECTIVE.txt',
            'work/CYCLE11_DIRECTIVE.txt',
            'work/CYCLE12_DIRECTIVE.txt',
            'work/ROUND_CLOSURE.txt',
            'work/c12_spin_compiler_root_replay.log',
            'work/close_round.py',
            'work/preserve_checkpoint.py',
            'outputs/research/CYCLE12_PROGRESS.txt',
            'outputs/research/ROUND_CLOSURE.json',
            'outputs/research/CYCLE10_PROGRESS.txt',
            'outputs/research/CYCLE9_PROGRESS.txt',
            'outputs/research/ACTIVE_GATES.json',
            'outputs/research/CURRENT_STATE.txt',
            'outputs/research/PRIOR_MANIFEST.json',
            'outputs/research/ENTRY_PIN_VERIFICATION.json',
            'outputs/research/FRONTIER_REFRESH.json',
            'outputs/research/RECORD_REPAIRS.json'):
    src = root / rel
    if src.exists():
        shutil.copyfile(src, out / src.name)
for filename in ('ROOT_REPLAY_CHECK.json', 'PROGRESS_AUDIT.txt'):
    src = root / 'outputs' / 'research' / filename
    if src.exists():
        shutil.copyfile(src, out / filename)
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
(out / 'CLAIM_LEDGER.json').write_text(json.dumps({
    'scientific_status': 'research stopped at user request after current round; objective unachieved; source/candidate/conditional/finite statuses remain local to each record',
    'snapshot_time_utc': stamp, 'ledgers': ledgers, 'parse_errors': parse_errors
}, indent=2) + '\n')
(out / 'MANIFEST.json').write_text(json.dumps({
    'snapshot_time_utc': stamp, 'retained_files': len(records),
    'policy': 'compact reports, proofs, ledgers, source notes and code; downloaded source/dependency directories excluded',
    'original_root': str(root), 'files': records
}, indent=2) + '\n')
(out / 'START_HERE.txt').write_text('ASTRA RESEARCH CHECKPOINT — USER-REQUESTED STOP\n\n'
    'Read ROUND_CLOSURE.json, CYCLE12_PROGRESS.txt, CURRENT_STATE.txt and ACTIVE_GATES.json, then ROOT_MANDATE.txt and numbered directives through CYCLE12_DIRECTIVE.txt.\n'
    'The objective is not complete and no externally validated breakthrough is asserted.\n'
    'CLAIM_LEDGER.json embeds scoped claim ledgers; MANIFEST.json maps original work paths to snapshot evidence paths.\n'
    'Inspect relevant evidence/<lead>/FINAL_REPORT.md and later cycle/attack files selectively.\n'
    'Some report crosslinks retain original workspace paths; use MANIFEST.json when relocating this archive.\n'
    'Downloaded paper bodies and installed dependencies are excluded. Source-note URLs preserve their retrieval routes.\n'
    'Snapshot integrity is a byte-level property, not proof verification, novelty, nature validation or external review.\n'
    'All live workers were instructed to freeze this round; ROUND_CLOSURE.json records their final inventory. No further cycle is authorized for this run.\n')
bad = []
for row in records:
    data = (out / row['snapshot']).read_bytes()
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        bad.append(row['snapshot'])
if bad or parse_errors:
    raise SystemExit(json.dumps({'hash_errors': bad, 'ledger_errors': parse_errors}))
archive = out.with_suffix('.zip')
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for file in sorted(out.rglob('*')):
        if file.is_file():
            z.write(file, Path(name) / file.relative_to(out))
with zipfile.ZipFile(archive) as z:
    crc_error = z.testzip()
if crc_error:
    raise SystemExit('ZIP CRC error: ' + crc_error)
integrity = {'snapshot': name, 'retained_evidence_files': len(records),
             'claim_ledgers': len(ledgers), 'ledger_parse_errors': len(parse_errors),
             'evidence_sha256_pass': True, 'zip_crc_pass': True,
             'zip_bytes': archive.stat().st_size,
             'zip_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
             'scientific_validation': 'not implied by these checks'}
(out / 'INTEGRITY.json').write_text(json.dumps(integrity, indent=2) + '\n')
print(json.dumps(integrity))
