"""Exact incremental algebra acquisition. The learner sees callbacks only."""
from dataclasses import dataclass
import json
from pathlib import Path
import random
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"planning_agent"))
from check_cyclic_exact import F,eye,mm,transpose,cols,rank,solve_columns,add,scale

@dataclass(eq=False)
class Word:
    name:str
    oracle:object=None
    generator:object=None
    parent:object=None

class Learner:
    def __init__(self,n,seed=1974):
        self.n,self.rng=n,random.Random(seed)
        self.basis,self.witnesses,self.caches=[Word("I")],[eye(n)[0]],[{}]
        self.generators,self.pairs=[],{}
        self.calls=self.checks=self.admissions=0
        self.events=[]
    def evaluate(self,w,v,cache):
        # Keep the object itself: cached id(w) can be recycled after a rejected
        # temporary word dies, silently aliasing unrelated operator programs.
        key=w,tuple(v)
        if key in cache:return cache[key]
        if w.name=="I":y=v[:]
        elif w.oracle is not None:
            y=w.oracle(v);self.calls+=1
        else:y=self.evaluate(w.generator,self.evaluate(w.parent,v,cache),cache)
        cache[key]=y
        return y
    def column(self,w):
        return sum([self.evaluate(w,h,c) for h,c in zip(self.witnesses,self.caches)],[])
    def challenge(self):
        self.checks+=1
        radius=1000*(self.checks+1)**2
        return [F(self.rng.randint(-radius,radius)) for _ in range(self.n)]
    def add_or_fit(self,w,purpose):
        old_d=len(self.basis)
        design=[self.column(b) for b in self.basis]
        assert rank(design)==old_d
        coefficients=solve_columns(design,self.column(w))
        reason="old_witness_inconsistent"
        if coefficients is not None:
            h,cache=self.challenge(),{}
            residual=self.evaluate(w,h,cache)[:]
            for c,b in zip(coefficients,self.basis):
                residual=[x-c*y for x,y in zip(residual,self.evaluate(b,h,cache))]
            if not any(residual):
                self.events.append({"purpose":purpose,"candidate":w.name,"outcome":"dependent_fresh_check_passed"})
                return coefficients,False
            self.witnesses.append(h);self.caches.append(cache)
            reason="fresh_witness_exposed_hidden_direction"
        self.basis.append(w)
        assert len(self.basis)<=self.n*self.n
        coefficients=[F(0)]*old_d+[F(1)]
        self.events.append({"purpose":purpose,"candidate":w.name,"outcome":"independent","reason":reason,"dimension":len(self.basis)})
        assert rank([self.column(b) for b in self.basis])==len(self.basis)
        return coefficients,True
    def admit(self,name,callback):
        self.admissions+=1
        w=Word(name,oracle=callback)
        coefficients,independent=self.add_or_fit(w,"external_admission")
        if not independent:return coefficients
        self.generators.append(w)
        while True:
            pending=[(g,i) for g in self.generators for i in range(len(self.basis)) if (id(g),i) not in self.pairs]
            if not pending:break
            g,i=pending[0]
            candidate=Word(f"{g.name}({self.basis[i].name})",generator=g,parent=self.basis[i])
            c,_=self.add_or_fit(candidate,"product_closure")
            self.pairs[id(g),i]=c
        return coefficients
    def representation(self):
        d=len(self.basis)
        evaluation=cols([self.column(w) for w in self.basis])
        metric=mm(transpose(evaluation),evaluation)
        matrices={}
        for g in self.generators:
            columns=[]
            for i in range(d):
                c=self.pairs[id(g),i]
                columns.append(c+[F(0)]*(d-len(c)))
            matrix=cols(columns)
            assert mm(metric,matrix)==mm(transpose(matrix),metric)
            matrices[g.name]=matrix
        return metric,matrices

def run():
    n,identity=4,eye(4)
    p=[[F(0)]*n for _ in range(n)];p[-1][-1]=F(1)
    a=[[F(0)]*n for _ in range(n)]
    for i in range(n):a[i][i]=F(1 if i%2==0 else -1)
    b=[[F(0)]*n for _ in range(n)]
    for i in range(n):b[i][i^1]=F(1)
    learner=Learner(n)
    def action(matrix,v):return [row[0] for row in mm(matrix,cols([v]))]
    assert not any(action(p,learner.witnesses[0]))
    sources=[("P",p),("A",a),("B",b),("A_plus_B",add(a,b)),("two_I",scale(F(2),identity))]
    for name,matrix in sources:learner.admit(name,lambda v,matrix=matrix:action(matrix,v))
    metric,representation=learner.representation()
    d=len(learner.basis)
    assert d==8
    assert len(learner.pairs)==len(learner.generators)*d
    assert any(e.get("reason")=="fresh_witness_exposed_hidden_direction" for e in learner.events)
    acquisition_calls=learner.calls
    direct=[cols([learner.evaluate(w,e,{}) for e in identity]) for w in learner.basis]
    for name,large in sources[:3]:
        small=representation[name]
        for j,basis_matrix in enumerate(direct):
            reconstructed=[[F(0)]*n for _ in range(n)]
            for i in range(d):reconstructed=add(reconstructed,scale(small[i][j],direct[i]))
            assert mm(large,basis_matrix)==reconstructed
    return {"status":"exact_acquired_regular_representation_passed","ambient_dimension":n,
            "final_algebra_dimension":d,"external_admissions":learner.admissions,
            "essential_generators":len(learner.generators),"product_candidates":len(learner.pairs),
            "product_bound":len(learner.generators)*d,"fresh_relation_checks":learner.checks,
            "witness_vectors":len(learner.witnesses),"metric_rank":rank(transpose(metric)),
            "acquisition_source_actions":acquisition_calls,
            "independent_truth_check_source_actions":learner.calls-acquisition_calls,"events":learner.events,
            "qualification":"Exact rational mechanism check; no wall-time or trace-refresh advantage claim."}

if __name__=="__main__":
    result=run()
    Path(__file__).with_name("cumulative_exact_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="events"},indent=2))

