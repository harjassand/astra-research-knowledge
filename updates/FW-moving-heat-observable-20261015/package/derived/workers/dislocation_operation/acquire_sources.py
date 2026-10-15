#!/usr/bin/env python3
"""Download public primary sources, preserving an acquisition receipt."""
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
SOURCES = {
    'montenegro_2025v2.html': 'https://arxiv.org/html/2506.07908v2',
    'montenegro_geometry_2024v1.html': 'https://arxiv.org/html/2404.16714v1',
    'genlik_2024.html': 'https://arxiv.org/html/2406.13044v1',
    'li_2023_with_SI.pdf': 'https://arxiv.org/pdf/2211.14933',
    'blackston_spectroscopy_2025v1.html': 'https://arxiv.org/html/2510.05357v1',
    'genlik_2025_accepted.pdf': 'https://link.aps.org/accepted/10.1103/PhysRevMaterials.9.054604',
    'vurgaftman_2001.pdf': 'https://ursemiconductors.web.illinois.edu/ECE536/Vurgaftman%282001%29.pdf',
}


def main():
    receipt_path = ROOT / 'source_receipts.json'
    records = json.loads(receipt_path.read_text()) if receipt_path.exists() else []
    for name, url in SOURCES.items():
        path = ROOT / 'sources' / name
        if path.exists():
            continue
        req = urllib.request.Request(url, headers={'User-Agent': 'Astra primary-source research'})
        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                data = response.read()
                record = {
                    'url': url, 'resolved_url': response.url,
                    'content_type': response.headers.get('Content-Type'),
                    'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                    'local_file': str(path.relative_to(ROOT)), 'status': 'downloaded',
                }
            path.write_bytes(data)
        except Exception as exc:
            record = {'url': url, 'local_file': str(path.relative_to(ROOT)),
                      'status': 'failed', 'error': str(exc)}
        records.append(record)
    receipt_path.write_text(json.dumps(records, indent=2) + '\n')
    print(json.dumps(records, indent=2))


if __name__ == '__main__':
    main()
