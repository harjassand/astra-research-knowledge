import itertools,json,random
from exact_gate_trace import trace_word

def parity_coefficient(types):
    return sum(all(t=='a' or t==b for t,b in zip(types,bs)) for bs in itertools.product('cd',repeat=len(types)) if bs.count('d')%2==0)

def gf2_rank(cols,n):
    piv={}
    for col in cols:
        while col:
            p=col.bit_length()-1
            if p in piv:col^=piv[p]
            else:piv[p]=col;break
    return len(piv)

checks=[]
for n in range(3,8):
    cols=[1<<i for i in range(n)]+[((1<<n)-1)^(1<<i) for i in range(n)]
    mismatch=[]
    for bs in itertools.product('cd',repeat=n):
        rank=gf2_rank([cols[i+(0 if b=='c' else n)] for i,b in enumerate(bs)],n)
        if (rank==n)!=(bs.count('d')%2==0):mismatch.append(''.join(bs))
    checks.append({'check':'binary_spike_transversals','n':n,'tested':2**n,'mismatches':mismatch})
for n in range(3,7):
    edges=[(i,i+1) for i in range(n-1)]+[(0,n-1)]
    mismatch=[]
    for ts in itertools.product('acd',repeat=n):
        predicted=2*parity_coefficient(ts)+ (2 if n%2==0 and 'a' not in ts else 0)
        actual=trace_word(n,edges,ts)
        if actual!=predicted:mismatch.append([''.join(ts),actual,predicted])
    checks.append({'check':'full_cycle_identity','n':n,'tested':3**n,'mismatches':mismatch})
A=[(0,1),(0,2),(1,2)];B=[(0,3),(0,4),(3,4)]
for p in [(0,1,2,3,4,5),(0,3,1,4,2,5)]:
    edges=[(A+B)[i] for i in p];mismatch=[]
    for ts in itertools.product('acd',repeat=6):
        ta=[ts[p.index(i)] for i in range(3)];tb=[ts[p.index(i)] for i in range(3,6)]
        predicted=2*parity_coefficient(ta)*parity_coefficient(tb)
        actual=trace_word(5,edges,ts)
        if actual!=predicted:mismatch.append([''.join(ts),actual,predicted])
    checks.append({'check':'bowtie_gluing','order':p,'tested':729,'mismatches':mismatch})
# Isolated and bridge-attach coefficient checks (triangle + bridge sharing vertex0).
edges=[(0,1),(0,2),(1,2),(0,3)]
mismatch=[]
for ts in itertools.product('acd',repeat=4):
    predicted=2*parity_coefficient(ts[:3])*(2 if ts[3]=='a' else 1)
    actual=trace_word(4,edges,ts)
    if actual!=predicted:mismatch.append([''.join(ts),actual,predicted])
checks.append({'check':'odd_cycle_bridge_gluing','tested':81,'mismatches':mismatch})
with open('work/agents/epr_matroid_gluing/results/replay.json','w') as f:json.dump(checks,f,indent=2)
for r in checks:print({k:(len(v) if k=='mismatches' else v) for k,v in r.items()})
assert all(not r['mismatches'] for r in checks if r['check']!='bowtie_gluing' or r['order']==(0,1,2,3,4,5))
assert len(checks[-2]['mismatches'])==64
