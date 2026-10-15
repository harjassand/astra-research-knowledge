#!/usr/bin/env python3
"""Archive primary documentation and author-hosted literature landing pages."""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent / 'sources'
SOURCES = {
    'pygt_home.html': 'https://pygt.readthedocs.io/en/latest/',
    'pygt_stats.html': 'https://pygt.readthedocs.io/en/latest/stats.html',
    'pymor_interpolation.html': 'https://docs.pymor.org/latest/tutorial_interpolation.html',
    'osogami_moment_matching.html': 'https://www.cs.cmu.edu/~osogami/code/momentmatching/index.html',
    'antoulas_research.html': 'https://antoulas.rice.edu/research/',
    'rational_interpolation_arxiv.html': 'https://arxiv.org/abs/1409.2140',
    'exponential_action_mims.html': 'https://eprints.maths.manchester.ac.uk/1591/',
    'kinetic_fpt_rsc.html': 'https://pubs.rsc.org/en/content/articlehtml/2024/cp/d3cp04199a',
    'bertsimas_author_publications.html': 'https://www.mit.edu/~dbertsim/papers.html',
}


def acquire(item):
    name, url = item
    receipt = {'url': url, 'fetched_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (research source archival)'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            receipt.update(status=response.status, final_url=response.url, content_type=response.headers.get('Content-Type'))
        (ROOT / name).write_bytes(data)
        receipt.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), file=name)
    except Exception as exc:
        receipt.update(error=repr(exc))
    return name, receipt


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        receipts = dict(pool.map(acquire, SOURCES.items()))
    (ROOT / 'RECEIPTS.json').write_text(json.dumps(receipts, indent=2) + '\n')
    for name, receipt in receipts.items():
        print(name, receipt.get('status', receipt.get('error')), receipt.get('bytes', ''))


if __name__ == '__main__':
    main()
