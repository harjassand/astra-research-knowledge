"""Small exact determinant comparator for the width-bounded count compiler."""
from representation_compiler import C,Q,matrix,det,minor
from banded_hard_bcs import count_coefficients,local_masks,recognize_bandwidth
from itertools import combinations
from random import Random
from pathlib import Path
from datetime import datetime,timezone
import json


def encode(x):
    if isinstance(x,C): return x.json()
    if isinstance(x,Q): return str(x)
    if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x


def determinant_table(f):
    """Exponential diagnostic comparator, outside the production interface."""
    n=len(f); table=[]
    for k in range(n//2+1):
        for up in combinations(range(n),k):
            for down in combinations(sorted(set(range(n))-set(up)),k):
                amplitude=det(minor(f,up,down))
                occupations=tuple(1 if i in up else 2 if i in down else 0 for i in range(n))
                table.append((k,occupations,amplitude.abs2()))
    return table


def table_prefix(table,n,mode_constraints=None,site_constraints=None):
    allowed=local_masks(n,mode_constraints,site_constraints); total=[Q(0)]*(n//2+1)
    for k,occupations,weight in table:
        if all(occupations[i] in allowed[i] for i in range(n)): total[k]+=weight
    return total


def run():
    start=datetime.now(timezone.utc).isoformat(); rng=Random(6203)
    fixtures=[]; counters={'matrices':0,'prefix_polynomials':0,'sector_coefficients':0,
                           'determinant_terms':0,'nonbipartite_connected':0}
    for n in range(0,7):
        for width in range(min(2,n-1)+1) if n else (0,):
            f=[[C(rng.randint(-2,2),rng.randint(-1,1))
                if abs(i-j) <= width else C(0) for j in range(n)] for i in range(n)]
            # Keep every distance-1,2 directed edge nonzero in the nonbipartite case.
            if width == 2:
                for i in range(n):
                    for j in range(n):
                        if 0 < abs(i-j) <= 2 and not f[i][j]: f[i][j]=C(1)
            fixtures.append(f)
    # Connected arbitrary-size sequence of triangles, not bounded components.
    n=8
    f=[[C(0) if i == j or abs(i-j) > 2 else C(1 if i < j else Q(1,2),Q((-1)**(i+j),3))
        for j in range(n)] for i in range(n)]
    fixtures.append(f)
    fixture_reports=[]
    for f in fixtures:
        n=len(f); table=determinant_table(f); counters['determinant_terms']+=len(table)
        counters['matrices']+=1
        queries=[({},{}),({}, {i:{1,2} for i in range(n)})]
        if n:
            # Arbitrary occupation-bit restrictions, including zero-support doubles.
            queries.extend([({(0,'U'):1},{}),({(0,'U'):1,(0,'D'):1},{}),
                            ({(n-1,'D'):0},{}),({}, {0:{0}})])
            for length in range(1,min(n,4)+1):
                constraints={(i,spin):rng.randrange(2) for i in range(length) for spin in ('U','D')}
                queries.append((constraints,{}))
        first=None
        for mode,site in queries:
            calculated=count_coefficients(f,mode,site,collect_stats=True)
            expected=table_prefix(table,n,mode,site)
            assert calculated['coefficients'] == expected, (n,mode,site,calculated,expected)
            counters['prefix_polynomials']+=1; counters['sector_coefficients']+=len(expected)
            if first is None: first=calculated
        fixture_reports.append({'n':n,'width':first['width'],'coefficients':first['coefficients'],
                                'stats':first['stats']})
        if n >= 3 and first['width'] == 2: counters['nonbipartite_connected']+=1
    rejection=recognize_bandwidth(matrix([[0,0,0,1],[0,0,0,0],[0,0,0,0],[0,0,0,0]]),2)
    assert rejection['status'] == 'REJECTED_WIDTH' and rejection['widest_nonzero_edge'] == [0,3]
    return {'status':'PASS','start_utc':start,'end_utc':datetime.now(timezone.utc).isoformat(),
            'counters':counters,'fixtures':fixture_reports,'width_rejection':rejection,
            'scope':'exact canonical/prefix count implementation compared with finite determinant enumeration',
            'quantum_circuit_status':'UNIMPLEMENTED','general_parity_status':'UNRESOLVED'}


if __name__ == '__main__':
    result=encode(run()); Path(__file__).with_name('banded_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'counters':result['counters'],
                      'last_fixture':result['fixtures'][-1],'end_utc':result['end_utc']}))
