"""Cache named primary sources read during Cycle04; read-only network GETs."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from datetime import datetime, timezone
import hashlib
import json

BASE = Path(__file__).resolve().parent
SOURCE = [
 ('hsr_2003.html', 'https://arxiv.org/html/quant-ph/0302031v2'),
 ('jencova_2016.html', 'https://arxiv.org/html/1601.06370v1'),
 ('monras_2010.html', 'https://arxiv.org/html/1002.2337v2'),
 ('spekkens_2008.html', 'https://arxiv.org/html/0805.1463v2'),
 ('jokinen_2024.html', 'https://arxiv.org/html/2406.07305v1'),
 ('jain_QStateGen.pdf', 'https://www.cse.cuhk.edu.hk/~syzhang/papers/QStateGen.pdf'),
 ('braun_eccc_2013_rev5.pdf', 'https://eccc.weizmann.ac.il/report/2013/056/revision/5/download/'),
 ('braun_jain_lee_pokutta_eccc158_rev2.pdf', 'https://eccc.weizmann.ac.il/report/2013/158/revision/2/download/'),
]


def acquire(item):
    name, url = item
    rec = {'path': str(BASE/'primary'/name), 'url': url,
           'retrieved_UTC': datetime.now(timezone.utc).isoformat()}
    try:
        if (BASE/'primary'/name).exists() and (BASE/'primary_cache_manifest.json').exists():
            old = json.loads((BASE/'primary_cache_manifest.json').read_text())['retrievals']
            for previous in old:
                if previous['path'] == rec['path'] and previous['url'] == url and previous['status'] == 'cached':
                    data = (BASE/'primary'/name).read_bytes()
                    if hashlib.sha256(data).hexdigest() == previous['sha256']:
                        return previous
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=30) as response:
            data = response.read()
            rec['final_url'] = response.geturl()
            rec['content_type'] = response.headers.get('Content-Type')
        (BASE/'primary'/name).write_bytes(data)
        rec.update(status='cached', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        if name.endswith('.pdf'):
            from pypdf import PdfReader
            reader = PdfReader(BASE/'primary'/name)
            text = '\n'.join(f'PAGE {i+1}\n'+page.extract_text() for i, page in enumerate(reader.pages))
            (BASE/'primary'/name.replace('.pdf','.txt')).write_text(text)
            rec['pages'] = len(reader.pages)
    except Exception as exc:
        rec.update(status='CACHE_FAILED_WEB_INSPECTION_RETAINED', error=repr(exc))
    return rec


def main():
    (BASE/'primary').mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as executor:
        acquired = list(executor.map(acquire, SOURCE))
    manifest = {'retrievals': acquired,
                'limitations': 'Snapshots and hashes do not certify proof or priority.'}
    (BASE/'primary_cache_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps([{'name':Path(r['path']).name, 'status':r['status'], 'bytes':r.get('bytes')}
                      for r in acquired]))


if __name__ == '__main__':
    main()
