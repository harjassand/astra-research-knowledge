"""Acquired weighted spin-projector coefficients for concave onsite energies.

No counting FPRAS is executed. Uses exact rational coefficients and separately
verifies small contraction identities against direct dense matrices.
"""
from fractions import Fraction as F
from dataclasses import dataclass
from math import comb
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from spin_projection_transfer import (Gate,CompiledCircuit,edge_gate,field_gate,
                                     ceil_log2,circuit_trace)


@dataclass(frozen=True)
class WeightedProjector:
    qubits: tuple
    weights: tuple
    kind: str="projector"

    def __post_init__(self):
        q=len(self.qubits)
        assert len(self.weights)==q+1 and all(w>0 for w in self.weights)
        assert all(self.weights[r+1]**2>=self.weights[r]*self.weights[r+2]
                   for r in range(q-1))

    def entry(self,row,col):
        r=row.bit_count()
        return F(0) if r!=col.bit_count() else self.weights[r]/comb(len(self.qubits),r)

    def range_bits(self):
        return len(self.qubits)+ceil_log2(max(self.weights)/min(self.weights))


def potential_gate(qubits,potential,s):
    """One combined G^2 gate, w_r=(1+s(M+f_r))^2 / binom(q,r)."""
    q=len(qubits); potential=tuple(map(F,potential)); s=F(s)
    assert len(potential)==q+1 and s>=0
    for r in range(q-1):
        if 2*potential[r+1]<potential[r]+potential[r+2]:
            raise ValueError("nonconcave onsite energy table at index %d"%(r+1))
    shift=max(abs(f) for f in potential)
    first=tuple(1+s*(shift+f) for f in potential)
    assert all(x>=1 for x in first)
    assert all(first[r+1]**2>=first[r]*first[r+2] for r in range(q-1))
    return WeightedProjector(tuple(qubits),tuple(w*w for w in first)),shift


def compile_weighted(nqubits,gates):
    circuit=CompiledCircuit(nqubits,gates)
    # The original unweighted constructor assigns the q-bit binomial bound.
    # Acquire the extra positive charge-weight ratio explicitly here.
    circuit.range_bits=sum(f.gate.range_bits() if isinstance(f.gate,WeightedProjector)
                           else f.range_bit_bound() for f in circuit.factors)
    assert circuit.p_coefficient(circuit.p_seed)>0
    return circuit


def checks():
    derivative_checks=0
    for q in range(2,11):
        potential=[F(-r*r,7)+F(2*r,5)-3 for r in range(q+1)]
        for s in (F(0),F(1,17),F(3,2)):
            gate,shift=potential_gate(tuple(range(q)),potential,s)
            weights=gate.weights
            for a in range(q-1):
                b=q-2-a; m=q-a; ell=q-b
                aa=weights[a+2]/comb(q,a+2)
                bb=weights[a+1]/comb(q,a+1)
                cc=weights[a]/comb(q,a)
                det=aa*cc*(m-1)*(ell-1)-bb*bb*m*ell
                assert det<=0
                derivative_checks+=1
    fixtures=[]
    for s in (F(1,7),F(2,11),F(1,100)):
        weighted,shift=potential_gate((0,1),(-2,0,-2),s)
        edge=edge_gate((0,2),F(1,4),F(-1,8),s)
        field=field_gate(2,F(1,3),F(-1,5),s)
        gates=[weighted,edge,field,field,edge]
        compiler=compile_weighted(3,gates)
        polynomial,work,accepted=compiler.exact_diagnostic_count()
        matrix=circuit_trace(gates,3)
        assert matrix==polynomial
        fixtures.append({"s":str(s),"shift":str(shift),"N":compiler.n,
                         "trace":str(matrix),"range_bits":compiler.range_bits,
                         "monomial_checks":work,"accepted":accepted})
    try:
        potential_gate((0,1),(0,-1,0),F(1,10))
    except ValueError:
        nonconcave_rejected=True
    else:
        raise AssertionError("nonconcave potential was not rejected")
    return {"status":"PASS","scope":"exact weighted projector and finite contraction identities, not a full FPRAS run",
            "quadratic_derivative_type_checks":derivative_checks,
            "fixtures":fixtures,"nonconcave_rejected":nonconcave_rejected}


if __name__=="__main__":
    result=checks()
    Path(__file__).with_name('concave_potential_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
