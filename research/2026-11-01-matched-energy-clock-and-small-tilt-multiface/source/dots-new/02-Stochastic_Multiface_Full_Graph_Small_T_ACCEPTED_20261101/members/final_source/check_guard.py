from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import multiface as M,receive_certificate as R
from certificate_guard import guard_tree
root=Path(__file__).resolve().parent;checks=0
original=R.certificate
def forbidden(*a,**kw):raise AssertionError('malformed tree reached producer')
R.certificate=forbidden
bad=[];deep={}
for _ in range(1100):deep={'child':deep}
bad.append(deep)
x={};x['cycle']=x;bad.append(x);x=[];x.append(x);bad.append({'cycle':x});x=[];bad.append({'a':x,'b':x})
bad.extend([{1:'bad'},{'leaf':object()},{'wide':[0]*100001}])
for x in bad:
 try:R.receive([],x)
 except M.BudgetRefusal:checks+=1
 else:raise AssertionError('malformed tree admitted')
for x in [None,[],True]:assert R.receive([],x) is False;checks+=1
R.certificate=original
for depth in [0,1,10,63,64]:
 x=0
 for _ in range(depth):x=[x]
 guard_tree(x);checks+=1
for depth in [65,128]:
 x=0
 for _ in range(depth):x=[x]
 try:guard_tree(x)
 except M.BudgetRefusal:checks+=1
 else:raise AssertionError('depth guard')
assert guard_tree([0,0,0],max_nodes=4)['maximum_pending_nodes']==3;checks+=1
for x in [[[0,0],[0,0]],{'a':[0,0],'b':[0,0]}]:
 try:guard_tree(x,max_nodes=6)
 except M.BudgetRefusal:checks+=1
 else:raise AssertionError('pending preallocation guard')
raw=M.fixture();c=R.certificate(raw);assert R.receive(raw,c);checks+=1
cyclic={'op':'mul'};cyclic['args']=[cyclic]
try:R.evaluate_expression(cyclic)
except M.BudgetRefusal:checks+=1
else:raise AssertionError('expression cycle guard')
shared={'op':'pow','base':2,'exponent':1}
try:R.evaluate_expression({'op':'mul','args':[shared,shared]})
except M.BudgetRefusal:checks+=1
else:raise AssertionError('expression alias guard')
for md,mn in [(True,100),(-1,100),(1,False),(1,0),(F(2),100)]:
 try:guard_tree(c,md,mn)
 except ValueError:checks+=1
 else:raise AssertionError('guard budget domain')
result=dict(status='PASS_SAME_AUTHOR_BOUNDED_TREE_AND_EXACT_TYPE_RECEIVING',checks=checks,actual_certificate_guard=guard_tree(c),bindings={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['certificate_guard.py','receive_certificate.py','check_guard.py']})
(root/'guard_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
