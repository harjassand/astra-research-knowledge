"""Deterministic relative physical-prefix counting from explicit small bias.

Owned c01_s03 phase-two derivation. Classical small-bias construction:
b_i(x,y) is the binary-coordinate dot product of x with y**i in GF(2**m).
The trace pairing gives an equivalent family after changing the x basis.
Finite-field irreducibles are acquired by bounded deterministic search.
No random signs, normalizer, unknown support oracle or Pfaffian is used.
"""
from fractions import Fraction
from random import SystemRandom
from color_sector_control import ColorSector
from low_sector_sampler import ceil_log2


def polynomial_mod(a,b):
    while a and a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length()-b.bit_length())
    return a


def polynomial_gcd(a,b):
    while b:
        a,b=b,polynomial_mod(a,b)
    return a


def polynomial_multiply_mod(a,b,modulus):
    degree=modulus.bit_length()-1
    answer=0
    while b:
        if b&1: answer ^= a
        b >>= 1
        a <<= 1
        if a & (1 << degree): a ^= modulus
    return answer


def irreducible(modulus):
    m=modulus.bit_length()-1
    if m <= 0 or not modulus&1: return False
    if m == 1: return modulus==3
    x=2
    h=x
    for j in range(1,m+1):
        h=polynomial_multiply_mod(h,h,modulus)
        if j <= m//2 and polynomial_gcd(h^x,modulus)!=1:
            return False
    return h==x


class BinaryField:
    def __init__(self,m):
        if not isinstance(m,int) or m<1: raise ValueError('positive field degree required')
        self.degree,self.order=m,1<<m
        self.modulus=None
        self.candidates_checked=0
        for candidate in range((1<<m)|1,1<<(m+1),2):
            self.candidates_checked+=1
            if irreducible(candidate):
                self.modulus=candidate
                break
        if self.modulus is None:
            raise AssertionError('irreducible polynomial existence violated')

    def mul(self,a,b):
        if not 0<=a<self.order or not 0<=b<self.order:
            raise ValueError('field element out of range')
        return polynomial_multiply_mod(a,b,self.modulus)

    def pow(self,a,e):
        answer=1
        while e:
            if e&1: answer=self.mul(answer,a)
            e >>=1
            if e: a=self.mul(a,a)
        return answer


def small_bias_histogram(free_count,field):
    """Exact weighted family of q^2 words, with bias <= (free_count-1)/q."""
    q,m=field.order,field.degree
    histogram={}
    for y in range(q):
        powers=[1]
        for _ in range(1,free_count): powers.append(field.mul(powers[-1],y))
        basis_words=[0]*m
        for i,power in enumerate(powers[:free_count]):
            for j in range(m):
                if (power>>j)&1: basis_words[j] |= 1<<i
        words=[0]*q
        histogram[0]=histogram.get(0,0)+1
        for x in range(1,q):
            low=x&-x
            word=words[x^low]^basis_words[low.bit_length()-1]
            words[x]=word
            histogram[word]=histogram.get(word,0)+1
    assert sum(histogram.values())==q*q
    return histogram


class DeterministicLowSector(ColorSector):
    def __init__(self,f):
        super().__init__(f)
        self.field_cache={}
        self.histogram_cache={}

    def deterministic_count(self,k,eta,up=(),down=(),empty=()):
        eta=Fraction(eta)
        if not 0<eta<=Fraction(1,2): raise ValueError('require 0<eta<=1/2')
        up,down,empty=self._restrictions(k,up,down,empty)
        a,b=len(up),len(down)
        if a>k or b>k or 2*k>self.n-len(empty): return Fraction(0)
        self.stats['deterministic_count_calls']=self.stats.get('deterministic_count_calls',0)+1
        r=2*k-a-b
        if r==0:
            return Fraction(self.prefix_draw_integer(k,[1]*self.n,up,down,empty),self.denominator**(2*k))
        free=sorted(set(range(self.n))-up-down-empty)
        f=len(free)
        # A pattern on r sites has relative probability error at most
        # (2^r-1)*(f-1)/q. Use q>=2 for a concrete binary field.
        required=max(Fraction(2),Fraction(max(f-1,0)*((1<<r)-1),1)/eta)
        degree=max(1,ceil_log2(required))
        if degree not in self.field_cache:
            field=BinaryField(degree)
            self.field_cache[degree]=field
            self.stats['irreducible_candidates']=self.stats.get('irreducible_candidates',0)+field.candidates_checked
        field=self.field_cache[degree]
        key=(f,degree)
        if key not in self.histogram_cache:
            self.histogram_cache[key]=small_bias_histogram(f,field)
            self.stats['family_words_constructed']=self.stats.get('family_words_constructed',0)+field.order**2
        histogram=self.histogram_cache[key]
        self.stats['maximum_field_order']=max(self.stats.get('maximum_field_order',0),field.order)
        self.stats['maximum_distinct_colorings']=max(self.stats.get('maximum_distinct_colorings',0),len(histogram))
        self.stats['family_words_charged']=self.stats.get('family_words_charged',0)+field.order**2
        numerator=0
        for word,count in histogram.items():
            signs=[1]*self.n
            for i,site in enumerate(free): signs[site]=-1 if (word>>i)&1 else 1
            numerator+=count*self.prefix_draw_integer(k,signs,up,down,empty)
        return Fraction(numerator,field.order**2*self.denominator**(2*k))

    def born_sample(self,k,epsilon,rng=None):
        """No estimation failure; returns OK on positive sectors, NO_SECTOR iff zero.

        Output distribution is within epsilon TV. Only the n categorical draws
        consume random bits. Counts are deterministic relative approximations.
        """
        epsilon=Fraction(epsilon)
        if not 0<epsilon<1: raise ValueError('require 0<epsilon<1')
        self._restrictions(k,(),(),())
        if k==0:return {'status':'OK','I':[],'J':[]}
        rng=SystemRandom() if rng is None else rng
        eta=epsilon/(8*self.n)
        bits=ceil_log2(8*self.n/epsilon)
        q=1<<bits
        up,down,empty=set(),set(),set()
        for site in range(self.n):
            weights=[self.deterministic_count(k,eta,up|{site},down,empty),
                     self.deterministic_count(k,eta,up,down|{site},empty),
                     self.deterministic_count(k,eta,up,down,empty|{site})]
            total=sum(weights)
            if total==0:
                assert site==0
                return {'status':'NO_SECTOR'}
            x=q*weights[0]/total;y=q*(weights[0]+weights[1])/total
            t1,t2=x.numerator//x.denominator,y.numerator//y.denominator
            word=rng.getrandbits(bits)
            if word<t1:up.add(site)
            elif word<t2:down.add(site)
            else:empty.add(site)
            self.stats['categorical_bits']=self.stats.get('categorical_bits',0)+bits
        assert len(up)==len(down)==k
        return {'status':'OK','I':sorted(up),'J':sorted(down)}
