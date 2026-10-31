"""Raw-list disjunction of two proved sufficient certificates; reject means UNKNOWN."""
from fractions import Fraction as F
from pathlib import Path
import sys,json
from pivot_lift import recognize,construct,encode
sys.path.insert(0,str(Path(__file__).parent/'terminal_gap'))
from exact_terminal_gap import compile_cones,verify_certificate,cycle

def compile_raw(species,reactions,t=F(2)):
    n=len(species)
    if not n or len(set(species))!=n:raise ValueError('nonempty distinct species required')
    for u,v,k in reactions:
        if len(u)!=n or len(v)!=n or any(type(z)!=int or z<0 for z in (*u,*v)) or F(k)<=0:
            raise ValueError('nonnegative integer complexes and positive rational rates required')
    pr=recognize(species,reactions)
    if pr['accepted']:
        pc=construct(pr,t)
        return {'accepted':True,'route':'acquired_pivot_star','pivot':species[pr['pivot']],
          'conclusion':'classwise nonexplosion and positive recurrence; all exponential total-count invariant moments',
          'certificate':pc}
    edges=[(tuple(u),tuple(v)) for u,v,k in reactions]
    cert=compile_cones(edges)
    if cert['accepted']:
        assert verify_certificate(edges,cert)
        return {'accepted':True,'route':'acquired_terminal_gap',
          'conclusion':'classwise nonexplosion and positive recurrence; finite invariant mean genuine jump intensity',
          'certificate':cert,'pivot_route_rejection':pr.get('reason')}
    return {'accepted':False,'conclusion':'UNKNOWN: no supplied sufficient certificate found',
      'pivot_route':pr,'terminal_gap_route':cert}

def main():
    core=[((0,0,0),(1,0,0),1),((1,0,0),(0,0,0),1),((2,0,0),(3,0,0),2),((3,0,0),(2,0,0),1),
          ((2,0,0),(1,1,0),1),((1,1,0),(2,0,0),1),((2,0,0),(1,0,1),1),((1,0,1),(2,0,0),1)]
    general=[(s,t,2 if s==(2,0,0) else 1) for s,t in cycle([(0,0,0),(1,1,0),(1,0,1),(0,1,1)])+cycle([(1,0,0),(0,1,0),(0,0,1),(2,0,0)])]
    bad=[((1,0),(2,0),1)]
    a=compile_raw(['A','B','C'],core);b=compile_raw(['A','B','C'],general);c=compile_raw(['A','B'],bad)
    assert a['route']=='acquired_pivot_star' and b['route']=='acquired_terminal_gap' and not c['accepted']
    print(json.dumps({'pivot_example':a,'terminal_example':b,'unknown_example':c},default=encode,indent=2))
if __name__=='__main__':main()
