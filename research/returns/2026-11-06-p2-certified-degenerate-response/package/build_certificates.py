"""Produce exact finite certificates; numerical displays are not proof inputs."""
import json
from pathlib import Path
from exact_response import *

ROOT = Path(__file__).resolve().parent


def save(name, value):
    (ROOT/name).write_text(json.dumps(serializable(value), indent=2)+'\n')


def laminate(j):
    # I_j=(2^-j,2^(1-j)], a_j=j (odd j), 1/j (even j).
    return Q(j) if j % 2 else Q(1, j)


def laminate_certificate(j):
    mass = Q(1, 2**j)
    a_prefix = sum((Q(1, 2**i)*laminate(i) for i in range(1, j+1)), Q(0))
    i_prefix = sum((Q(1, 2**i)/laminate(i) for i in range(1, j+1)), Q(0))
    odd_mass = Q(2, 3)-sum((Q(1, 2**i) for i in range(1, j+1, 2)), Q(0))
    even_mass = Q(1, 3)-sum((Q(1, 2**i) for i in range(2, j+1, 2)), Q(0))
    odd_linear = Q(10, 9)-sum((Q(i, 2**i) for i in range(1, j+1, 2)), Q(0))
    even_linear = Q(8, 9)-sum((Q(i, 2**i) for i in range(2, j+1, 2)), Q(0))
    tail_a = odd_linear+even_mass/Q(j+1)
    tail_i = even_linear+odd_mass/Q(j+1)
    assert tail_a+tail_i == Q(j, 2**j)+mass*(2+Q(1,j+1))
    h = 1/(i_prefix+mass)
    lower1 = 2*h-h*h*(i_prefix+tail_i)
    upper1 = h*h*(i_prefix+tail_a)
    lower2 = a_prefix+2*mass-tail_i
    upper2 = a_prefix+tail_a
    gap1, gap2 = upper1-lower1, upper2-lower2
    assert gap1 >= 0 and gap2 >= 0
    # A posteriori certificates for d=2, mu1=M/tau=8.
    tensor_target = Q(1, 10**6)
    assert 2*8*max(gap1, gap2) <= tensor_target**2
    b2_mean = a_prefix+mass
    return dict(
        family='alternating_dyadic_laminate', dimension=2,
        coefficient='A(x)=a(x_1) I; a=j on I_j for odd j, 1/j for even j',
        interval='I_j=(2^(-j),2^(1-j)]',
        tau=Q(1,4), exponential_moment_upper=Q(2),
        moment_proof='sum_j 2^(-j) exp(j/4)<sum_j (2/3)^j=2; exp(1/4)<4/3',
        truncation_index=j, tail_mass=mass,
        input_L1_error_upper=Q(j+3,2**j),
        prefix_a=a_prefix, prefix_inverse_a=i_prefix,
        tail_a_lower=odd_linear, tail_a_upper=tail_a,
        tail_inverse_a_lower=even_linear, tail_inverse_a_upper=tail_i,
        first_loading=dict(trial_electric='E=(h/a_J,0)',
            trial_flux='B=(h,0)', h=h, lower=lower1, upper=upper1, gap=gap1),
        second_loading=dict(trial_electric='E=(0,1)',
            trial_flux='B=(0,a_J)', lower=lower2, upper=upper2, gap=gap2),
        tensor_approximation=[[h,Q(0)],[Q(0),b2_mean]],
        tensor_operator_error_upper=tensor_target,
        exact_tensor_reference='diag(1/(8/9+(log 3)/2),10/9+(log(4/3))/2)',
        proof_input='Analytic dyadic series and rational tail bounds; no logarithm oracle')


def main():
    d = 2
    vals = {p:[[Q(1+p[0]),Q(0)],[Q(0),Q(1+p[0])]]
            for p in product(range(2), repeat=2)}
    a = StepField(2, 1, vals)
    calls = []
    def name(n):
        calls.append(n)
        return a
    result = certified_solve(name, Q(1,4), Q(2), [1,0], Q(1,4), max_stages=8)
    assert result['lower'] <= Q(4,3) <= result['upper']
    result.update(family='two_phase_exact_grid', exact_minimum=Q(4,3),
                  name_precision_requests=calls, name_error=Q(0))
    save('FINITE_GRID_CERTIFICATE.json', result)

    amat = [[Q(2),Q(1)],[Q(1),Q(2)]]
    a2 = StepField(2,0,{(0,0):amat})
    f2 = StepField(2,1,{p:([Q(1),Q(2)] if p[0]==0 else [Q(-1),Q(1)])
                         for p in product(range(2),repeat=2)})
    forced = certified_solve(lambda n:a2,Q(1,4),Q(3),[Q(1,2),0],Q(1,2),
                             source=f2,max_stages=10)
    assert forced['lower'] <= 0 <= forced['upper']
    forced.update(family='off_diagonal_with_source',exact_minimum=Q(0))
    save('FORCED_PROBLEM_CERTIFICATE.json',forced)

    exact = [[Q(2),Q(1,2)],[Q(1,2),Q(1)]]
    def perturbed(n):
        err=Q(1,2**n)
        s=[[exact[0][0]+err,exact[0][1]],
           [exact[1][0],exact[1][1]-err]]
        return StepField(2,0,{(0,0):s},err)
    c, pars = inverse_name(perturbed,8,Q(1,4),Q(3))
    ref = inverse(exact)
    row_bound=max(sum((abs(ref[i][j]-c.values[(0,0)][i][j]) for j in range(2)),Q(0))
                  for i in range(2))
    assert row_bound<=c.error<=Q(1,256)
    save('INVERSE_FILTER_CERTIFICATE.json',dict(
         coefficient=exact,parameters=pars,certified_L1_error=c.error,
         inverse_approximant=c.values[(0,0)],exact_inverse=ref,
         actual_operator_error_upper=row_bound,
         perturbation='2^(-s) diag(1,-1); does not commute with A'))
    save('UNBOUNDED_LAMINATE_CERTIFICATE.json',laminate_certificate(50))
    print(json.dumps(dict(
        finite_grid=dict(stage=result['stage'],mesh=result['mesh_level'],
                         lower=float(result['lower']),upper=float(result['upper'])),
        forced=dict(stage=forced['stage'],mesh=forced['mesh_level'],
                    lower=float(forced['lower']),upper=float(forced['upper'])),
        inverse_filter=dict(source_precision=pars['source_precision'],k=pars['k'],
                            error=float(c.error)),
        laminate=dict(J=50,first_gap=float(laminate_certificate(50)['first_loading']['gap']),
                      second_gap=float(laminate_certificate(50)['second_loading']['gap']))),indent=2))


if __name__=='__main__':
    main()
