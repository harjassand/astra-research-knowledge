import itertools,json
from exact_gate_trace import trace_word
out=[]
for n in (4,5):
    E=[(i,i+1) for i in range(n-1)]+[(0,n-1)]
    errors=[];tested=0
    for p in itertools.permutations(range(n)):
        for ts in itertools.product('cd',repeat=n):
            tested+=1
            tr=trace_word(n,[E[i] for i in p],[ts[i] for i in p])
            expected=2*(ts.count('d')%2==0)+(2 if n%2==0 else 0)
            if tr!=expected:errors.append([p,ts,tr,expected])
    out.append({'n':n,'all_orders':True,'only_c_d':True,'tested':tested,'errors':errors})
print(json.dumps([{**r,'errors':len(r['errors'])} for r in out]))
with open('work/agents/epr_matroid_gluing/results/order_check.json','w') as f:json.dump(out,f,indent=2)
assert all(not r['errors'] for r in out)
