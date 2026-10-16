"""Read-only primary-source acquisition; downloaded material stays excluded."""
import concurrent.futures, datetime, hashlib, json, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / 'acquired_excluded_from_publication'
OUT.mkdir(parents=True, exist_ok=True)
SOURCES = {
 'gw2007.pdf': 'https://cs.uwaterloo.ca/~watrous/Papers/GeneralTheoryQuantumGames.pdf',
 'gutoski2010.pdf': 'https://arxiv.org/pdf/1008.4636',
 'watrous2013.pdf': 'https://cs.uwaterloo.ca/~watrous/Papers/SimplerSDPforCBnorm.pdf',
 'agp2006.pdf': 'https://arxiv.org/pdf/quant-ph/0504218',
 'terhal_burkard2005.pdf': 'https://arxiv.org/pdf/quant-ph/0402104',
 'ng_lidar_preskill2011.pdf': 'https://preskill.caltech.edu/pubs/preskill-2011-dynamical-decoupling.pdf',
 'cleve_query2009.pdf': 'https://arxiv.org/pdf/0811.4428',
 'berry_fractional2014.pdf': 'https://arxiv.org/pdf/1312.1414',
 'pr107.json': 'https://api.github.com/repos/harjassand/astra-research-knowledge/pulls/107',
 'pr106.json': 'https://api.github.com/repos/harjassand/astra-research-knowledge/pulls/106',
 'pr95.json': 'https://api.github.com/repos/harjassand/astra-research-knowledge/pulls/95',
 'openai_math_repository.json': 'https://api.github.com/repos/openai/math',
 'openai_math_head.json': 'https://api.github.com/repos/openai/math/commits/main',
}

def fetch(item):
    name, url = item
    req = urllib.request.Request(url, headers={'User-Agent':'Astra-primary-proof-audit/1.0', 'Accept':'application/vnd.github+json' if name.endswith('.json') else '*/*'})
    began = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
            final_url = response.url
        (OUT / name).write_bytes(data)
        entry = {'name':name, 'url':url, 'final_url':final_url, 'retrieved_utc':began, 'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest(), 'status':'acquired'}
        if name.endswith('.pdf'):
            import pypdf
            doc = pypdf.PdfReader(OUT / name)
            txt = '\n\n'.join('=== PDF PAGE %d ===\n%s' % (i+1, p.extract_text()) for i,p in enumerate(doc.pages))
            (OUT / name.replace('.pdf','.txt')).write_text(txt)
            entry['pages'] = len(doc.pages)
        return entry
    except Exception as err:
        return {'name':name, 'url':url, 'retrieved_utc':began, 'status':'failed', 'error':str(err)}

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        entries = list(pool.map(fetch, SOURCES.items()))
    (ROOT / 'PRIMARY_ACQUISITION.json').write_text(json.dumps(entries, indent=2)+'\n')
    print(json.dumps([{k:v for k,v in e.items() if k in ('name','status','bytes','pages','error')} for e in entries], indent=2))
