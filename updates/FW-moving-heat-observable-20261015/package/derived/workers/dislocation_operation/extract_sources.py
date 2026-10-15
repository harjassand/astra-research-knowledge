#!/usr/bin/env python3
"""Create searchable internal transcriptions; figures remain authoritative."""
from html.parser import HTMLParser
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.out = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'annotation', 'annotation-xml'):
            self.skip += 1
        if not self.skip and tag in ('p', 'h1', 'h2', 'h3', 'h4', 'figcaption', 'tr', 'li'):
            self.out.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'annotation', 'annotation-xml'):
            self.skip = max(0, self.skip - 1)
        if not self.skip and tag in ('p', 'h1', 'h2', 'h3', 'h4', 'figcaption', 'tr', 'li'):
            self.out.append('\n')

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


for path in (ROOT / 'sources').glob('*.html'):
    parser = TextParser()
    parser.feed(path.read_text())
    lines = [' '.join(line.split()) for line in ''.join(parser.out).splitlines()]
    path.with_suffix('.txt').write_text('\n'.join(line for line in lines if line) + '\n')

for path in (ROOT / 'sources').glob('*.pdf'):
    reader = PdfReader(path)
    pages = [f'\nPDF PAGE {i+1}\n' + (page.extract_text() or '') for i, page in enumerate(reader.pages)]
    path.with_suffix('.txt').write_text(''.join(pages))
    print(f'{path.name}: {len(reader.pages)} pages')
