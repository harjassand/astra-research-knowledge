"""Bounded exact algebra/support diagnostics; does not run an FPRAS."""
import json
from pathlib import Path
from itertools import combinations, product
from random import Random
from datetime import datetime, timezone
from representation_compiler import (C,Q,matrix,minor,det,inverse,rank,
    strip_diagonal,bipartition,recognize,prefix_support,exhaustive_prefix_norm)


def encode(x):
    if isinstance(x,C): return x.json()
    if isinstance(x,Q): return str(x)
    if isinstance(x,dict): return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x


def run():
    started=datetime.now(timezone.utc).isoformat(); rng=Random(203)
    counters={'jacobi_amplitudes':0,'slater_weights':0,'prefix_supports':0,
              'prefix_norm_identities':0,'inverse_cases':0,'direct_cases':0,
              'strict_nonbipartite_examples':0,'shifted_cases':0}
    fixtures=[]
    for n in (2,4,6):
        for t in range(3 if n < 6 else 2):
            a=n//2
            h=[[C(5+i) if i == j else C(0) for j in range(n)] for i in range(n)]
            for i in range(a):
                for j in range(a,n):
                    h[i][j]=C(rng.randint(-2,2), rng.randint(-1,1))
                    h[j][i]=h[i][j] if t%2 == 0 else C(rng.randint(-2,2),rng.randint(-1,1))
            if not det(h): continue
            f=inverse(h); fixtures.append((f,'inverse'))
            fixtures.append((strip_diagonal(h),'direct'))
    strict_h=matrix([[2,0,1,1],[0,3,1,2],[1,1,5,0],[1,2,0,7]])
    strict_f=inverse(strict_h)
    fixtures.append((strict_f,'inverse'))
    witnesses=[]
    for f,kind in fixtures:
        n=len(f); k=n//2; c=recognize(f,k)
        assert c['status'] == 'COMPILED', (n,kind,c)
        branch=c['branch']; counters['inverse_cases' if branch.startswith('INVERSE') else 'direct_cases']+=1
        original_color,odd=bipartition(strip_diagonal(f))
        if original_color is None:
            counters['strict_nonbipartite_examples']+=1
        h=c['H']; factor=c['scalar']; normf=Q(0); normh=Q(0)
        for up in combinations(range(n),k):
            down=sorted(set(range(n))-set(up))
            af=det(minor(f,up,down)); ah=det(minor(h,up,down))
            assert af == factor*ah
            counters['jacobi_amplitudes']+=1; normf+=af.abs2(); normh+=ah.abs2()
            rows=sorted(x for x in range(2*n) if c['row_spins'][x] == ('U' if c['row_sites'][x] in up else 'D'))
            if len(c['G'][0]) == n:
                assert det([c['G'][x] for x in rows]).abs2() == ah.abs2()
                counters['slater_weights']+=1
        assert normf == c['norm_factor']*normh
        # Every binary prefix through depth 3 and every complete assignment.
        constraints=[{}]
        for length in range(1,min(n,3)+1):
            constraints.extend(dict(enumerate(s)) for s in product('UD',repeat=length))
        constraints.extend(dict(enumerate(s)) for s in product('UD',repeat=n))
        for prefix in constraints:
            exact=exhaustive_prefix_norm(f,prefix)
            exacth=exhaustive_prefix_norm(h,prefix)
            assert exact == c['norm_factor']*exacth
            counters['prefix_norm_identities']+=1
            result=prefix_support(c,prefix)
            assert (result['status'] == 'POSITIVE') == bool(exact), (prefix,result,exact)
            if exact:
                assert all(('U' if i in result['up'] else 'D') == s for i,s in prefix.items())
                assert result['amplitude'] and result['weight'] > 0
            counters['prefix_supports']+=1
        witnesses.append({'n':n,'kind':kind,'branch':branch,'norm':str(normf),
                          'norm_factor':str(c['norm_factor']),'odd_walk':odd})
    # Singular input repaired by a supplied bounded scalar diagonal shift.
    shifted_f=[[x-(strict_f[0][0] if i == j else C(0)) for j,x in enumerate(row)]
               for i,row in enumerate(strict_f)]
    shifted=recognize(shifted_f,2,shifts=(strict_f[0][0],))
    assert shifted['status'] == 'COMPILED'
    for up in combinations(range(4),2):
        down=sorted(set(range(4))-set(up))
        assert det(minor(shifted_f,up,down)) == shifted['scalar']*det(minor(shifted['H'],up,down))
    counters['shifted_cases']+=1
    # Outside full occupancy, the inverse formula can change support.
    low=det(minor(strict_f,[0],[1])); lowh=det(minor(strip_diagonal(strict_h),[0],[1]))
    assert low and not lowh
    boundary={'n':4,'k':1,'up':[0],'down':[1],
              'F_amplitude':low,'H_amplitude':lowh}
    return {'status':'PASS','started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
            'scope':'finite exact identities and deterministic support diagnostics only',
            'counters':counters,'fixtures':witnesses,'strict_fixture':{'H':strict_h,'F':strict_f,
              'norm_F':exhaustive_prefix_norm(strict_f,{}),
              'norm_H':exhaustive_prefix_norm(strip_diagonal(strict_h),{})},
            'non_half_filling_counterexample':boundary}


if __name__ == '__main__':
    result=encode(run())
    Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'counters':result['counters'],
                      'finished_utc':result['finished_utc']}))
