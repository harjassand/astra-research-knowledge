"""Exact-rational support-safe empirical teacher, construction prototype.

The external conditional_draw(h) must return a fresh independent FULL Q future
at the certified-positive prefix h. randbelow(n) must be exactly uniform and
independent of those empirical draws. No Q probability evaluator is accepted.
Only AST/syntax inspection is claimed for this file; no new source instance run.
"""
from fractions import Fraction as F
from math import lcm


def fair_randbelow(n, next_bit):
    """Exact uniform integer from supplied iid fair bits; expected <2 trials."""
    if n<1:raise ValueError('positive integer bound required')
    if n==1:return 0
    bits=(n-1).bit_length()
    while True:
        value=0
        for _ in range(bits):value=(value<<1)|int(next_bit())
        if value<n:return value


class EmpiricalTeacher:
    def __init__(self,alphabet,horizon,batch,rho,alpha,conditional_draw,randbelow):
        self.O,self.T,self.m=int(alphabet),int(horizon),int(batch)
        self.rho,self.alpha=F(rho),F(alpha)
        if self.O<2 or self.T<1 or self.m<1:raise ValueError('invalid dimensions')
        if not 0<self.rho<=F(1,10*self.O):raise ValueError('rho outside theorem domain')
        if not 0<self.alpha<=F(1,4):raise ValueError('alpha outside theorem domain')
        self.conditional_draw,self.randbelow=conditional_draw,randbelow
        self.rows={};self.certified={()};self.locked=False
        self.api_queries=self.q_conditional_draws=self.returned_symbols=0

    def _query(self):
        if self.locked:raise RuntimeError('empirical teacher unavailable after compilation')
        self.api_queries+=1

    def _word(self,h):
        h=tuple(h)
        if len(h)>self.T or any(not isinstance(o,int) or not 0<=o<self.O for o in h):
            raise ValueError('word outside finite alphabet/horizon')
        return h

    def _row(self,h):
        if h in self.rows:return self.rows[h]
        if h not in self.certified or len(h)>=self.T:
            raise RuntimeError('attempted original-Q query without observed support certificate')
        counts=[0]*self.O
        for _ in range(self.m):
            future=tuple(self.conditional_draw(h))
            self.q_conditional_draws+=1;self.returned_symbols+=len(future)
            if len(future)!=self.T-len(h) or any(not isinstance(o,int) or not 0<=o<self.O for o in future):
                raise ValueError('conditional sample primitive violated its contract')
            counts[future[0]]+=1
        norm=1+self.O*self.rho
        probs=tuple((F(c,self.m)+self.rho)/norm for c in counts)
        assert sum(probs)==1 and min(probs)>0
        observed=tuple(c>0 for c in counts)
        for o,yes in enumerate(observed):
            if yes:self.certified.add(h+(o,))
        self.rows[h]=(probs,observed)
        return self.rows[h]

    def _bar_prefix(self,h):
        prefix=();mass=F(1);active=True
        for o in h:
            if active:
                probs,observed=self._row(prefix)
                mass*=probs[o]
                if not observed[o]:active=False
            else:mass/=self.O
            prefix+=(o,)
        return mass,active

    def _mass(self,h):
        mass,_=self._bar_prefix(h)
        return (1-self.alpha)*mass+self.alpha/F(self.O**len(h))

    def _choose(self,probs):
        if sum(probs)!=1 or min(probs)<0:raise ValueError('invalid categorical row')
        denom=1
        for p in probs:denom=lcm(denom,p.denominator)
        weights=[p.numerator*(denom//p.denominator) for p in probs]
        r=self.randbelow(denom)
        if not isinstance(r,int) or not 0<=r<denom:raise ValueError('randbelow contract violated')
        for o,w in enumerate(weights):
            if r<w:return o
            r-=w
        raise AssertionError('categorical normalization mismatch')

    def prefix_probability(self,h):
        self._query();return self._mass(self._word(h))

    def conditional_probability(self,h,f):
        self._query();h=self._word(h);f=tuple(f)
        full=self._word(h+f)
        return self._mass(full)/self._mass(h)

    def next_probabilities(self,h):
        self._query();h=self._word(h)
        if len(h)>=self.T:raise ValueError('terminal word has no next token')
        bar,active=self._bar_prefix(h)
        qbar=self._row(h)[0] if active else (F(1,self.O),)*self.O
        uniform_prefix=F(1,self.O**len(h))
        denominator=(1-self.alpha)*bar+self.alpha*uniform_prefix
        row=tuple(((1-self.alpha)*bar*p+self.alpha*uniform_prefix/self.O)/denominator for p in qbar)
        assert sum(row)==1 and min(row)>0
        return row

    def conditional_sample(self,h):
        self._query();h=self._word(h)
        bar,active=self._bar_prefix(h)
        total=(1-self.alpha)*bar+self.alpha/F(self.O**len(h))
        pbar=(1-self.alpha)*bar/total
        component=self._choose((pbar,1-pbar))
        if component==1:
            return tuple(self.randbelow(self.O) for _ in range(self.T-len(h)))
        prefix=h;future=[]
        while len(prefix)<self.T:
            if active:
                probs,observed=self._row(prefix);o=self._choose(probs)
                if not observed[o]:active=False
            else:o=self.randbelow(self.O)
            future.append(o);prefix+=(o,)
        return tuple(future)

    def lock(self):
        """The completed compiler must retain only its finite model, never self."""
        self.locked=True

    def costs(self):
        return {'R_api_queries':self.api_queries,'original_Q_nodes':len(self.rows),
                'original_Q_full_future_draws':self.q_conditional_draws,
                'original_Q_returned_symbols':self.returned_symbols,
                'original_Q_probability_value_queries':0,
                'node_bound_T_times_API_queries':self.T*self.api_queries,
                'independence':'conditional_draw and randbelow must supply independent randomness'}
