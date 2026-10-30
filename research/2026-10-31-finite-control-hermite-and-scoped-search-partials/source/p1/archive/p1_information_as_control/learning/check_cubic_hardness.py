"""Executable algebra for the cubic affine-direction hardness reduction.

The program does not prove a global numerical minimization result. It checks
the exact Boolean encoding and the cubic derivative identity independently
from an expanded sparse coefficient representation.
"""
from itertools import product
from pathlib import Path
import json
import random


def add_term(poly,indices,value):
    key=tuple(sorted(indices))
    poly[key]=poly.get(key,0)+value
    if poly[key]==0:
        del poly[key]


def multiply_linear(left,right):
    poly={}
    for i,a in left.items():
        for j,b in right.items():
            add_term(poly,(i,j),a*b)
    return poly


def false_form(literal):
    return {0:1,literal:-1} if literal>0 else {-literal:1}


def constraints(n,clauses):
    total=n+len(clauses)
    answer=[]
    for i in range(1,total+1):
        answer.append({(i,i):1,(0,i):-1})
    for j,clause in enumerate(clauses):
        auxiliary=n+j+1
        gate=multiply_linear(false_form(clause[0]),false_form(clause[1]))
        add_term(gate,(0,auxiliary),-1)
        answer.append(gate)
        answer.append(multiply_linear({auxiliary:1},false_form(clause[2])))
    return answer


def evaluate(poly,x):
    return sum(coefficient*product_values(x[i] for i in term)
               for term,coefficient in poly.items())


def product_values(values):
    result=1
    for value in values:
        result*=value
    return result


def gradient(poly,x):
    answer=[0]*len(x)
    for term,coefficient in poly.items():
        for place,i in enumerate(term):
            answer[i]+=coefficient*product_values(x[j] for k,j in enumerate(term) if k!=place)
    return answer


def cubic_from_constraints(quadratics,dimension_v):
    j=len(quadratics); polynomial={(0,0,0):1}
    for k,q in enumerate(quadratics):
        zi=1+k
        add_term(polynomial,(0,zi,zi),3)
        for (a,b),coefficient in q.items():
            add_term(polynomial,(zi,1+j+a,1+j+b),coefficient)
    return polynomial,1+j+dimension_v


def assignment_vector(n,clauses,assignment):
    def false(lit):
        return 1-assignment[lit-1] if lit>0 else assignment[-lit-1]
    auxiliary=[false(c[0])*false(c[1]) for c in clauses]
    satisfies=all(not all(false(lit) for lit in c) for c in clauses)
    return [1]+list(assignment)+auxiliary,satisfies


def main():
    rng=random.Random(20261101)
    clauses=[tuple((i+1)*signs[i] for i in range(3)) for signs in product((-1,1),repeat=3)]
    out=dict(boolean_formulas=0,boolean_assignment_checks=0,affine_direction_checks=0,
             exact_derivative_identity_checks=0,satisfiable_formulas=0,unsatisfiable_formulas=0)
    for subset in product((0,1),repeat=len(clauses)):
        formula=[c for c,use in zip(clauses,subset) if use]
        q=constraints(3,formula); vdim=4+len(formula)
        cubic,dimension=cubic_from_constraints(q,vdim)
        satisfiable=False
        for assignment in product((0,1),repeat=3):
            v,sat=assignment_vector(3,formula,assignment)
            zero=all(evaluate(polynomial,v)==0 for polynomial in q)
            assert zero==sat
            out["boolean_assignment_checks"]+=1
            if sat:
                direction=[0]*(1+len(q))+v
                assert gradient(cubic,direction)==[0]*dimension
                out["affine_direction_checks"]+=1
                satisfiable=True
        out["boolean_formulas"]+=1
        out["satisfiable_formulas" if satisfiable else "unsatisfiable_formulas"]+=1
        base=[rng.randint(-2,2) for _ in range(dimension)]
        direction=[rng.randint(-2,2) for _ in range(dimension)]
        plus=[x+d for x,d in zip(base,direction)]
        minus=[x-d for x,d in zip(base,direction)]
        second=evaluate(cubic,plus)-2*evaluate(cubic,base)+evaluate(cubic,minus)
        derivative=2*sum(g*x for g,x in zip(gradient(cubic,direction),base))
        assert second==derivative
        out["exact_derivative_identity_checks"]+=1
    q=constraints(3,clauses); N=3+len(clauses)
    cubic,dimension=cubic_from_constraints(q,N+1)
    out["unsatisfiable_example"]=dict(original_variables=3,clauses=len(clauses),
        boolean_and_aux_variables=N,quadratic_constraints=len(q),cubic_dimension=dimension,
        sparse_cubic_monomials=len(cubic),maximum_absolute_coefficient=max(map(abs,cubic.values())),
        proved_unit_gradient_lower_bound=1/(384*N),
        proved_Gaussian_directional_curvature_squared_lower_bound=4/(384*N)**2)
    out["status"]="PASS"
    directory=Path(__file__).parent
    (directory/"check_cubic_hardness_results.json").write_text(json.dumps(out,indent=2)+"\n")
    example=dict(clauses=clauses,variable_order="w, z_1..z_J, t, x_1..x_n, a_1..a_m",
                 cubic_coefficients=[dict(indices=term,coefficient=coefficient)
                                     for term,coefficient in sorted(cubic.items())])
    (directory/"cubic_hardness_example.json").write_text(json.dumps(example,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
