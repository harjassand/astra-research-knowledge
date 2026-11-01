#!/usr/bin/env python3
"""Preserve primary HTML and plain-text access copies, with byte receipts."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request,urlopen
import hashlib,json
P=Path(__file__).resolve().parent
class Text(HTMLParser):
 def __init__(self): super().__init__();self.out=[];self.hide=0
 def handle_starttag(self,t,a):
  if t in ('script','style'): self.hide+=1
  if t in ('p','section','div','h1','h2','h3','h4','li','tr','br'): self.out.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'):self.hide-=1
  if t in ('p','section','div','h1','h2','h3','h4','li','tr'):self.out.append('\n')
 def handle_data(self,d):
  if not self.hide:self.out.append(d)
def extract(p,out):
 parser=Text();parser.feed(p.read_text());out.write_text(''.join(parser.out))
if __name__=='__main__':
 p=P/'sources'/'2609.18757v1.html'
 if not p.exists():p.write_bytes(urlopen(Request('https://arxiv.org/html/2609.18757v1',headers={'User-Agent':'research primary-source retrieval'}),timeout=45).read())
 extract(p,p.with_suffix('.txt'))
 q=P.parent/'sources'/'2610.29372v1.html'
 extract(q,P/'sources'/'2610.29372v1.txt')
 for f in [p,q]:print(f.name,len(f.read_bytes()),hashlib.sha256(f.read_bytes()).hexdigest())
