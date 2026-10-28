#!/usr/bin/env python3
"""Independent exact Singer certificates, rational bounds and complete record tests.
Finite fields use integer-encoded coefficient arithmetic, not the author's code.
No floating point, source calls, RNG, hardware or sampling.
"""
from pathlib import Path
from collections import Counter
from itertools import product
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import json
import sympy as s

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'PHYSICAL_QUADRATIC_DISTINGUISHING_LENGTH.md'
EXPECTED_SOURCE_SHA256='fb24c0a5e0e2033276c823363f52dbfa0e514790835a18cf4f13698fee81665f'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED_SOURCE_SHA256
x=s.symbols('x')

class Field:
    def __init__(self,p,low):
        self.p=p;self.low=low;self.m=len(low);self.size=p**self.m
        assert s.Poly(x**self.m+sum(c*x**i for i,c in enumerate(low)),x,modulus=p).is_irreducible
    def digits(self,a):
        out=[]
        for _ in range(self.m):out.append(a%self.p);a//=self.p
        return out
    def encode(self,a):return sum(c*self.p**i for i,c in enumerate(a))
    def add(self,a,b):return self.encode([(u+v)%self.p for u,v in zip(self.digits(a),self.digits(b))])
    @lru_cache(None)
    def mul(self,a,b):
        aa,bb=self.digits(a),self.digits(b)
        c=[0]*(2*self.m-1)
        for i,u in enumerate(aa):
            for j,v in enumerate(bb):c[i+j]=(c[i+j]+u*v)%self.p
        for k in reversed(range(self.m,len(c))):
            t=c[k];c[k]=0
            for j,z in enumerate(self.low):c[k-self.m+j]=(c[k-self.m+j]-t*z)%self.p
        return self.encode(c[:self.m])
    def pow(self,a,n):
        value=1
        while n:
            if n%2:value=self.mul(value,a)
            a=self.mul(a,a);n//=2
        return value
    def primitive(self,a):
        return a!=0 and all(self.pow(a,(self.size-1)//int(l))!=1 for l in s.factorint(self.size-1))

author=json.loads((ROOT/'physical_quadratic_length_exact_check.json').read_text())
assert author['source_sha256']==EXPECTED_SOURCE_SHA256
inputs=[(row['field_characteristic'],row['base_extension_degree'],
         row['irreducible_polynomial_low_coefficients'],row['primitive_element'])
        for row in author['dimensions']]
# Two extra prime powers, including characteristic-three cubic trace with Tr(1)=0.
inputs += [(3,2,[2,1,0,0,0,0],None),(2,4,[1,0,0,1,0,0,0,0,0,0,0,0],None)]
reports=[]
for p,n,modulus,proposed in inputs:
    q=p**n;d=q+1;r=q*q+q+1
    field=Field(p,modulus)
    g=field.encode(proposed) if proposed is not None else next(a for a in range(2,field.size) if field.primitive(a))
    assert field.primitive(g)
    powers=[1]
    for _ in range(field.size-2):powers.append(field.mul(powers[-1],g))
    assert len(set(powers))==field.size-1 and field.mul(powers[-1],g)==1
    N=field.size-1
    traces=[field.add(field.add(powers[e],powers[(q*e)%N]),powers[(q*q*e)%N]) for e in range(N)]
    assert len(set(traces+[0]))==q
    assert traces.count(0)==q*q-1
    assert all(field.pow(t,q)==t for t in traces)
    D=[e for e in range(r) if traces[e]==0]
    assert len(D)==d
    differences=Counter((i-j)%r for i in D for j in D if i!=j)
    assert differences==Counter(range(1,r))
    # Direct projective kernel-intersection certificate, separate from difference counting.
    assert all(sum(traces[e]==0 and traces[(e+t)%N]==0 for e in range(r))==1 for t in range(1,r))

    # Directly compute the orbit Gram squared numerator from all d^2 terms,
    # not by assuming the claimed equiangular identity. Works for composite r.
    cyclo=s.Poly(s.cyclotomic_poly(r,x),x)
    moments=[]
    for t in range(r):
        terms=Counter()
        for i in D:
            for j in D:
                terms[((i-j)*t)%r]+=1
        polynomial=s.Poly.from_dict({(i,):v for i,v in terms.items()},x)
        remainder=s.rem(polynomial,cyclo)
        expected=s.Poly(d*d if t==0 else d-1,x)
        assert remainder==expected
        moments.append(int(expected.as_expr()))
    rho_eigenvalues=[Q(1,2)+Q(1,2*d)]+[Q(1,2*d)]*(d-1)
    assert sum(rho_eigenvalues)==1 and min(rho_eigenvalues)==Q(1,2*d)
    effect_eigenvalues=[Q(3,4)]+[Q(1,2)]*(d-1)
    assert min(effect_eigenvalues)==Q(1,2)
    assert min(1-e for e in effect_eigenvalues)==Q(1,4)
    signal=Q(r,8*d*d)
    assert signal>=Q(3,32)
    beta=Q(1,2*r);damping=(1-beta)**(r-2)
    assert damping>Q(1,2)
    late_signal=damping*signal
    assert late_signal>Q(3,64)
    # These probabilities come directly from the above Gram polynomial.
    for alpha in [Q(1),1-beta]:
        probabilities={j:[Q(1,2)+Q(1,4*d)+alpha**k*Q(moments[(k+j)%r]-d,8*d*d)
                          for k in range(r-1)] for j in [1,2]}
        assert probabilities[1][:-1]==probabilities[2][:-1]
        assert probabilities[2][-1]-probabilities[1][-1]==signal*alpha**(r-2)
        assert all(0<p0<1 for probs in probabilities.values() for p0 in probs)
    reports.append({'q':q,'d':d,'r':r,'field_modulus':modulus,
                    'primitive_element_integer':g,'difference_set':D,
                    'trace_zero_nonzero_field_vectors':q*q-1,
                    'trace_image_size':q,'trace_of_one_zero':traces[0]==0,
                    'projective_kernel_intersections_checked':r-1,
                    'cyclotomic_orbit_Gram_checks':len(moments),
                    'short_max_native_length':r-2,'target_native_length':r-1,
                    'unitary_signal_exact':str(signal),
                    'depolarized_signal_exact':str(late_signal),
                    'forward_choi_floor':str(beta/d),'test_choi_floor':str(Q(1,4*d)),
                    'initial_state_eigenvalue_floor':str(Q(1,2*d)),
                    'reset_outcome1_probability':str(Q(1,2)+Q(1,4*d))})

# Complete words, feedback, repeated reset episodes and clocked target.
q=2;d=3;r=7;signal=Q(r,8*d*d);reset_p=Q(1,2)+Q(1,4*d)
def outcome1(world,k,beta):
    return reset_p+(1-beta)**k*Q(r*((k+world)%r==0)-1,8*d*d)
def word_probability(word,world,beta):
    k=0;reset=False;mass=Q(1)
    for symbol in word:
        if symbol=='a':
            if not reset:k+=1
        else:
            p=reset_p if reset else outcome1(world,k,beta)
            mass*=p if symbol=='1' else 1-p
            reset=True
    return mass
word_checks=0;short_equalities=0;long_different_words=0;rank_checks=0
for beta in [Q(0),Q(1,2*r)]:
    for length in range(r):
        for word in product(['a','0','1'],repeat=length):
            p1=word_probability(word,1,beta);p2=word_probability(word,2,beta)
            if length<=r-2:
                assert p1==p2
                short_equalities+=1
            elif p1!=p2:
                assert word[:-1]==('a',)*(r-2) and word[-1] in ('0','1')
                assert abs(p1-p2)==signal*(1-beta)**(r-2)
                long_different_words+=1
            word_checks+=1
    for world in [1,2]:
        hankel=s.Matrix(r,r,lambda i,j:s.Rational(outcome1(world,i+j,beta)))
        assert hankel.rank()==r
        rank_checks+=1
assert long_different_words==4

def policy(h,selector):
    if len(h)>=4 and h[-1:] == ('1',):return None
    score=sum({'a':0,'0':1,'1':2}[v] for v in h)
    return 'a' if (len(h)+score+selector)%3==0 else 'b'
def record_law(world,beta,selector,h=(),k=0,reset=False,mass=Q(1)):
    a=policy(h,selector)
    if len(h)==r-2 or a is None:return {h:mass}
    if a=='a':return record_law(world,beta,selector,h+('a',),k+(not reset),reset,mass)
    p=reset_p if reset else outcome1(world,k,beta)
    out=record_law(world,beta,selector,h+('1',),k,True,mass*p)
    out.update(record_law(world,beta,selector,h+('0',),k,True,mass*(1-p)))
    return out
feedback_checks=0
for beta in [Q(0),Q(1,2*r)]:
    for selector in range(6):
        pp=record_law(1,beta,selector);pm=record_law(2,beta,selector)
        assert pp==pm and sum(pp.values())==1
        feedback_checks+=1
        # Adapt the second independent reset episode to the entire first record.
        joint=[]
        for world in [1,2]:
            answer={}
            for h,p0 in record_law(world,beta,selector).items():
                second_selector=sum({'a':1,'0':2,'1':4}[v] for v in h)%6
                for hh,p1 in record_law(world,beta,second_selector).items():answer[h,hh]=p0*p1
            joint.append(answer)
        assert joint[0]==joint[1] and sum(joint[0].values())==1
        feedback_checks+=1

clock_checks=0
for beta in [Q(0),Q(1,2*r)]:
    for gamma in [Q(1,3),Q(3,5),Q(9,10)]:
        laws=[]
        for world in [1,2]:
            law={('abort',k):(1-gamma)*gamma**k for k in range(r-1)}
            p1=outcome1(world,r-2,beta)
            law['complete',1]=gamma**(r-1)*p1
            law['complete',0]=gamma**(r-1)*(1-p1)
            assert sum(law.values())==1
            laws.append(law)
        tv=sum(abs(laws[0][key]-laws[1][key]) for key in laws[0])/2
        assert tv==gamma**(r-1)*signal*(1-beta)**(r-2)
        clock_checks+=1

for Dmax in range(3,2001):
    q=2
    while 2*q<=Dmax-1:q*=2
    assert q+1<=Dmax and q>Q(Dmax-1,2)
    assert q*q+q>Q((Dmax-1)**2,4)

report={'status':'PASS independent exact finite-field and physical-delay certificates',
        'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_calls':0,'episode_starts':0,'rng_calls':0,'floating_point_used':False,
        'finite_field_cases':reports,'complete_word_checks_through_first_distinguishing_length':word_checks,
        'short_equalities':short_equalities,'first_length_different_words':long_different_words,
        'exact_small_Hankel_rank_checks':rank_checks,'clocked_target_checks':clock_checks,
        'single_and_adaptive_two_episode_record_checks':feedback_checks,
        'dimension_bound_corollary_cases':1998,
        'model_variant':'two-shift harmonic frame, shifts 1 and 2; target length r-1'}
(ROOT/'physical_quadratic_length_independent_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='finite_field_cases'},indent=2))
print('field q values:',[v['q'] for v in reports])
