from pathlib import Path
from html.parser import HTMLParser
import concurrent.futures
import subprocess
import sys
import urllib.request


ROOT = Path(__file__).resolve().parent


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out, self.skip, self.math = [], 0, 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        elif tag == 'math':
            self.math += 1
            if self.math == 1:
                self.out.append(' $' + dict(attrs).get('alttext', '') + '$ ')
        elif tag in ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'section', 'li', 'tr'):
            self.out.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip -= 1
        elif tag == 'math':
            self.math -= 1
        elif tag in ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'section', 'li', 'tr'):
            self.out.append('\n')

    def handle_data(self, data):
        if not self.skip and not self.math:
            self.out.append(data)


def parse_html(data):
    parser = TextParser()
    parser.feed(data.decode())
    return '\n'.join(line.strip() for line in ''.join(parser.out).splitlines() if line.strip()) + '\n'


def fetch(identifier):
    stem = identifier.replace('/', '_')
    errors = []
    for kind in ('html', 'pdf'):
        try:
            url = 'https://arxiv.org/' + kind + '/' + identifier
            request = urllib.request.Request(url, headers={'User-Agent': 'ResearchAudit/1.0'})
            data = urllib.request.urlopen(request, timeout=40).read()
            if kind == 'html':
                if b'ltx_document' not in data:
                    continue
                (ROOT / (stem + '.html')).write_bytes(data)
                (ROOT / (stem + '.txt')).write_text(parse_html(data))
            else:
                if not data.startswith(b'%PDF'):
                    continue
                pdf = ROOT / (stem + '.pdf')
                pdf.write_bytes(data)
                subprocess.run(['pdftotext', '-layout', str(pdf), str(ROOT / (stem + '.txt'))], check=True)
            return {'id': identifier, 'format': kind, 'bytes': len(data)}
        except Exception as exc:
            errors.append(str(exc))
    return {'id': identifier, 'error': errors}


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for result in executor.map(fetch, sys.argv[1:]):
            print(result)
