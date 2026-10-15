#!/usr/bin/env python3
"""Extract saved article text; PDFs retain form-feed page boundaries."""
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess

BASE = Path(__file__).resolve().parent

class Extract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip += 1
        if tag in ('p','div','h1','h2','h3','li','section','tr','figure'): self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip = max(0,self.skip-1)
        if tag in ('p','div','h1','h2','h3','li','section','tr','figure'): self.parts.append('\n')
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)

def main():
    dst = BASE / 'text'
    dst.mkdir(exist_ok=True)
    receipts = [json.loads(line) for line in (BASE / 'acquisition_receipts.jsonl').read_text().splitlines()]
    for r in receipts:
        if r.get('status') != 200: continue
        src = BASE / r['local_path']
        out = dst / (src.stem + '.txt')
        if out.exists(): continue
        if r['pdf_magic']:
            subprocess.run(['/Users/harjas/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin/pdftotext','-layout',str(src),str(out)],check=True)
        elif src.suffix == '.html':
            parser = Extract()
            parser.feed(src.read_text(errors='replace'))
            lines = [' '.join(x.split()) for x in ''.join(parser.parts).splitlines()]
            out.write_text('\n'.join(x for x in lines if x) + '\n')
        print(out.name)

if __name__ == '__main__': main()
