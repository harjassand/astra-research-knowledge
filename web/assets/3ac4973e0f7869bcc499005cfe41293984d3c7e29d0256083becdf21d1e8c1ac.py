import itertools,json

def make_dag(a,c,d):
    n=len(a);s=('p',0,0);t=('p',n,0)
    vertices=[s]+[('p',i,p) for i in range(1,n) for p in (0,1)]+[t]
    arcs={}
    for i in range(n):
        for p in (0,1):
            x=('p',i,p)
            if x not in vertices:continue
            for q,w in [(p,a[i]+c[i]),(1-p,a[i]+d[i])]:
                y=('p',i+1,q)
                if y in vertices:arcs[x,y]=w
    if n%2==0:
        branch=[s]+[('q',i) for i in range(1,n)]+[t]
        vertices +=branch[1:-1]
        for i in range(n):arcs[branch[i],branch[i+1]]=c[i]+d[i]
    return vertices,arcs,s,t

def weighted_matching_sum(V,arcs,s,t):
    rows=[x for x in V if x!=t];cols=[x for x in V if x!=s]
    opts={x:[(y,w) for (z,y),w in arcs.items() if z==x and y in cols] for x in rows}
    for x in rows:
        if x in cols:opts[x].append((x,1))
    rows.sort(key=lambda x:len(opts[x]))
    def rec(i,used):
        if i==len(rows):return 1
        return sum(w*rec(i+1,used|{y}) for y,w in opts[rows[i]] if y not in used)
    return rec(0,set())

checks=[]
for n in (3,4,5):
    for offset in range(3):
        a=[(i+offset)%3 for i in range(n)]
        c=[(2*i+offset)%4 for i in range(n)]
        d=[(i+2*offset)%5 for i in range(n)]
        even_sum=sum(__import__('math').prod((a[i]+d[i] if bits[i] else a[i]+c[i]) for i in range(n)) for bits in itertools.product((0,1),repeat=n) if sum(bits)%2==0)
        expected=even_sum+(0 if n%2 else __import__('math').prod(c[i]+d[i] for i in range(n)))
        V,E,s,t=make_dag(a,c,d);actual=weighted_matching_sum(V,E,s,t)
        checks.append({'n':n,'offset':offset,'vertices':len(V),'arcs':len(E),'actual':actual,'expected':expected})
assert all(r['actual']==r['expected'] for r in checks)
print(json.dumps(checks))
with open('work/agents/epr_matroid_gluing/results/dag_common_bases.json','w') as f:json.dump(checks,f,indent=2)
