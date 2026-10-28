"""Independent exact response-equivalent fracture-network construction.

Same local Gamma_e=c_e/2 law, same protected finite host. Scalar Dirichlet
spring model only; neither graph is asserted to be a continuum component.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json,time


def solve(A,b):
    n=len(b);M=[list(row)+[v] for row,v in zip(A,b)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if M[i][j])
        M[j],M[pivot]=M[pivot],M[j];div=M[j][j]
        M[j]=[x/div for x in M[j]]
        for i in range(n):
            if i!=j:
                coeff=M[i][j];M[i]=[x-coeff*y for x,y in zip(M[i],M[j])]
    return [row[-1] for row in M]


HOST=[(0,3,F(1)),(1,4,F(1)),(2,5,F(1))]
NETWORKS={'Y':[(3,6,F(1)),(4,6,F(1)),(5,6,F(1))],
          'Delta':[(3,4,F(1,3)),(4,5,F(1,3)),(5,3,F(1,3))]}


def energy(edges,values):
    # Only nodes connected to the prescribed boundary affect the minimum.
    reachable={0,1,2}
    while True:
        new=reachable|{j for i,j,c in edges if i in reachable}|{i for i,j,c in edges if j in reachable}
        if new==reachable:break
        reachable=new
    free=sorted(reachable-{0,1,2});ix={x:i for i,x in enumerate(free)}
    A=[[F(0)]*len(free) for _ in free];b=[F(0)]*len(free)
    for i,j,c in edges:
        for a,z in [(i,j),(j,i)]:
            if a in ix:
                ai=ix[a];A[ai][ai]+=c
                if z in ix:A[ai][ix[z]]-=c
                else:b[ai]+=c*values[z]
    potential=dict(enumerate(map(F,values)))
    potential.update(zip(free,solve(A,b)))
    return sum((c*(potential.get(i,F(0))-potential.get(j,F(0)))**2/2 for i,j,c in edges),F(0))


def dtn(edges):
    basis=[[F(int(i==j)) for i in range(3)] for j in range(3)]
    e=[energy(edges,x) for x in basis];M=[[F(0)]*3 for _ in range(3)]
    for i in range(3):
        M[i][i]=2*e[i]
        for j in range(i):
            M[i][j]=M[j][i]=energy(edges,[x+y for x,y in zip(basis[i],basis[j])])-e[i]-e[j]
    return M


start=time.monotonic();records={};responses={}
for name,inner in NETWORKS.items():
    full=HOST+inner;initial=energy(full,[1,-1,0]);responses[name]=dtn(full)
    assert initial==F(1,2)
    cases=[]
    for size in range(1,4):
        for damaged in combinations(range(3),size):
            after=energy(HOST+[e for j,e in enumerate(inner) if j not in damaged],[1,-1,0])
            release=initial-after;cost=sum((inner[j][2]/2 for j in damaged),F(0))
            assert release>=0
            cases.append({'damaged_edge_indices':list(damaged),'release_at_unit_t':str(release),
                'fracture_cost':str(cost),'critical_t_squared':str(cost/release) if release else 'INFINITE'})
    first=min(F(x['critical_t_squared']) for x in cases if x['critical_t_squared']!='INFINITE')
    records[name]={'initial_energy_at_t1':str(initial),'all_damage_sets':cases,
                   'first_global_energy_threshold_t_squared':str(first),
                   'globally_stable_at_t1':first>1}
assert responses['Y']==responses['Delta']
assert records['Y']['first_global_energy_threshold_t_squared']=='4/3'
assert records['Delta']['first_global_energy_threshold_t_squared']=='2/3'
out={'status':'EXACT_SAME_FULL_PORT_RESPONSE_DIFFERENT_FINITE_DAMAGE_STABILITY',
 'same_local_fracture_law':'Gamma_e=c_e/2 (unit critical-extension parameter)',
 'same_protected_host':[[i,j,str(c)] for i,j,c in HOST],
 'full_common_initial_DtN':[[str(x) for x in row] for row in responses['Y']],
 'records':records,'seconds':time.monotonic()-start,
 'scope':'Finite interacting scalar spring networks; protected unit host, Dirichlet external drive(t,-t,0), deletion damage. Not 3D continuum fracture, equal hidden material budget or proof of real-component instability.'}
(Path(__file__).parent/'EXACT_NETWORK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))
print(json.dumps({k:{q:v for q,v in rec.items() if q!='all_damage_sets'} for k,rec in records.items()},indent=2))
