"""Competent exact comparator for admitted small constituent count only.

This is explicitly exponential in Q. It checks physical charge readout and
does not claim the large-Q imported polynomial counting result.
"""
from fractions import Fraction as F
from pathlib import Path
import time,json
from higher_order_certificate import projected_plan,acquire_projected_circuit
from projected_chain import Gate,local_gate,mm,CoinTape,sampler_plan
from check_projected import embed


def matrix_product(Q,gates):
    matrix=[[F(i==j) for j in range(1<<Q)] for i in range(1<<Q)]
    for g in gates: matrix=mm(matrix,embed(g,Q))
    return matrix


def exact_comparator(plan,*,constituent_cap=8,gate_cap=200,seed=20261007):
    Q=plan["constituents"]
    if Q>constituent_cap or plan["Hamiltonian_gate_occurrences"]+plan["projector_occurrences"]>gate_cap:
        raise ValueError("exact comparator admission exceeded before dense allocation")
    started=time.monotonic()
    instance,gates=acquire_projected_circuit(plan,coordinate_cap=10000)
    forward=[local_gate("edge",(u,v),plan["s"],a,g,plan["degree"]) for u,v,a,g in plan["embedded_edges"]]
    forward += [local_gate("field",(v,),plan["s"],b,c,plan["degree"]) for v,b,c in plan["embedded_fields"]]
    Pi=matrix_product(Q,[Gate("projector",tuple(qs)) for qs in plan["qsets"]])
    B0=matrix_product(Q,forward+list(reversed(forward)))
    Bphys=mm(mm(Pi,B0),Pi)
    compressed=[[F(i==j) for j in range(1<<Q)] for i in range(1<<Q)]
    for _ in range(plan["m"]): compressed=mm(compressed,Bphys)
    raw=matrix_product(Q,gates)
    Z=sum((compressed[i][i] for i in range(1<<Q)),F(0))
    assert Z>0 and Z==sum((raw[i][i] for i in range(1<<Q)),F(0))
    laws=[]
    for matrix in (raw,compressed):
        weights={}
        for i in range(1<<Q):
            charge=tuple(len(qs)-2*sum((i>>v)&1 for v in qs) for qs in plan["qsets"])
            assert matrix[i][i]>=0
            weights[charge]=weights.get(charge,F(0))+matrix[i][i]/Z
        laws.append(weights)
    assert laws[0]==laws[1]
    # Constituent marginals need not be physical at this cut; only charges are.
    different_constituent_diagonal=any(raw[i][i]!=compressed[i][i] for i in range(1<<Q))
    witness=next(({"constituent_basis_integer":i,"raw_cut_diagonal":str(raw[i][i]),
                   "compressed_physical_diagonal":str(compressed[i][i])} for i in range(1<<Q)
                  if raw[i][i]!=compressed[i][i]),None)
    law=laws[1]
    tape=CoinTape(seed,64,100)
    outcomes=sorted(law)
    choice=tape.categorical([(j,law[c]) for j,c in enumerate(outcomes)])
    elapsed=time.monotonic()-started
    def height(x): return max(x.numerator.bit_length(),x.denominator.bit_length())
    return {"status":"PASS_EXACT_BOUNDED_Q_COMPARATOR","Q":Q,"matrix_dimension":1<<Q,
            "matrix_entries":1<<(2*Q),"layers":plan["m"],"Taylor_degree":plan["degree"],
            "ground_size":instance.n,"exact_trace":str(Z),
            "charge_probabilities":[{"twice_Sz":c,"probability":str(law[c])} for c in outcomes],
            "raw_cut_charge_law_equals_compressed_physical_law":True,
            "raw_constituent_diagonal_differs":different_constituent_diagonal,
            "constituent_readout_counterexample":witness,
            "sampled_twice_Sz":outcomes[choice],"coin_choices":tape.choices,"coin_bits":tape.bits,
            "max_compressed_entry_operand_bits":max(height(x) for row in compressed for x in row),
            "elapsed_seconds":elapsed,"polynomial_sampler_plan":sampler_plan(instance),
            "scope":"Exact sampler for rational projected transfer at Q<=8; exponential dense comparator. Not exact Gibbs at nonzero temperature; log-generator approximation error still applies. Seeded replay, fair-bit theorem conditional on no cap abort."}


if __name__=="__main__":
    plan=projected_plan([2,1],[(0,1,F(1),F(-1,2))],[(0,F(1,3),F(0))],F(1,2),F(1,10),3,4)
    result=exact_comparator(plan)
    Path(__file__).with_name("small_comparator.json").write_text(json.dumps(result,indent=2,default=str)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ("charge_probabilities","exact_trace","polynomial_sampler_plan")},indent=2,default=str))
