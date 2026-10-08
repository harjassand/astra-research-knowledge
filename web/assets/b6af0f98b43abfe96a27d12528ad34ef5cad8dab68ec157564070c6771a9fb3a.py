import itertools,json,math

from exact_gate_trace import trace_word

def spike_coeff(types):
    n=len(types)
    return 2*sum(all(t=='a' or t==b for t,b in zip(types,bs)) for bs in itertools.product('cd',repeat=n) if bs.count('d')%2==0)
results=[]
for n in range(3,7):
    edges=[(i,i+1) for i in range(n-1)]+[(0,n-1)]
    diffs=[]
    for ts in itertools.product('acd',repeat=n):
        tr=trace_word(n,edges,ts); pred=spike_coeff(ts)
        if tr!=pred:diffs.append({'word':''.join(ts),'actual':tr,'spike':pred})
    result={'n':n,'edges':edges,'differences':diffs}
    results.append(result)
    print(json.dumps(result))
with open('work/agents/epr_matroid_gluing/results/cycle_coefficients.json','w') as f:json.dump(results,f,indent=2)
