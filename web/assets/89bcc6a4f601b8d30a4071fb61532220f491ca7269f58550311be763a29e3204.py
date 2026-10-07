"""Read-only worker harvesting; preserve initial hashes and flag modifications."""
import json, hashlib, datetime, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'outputs/round6'
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
prior_path = OUT / 'INITIAL_RECEIPTS.json'
prior = json.loads(prior_path.read_text()) if prior_path.exists() else {'workers': {}}
workers = prior['workers']
for cohort, count in [('s', 3), ('l', 10)]:
    for cluster in range(1, 11):
        for index in range(1, count+1):
            wid = f'c{cluster:02}_{cohort}{index:02}'
            p = ROOT / 'work/cycle6' / wid / 'INITIAL.txt'
            if not p.exists():
                p = OUT / wid / 'INITIAL.txt'
            if not p.exists():
                continue
            raw = p.read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            metadata = p.with_suffix('.json')
            if not metadata.exists():
                alternate = OUT / wid / 'INITIAL.json'
                if alternate.exists():
                    metadata = alternate
            try:
                md = json.loads(metadata.read_text())
            except (FileNotFoundError, json.JSONDecodeError):
                continue
            if wid not in workers:
                workers[wid] = {'first_seen_utc': now, 'path': str(p.relative_to(ROOT)),
                    'metadata_path': str(metadata.relative_to(ROOT)),
                    'sha256': digest, 'bytes': len(raw), 'metadata': md,
                    'cohort': 'sol' if cohort == 's' else 'luna', 'modifications': []}
            elif workers[wid]['sha256'] != digest:
                event = {'observed_utc': now, 'sha256': digest}
                if not workers[wid]['modifications'] or workers[wid]['modifications'][-1]['sha256'] != digest:
                    workers[wid]['modifications'].append(event)
prior['captured_utc'] = now
for wid, record in workers.items():
    source = ROOT / record['path']
    if hashlib.sha256(source.read_bytes()).hexdigest() != record['sha256']:
        continue
    frozen = OUT / 'frozen_initials' / wid
    frozen.mkdir(parents=True, exist_ok=True)
    for ext in ['txt', 'json']:
        src = source.with_suffix('.'+ext)
        if ext == 'json' and record.get('metadata_path'):
            src = ROOT / record['metadata_path']
        dst = frozen / ('INITIAL.'+ext)
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
prior['counts'] = {c: sum(w['cohort'] == c for w in workers.values()) for c in ['sol', 'luna']}
prior_path.write_text(json.dumps(prior, indent=2)+'\n')
summary = {'utc': now, 'initial_counts': prior['counts'],
    'science_starts': len(list((ROOT/'work/cycle6').glob('*/SCIENCE_START.json'))),
    'science_ends': len(list((ROOT/'work/cycle6').glob('*/SCIENCE_END.json'))),
    'modified_initials': [wid for wid, w in workers.items() if w['modifications']],
    'missing_sol_initials': [f'c{c:02}_s{s:02}' for c in range(1,11) for s in range(1,4)
                             if f'c{c:02}_s{s:02}' not in workers]}
(OUT/'PROGRESS.json').write_text(json.dumps(summary, indent=2)+'\n')
print(json.dumps(summary))
