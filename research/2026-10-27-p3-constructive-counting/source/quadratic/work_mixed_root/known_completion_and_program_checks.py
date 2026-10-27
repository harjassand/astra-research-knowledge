#!/usr/bin/env python3
"""Execute the known Kogan completion comparator and the raw XOR/AND compiler.

Kogan's diagonal algorithm is prior work, arXiv:2104.10668 (2021).
Phase sums below use finite exhaustive evaluation, not an asymptotic solver.
"""
from pathlib import Path
import json
import random

from mixed_quadratic_compiler import (
    independent, restrict, matrix_from_edges, finite_phase, exact_original,
)
from diagonal_completion_compiler import off_diagonal, symmetric


def kogan_completion(B):
    """O(n^4) completion, rank at most twice the minimum diagonal rank."""
    n = len(B)
    full = list(B)
    for i in range(n):
        full[i] &= ~(1 << i)
        determinant = int(len(independent(restrict(full,list(range(i+1))))) == i+1)
        full[i] |= (1-determinant) << i
        assert len(independent(restrict(full,list(range(i+1))))) == i+1
    result = [row ^ (1 << i) for i,row in enumerate(full)]
    assert symmetric(result) and off_diagonal(result) == off_diagonal(B)
    return result


def compile_program(n, gates, output, target):
    """Eliminate all affine states, retaining n+6t+1 phase variables."""
    t = sum(gate[0] == 'and' for gate in gates)
    affine = [(1 << i,0) for i in range(n)]
    operands = []
    for gate in gates:
        if gate[0] == 'xor':
            left,right = affine[gate[1]],affine[gate[2]]
            affine.append((left[0]^right[0],left[1]^right[1]))
        elif gate[0] == 'not':
            value = affine[gate[1]]
            affine.append((value[0],value[1]^1))
        elif gate[0] == 'const':
            affine.append((0,gate[1]))
        elif gate[0] == 'and':
            operands.append((affine[gate[1]],affine[gate[2]]))
            affine.append((1 << (n+len(operands)-1),0))
        else:
            raise ValueError(gate[0])
    N = n+6*t+1
    terms = set()

    def toggle(mask):
        if mask in terms:
            terms.remove(mask)
        else:
            terms.add(mask)

    def character_affine(character, expression):
        mask,constant = expression
        for j in range(n+t):
            if mask >> j & 1:
                toggle((1 << character)|(1 << j))
        if constant:
            toggle(1 << character)

    for j,(a,b) in enumerate(operands):
        u,v,w = n+j,n+t+j,n+2*t+j
        alpha,beta,lam = n+3*t+j,n+4*t+j,n+5*t+j
        toggle((1 << alpha)|(1 << v))
        toggle((1 << beta)|(1 << w))
        character_affine(alpha,a)
        character_affine(beta,b)
        toggle((1 << lam)|(1 << u))
        toggle((1 << lam)|(1 << v)|(1 << w))
    value = affine[output]
    character_affine(n+6*t,(value[0],value[1]^target))
    B = [0]*N
    local = []
    for support in sorted(terms):
        if support.bit_count() == 2:
            i = (support & -support).bit_length()-1
            j = (support ^ (1 << i)).bit_length()-1
            B[i] ^= 1 << j
            B[j] ^= 1 << i
        else:
            local.append((support,1))
    assert sum(s.bit_count() == 3 for s,c in local) == t
    return dict(variables=N,quadratic=B,local_terms=local,
                normalization_power=3*t+1,nonlinear_gates=t,
                original_inputs=n,instructions=len(gates))


def evaluate_program(n,gates,output,x):
    states = [(x >> i)&1 for i in range(n)]
    for gate in gates:
        if gate[0] == 'xor':
            states.append(states[gate[1]]^states[gate[2]])
        elif gate[0] == 'not':
            states.append(states[gate[1]]^1)
        elif gate[0] == 'const':
            states.append(gate[1])
        else:
            assert gate[0] == 'and'
            states.append(states[gate[1]]&states[gate[2]])
    return states[output]


def validate():
    comparator_checks = 0
    for n in range(6):
        slots = [(i,j) for i in range(n) for j in range(i)]
        for mask in range(1 << len(slots)):
            B = matrix_from_edges(n,[edge for h,edge in enumerate(slots) if mask >> h & 1])
            D = kogan_completion(B)
            rank = len(independent(D))
            optimum = min(len(independent([row ^ (((diag >> i)&1) << i)
                                           for i,row in enumerate(B)]))
                          for diag in range(1 << n))
            assert optimum <= rank <= 2*optimum
            comparator_checks += 1
    input_results = json.loads(Path(__file__).with_name('diagonal_completion_results.json').read_text())
    profiles = []
    for fixture in input_results['fixtures'][::3]:
        B = fixture['raw_matrix']
        prior = kogan_completion(B)
        profiles.append(dict(n=len(B),mode=fixture['mode'],raw_rank=fixture['raw_matrix_rank'],
            known_completion_rank=len(independent(prior)),
            acquired_completion_rank=fixture['certificate']['low_rank'],
            acquired_residual_edges=fixture['certificate']['residual_edges'],
            acquired_deletions=len(fixture['certificate']['removed'])))
    programs = []
    programs.append((2,[('xor',0,1)],2))
    long_gates = []
    prev = 1
    for _ in range(10000):
        long_gates.append(('xor',prev,0))
        prev = 2+len(long_gates)-1
    long_gates.append(('and',0,prev))
    programs.append((2,long_gates,2+len(long_gates)-1))
    programs.append((3,[('xor',0,1),('and',3,2),('xor',4,1),
                        ('not',5),('and',6,3),('xor',7,0)],8))
    programs.append((4,[('xor',0,3),('xor',1,2),('and',4,5),
                        ('xor',6,0),('not',7),('and',8,4),('xor',9,2)],10))
    records = []
    for n,gates,output in programs:
        for target in (0,1):
            compiled = compile_program(n,gates,output,target)
            direct = sum(evaluate_program(n,gates,output,x) == target for x in range(1 << n))
            phase = exact_original(compiled['quadratic'],compiled['local_terms'],1)[0]
            divisor = 1 << compiled['normalization_power']
            assert phase % divisor == 0
            assert phase//divisor == direct
            records.append(dict(original_inputs=n,instructions=len(gates),target=target,
                phase_variables=compiled['variables'],nonlinear_gates=compiled['nonlinear_gates'],
                cubic_terms=sum(s.bit_count()==3 for s,c in compiled['local_terms']),
                exact_input_count=direct,phase_sum=phase,divisor=divisor,
                quadratic_rank=len(independent(compiled['quadratic'])),
                finite_phase_assignments=1 << compiled['variables']))
    return dict(status='all exact assertions passed',known_completion_checks=comparator_checks,
                known_completion_profiles=profiles,program_count_checks=len(records),
                program_checks=records,
                attribution='Kogan O(n^4) diagonal completion is known prior work; no speed claim',
                backend='all phase sums use finite exhaustive enumeration')


if __name__ == '__main__':
    result = validate()
    Path(__file__).with_name('known_completion_and_program_results.json').write_text(
        json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
