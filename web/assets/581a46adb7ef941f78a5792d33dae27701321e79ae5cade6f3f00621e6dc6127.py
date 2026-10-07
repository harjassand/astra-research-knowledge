"""Acquire low-degree Pauli defects and a rational remainder certificate.

Positive Taylor degree improves local truncation, not generic Strang order.
No dense 2**Q matrix; cost counters and admission precede expansion.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"001"))
from pauli_order_certificate import (local_paulis, pmul, padd, pscale, ONE)
from projected_chain import Gate, local_gate, compile_projected_trace


def acquire_defects(edges, fields, degree=2, order=4, *, term_cap=12, key_cap=4096):
    if not 2 <= degree <= 12 or not 3 <= order <= 4:
        raise ValueError("Taylor/certificate order admission")
    terms = local_paulis(edges,fields)
    if len(terms) > term_cap:
        raise ValueError("term cap exceeded before polynomial acquisition")
    counters = {"dictionary_multiplications":0,"Pauli_pair_products":0,"peak_keys":1}
    def multiply(a,b):
        counters["dictionary_multiplications"] += 1
        counters["Pauli_pair_products"] += len(a)*len(b)
        result = pmul(a,b,key_cap=key_cap)
        counters["peak_keys"] = max(counters["peak_keys"],len(result))
        return result
    identity = {(0,0):ONE}
    coefficients = [identity]+[{} for _ in range(order)]
    local_polys = []
    for A in terms:
        powers = [identity]
        for k in range(1,min(degree,order)+1):
            powers.append(multiply(powers[-1],A))
        local_polys.append([pscale(v,F(1,factorial(k))) for k,v in enumerate(powers)])
    for poly in local_polys + list(reversed(local_polys)):
        new = [{} for _ in range(order+1)]
        for k in range(order+1):
            for j in range(min(len(poly)-1,k)+1):
                new[k] = padd(new[k],multiply(coefficients[k-j],poly[j]))
                counters["peak_keys"] = max(counters["peak_keys"],len(new[k]))
                if len(new[k]) > key_cap:
                    raise ValueError("accumulated Pauli key cap exceeded")
        coefficients = new
    S = coefficients[1]
    powers = [identity]
    for k in range(1,order+1): powers.append(multiply(powers[-1],S))
    assert coefficients[2] == pscale(powers[2],F(1,2))
    defects, bounds = {}, {}
    for k in range(3,order+1):
        defect = padd(coefficients[k],pscale(powers[k],F(-1,factorial(k))))
        counters["peak_keys"] = max(counters["peak_keys"],len(defect))
        assert all(imag == 0 for _,imag in defect.values())
        defects[k] = defect
        bounds[k] = sum((abs(real) for real,_ in defect.values()),F(0))
    return defects,bounds,counters


def error_bound(beta,tau,m,bounds):
    beta,tau = F(beta),F(tau)
    K = max(bounds)
    delta = tau/m
    if delta >= K+2:
        raise ValueError("geometric tail ratio must be <1")
    explicit = sum((beta**k * L / (2**k * m**(k-1)) for k,L in bounds.items()),F(0))
    # Both product and exponential degree tails are dominated by exp(delta).
    tail = 2*tau**(K+1)/(factorial(K+1)*m**K*(1-delta/F(K+2)))
    return explicit+tail


def minimum_layers(beta,tau,error,bounds):
    beta,tau,error = F(beta),F(tau),F(error)
    if beta < 0 or tau < 0 or not 0 < error <= 1:
        raise ValueError("invalid plan")
    lower = max(1,int(tau/(max(bounds)+2))+1)
    upper = lower
    while error_bound(beta,tau,upper,bounds) > error/4:
        upper *= 2
    lo,hi = lower,upper
    while lo < hi:
        mid = (lo+hi)//2
        if error_bound(beta,tau,mid,bounds) <= error/4: hi=mid
        else: lo=mid+1
    assert error_bound(beta,tau,lo,bounds) <= error/4
    return lo


def high_spin_terms(qvalues, edges, fields, *, constituent_cap=100000, term_cap=12):
    if not qvalues or any(not isinstance(q,int) or q<1 for q in qvalues):
        raise ValueError("explicit positive constituent counts required")
    if sum(qvalues)>constituent_cap:
        raise ValueError("constituent admission exceeded before allocation")
    planned_terms=0
    for u,v,a,g in edges:
        if not 0<=u<len(qvalues) or not 0<=v<len(qvalues) or u==v or F(a)<abs(F(g)):
            raise ValueError("allowed site edge required")
        if F(a): planned_terms+=qvalues[u]*qvalues[v]
    for v,b,c in fields:
        if not 0<=v<len(qvalues) or F(b)<0:
            raise ValueError("allowed site field required")
        if F(b) or F(c): planned_terms+=qvalues[v]
    if planned_terms>term_cap:
        raise ValueError("embedded term admission exceeded before constituent expansion")
    qsets,cursor = [],0
    for q in qvalues:
        qsets.append(tuple(range(cursor,cursor+q))); cursor+=q
    embedded_edges,embedded_fields = [],[]
    seen = set()
    for u,v,a,g in edges:
        a,g = F(a),F(g)
        if not 0 <= u < len(qsets) or not 0 <= v < len(qsets) or u==v or a<abs(g):
            raise ValueError("allowed site edge required")
        if tuple(sorted((u,v))) in seen:
            raise ValueError("combine parallel edges explicitly")
        seen.add(tuple(sorted((u,v))))
        if a:
            embedded_edges.extend((x,y,a/4,g/4) for x in qsets[u] for y in qsets[v])
    for v,b,c in fields:
        b,c = F(b),F(c)
        if not 0 <= v < len(qsets) or b<0:
            raise ValueError("allowed site field required")
        if b or c: embedded_fields.extend((x,b/2,c/2) for x in qsets[v])
    return qsets,embedded_edges,embedded_fields


def projected_plan(qvalues,edges,fields,beta,error,degree=2,order=4,*,term_cap=12,key_cap=4096):
    qsets,ee,ff = high_spin_terms(qvalues,edges,fields,term_cap=term_cap)
    C = 3*sum((a for _,_,a,_ in ee),F(0))+sum((b+abs(c) for _,b,c in ff),F(0))
    tau = 2*F(beta)*C
    defects,bounds,cost = acquire_defects(ee,ff,degree,order,term_cap=term_cap,key_cap=key_cap)
    m = minimum_layers(beta,tau,error,bounds)
    p,Q = len(ee)+len(ff),sum(qvalues)
    return {"degree":degree,"certificate_order":order,"beta":F(beta),"error":F(error),
            "qvalues":qvalues,"qsets":qsets,"C":C,"tau":tau,"m":m,"s":F(beta)/(2*m),
            "embedded_edges":ee,"embedded_fields":ff,"local_terms":p,"constituents":Q,
            "Hamiltonian_gate_occurrences":2*m*p,"projector_occurrences":m*len(qvalues),
            "ground_size":8*m*p+2*m*Q,"log_error_bound":error_bound(beta,tau,m,bounds),
            "defect_l1_bounds":bounds,"defect_nonzero_keys":{k:len(d) for k,d in defects.items()},
            "acquisition_cost":cost,"admission":{"term_cap":term_cap,"key_cap":key_cap},
            "scope":"Operator bound internally derived; actual counting/mixing remains source-conditional."}


def acquire_projected_circuit(plan,*,coordinate_cap=100000):
    if plan["ground_size"] > coordinate_cap:
        raise ValueError("circuit admission exceeded before allocation")
    s = plan["s"]
    forward = [local_gate("edge",(u,v),s,a,g,plan["degree"]) for u,v,a,g in plan["embedded_edges"]]
    forward += [local_gate("field",(v,),s,b,c,plan["degree"]) for v,b,c in plan["embedded_fields"]]
    projectors = [Gate("projector",tuple(qs)) for qs in plan["qsets"]]
    gates = (forward+list(reversed(forward))+projectors)*plan["m"]
    instance = compile_projected_trace(plan["constituents"],gates,coordinate_cap=coordinate_cap)
    assert instance.n == plan["ground_size"]
    return instance,gates
