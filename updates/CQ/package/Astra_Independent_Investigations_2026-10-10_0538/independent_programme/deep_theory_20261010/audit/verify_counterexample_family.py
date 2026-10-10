"""Exact stationary-averaging counterexamples. Only standard library needed."""
from fractions import Fraction as F
from pathlib import Path
import json

ROOT=Path(__file__).parent
H=[set() for _ in range(16)]
classes=[list(range(0,4)),list(range(4,7)),list(range(7,11)),list(range(11,15)),[15]]
for i in range(4):
    for u in classes[i]:H[u].update(classes[(i+1)%4])
for u in range(4):H[u].add((u+1)%4)
H[15].update(classes[0])

def second(adj,u):
    return set().union(*(adj[v] for v in adj[u]))-adj[u]-{u}

def reachable(adj,start):
    seen={start};todo=[start]
    while todo:
        u=todo.pop()
        for v in adj[u]-seen:seen.add(v);todo.append(v)
    return seen

def rho_values(q):
    D=256*q**3+240*q**2+84*q+13
    return [F((2*q+1)*(16*q*q+9*q+2),2*D),
            F(64*q**3+60*q*q+23*q+4,4*D),
            F(256*q**3+224*q*q+73*q+12,16*D),
            F((8*q+3)*(128*q**3+104*q*q+31*q+4),16*(4*q+1)*D),
            F(q,4*(4*q+1))]

def verify(q):
    t=3*q+1;n=16*t;r=16*q+4
    adj=[set() for _ in range(n)]
    rho=[F(0)]*16
    for c,value in zip(classes,rho_values(q)):
        for u in c:rho[u]=value
    assert sum(rho)==1
    for i in range(t):
        for u in range(16):
            v=16*i+u
            adj[v].update(16*i+x for x in H[u])
            for jump in range(1,q+1):
                adj[v].update(16*((i+jump)%t)+x for x in range(16))
    assert all(len(row)==r for row in adj)
    assert all(u not in adj[u] for u in range(n))
    assert all(u not in adj[v] for u in range(n) for v in adj[u])
    assert all(u not in adj[w] for u in range(n) for v in adj[u] for w in adj[v])
    reverse=[set() for _ in range(n)]
    for u in range(n):
        for v in adj[u]:reverse[v].add(u)
    assert len(reachable(adj,0))==n and len(reachable(reverse,0))==n
    pi=[rho[u%16]/t for u in range(n)]
    assert min(pi)>0 and sum(pi)==1
    assert all(sum(pi[u] for u in reverse[v])==r*pi[v] for v in range(n))
    s=[len(second(adj,u)) for u in range(n)]
    din=[len(row) for row in reverse]
    assert all(s[u]==16*q+len(second(H,u%16)) for u in range(n))
    Es=sum(pi[u]*s[u] for u in range(n));Ed=sum(pi[u]*din[u] for u in range(n))
    D=256*q**3+240*q**2+84*q+13
    sg=-F((2*q-1)*(16*q*q+11*q+2),2*D)
    dg=F(576*q**3+524*q*q+163*q+20,4*(4*q+1)*D)
    jg=-F(256*q**4-464*q**3-568*q*q-193*q-24,4*(4*q+1)*D)
    assert Es-r==sg and Ed-r==dg and Es+Ed-2*r==jg
    rec={'q':q,'n':n,'r':r,'second_gap':str(sg),'indegree_gap':str(dg),'joint_gap':str(jg),
         'rho_per_vertex_by_class':dict(zip(['A','B','C','D','U'],map(str,rho_values(q)))),
         'verified_exactly':['loopless','no digons','no directed triangles','strongly connected','r-outregular','positive normalized stationary distribution','all second-neighborhood counts','second, indegree and joint expectations'],
         'adjacency_list':[sorted(row) for row in adj],'pi_exact':list(map(str,pi)),'second_sizes':s,'indegrees':din}
    json.dump(rec,open(ROOT/f'counterexample_q{q}_n{n}_r{r}.json','w'),indent=2)
    print({key:rec[key] for key in ['q','n','r','second_gap','indegree_gap','joint_gap']})
    return rec

if __name__=='__main__':
    assert all(len(x)==4 for x in H)
    assert [len(second(H,u)) for u in range(16)]==[5]*4+[4]*7+[3]*5
    results=[verify(q) for q in [1,2,3,4,5]]
    assert F(results[0]['second_gap'])<0
    assert F(results[0]['joint_gap'])>0 and F(results[1]['joint_gap'])>0
    assert all(F(x['joint_gap'])<0 for x in results[2:])
    print('All exact checks passed.')
