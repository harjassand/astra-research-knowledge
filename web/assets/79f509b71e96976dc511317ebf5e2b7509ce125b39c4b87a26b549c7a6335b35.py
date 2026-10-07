"""Exact bounded integration checks; finite diagnostics, not uniform proof."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from math import factorial
from pathlib import Path
import json
import time

from projected_chain import (Gate, ProjectorFactor, ProjectedExchange, CoinTape,
                             TapeAbort, compile_projected_trace, local_gate,
                             enumerate_pairs, sampler_plan, ResourceRefusal,
                             sample_projected, mm)
from higher_order_certificate import (projected_plan, acquire_projected_circuit,
                                      acquire_defects, local_paulis)


class Branch(Exception):
    def __init__(self,p): self.p=p


class PathTape:
    def __init__(self,path): self.path=path; self.cursor=0
    def bernoulli(self,p):
        if p in (0,1): return bool(p)
        if self.cursor==len(self.path): raise Branch(p)
        answer=self.path[self.cursor]; self.cursor+=1; return answer


def chooser_law(chain,u):
    out={}; pending=[((),F(1))]
    while pending:
        path,p = pending.pop()
        try:
            v=chain._choose_mu(u,PathTape(path))
            out[v]=out.get(v,F(0))+p
        except Branch as e:
            pending.extend(((path+(True,),p*e.p),(path+(False,),p*(1-e.p))))
    return out


def projector_candidates():
    cases=0
    for q in range(1,5):
        instance=compile_projected_trace(q,[Gate("projector",tuple(range(q)))])
        z=[F(u+2,u+1) for u in range(2*q)]
        for selected in combinations(range(2*q),q):
            S=set(selected); T=instance.seed()[1]
            for u in S:
                pin_cases=[(frozenset(),)*4]
                if q>1:
                    forced=frozenset(S-{u})
                    absent=next(v for v in range(2*q) if v not in S)
                    pin_cases.append((forced,frozenset({absent}),frozenset(),frozenset()))
                for pins in pin_cases:
                    chain=ProjectedExchange(instance,z=z,pins=pins,state=(S,T))
                    literal=chain.candidates(0,u)
                    Z=sum((w for _,w in literal),F(0))
                    assert chooser_law(chain,u)=={v:w/Z for v,w in literal}
                    cases+=1
    return cases


def literal_kernel(instance,S,T,z,t):
    start=(frozenset(S),frozenset(T)); row={start:F(1)}
    for side,selected,other in ((0,S,T),(1,T,S)):
        weight=instance.mu if side==0 else instance.nu
        for u in selected:
            rest=set(selected)-{u}
            candidates=[(v,z[v]*weight(rest|{v})) for v in range(instance.n) if v not in rest]
            candidates=[(v,w) for v,w in candidates if w>0]
            Z=sum((w for _,w in candidates),F(0))
            scale=(F(1,2) if u in other else t/2)/instance.n
            for v,w in candidates:
                if v==u: continue
                target=(frozenset(rest|{v}),frozenset(T)) if side==0 else (frozenset(S),frozenset(rest|{v}))
                row[target]=row.get(target,F(0))+scale*w/Z
                row[start]-=scale*w/Z
    return row


def finite_projector_certificate():
    instance=compile_projected_trace(2,[Gate("projector",(0,1))])
    states=enumerate_pairs(instance)
    t=F(1,4096); z=[F(1)]*4
    weights,rows={},{}
    for state in states:
        chain=ProjectedExchange(instance,t=t,state=state)
        rows[state]=chain.kernel_row()
        assert rows[state]==literal_kernel(instance,*state,z,t)
        assert min(rows[state].values())>=0 and sum(rows[state].values(),F(0))==1
        weights[state]=chain.supported_weight()
    Z=sum(weights.values(),F(0)); pi=[weights[s]/Z for s in states]
    for s in states:
        for dest,p in rows[s].items():
            assert weights[s]*p==weights[dest]*rows[dest].get(s,F(0))
    gap=t/(2*instance.n)
    A=[[pi[i]*(int(i==j)-rows[s].get(dest,F(0))) -
        gap*(int(i==j)*pi[i]-pi[i]*pi[j]) for j,dest in enumerate(states)] for i,s in enumerate(states)]
    pivots=[]
    for k in range(len(A)):
        pivot=A[k][k]; assert pivot>=0; pivots.append(str(pivot))
        if pivot==0:
            assert all(A[k][j]==0 for j in range(k+1,len(A))); continue
        for i in range(k+1,len(A)):
            for j in range(i,len(A)):
                A[i][j]-=A[i][k]*A[k][j]/pivot; A[j][i]=A[i][j]
    hard=sum((pi[i] for i,(S,T) in enumerate(states) if S.isdisjoint(T)),F(0))
    assert hard>=F(3,4)
    law={0:F(0),1:F(0),2:F(0)}
    for i,(S,T) in enumerate(states):
        if S.isdisjoint(T): law[len(S&{0,1})]+=pi[i]/hard
    assert law=={0:F(1,3),1:F(1,3),2:F(1,3)}
    return {"states":len(states),"gap_lower_bound":gap,"hard_probability":hard,
            "exact_hard_charge_law":law,"psd_pivots":pivots,
            "scope":"24-state projector instance only; independent of imported all-size gap."}


def tree_updates():
    gates=[local_gate("field",(0,),F(1,9),F(1),F(1,3),3),
           local_gate("field",(1,),F(1,9),F(1),F(-1,4),3),
           Gate("projector",(0,1))]
    instance=compile_projected_trace(2,gates)
    chain=ProjectedExchange(instance,z=[F(u+2,u+1) for u in range(instance.n)],t=F(1,5))
    tape=CoinTape(773,64,1000000)
    for j in range(4000):
        if j%71==0: chain.set_field(j%instance.n,F(1+j%7,2+j%5))
        chain.step(tape)
        if j%41:
            continue
        assert instance.mu(chain.S)>0 and instance.nu(chain.T)>0
        for factor, (trees,row_count) in chain.projectors.items():
            f=instance.factors[factor]
            assert row_count==len(chain.S.intersection(f.rows))
            for side,coords in enumerate((f.rows,f.cols)):
                for k,u in enumerate(coords):
                    assert trees[side].nodes[trees[side].leaves+k]==(chain.z[u] if u not in chain.S else 0)
        for group,tree in chain.trees.items():
            for k,u in enumerate(instance.groups[group][0]):
                assert tree.nodes[tree.leaves+k]==(chain.z[u] if u not in chain.T else 0)
    return {"steps":4000,"choices":tape.choices,"bits":tape.bits}


def entry(g,row,col):
    if g.kind=="projector":
        return F(1,comb(len(g.vertices),row.bit_count())) if row.bit_count()==col.bit_count() else F(0)
    return F(g.table[row][col])


def embed(g,Q):
    d=1<<Q; outside=set(range(Q))-set(g.vertices)
    return [[entry(g,sum(((i>>v)&1)<<k for k,v in enumerate(g.vertices)),
                       sum(((j>>v)&1)<<k for k,v in enumerate(g.vertices)))
             if all(((i^j)>>v)&1==0 for v in outside) else F(0) for j in range(d)] for i in range(d)]


def exact_trace(instance,gates,cap=100000):
    work=1
    for f in instance.factors: work*=comb(2*f.q,f.q) if isinstance(f,ProjectorFactor) else len(f.table)
    if work>cap: raise ValueError("hard diagnostic tuple cap exceeded before expansion")
    local=[]
    for f in instance.factors:
        options=(combinations(f.coordinates,f.q) if isinstance(f,ProjectorFactor) else
                 ({u for j,u in enumerate(f.coordinates) if m>>j&1} for m in f.table))
        local.append([(frozenset(S),f.weight(S)) for S in options])
    value=F(0); accepted=0; U=frozenset(range(instance.n))
    for parts in product(*local):
        S=frozenset().union(*(p[0] for p in parts))
        if instance.nu(U-S):
            w=F(1)
            for _,c in parts: w*=c
            value+=w; accepted+=1
    Q=instance.qubits; matrix=[[F(i==j) for j in range(1<<Q)] for i in range(1<<Q)]
    for g in gates: matrix=mm(matrix,embed(g,Q))
    trace=sum((matrix[i][i] for i in range(1<<Q)),F(0))
    value*=2**instance.inactive_qubits
    assert value==trace
    return {"ground_size":instance.n,"tuples":work,"accepted":accepted,"trace":trace}


def integration_traces():
    outputs=[]
    for degree in (2,3,4):
        # Symmetric two-constituent field is a physical spin-1 generator.
        forward=[local_gate("field",(v,),F(1,7),F(1,6),F(0),degree) for v in (0,1)]
        gates=forward+list(reversed(forward))+[Gate("projector",(0,1))]
        outputs.append({"degree":degree,**exact_trace(compile_projected_trace(2,gates),gates)})
    forward=[local_gate("edge",(v,2),F(1,7),F(1,4),F(-1,8),3) for v in (0,1)]
    gates=forward+list(reversed(forward))+[Gate("projector",(0,1)),Gate("projector",(2,))]
    outputs.append({"degree":3,"physical_model":"spin1/spinhalf",**exact_trace(compile_projected_trace(3,gates),gates)})
    return outputs


def higher_order_plans():
    results=[]
    for degree in (2,3,4):
        for order in (3,4):
            plan=projected_plan([2,1],[(0,1,F(1),F(-1,2))],[(0,F(1,3),F(0))],F(1,2),F(1,10),degree,order)
            instance,gates=acquire_projected_circuit(plan,coordinate_cap=20000)
            assert instance.complement_symmetric()
            sample=sampler_plan(instance)
            plan["sampler_plan"]=sample
            try:
                sample_projected(instance,plan["qsets"],max_steps=10000000)
                raise AssertionError("interacting sampler should refuse admission")
            except ResourceRefusal:
                plan["sampling_admission"]="REFUSED_BEFORE_RANDOM_WORK"
            results.append(plan)
    return results


def dense_defect_check():
    """Independent dense polynomial recurrence versus Pauli acquisition."""
    edges=[(0,1,F(1),F(1,2)),(1,2,F(2,3),F(-1,3))]
    fields=[(0,F(1,4),F(0)),(2,F(1,3),F(0))]
    Q=3; d=1<<Q
    I=[[F(i==j) for j in range(d)] for i in range(d)]
    Z=[[F(0) for _ in range(d)] for _ in range(d)]
    def add(A,B): return [[A[i][j]+B[i][j] for j in range(d)] for i in range(d)]
    def scale(A,s): return [[s*A[i][j] for j in range(d)] for i in range(d)]
    terms=[]
    for u,v,a,g in edges:
        A=((3*a+g,0,0,0),(0,3*a-g,2*a,0),(0,2*a,3*a-g,0),(0,0,0,3*a+g))
        terms.append(embed(Gate("edge",(u,v),A),Q))
    for v,b,c in fields:
        r=b+abs(c); terms.append(embed(Gate("field",(v,),((r+c,b),(b,r-c))),Q))
    checks=0; summaries=[]
    for degree in (2,3,4):
        coefficients=[I]+[Z for _ in range(4)]
        for A in terms+list(reversed(terms)):
            poly=[I]
            power=I
            for k in range(1,min(degree,4)+1):
                power=mm(power,A); poly.append(scale(power,F(1,factorial(k))))
            new=[Z for _ in range(5)]
            for k in range(5):
                for j in range(min(degree,k)+1): new[k]=add(new[k],mm(coefficients[k-j],poly[j]))
            coefficients=new
        S=coefficients[1]; powers=[I]
        for k in range(1,5): powers.append(mm(powers[-1],S))
        defects,bounds,cost=acquire_defects(edges,fields,degree,4)
        for k in (3,4):
            dense=add(coefficients[k],scale(powers[k],F(-1,factorial(k))))
            reconstruction=[[F(0) for _ in range(d)] for _ in range(d)]
            for (x,z),(real,imag) in defects[k].items():
                assert imag==0 and (x&z).bit_count()%2==0
                sign=(-1)**((x&z).bit_count()//2)
                for bit in range(d): reconstruction[bit^x][bit]+=real*sign*(-1)**((z&bit).bit_count())
            assert reconstruction==dense; checks+=1
        summaries.append({"degree":degree,"defect_l1_bounds":bounds,"nonzero_keys":{k:len(v) for k,v in defects.items()},"acquisition_cost":cost})
    assert summaries[1]["defect_l1_bounds"][3]>0
    assert summaries[1]["defect_l1_bounds"][3]==summaries[2]["defect_l1_bounds"][3]
    return {"exact_dense_Pauli_matches":checks,"summaries":summaries,
            "nonzero_generic_Strang_cubic_after_Taylor_degree3":True}


if __name__=="__main__":
    started=time.monotonic()
    output={"status":"PASS_EXACT_FINITE_INTEGRATION","projector_choice_cases":projector_candidates(),
            "finite_projector_certificate":finite_projector_certificate(),"tree_updates":tree_updates(),
            "trace_identities":integration_traces(),"higher_order_plans":higher_order_plans(),
            "independent_dense_defect_check":dense_defect_check()}
    output["elapsed_seconds"]=time.monotonic()-started
    output["scope"]="Bounded finite checks plus algebraic certificates. No general-source proof or empirical TV validation."
    Path(__file__).with_name("checks.json").write_text(json.dumps(output,indent=2,default=str)+'\n')
    print(json.dumps({"status":output["status"],"projector_choice_cases":output["projector_choice_cases"],
                      "trace_identities":output["trace_identities"],"plans":[
                          {k:p[k] for k in ("degree","certificate_order","m","ground_size","log_error_bound","defect_l1_bounds","sampling_admission")}
                          for p in output["higher_order_plans"]],"elapsed_seconds":output["elapsed_seconds"]},indent=2,default=str))
