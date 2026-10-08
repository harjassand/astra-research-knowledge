import json
E=[(0,1),(0,3),(0,2),(0,4),(1,2),(3,4)]
def bits(x):return ''.join(str((x>>i)&1) for i in range(5))
def paths(types):
    out=[]
    for start in range(32):
        vec=[(start,[start])]
        for (i,j),t in zip(E,types):
            nxt=[];mask=(1<<i)|(1<<j)
            for x,history in vec:
                b=(x>>i)&1;d=(x>>j)&1
                if t=='c':ys=() if b==d else (x,x^mask)
                elif t=='d':ys=(x if b!=d else x^mask,)
                for y in ys:nxt.append((y,history+[y]))
            vec=nxt
        out +=[[bits(x) for x in h] for y,h in vec if y==start]
    return out
r={w:paths(w) for w in ['cccccc','cccccd']}
print(json.dumps(r,indent=2))
with open('work/agents/epr_matroid_gluing/results/bowtie_paths.json','w') as f:json.dump(r,f,indent=2)
