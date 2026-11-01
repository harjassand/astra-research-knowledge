from copy import deepcopy
from pathlib import Path
import json
import receive_clock as c
checks=0
# Prove malformed proof trees fail before any expensive raw/scalar receiving.
original=c.certify
def forbidden(*args,**kwargs):raise AssertionError('malformed certificate reached expensive producer')
c.certify=forbidden
bad=[]
x={}
for _ in range(1100):x={'child':x}
bad.append(x)
x={};x['cycle']=x;bad.append(x)
a=[];bad.append({'left':a,'right':a})
bad.extend([{1:'bad key'},{'leaf':object()},{'large':[0]*100001},None,[],True])
for cert in bad:
 try:c.verify({},cert)
 except c.Unknown:checks+=1
 else:raise AssertionError('malformed proof admitted')
c.certify=original
# Exact depth boundary and ignored diagnostics are intentional.
for depth in [0,1,10,63,64]:
 x=0
 for _ in range(depth):x=[x]
 c.guard_certificate_tree(x);checks+=1
for depth in [65,128]:
 x=0
 for _ in range(depth):x=[x]
 try:c.guard_certificate_tree(x)
 except c.Unknown:checks+=1
 else:raise AssertionError('depth budget omitted')
x={};x['cycle']=x;c.guard_certificate_tree({'work':x,'display':x,'seconds':x});checks+=1
raw=json.loads(Path('small_raw_fixture.json').read_text());cert=json.loads(Path('small_certificate.json').read_text())
assert c.verify(raw,cert,**c.external_from_record(cert))['status']=='PASS';checks+=1
out={'status':'PASS','checks':checks,'scope':'iterative malformed-proof receiving and one actual small replay; no source numerical formula changed'}
Path('bounded_tree_check_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
