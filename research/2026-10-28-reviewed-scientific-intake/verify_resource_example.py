"""Independent exact-resource check of the cited rational star, not optimality.

Reads source declarations as evidence, never imports producer certificate code.
All arithmetic is Fraction; checks the stated normalized m=K=1, M=2 model only.
"""
from fractions import Fraction as F
import json

def verify():
    masses = [F(499743221017, 500000000000), F(256778983, 500000000000)]
    springs = [F(1998226783251, 100000000000), F(3763216749, 100000000000)]
    assert all(x > 0 for x in masses + springs)
    assert sum(masses) == 1  # With backbone mass one, total cell mass is two.
    stiffness = sum(springs)
    assert stiffness == F(200199, 10000)
    assert F(1001, 50) - stiffness == F(1, 10000)
    # For relative-CM load (-1,m1,m2) on a positive star, branch force=m_j,
    # branch extension=m_j/k_j; compliance=sum(m_j^2/k_j).
    compliance = sum(m*m/k for m, k in zip(masses, springs))
    assert compliance == F(31332329146138066741147837, 626646708252546322583250000)
    assert compliance < F(1, 20)
    assert stiffness * compliance >= 1
    # The exact joint optimum saturates20.02; this rational strictly feasible
    # example spends20.0199. It must never be relabeled as that exact root.
    assert stiffness != F(1001, 50)
    return {'passed': True, 'scope': 'Exact positive rational parts, mass, stiffness and relative-CM compliance only; no all-band optimality, tolerance, device or advantage verification',
            'model': 'Scalar normalized m=K=1, M=2; relative-CM compliance',
            'total_internal_stiffness': str(stiffness),
            'stiffness_slack_to_20_02': '1/10000',
            'compliance': str(compliance),
            'compliance_below_1_20': True,
            'distinct_from_exact_joint_optimum': True}

if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
