"""Experimental exact stationary word-observable sampler for noisy Heisenberg-group networks.

Model: H_p over odd prime p, synchronous site-time independent Haar resets,
fixed residual resets, or deterministic group-word gate.  Expected query cost
independent of network size for bounded-size requested group words.

IMPORTANT: This is an experimental research implementation, not externally vetted.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict, Counter
import random

# A group expression is a (A,B,C) triple of sparse polynomials.
# Sparse monomial= tuple of coordinate labels (site,time,component), sorted;
# lengths <=2 (except constant ()), coefficients in F_p.

def add_term(P, mon, value, q):
    value %= q
    if not value: return
    value = (P.get(mon, 0) + value) % q
    if value: P[mon] = value
    else: P.pop(mon, None)


def const_poly(v, q):
    v %= q
    return {(): v} if v else {}


def symbol_poly(key, c):
    return {((key[0], key[1], c),): 1}


def plus(P, Q, q):
    R = P.copy()
    for mon, coef in Q.items(): add_term(R, mon, coef, q)
    return R


def neg(P, q):
    return {mon: (-coef) % q for mon, coef in P.items() if coef % q}


def product(P, Q, q):
    R = {}
    for mon1, c1 in P.items():
        for mon2, c2 in Q.items():
            mon = tuple(sorted(mon1 + mon2))
            if len(mon)>2:
                raise ValueError('The group-word coordinate algebra exceeded quadratic degree')
            add_term(R, mon, c1*c2, q)
    return R


def group_mul(x, y, q):
    a,b,c=x; u,v,w=y
    return ((a+u)%q,(b+v)%q,(c+w+a*v)%q)


def group_inv(x,q):
    a,b,c=x
    return ((-a)%q,(-b)%q,(-c+a*b)%q)


def expr_const(g,q):
    return tuple(const_poly(x,q) for x in g)


def expr_var(z):
    return (symbol_poly(z,'a'),symbol_poly(z,'b'),symbol_poly(z,'c'))


def expr_mul(X,Y,q):
    A,B,C = X
    U,V,W = Y
    return (plus(A,U,q),plus(B,V,q),plus(plus(C,W,q),product(A,V,q),q))


def expr_inv(X,q):
    A,B,C=X
    return neg(A,q),neg(B,q),plus(neg(C,q),product(A,B,q),q)


def expr_power(X,e,q):
    # e from user defined bounded-length word; cost explicitly charged
    if e<0:
        X=expr_inv(X,q); e=-e
    acc=expr_const((0,0,0),q)
    while e:
        if e&1: acc=expr_mul(acc,X,q)
        e//=2
        if e: X=expr_mul(X,X,q)
    return acc


def gate_expr(z, factors, q):
    """factors of ('v',site, exponent) or ('c',(a,b,c))"""
    X=expr_const((0,0,0),q)
    for F in factors:
        if F[0]=='v':
            term=expr_power(expr_var((int(F[1]),z[1]-1)),int(F[2]),q)
        elif F[0]=='c':
            term=expr_const(F[1],q)
        else: raise ValueError('Invalid factor')
        X=expr_mul(X,term,q)
    return X


def expr_replace(X,z,R,q):
    mapping = { 'a':R[0], 'b':R[1], 'c':R[2] }
    result=[]
    for P in X:
        out={}
        for mon, coeff in P.items():
            cur=const_poly(coeff,q)
            for v in mon:
                if v[0]==z[0] and v[1]==z[1]:
                    cur=product(cur,mapping[v[2]],q)
                else:
                    cur=product(cur,{(v,):1},q)
            out=plus(out,cur,q)
        result.append(out)
    return tuple(result)


def expr_vars(X):
    return { (label[0],label[1]) for P in X for mon in P for label in mon }


def word_exponents(X,q):
    A,B,C=X
    e={}
    for mon,val in A.items():
        if len(mon)==1:
            assert mon[0][2]=='a'
            e[mon[0][:2]]=val%q
        else: assert mon==()
    # exact algebraic invariant: a,b,c linear coefficients agree
    for z,coef in e.items():
        assert B.get(((z[0],z[1],'b'),),0)%q==coef
        assert C.get(((z[0],z[1],'c'),),0)%q==coef
    assert not any(len(mon)==1 and mon[0][2]=='c' and mon[0][:2] not in e for mon in C)
    return {z:c for z,c in e.items() if c}


def expr_eval(X, vals,q):
    out=[]
    for P in X:
        total=0
        for mon,coeff in P.items():
            term=coeff
            for v in mon: term=(term*vals[v])%q
            total=(total+term)%q
        out.append(total)
    return tuple(out)


def exact_rank_basis_add(B,v,q):
    """Incremental RREF-ish echelon by pivot index, independent random Haar vector basis."""
    n=len(v)
    w=list(v)
    for pivot,b in sorted(B.items()):
        if w[pivot]:
            f=w[pivot]
            w=[(x-f*y)%q for x,y in zip(w,b)]
    for i,x in enumerate(w):
        if x:
            inv=pow(x,-1,q)
            B[i]=tuple(y*inv%q for y in w)
            return True
    return False


def span_contains(B,v,q):
    w=list(v)
    for pivot,b in sorted(B.items()):
        if w[pivot]:
            f=w[pivot]
            w=[(x-f*y)%q for x,y in zip(w,b)]
    return not any(w)


def vec_add_inplace(dest,v,a,q):
    if a%q:
        for i,x in enumerate(v): dest[i]=(dest[i]+a*x)%q


@dataclass
class Model:
    n: int
    q: int
    s: float                 # fresh full Haar probability
    r: float                 # residual reset probability
    gates: object            # site -> list of factors; OR callable(site)->factors
    residual: object = (0,0,0)  # constant OR callable(site)->constant

    def factors(self,i):
        return self.gates(i) if callable(self.gates) else self.gates[i]

    def reset_value(self,i):
        return self.residual(i) if callable(self.residual) else self.residual


class Oracle:
    def __init__(self,model,rng):
        self.model=model
        self.rng=rng
        self.memo={}
        self.fresh=0
        self.parent_queries=0
    def event(self,z):
        if z in self.memo: return self.memo[z],False
        self.fresh+=1
        u=self.rng.random()
        if u<self.model.s: result=('haar',None)
        elif u<self.model.s+self.model.r: result=('residual',self.model.reset_value(z[0]))
        else: result=('gate',None)
        self.memo[z]=result
        return result, True


def gate_quotient(model,z):
    """(a0,b0, multiplicity coefficient for each parent) from a word gate."""
    X=gate_expr(z,model.factors(z[0]),model.q)
    e=word_exponents(X,model.q)
    return X[0].get((),0),X[1].get((),0),e


def quotient_joint_sample(model,targets,oracle):
    """Sample joint (a,b) for arbitrary site-time targets, conditioned on oracle.memo.

    Exact symbolic Haar-subspace absorption on finite-field vector-valued states.
    Returns list of (a,b), with a cached category field shared with outer sampler.
    """
    q=model.q
    # coordinate order: a_z, b_z for z in targets
    targets=list(targets)
    d=2*len(targets)
    residual=[0]*d
    coefficients={}
    basis={}
    for j,z in enumerate(targets):
        if z not in coefficients: coefficients[z]=([0]*d,[0]*d)
        coefficients[z][0][2*j]=(coefficients[z][0][2*j]+1)%q
        coefficients[z][1][2*j+1]=(coefficients[z][1][2*j+1]+1)%q
    while coefficients:
        z=max(coefficients,key=lambda k:(k[1],k[0]))
        ca,cb=coefficients.pop(z)
        if span_contains(basis,ca,q) and span_contains(basis,cb,q): continue
        (kind,value),fresh=oracle.event(z)
        if kind=='haar':
            exact_rank_basis_add(basis,ca,q)
            exact_rank_basis_add(basis,cb,q)
        elif kind=='residual':
            vec_add_inplace(residual,ca,value[0],q)
            vec_add_inplace(residual,cb,value[1],q)
        else:
            a0,b0,terms=gate_quotient(model,z)
            vec_add_inplace(residual,ca,a0,q)
            vec_add_inplace(residual,cb,b0,q)
            oracle.parent_queries+=sum(abs(F[2]) for F in model.factors(z[0]) if F[0]=='v')
            for parent,coef in terms.items():
                if parent not in coefficients: coefficients[parent]=([0]*d,[0]*d)
                pa,pb=coefficients[parent]
                vec_add_inplace(pa,ca,coef,q)
                vec_add_inplace(pb,cb,coef,q)
                if not any(pa) and not any(pb): coefficients.pop(parent,None)
    for pivot,vec in basis.items():
        coeff=oracle.rng.randrange(q)
        vec_add_inplace(residual,vec,coeff,q)
    return [tuple(residual[2*i:2*i+2]) for i in range(len(targets))]


def sample_word_observable(model,root_factors,rng=None,diagnostics=False):
    """Perfect stationary distribution sample for group-word observable.

    root_factors: ('v',site, exponent) or ('c',(a,b,c)), at time 0.
    E.g. [('v',0,1), ('v',1,1), ('v',0,-1), ('v',1,-1)].
    """
    rng=rng or random.Random()
    oracle=Oracle(model,rng)
    q=model.q
    W=expr_const((0,0,0),q)
    for F in root_factors:
        if F[0]=='v': term=expr_power(expr_var((F[1],0)),F[2],q)
        else: term=expr_const(F[1],q)
        W=expr_mul(W,term,q)
    stage1=0
    while True:
        exponents=word_exponents(W,q)
        if not exponents: break
        # All unexpanded variables with nonzero exponent at later times MUST be processed first.
        z=max(exponents,key=lambda k:(k[1],k[0]))
        kind,value=oracle.event(z)[0]
        stage1+=1
        if kind=='haar':
            ans=(rng.randrange(q),rng.randrange(q),rng.randrange(q))
            if diagnostics: return ans, {'group_events':stage1, 'quotient':False,'fresh':oracle.fresh,'parent_queries':oracle.parent_queries,'frontier':len(expr_vars(W))}
            return ans
        if kind=='residual': replacement=expr_const(value,q)
        else:
            oracle.parent_queries+=sum(abs(F[2]) for F in model.factors(z[0]) if F[0]=='v')
            replacement=gate_expr(z,model.factors(z[0]),q)
        W=expr_replace(W,z,replacement,q)
    relevant=sorted(expr_vars(W))
    # Since all exponents vanish, the entire word is independent of central
    # coordinates of all unresolved site-time variables.
    assert all(lbl[2]!='c' for P in W for mon in P for lbl in mon)
    av=quotient_joint_sample(model,relevant,oracle)
    assigned={}
    for z,(a,b) in zip(relevant,av):
        assigned[(z[0],z[1],'a')]=a
        assigned[(z[0],z[1],'b')]=b
    ans=expr_eval(W,assigned,q)
    if diagnostics: return ans, {'group_events':stage1, 'quotient':True,'fresh':oracle.fresh,'parent_queries':oracle.parent_queries,'frontier':len(relevant)}
    return ans


def group_word_eval(values,factors,q):
    a=(0,0,0)
    for F in factors:
        if F[0]=='c': v=F[1]
        else:
            v=values[F[1]]
            e=F[2]
            if e<0: v=group_inv(v,q);e=-e
            power=(0,0,0)
            while e:
                if e&1:power=group_mul(power,v,q)
                e//=2
                if e: v=group_mul(v,v,q)
            v=power
        a=group_mul(a,v,q)
    return a

if __name__=='__main__':
    # Self-test on noncommutative H_3 with an exact group commutator.
    G={
      0:[('v',0,1),('v',1,1),('v',0,-1),('v',1,-1)],
      1:[('v',1,1),('v',0,1),('v',1,1)]
    }
    model=Model(n=2,q=3,s=.16,r=.12,gates=G,residual=(1,0,1))
    rng=random.Random(200412)
    for observable in [[('v',0,1)],[('v',1,1)],[('v',0,1),('v',1,1),('v',0,-1),('v',1,-1)]]:
        vals=[sample_word_observable(model,observable,rng,True) for i in range(100)]
        cnt=Counter(x[0] for x in vals)
        stats=[x[1]['fresh'] for x in vals]
        print('root',observable,'unique',len(cnt),'mean oracle symbols',sum(stats)/len(stats),'top',cnt.most_common(4))
