"""Explicit conditional higher-spin partition pipeline with finite-bit output.

The CLI exercises only a tiny exact tensor fallback. Larger inputs call the
complete imported-theorem count implementation, with enormous explicit caps.
No generic MCMC branch is shortened for an experiment or silently substituted.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,sys,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from spin_projection_transfer import edge_gate,field_gate
from concave_spin_potentials import potential_gate,compile_weighted
from homogeneous_count import Problem,certified_plan,amplified_count


def ceil_fraction(q):
    q=F(q); return (q.numerator+q.denominator-1)//q.denominator


def finite_exp_minus(x,rho):
    """Rational lower approximation to exp(-x), relative error <=rho/8.

    Scaling k=ceil(x) costs NUMERICAL x through the output rational's bit length.
    The odd alternating Taylor sum at x/k<=1 is a certified lower bound.
    """
    x,rho=F(x),F(rho)
    assert x>=0 and 0<rho<=1
    if x==0: return F(1)
    k=max(1,ceil_fraction(x)); y=x/k
    degree=3; factorial=24  # (degree+1)!
    while F(1,factorial)>rho/(24*k):
        degree+=1; factorial*=degree+1
    if degree%2==0: degree+=1
    term=F(1); lower=term
    for j in range(1,degree+1):
        term*=(-y)/j; lower+=term
    assert lower>0
    return lower**k


def compile_instance(spins,edges,b,c,potentials,beta,epsilon):
    """spins are integer q=2S; onsite tables list f(S-r) in charge order."""
    spins=tuple(spins); b=tuple(map(F,b)); c=tuple(map(F,c))
    beta,epsilon=F(beta),F(epsilon)
    assert len(spins)==len(b)==len(c)==len(potentials)
    assert all(isinstance(q,int) and q>=1 for q in spins)
    assert all(x>=0 for x in b) and beta>=0 and 0<epsilon<=1
    blocks=[]; cursor=0
    for q in spins:
        blocks.append(tuple(range(cursor,cursor+q))); cursor+=q
    Q=cursor
    edges=[(int(u),int(v),F(alpha),F(gamma)) for u,v,alpha,gamma in edges]
    assert all(0<=u<len(spins) and 0<=v<len(spins) and u!=v and alpha>=abs(gamma)
               for u,v,alpha,gamma in edges)
    tables=[tuple(map(F,p)) for p in potentials]
    for q,table in zip(spins,tables):
        assert len(table)==q+1
        assert all(2*table[r+1]>=table[r]+table[r+2] for r in range(q-1))
    C0=sum((3*alpha*spins[u]*spins[v]/4 for u,v,alpha,gamma in edges),F(0))
    C0+=sum((F(q,2)*(bv+abs(cv)) for q,bv,cv in zip(spins,b,c)),F(0))
    shifts=[max(abs(f) for f in table) for table in tables]
    C=C0+sum(shifts,F(0)); dimension=1
    for q in spins: dimension*=q+1
    if beta==0 or C==0:
        return {"exact":F(dimension),"dimension":dimension,"Q":Q,"C":C,
                "beta":beta,"epsilon":epsilon}
    tau=2*beta*C
    m=ceil_fraction(max(F(1),4*tau,20*tau*tau/epsilon))
    s=beta/(2*m)
    w0=[]
    for u,v,alpha,gamma in edges:
        if alpha:
            for i in blocks[u]:
                for j in blocks[v]: w0.append(edge_gate((i,j),alpha/4,gamma/4,s))
    for block,bv,cv in zip(blocks,b,c):
        if bv or cv:
            for i in block: w0.append(field_gate(i,bv/2,cv/2,s))
    projections=[potential_gate(block,table,s)[0] for block,table in zip(blocks,tables)]
    # Cyclic trace identity: Tr(G W0 W0* G)^m=Tr(G^2 W0 W0*)^m.
    layer=projections+w0+list(reversed(w0))
    gates=layer*m
    compiler=compile_weighted(Q,gates)
    symmetric=all(cv==0 for cv in c) and all(tuple(reversed(p))==p for p in tables)
    problem=Problem(compiler.n,compiler.degree,compiler.p_coefficient,compiler.q_coefficient,
                    compiler.p_seed,compiler.q_seed,compiler.range_bits,0,symmetric)
    problem.validate()
    return {"compiler":compiler,"problem":problem,"m":m,"s":s,"C":C,
            "beta":beta,"epsilon":epsilon,
            "Q":Q,"dimension":dimension,"self_complementary":symmetric}


def exact_monomial_upper_bound(compiler,cap):
    bound=1
    for factor in compiler.factors:
        local=6 if factor.gate.kind in ("edge","field") else comb(2*len(factor.rows),len(factor.rows))
        bound*=local
        if bound>cap: return None
    return bound


def estimate_partition(instance,beta,epsilon,failure_probability,bit_source,exact_monomial_cap=20000):
    beta,epsilon=F(beta),F(epsilon)
    assert beta==instance["beta"] and epsilon==instance["epsilon"]
    if "exact" in instance:
        return instance["exact"],{"branch":"exact trivial","full_markov_fpras_executed":False}
    compiler=instance["compiler"]
    upper=exact_monomial_upper_bound(compiler,exact_monomial_cap)
    if upper is not None:
        count,work,accepted=compiler.exact_diagnostic_count(cap=exact_monomial_cap)
        branch={"branch":"bounded exact local-factor fallback","monomial_checks":work,"accepted":accepted,
                "full_markov_fpras_executed":False}
    else:
        count=amplified_count(instance["problem"],epsilon/8,failure_probability,bit_source)
        count*=2**compiler.isolated
        branch={"branch":"certified homogeneous count program","full_markov_fpras_executed":True}
    value=count*finite_exp_minus(beta*instance["C"],epsilon/8)
    return value,branch


def diagnostics():
    rng=random.Random(130)
    beta=F(1,100000); epsilon=F(1,100)
    instance=compile_instance((2,1),[(0,1,1,F(1,2))],(0,0),(0,0),[(-1,0,-1),(0,0)],beta,epsilon)
    value,branch=estimate_partition(instance,beta,epsilon,F(1,4),lambda:rng.getrandbits(1))
    assert instance["m"]==1 and instance["self_complementary"]
    assert branch["branch"]=="bounded exact local-factor fallback"
    plan=certified_plan(instance["problem"],epsilon/8)
    # Compare complement oracles on every compiled local-factor monomial.
    c=instance["compiler"]; all_bits=(1<<c.n)-1
    from itertools import product
    for local in product(*[list(f.options()) for f in c.factors]):
        mask=0
        for m,w in local: mask|=m
        assert c.p_coefficient(mask)==c.p_coefficient(all_bits^mask)
    # Rational exponential interval checks against a high-precision standard
    # library reference are diagnostics; the Taylor remainder is the proof.
    from decimal import Decimal,localcontext
    for x in (F(1,100),F(1),F(11,3),F(20)):
        answer=finite_exp_minus(x,F(1,1000))
        with localcontext() as context:
            context.prec=80
            reference=(-Decimal(x.numerator)/Decimal(x.denominator)).exp()
            ratio=(Decimal(answer.numerator)/Decimal(answer.denominator))/reference
            assert 1-Decimal(1)/Decimal(8000)<=ratio<=1
    return {"status":"PASS","scope":"one tiny complete thermal pipeline through exact fallback; generic certified Markov loops NOT executed",
            "physical_interface":"spin1 + spinhalf, alpha=1, gamma=1/2, physical + (S0^z)^2, zero fields",
            "beta":str(beta),"epsilon":str(epsilon),"m":instance["m"],"N":c.n,
            "C":str(instance["C"]),"estimate":str(value),"estimate_float":float(value),
            "branch":branch,"compiled_self_complement_symmetry_checked":True,
            "unused_certified_markov_plan":plan.json()}


if __name__=="__main__":
    result=diagnostics()
    Path(__file__).with_name('higher_spin_pipeline_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
