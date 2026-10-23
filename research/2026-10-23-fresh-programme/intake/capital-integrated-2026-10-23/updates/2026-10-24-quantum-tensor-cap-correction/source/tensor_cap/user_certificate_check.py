"""Source-exposed check of supplied primal/dual tables; no producer imports."""
from fractions import Fraction as F
from itertools import permutations
import json

TABLES = {
2: [('1/4','00','00'),('1/2','00','00 01 10'),
    ('1/4','00','00 01 10 11'),('3/4','01','01'),
    ('1/4','00 01','01 11'),('1/8','01 11','11'),
    ('1/8','00 01 11','11'),('1/2','01 10 11','11')],
3: [('1/5','000','000 001 010 011 100'),
    ('1/20','000','000 001 010 011 101'),
    ('1/30','000','000 001 010 011 100 101'),
    ('4/15','001','001'),('19/60','001','001 011'),
    ('1/10','000 001','001 011 101'),('4/15','011','011'),
    ('3/20','001 011','011'),('1/10','001 010 011','011 111'),
    ('1/3','000 001 010 011','011 111'),
    ('1/30','001 010 111','111'),('1/30','001 010 011 111','111'),
    ('4/15','011 101 111','111')]
}

def subset(s,t): return s & t == s
def permute(s,p): return sum(((s>>i)&1)<<j for i,j in enumerate(p))

def check(n):
    size=1<<n
    cover=[[F(0) for _ in range(size)] for _ in range(size)]
    rows=[F(0)]*size; cols=[F(0)]*size
    for weight,aa,bb in TABLES[n]:
        aa=[int(s,2) for s in aa.split()]; bb=[int(s,2) for s in bb.split()]
        orbit={(tuple(sorted(permute(s,p) for s in aa)),
                tuple(sorted(permute(t,p) for t in bb))) for p in permutations(range(n))}
        for a,b in orbit:
            for s in a: rows[s]+=F(weight)
            for t in b: cols[t]+=F(weight)
            for s in a:
                for t in b: cover[s][t]+=F(weight)
    assert all(cover[s][t]==int(subset(s,t)) for s in range(size) for t in range(size))
    if n==2:
        u=[F(1,4) if s==0 else F(0) for s in range(size)]
        v=[F(1,4) if t.bit_count() in (1,2) else F(0) for t in range(size)]
        y=lambda s,t:F(0) if (s.bit_count(),t.bit_count())==(1,2) else F(1,4)
    else:
        u=[F(1,5) if s==0 else F(1,10) if s.bit_count()==1 else F(0) for s in range(size)]
        v=[F(1,5) if t==7 else F(1,10) if t.bit_count()==2 else F(0) for t in range(size)]
        def y(s,t):
            k,l=s.bit_count(),t.bit_count()
            if (k,l) in {(0,0),(3,3)}:return F(1,5)
            return F(1,10) if (k,l) in {(0,2),(0,3),(1,1),(1,2),(1,3),(2,2)} else F(0)
    assert sum(u)+sum(v)==1
    objective=sum(y(s,t) for s in range(size) for t in range(size) if subset(s,t))
    rectangles=0
    for row_bits in range(1,1<<size):
        a=[s for s in range(size) if row_bits>>s&1]
        possible=[t for t in range(size) if all(subset(s,t) for s in a)]
        for mask in range(1,1<<len(possible)):
            b=[t for j,t in enumerate(possible) if mask>>j&1]
            assert sum(y(s,t) for s in a for t in b)<=sum(u[s] for s in a)+sum(v[t] for t in b)
            rectangles+=1
    primal=max(rows+cols)
    assert primal==objective=={2:F(7,4),3:F(23,10)}[n]
    assert primal<F(4,3)**n
    return {'copies':n,'allowed_rectangles':rectangles,'primal_dual_cap':str(primal),
            'ratio_to_supplied_quantum_product':str(primal/(F(4,3)**n))}

if __name__=='__main__':
    print(json.dumps({'scope':'Source-exposed independent table check; not a full repetition-proof audit',
                      'checks':[check(2),check(3)]},indent=2))
