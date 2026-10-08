import itertools,json
EDGES=[(0,1),(1,2),(0,2)]
def action(x,edge,t):
    y=list(x)
    if t=='a': return tuple(y)
    i,j=edge
    y[i],y[j]=y[j],y[i]
    if t=='d':y[i]^=1;y[j]^=1
    return tuple(y)
def trace(types):
    return sum(all(v==u for v,u in zip(x,apply(x,types))) for x in itertools.product((0,1),repeat=3))
def apply(x,types):
    for e,t in zip(EDGES,types):x=action(x,e,t)
    return x
rows=[]
for ts in itertools.product('acd',repeat=3):
    coeff=0
    for bs in ('ccc','cdd','dcd','ddc'):
        if all(t=='a' or t==b for t,b in zip(ts,bs)):coeff+=2
    rows.append({'monomial':''.join(ts),'literal_trace':trace(ts),'proposed_identity':coeff})
print(json.dumps(rows,indent=2))
with open('work/agents/epr_matroid_gluing/results/triangle_coefficients.json','w') as f:json.dump(rows,f,indent=2)
