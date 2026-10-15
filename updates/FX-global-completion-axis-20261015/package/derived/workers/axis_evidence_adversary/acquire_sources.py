#!/usr/bin/env python3
"""Public source-byte retrieval with append-only receipts; no instrument collection."""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

BASE = Path(__file__).resolve().parent

def acquire(item):
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    receipt = {**item, 'retrieved_utc': stamp, 'method': 'urllib.request GET',
               'raw_instrument_data': False}
    req = urllib.request.Request(item['url'], headers={'User-Agent': 'Mozilla/5.0 (research source audit)'})
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            data = response.read()
            receipt.update(status=response.status, final_url=response.url,
                           headers=dict(response.headers.items()))
    except urllib.error.HTTPError as error:
        data = error.read()
        receipt.update(status=error.code, final_url=error.url,
                       headers=dict(error.headers.items()), error=str(error))
    except Exception as error:
        receipt['error'] = repr(error)
        data = b''
    receipt.update(byte_count=len(data), sha256=hashlib.sha256(data).hexdigest())
    ctype = receipt.get('headers', {}).get('Content-Type','').lower()
    ext = '.pdf' if data.startswith(b'%PDF') else '.jpg' if data.startswith(b'\xff\xd8\xff') else '.png' if data.startswith(b'\x89PNG') else '.docx' if data.startswith(b'PK') and 'wordprocessingml' in ctype else '.zip' if data.startswith(b'PK') else '.xml' if data.lstrip().startswith(b'<?xml') else '.html' if b'<html' in data[:1000].lower() or b'<!doctype html' in data[:1000].lower() else '.bin'
    dest = BASE / 'acquired' / (item['id'] + '_' + stamp + ext)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    receipt['local_path'] = str(dest.relative_to(BASE))
    receipt['pdf_magic'] = data.startswith(b'%PDF')
    receipt['successful_transport_response'] = receipt.get('status') == 200 and len(data) > 0
    return receipt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url_json', help='list of id/url/evidence-class objects')
    args = parser.parse_args()
    items = json.loads(Path(args.url_json).read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(acquire, items))
    with (BASE / 'acquisition_receipts.jsonl').open('a') as handle:
        for result in results:
            handle.write(json.dumps(result, sort_keys=True) + '\n')
    for r in results:
        print(json.dumps({k: r.get(k) for k in ['id','status','byte_count','pdf_magic','local_path','error']}))

if __name__ == '__main__':
    main()
