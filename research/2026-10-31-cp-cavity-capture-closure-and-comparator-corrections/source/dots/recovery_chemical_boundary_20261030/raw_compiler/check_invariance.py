"""Regression/falsification checks; not mathematical soundness proof."""
import copy,json,random
from fractions import Fraction
from acquire import acquire,full_network
rng=random.Random(20261030)
out=[]
for trial in range(6):
    net=copy.deepcopy(full_network(True))
    old=net['species'][:];new=[f'S{trial}_{j}' for j in range(len(old))];rng.shuffle(new);ren=dict(zip(old,new))
    net['species']=[ren[x] for x in old];rng.shuffle(net['species'])
    for r in net['reactions']:
        r['source']={ren[k]:v for k,v in r['source'].items()};r['target']={ren[k]:v for k,v in r['target'].items()}
        r['rate']=str(Fraction(rng.randint(1,7),rng.randint(1,5)))
    rng.shuffle(net['reactions']);ans=acquire(net)
    assert ans['status']=='CERTIFICATE_FOUND',ans
    pools={frozenset(p) for p in ans['pool_certificate']['pool_species']}
    expected={frozenset([ren['A']]),frozenset([ren['C']]),frozenset([ren['E'],ren['D']])}
    assert pools==expected
    assert ans['pivot']==ren['D'] and ans['connector']['A']==ren['A'] and ans['connector']['B']==ren['B']
    out.append(dict(trial=trial,status=ans['status'],L=ans['pool_certificate']['L'],trace_constant=ans['trace_certificate']['trace_total']))
print(json.dumps(out,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(out,indent=2)+'\n')
