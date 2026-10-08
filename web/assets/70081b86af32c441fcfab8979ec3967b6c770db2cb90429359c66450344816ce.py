import itertools,json,sys
from exact_gate_trace import trace_word
A=[(0,1),(0,2),(1,2)]
B=[(0,3),(0,4),(3,4)]
edge=A+B
out=[]
for perm in itertools.permutations(range(6)):
    es=[edge[i] for i in perm]
    tr=trace_word(5,es,'cccccc')
    if tr!=2:out.append({'permutation':perm,'trace':tr,'factor_prediction':2})
print('all-C permutations mismatching',len(out))
print(json.dumps(out[:10],indent=2))
# Fix a maximally interleaved order and exhaust all three-type coefficients.
p=(0,3,1,4,2,5)
es=[edge[i] for i in p]
mismatch=[]
for ts in itertools.product('acd',repeat=6):
    ta=[ts[p.index(i)] for i in range(3)]
    tb=[ts[p.index(i)] for i in range(3,6)]
    zA=trace_word(3,[(0,1),(0,2),(1,2)],ta)
    zB=trace_word(3,[(0,1),(0,2),(1,2)],tb)
    pr=zA*zB//2
    tr=trace_word(5,es,ts)
    if pr!=tr:mismatch.append({'word':''.join(ts),'trace':tr,'factor_prediction':pr,'A_word':''.join(ta),'B_word':''.join(tb)})
print('interleaved mismatch',len(mismatch))
print(json.dumps(mismatch[:20],indent=2))
with open('work/agents/epr_matroid_gluing/results/cactus_gluing.json','w') as f:json.dump({'all_c_counterexamples':out,'interleaved_order':p,'interleaved_coefficients_mismatch':mismatch},f,indent=2)
