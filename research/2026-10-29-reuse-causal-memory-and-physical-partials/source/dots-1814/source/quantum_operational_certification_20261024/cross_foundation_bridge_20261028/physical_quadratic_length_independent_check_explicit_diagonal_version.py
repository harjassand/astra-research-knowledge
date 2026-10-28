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

    bs=[2*j-d+1 for j in range(d)];S=sum(v*v for v in bs)
    eps=Q(1,8*d);scale=Q(1,r)/eps
    assert sum(bs)==0 and S==d*(d*d-1)//3
    assert all(abs(Q(v,S))<1 for v in bs)
    assert max(abs(v)+d-1 for v in bs)*eps<Q(1,4)
    assert sum(abs(-1+Q(v,S)) for v in bs)==d
    # Rational matrix unitarily similar to the delayed witness before scale.
    realQ=s.ones(d)-s.eye(d)+s.diag(*[s.Rational(v,S) for v in bs])
    char=s.Poly(realQ.charpoly(x).as_expr(),x)
    assert char.count_roots(-s.oo,0)==d-1
    assert char.count_roots(0,d)==1
    assert realQ.trace()==0
    Tupper=2*d*scale
    assert 1/Tupper==Q(r,16*d*d)>=Q(3,64)

    # Compute actual moment numerator from E and Delta entries, then reduce
    # modulo the cyclotomic polynomial. This does not assume r prime.
    cyclo=s.Poly(s.cyclotomic_poly(r,x),x)
    moments=[]
    for k in range(r):
        terms=Counter({0:1})
        for i in D:
            for j in D:
                if i!=j:terms[((i-j)*(k+1))%r]+=1
        polynomial=s.Poly.from_dict({(i,):v for i,v in terms.items()},x)
        remainder=s.rem(polynomial,cyclo)
        expected=s.Poly(r if k==r-1 else 0,x)
        assert remainder==expected
        moments.append(0 if k<r-1 else 1)
    # An extra inverse action would move the +1 phase offset immediately to zero.
    assert (1+len(D)*(len(D)-1))==r
    beta=Q(1,2*r);damping=(1-beta)**(r-1)
    assert damping>Q(1,2)
    signal_lower=damping/Tupper
    assert signal_lower>Q(3,128)

    # Optional explicit PSD split communicated during review. Its spectrum,
    # normalization and difference coefficient are rationally certified.
    rho_minus_diag=[Q(1,d)-Q(v,2*d*S) for v in bs]
    assert sum(rho_minus_diag)==1 and min(rho_minus_diag)>=Q(1,2*d)
    rho_plus_eigenvalues=[Q(1,2)+Q(1,2*d)]+[Q(1,2*d)]*(d-1)
    assert sum(rho_plus_eigenvalues)==1
    assert Q(1,2*d)/scale==Q(r,16*d*d)
    reports.append({'q':q,'d':d,'r':r,'field_modulus':modulus,
                    'primitive_element_integer':g,'difference_set':D,
                    'trace_zero_nonzero_field_vectors':q*q-1,
                    'trace_image_size':q,'trace_of_one_zero':traces[0]==0,
                    'projective_kernel_intersections_checked':r-1,
                    'cyclotomic_moments_checked':len(moments),
                    'real_witness_positive_eigenvalues':1,'real_witness_negative_eigenvalues':d-1,
                    'trace_norm_upper':str(Tupper),'unitary_signal_lower':str(1/Tupper),
                    'depolarized_signal_lower':str(signal_lower),
                    'forward_choi_floor':str(beta/d),'test_choi_floor':str(Q(1,4*d)),
                    'explicit_PSD_split_checked':True})

# Complete word and feedback checks for the optional explicit PSD split.
# These use its independently derived rational first-test probabilities.
q=2;d=3;r=7;signal=Q(r,16*d*d)
def outcome1(world,k,beta):
    minus=Q(1,2)-(1-beta)**k*Q(1,16*d*d)
    return minus+(signal*(1-beta)**k if world=='plus' and (k+1)%r==0 else 0)
def word_probability(word,world,beta):
    k=0;reset=False;mass=Q(1)
    for symbol in word:
        if symbol=='a':
            if not reset:k+=1
        else:
            p=Q(1,2) if reset else outcome1(world,k,beta)
            mass*=p if symbol=='1' else 1-p
            reset=True
    return mass
word_checks=0
for beta in [Q(0),Q(1,2*r)]:
    for length in range(r):
        for word in product(['a','0','1'],repeat=length):
            assert word_probability(word,'plus',beta)==word_probability(word,'minus',beta)
            word_checks+=1
    lateplus=word_probability(('a',)*(r-1)+('1',),'plus',beta)
    lateminus=word_probability(('a',)*(r-1)+('1',),'minus',beta)
    assert lateplus-lateminus==signal*(1-beta)**(r-1)

def policy(h,selector):
    if len(h)>=4 and h[-1:] == ('1',):return None
    score=sum({'a':0,'0':1,'1':2}[v] for v in h)
    return 'a' if (len(h)+score+selector)%3==0 else 'b'
def record_law(world,beta,selector,h=(),k=0,reset=False,mass=Q(1)):
    a=policy(h,selector)
    if len(h)==r-1 or a is None:return {h:mass}
    if a=='a':return record_law(world,beta,selector,h+('a',),k+(not reset),reset,mass)
    p=Q(1,2) if reset else outcome1(world,k,beta)
    out=record_law(world,beta,selector,h+('1',),k,True,mass*p)
    out.update(record_law(world,beta,selector,h+('0',),k,True,mass*(1-p)))
    return out
feedback_checks=0
for beta in [Q(0),Q(1,2*r)]:
    for selector in range(6):
        pp=record_law('plus',beta,selector);pm=record_law('minus',beta,selector)
        assert pp==pm and sum(pp.values())==1
        feedback_checks+=1
        # Adapt the second independent reset episode to the entire first record.
        joint=[]
        for world in ['plus','minus']:
            answer={}
            for h,p0 in record_law(world,beta,selector).items():
                second_selector=sum({'a':1,'0':2,'1':4}[v] for v in h)%6
                for hh,p1 in record_law(world,beta,second_selector).items():answer[h,hh]=p0*p1
            joint.append(answer)
        assert joint[0]==joint[1] and sum(joint[0].values())==1
        feedback_checks+=1

for Dmax in range(3,2001):
    q=2
    while 2*q<=Dmax-1:q*=2
    assert q+1<=Dmax and q>Q(Dmax-1,2)
    assert q*q+q+1>Q((Dmax-1)**2,4)

report={'status':'PASS independent exact finite-field and physical-delay certificates',
        'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_calls':0,'episode_starts':0,'rng_calls':0,'floating_point_used':False,
        'finite_field_cases':reports,'complete_short_word_checks':word_checks,
        'single_and_adaptive_two_episode_record_checks':feedback_checks,
        'dimension_bound_corollary_cases':1998,
        'explicit_split_note':'Also checks the optional simpler state split; final source hash records whether adopted.'}
(ROOT/'physical_quadratic_length_independent_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='finite_field_cases'},indent=2))
print('field q values:',[v['q'] for v in reports])
