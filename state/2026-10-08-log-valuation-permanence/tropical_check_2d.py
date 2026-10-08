#!/usr/bin/env python3
"""Exact 2-D tropical-endotacticity checker for positive rational power-law supports.

No numerical sampling is used to decide the criterion. Directions on every ray
and every open angular sector of a rational hyperplane arrangement are tested.
A reaction comprises numerator and denominator positive-monomial exponent lists
and its actual stoichiometric vector. Positive coefficients do not change tau.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
from functools import cmp_to_key
from math import gcd, lcm


def vec(*xs): return tuple(F(x) for x in xs)

def dot(a, b): return sum(x*y for x,y in zip(a,b))

def sub(a, b): return tuple(x-y for x,y in zip(a,b))

def primitive(a):
    a = tuple(F(x) for x in a)
    if not any(a): return None
    L = lcm(*(x.denominator for x in a))
    b = tuple(int(x*L) for x in a)
    g = gcd(*b)
    b = tuple(x//g for x in b)
    if next(x for x in b if x) < 0: b = tuple(-x for x in b)
    return b

def half(v):
    return 0 if v[1] > 0 or v[1] == 0 and v[0] > 0 else 1

def angle_cmp(u,v):
    a,b = half(u), half(v)
    if a != b: return -1 if a<b else 1
    cross = u[0]*v[1]-u[1]*v[0]
    return -1 if cross>0 else (1 if cross<0 else 0)

@dataclass(frozen=True)
class Reaction:
    name: str
    numerator: tuple
    denominator: tuple
    nu: tuple
    def tau(self,r):
        return min(dot(a,r) for a in self.numerator) - min(dot(b,r) for b in self.denominator)


def reaction(name, numerator, denominator, nu):
    return Reaction(name,tuple(vec(*v) for v in numerator),
                    tuple(vec(*v) for v in denominator),vec(*nu))


def all_directions(reactions):
    # An over-refined but sufficient central arrangement: on every face,
    # ordering of all possible alpha-beta forms and signs r.nu is fixed.
    slopes = sorted({sub(a,b) for e in reactions for a in e.numerator for b in e.denominator})
    normals = {primitive(e.nu) for e in reactions if any(e.nu)}
    normals |= {primitive(sub(a,b)) for a,b in combinations(slopes,2)}
    normals.discard(None)
    rays = set()
    for a,b in normals:
        v = (-b,a)
        rays.add(v)
        rays.add((-v[0],-v[1]))
    rays = sorted(rays,key=cmp_to_key(angle_cmp))
    if not rays: return [],0
    directions=[]
    for i,u in enumerate(rays):
        directions.append((u,'boundary'))
        v=rays[(i+1)%len(rays)]
        w=(u[0]+v[0],u[1]+v[1])
        if w == (0,0): w=(-u[1],u[0])
        assert w!=(0,0)
        directions.append((w,'open sector'))
    return directions,len(normals)


def check(reactions):
    directions,num_hyperplanes=all_directions(reactions)
    tested=0
    for r,where in directions:
        tested+=1
        active=[(e,e.tau(r),dot(r,e.nu)) for e in reactions if dot(r,e.nu)!=0]
        if not active: continue
        minimal=min(x[1] for x in active)
        bad=[x for x in active if x[1]==minimal and x[2]<0]
        if bad:
            return {'valid':False,'direction':r,'stratum':where,
                    'bad_edges':[x[0].name for x in bad],
                    'minimal_exponent':minimal,'normal_count':num_hyperplanes,
                    'directions_tested':tested,'total_directions':len(directions)}
    return {'valid':True,'normal_count':num_hyperplanes,
            'directions_tested':tested,'total_directions':len(directions)}


def tests():
    one=[(0,0)]
    hill=[
        reaction('birth_X',one,[(0,0),(0,2)],(1,0)),
        reaction('death_X',[(1,0)],one,(-1,0)),
        reaction('birth_Y',one,[(0,0),(3,0)],(0,1)),
        reaction('death_Y',[(0,1)],one,(0,-1)),
    ]
    bad=[reaction('autocatalysis',[(2,0)],one,(1,0)),
         reaction('loss',[(1,0)],one,(-1,0))]
    # Unique failure on codimension-one boundary: dx=-k x y, dy=a-b y^2.
    # The genuine species source complexes are (0,0), (0,2), (1,1).
    face_only=[
        reaction('zero_to_Y',one,one,(0,1)),
        reaction('twoY_to_Y',[(0,2)],one,(0,-1)),
        reaction('XplusY_to_Y',[(1,1)],one,(-1,0)),
    ]
    for name,rr,expect in [('Hill_toggle',hill,True),
                           ('autocatalytic_loss',bad,False),
                           ('face_only_failure',face_only,False)]:
        ans=check(rr)
        print(name,ans)
        assert ans['valid']==expect, (name,ans)
    # Assert the face-only example passes every OPEN angular sector, not just
    # a floating random grid, while failing on the boundary r=(1,0).
    directions,nh=all_directions(face_only)
    invalid=[]
    for r,where in directions:
        active=[(e,e.tau(r),dot(r,e.nu)) for e in face_only if dot(r,e.nu)!=0]
        if active:
            t=min(a[1] for a in active)
            if any(a[1]==t and a[2]<0 for a in active): invalid.append((r,where))
    print('face_only_ALL_failures',invalid,'normals',nh)
    assert invalid==[((1,0),'boundary')],invalid
    print('ALL 2D EXACT CHECKER TESTS PASSED')

if __name__=='__main__': tests()
