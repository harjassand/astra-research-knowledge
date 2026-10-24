#!/usr/bin/env python3
"""Private clocked statistical fixture. Only noisy reads/update calls are exposed.

The source chooses unknown local response tables. The native initial field is
zero in this replay fixture; the learner is not given it or an initializer.
No source parameters, sensor truth, contexts, or response probabilities are
returned through the acquisition API. Random.binomialvariate aggregates actual
read noise; every represented raw sensor read/hold tick is charged.
"""
from fractions import Fraction
from itertools import combinations
from random import Random


class LocalPlant:
    def __init__(self,seed,sites=1001):
        self._rng=Random(seed)
        self._sites=sites
        params=Random(seed+7919)
        self._good={i: params.choice(("a","b")) for i in range(-(sites//2),sites//2+1)}
        self._base={i: params.randrange(35,46) for i in self._good}
        self._state={}
        self.site_updates=0
        self.update_rounds=0
        self.sensor_reads=0
        self.hold_read_ticks=0
        self.full_initializer_calls=0

    def _bit(self,i):
        return self._state.get(i,0)

    def _prob100(self,i,a,old):
        left,center,right=(old.get(j,0) for j in (i-1,i,i+1))
        if a == "c":
            return 10+80*(left ^ center ^ right)
        if a not in ("a","b"):
            raise ValueError(a)
        if a == self._good[i]:
            return self._base[i]+4*(left+center+right)
        return 1+98*center

    def read_counts(self,sites,repetitions):
        result=[]
        for i in sites:
            flips=self._rng.binomialvariate(repetitions,.1)
            result.append(repetitions-flips if self._bit(i) else flips)
        self.sensor_reads += repetitions*len(sites)
        self.hold_read_ticks += repetitions*len(sites)
        return result

    def parallel_update(self,modes):
        old=self._state.copy()
        changed={i: int(self._rng.randrange(100)<self._prob100(i,a,old)) for i,a in modes.items()}
        self._state.update(changed)
        self.site_updates += len(modes)
        self.update_rounds += 1

    def local_future_program(self,name):
        if name == "unmeasured_c":
            self.parallel_update({0:"c"})
        elif name == "local_feedback_c":
            first=self.read_counts([0],1)[0]
            self.parallel_update({0:"c" if first else "a"})
        else:
            raise ValueError(name)
        return self.read_counts([0],1)[0]

    def counters(self):
        return {"site_updates":self.site_updates,"update_rounds":self.update_rounds,
                "raw_sensor_reads":self.sensor_reads,"native_hold_read_ticks":self.hold_read_ticks,
                "full_initializer_calls":self.full_initializer_calls}


# Private post-execution evaluator. Sparse polynomials are evaluated only
# after acquisition and future experiments. No closure/grammar reaches learner.
def multiply(p,q):
    out={}
    for x,c in p.items():
        for y,d in q.items():
            z=x|y
            out[z]=out.get(z,Fraction(0))+c*d
    return {x:c for x,c in out.items() if c}


def add(*polys):
    out={}
    for p in polys:
        for x,c in p.items():
            out[x]=out.get(x,Fraction(0))+c
    return {x:c for x,c in out.items() if c}


def scale(p,a):
    return {x:c*a for x,c in p.items() if c*a}


def post_execution_reference(plant,certificate,contract):
    b=contract["guard"]
    modes=certificate["selected_public_modes"]
    empty=frozenset()
    variables=[frozenset(s) for k in range(4) for s in combinations(b,k)]
    local={}
    for i in b:
        if modes[str(i)] == plant._good[i]:
            local[i]={empty:Fraction(plant._base[i],100)}
            for j in (i-1,i,i+1):
                if j in b:
                    local[i][frozenset((j,))]=Fraction(1,25)
        else:
            local[i]={empty:Fraction(1,100),frozenset((i,)):Fraction(49,50)}
    transform={}
    for s in variables:
        p={empty:Fraction(1)}
        for i in s:
            p=multiply(p,local[i])
        transform[s]=p
    # Reference is guard preparation applied to the actual all-zero initial
    # field of this fixture. It is not a learner-provided state sampler.
    moments={s:Fraction(int(not s)) for s in variables}
    for _ in range(contract["preparation_rounds"]):
        moments={s:sum(c*moments[u] for u,c in p.items()) for s,p in transform.items()}
    xs=[{frozenset((i,)):Fraction(1)} for i in (-1,0,1)]
    parity=add(*xs,*(scale(multiply(xs[i],xs[j]),Fraction(-2))
                            for i,j in combinations(range(3),2)),
               scale(multiply(multiply(xs[0],xs[1]),xs[2]),Fraction(4)))
    pc=add({empty:Fraction(1,10)},scale(parity,Fraction(4,5)))
    if modes["0"] == "a":
        # Source mode a can be either good or bad; evaluator uses truth.
        pa=local[0]
    elif plant._good[0] == "a":
        pa={empty:Fraction(plant._base[0],100)}
        for x in xs:
            pa=add(pa,scale(x,Fraction(1,25)))
    else:
        pa={empty:Fraction(1,100),frozenset((0,)):Fraction(49,50)}
    first=add({empty:Fraction(1,10)},scale(xs[1],Fraction(4,5)))
    feedback=add(multiply(first,pc),multiply(add({empty:Fraction(1)},scale(first,Fraction(-1))),pa))
    program={"unmeasured_c":pc,"local_feedback_c":feedback}
    means={name:Fraction(1,10)+Fraction(4,5)*sum(c*moments[s] for s,c in p.items())
           for name,p in program.items()}
    cone_joint=[]
    for z in range(8):
        ones={i for bit,i in enumerate((-1,0,1)) if z & (1 << bit)}
        zeros=[i for bit,i in enumerate((-1,0,1)) if not z & (1 << bit)]
        probability=sum((-1)**len(extra)*moments[frozenset(ones|set(extra))]
                        for k in range(len(zeros)+1) for extra in combinations(zeros,k))
        cone_joint.append(probability)
    return {"reference_event_probabilities":means,
            "selected_modes_all_actual_good":all(modes[str(i)]==plant._good[i] for i in b),
            "actual_selected_max_row_influence":Fraction(3,25),
            "source_parameter_or_model_closure_given_to_learner":False,
            "reference_scope":"guard kernel on actual fixture initial zero field; scorer only",
            "global_native_cells_in_fixture":plant._sites,
            "global_hankel_rank_bound_supplied_to_learner":False,
            "reference_cone_configuration_probabilities":cone_joint,
            "private_evaluator_moments":len(moments)}
