from pathlib import Path
from urllib.request import urlopen
from html.parser import HTMLParser
p=Path(__file__).resolve().parent
sources={
'quantumness_2104':'https://arxiv.org/html/2104.09095v1',
'fidelities_1408':'https://arxiv.org/html/1408.3462v1',
'LAN_0606':'https://arxiv.org/html/quant-ph/0606213v2',
'multivariate_2404':'https://arxiv.org/html/2404.16101v3',
'approx_broadcast_1608':'https://arxiv.org/html/1608.07569v2',
'accessible_1710':'https://arxiv.org/html/1710.01599v1',
'fc_9601':'https://arxiv.org/html/quant-ph/9601020v1',
}
class Extract(HTMLParser):
 def __init__(self): super().__init__(); self.s=[]
 def handle_data(self,x): self.s.append(x)
for name,url in sources.items():
 try:
  raw=urlopen(url,timeout=30).read().decode()
  (p/(name+'.html')).write_text(raw)
  e=Extract();e.feed(raw)
  (p/(name+'.txt')).write_text('\n'.join(e.s))
  print(name,len(raw))
 except Exception as ex: print(name,type(ex).__name__,str(ex))
