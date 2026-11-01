"""Exact generic-gap and finite-state audits of the all-order cost construction.

Sparse symbolic polynomials are integer dictionaries of square-free monomials.
No symbolic algebra dependency is required.  These are discriminating checks;
the ordinary coefficient-count proof is in the parent/interacting proof files.
"""

from collections import defaultdict
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json


def alternating_polynomial(gaps, degree):
    result = defaultdict(int)
    for indices in combinations(range(len(gaps)), degree):
        if any((indices[j+1]-indices[j]) % 2 == 0 for j in range(degree-1)):
            continue
        term = {0: 1}
        for i in indices:
            product = defaultdict(int)
            for left, a in term.items():
                for right, b in gaps[i].items():
                    assert not left & right
                    product[left | right] += a*b
            term = product
        for mask, value in term.items():
            result[mask] += value
    return dict(result)


def polynomial_check(count):
    gaps = [{1 << i: 1} for i in range(count)]
    cubic = alternating_polynomial(gaps, 3)
    quintic = alternating_polynomial(gaps, 5)
    difference = defaultdict(int)
    for pivot in range(count):
        cyclic = gaps[pivot:]+gaps[:pivot]
        left, right = dict(cyclic[-1]), dict(cyclic[0])
        left[0], right[0] = -1, -1
        replacement = [{0: 1}, right]+cyclic[1:-1]+[left, {0: 1}]
        for mask, value in alternating_polynomial(replacement, 5).items():
            difference[mask] += value
        for mask, value in quintic.items():
            difference[mask] -= value
    prediction = defaultdict(int)
    for mask, value in cubic.items():
        prediction[mask] += 3*value
    for i in range(count):
        prediction[1 << i] += (count-1)//2
        for j in range(i+1, count):
            distance = j-i
            coefficient = distance//2 if distance % 2 == 0 else (count-distance)//2
            prediction[(1 << i) | (1 << j)] -= 2*coefficient
    difference = {mask: value for mask, value in difference.items() if value}
    prediction = {mask: value for mask, value in prediction.items() if value}
    assert difference == prediction
    return {"odd_particle_count": count, "polynomial_terms": len(difference), "exact_identity": True}


def state_check(n):
    @lru_cache(None)
    def data(state):
        positions = [i for i in range(n) if state >> i & 1]
        count = len(positions)
        gaps = [positions[(i+1) % count]-positions[i] for i in range(count)]
        gaps[-1] += n
        fg = []
        for degree in (3, 5):
            value = 0
            for indices in combinations(range(count), degree):
                if all((indices[j+1]-indices[j]) % 2 for j in range(degree-1)):
                    product = 1
                    for i in indices:
                        product *= gaps[i]
                    value += product
            fg.append(value)
        # U has denominator 12*n, h and Q have denominator n.
        u_num = 0
        h_alternative = 0
        for i, j, k in combinations(range(count), 3):
            a, b = positions[j]-positions[i], positions[k]-positions[j]
            c = n-a-b
            sign = (-1)**(i+j+k+1)
            h_alternative += sign*a*b*c
            u_num += sign*a*b*c*(a*b+b*c+c*a+1)
        assert h_alternative == fg[0]
        assert u_num >= 0
        return count, fg[0], fg[1], u_num

    checked = 0
    largest_ratio = 0
    for state in range(1, 1 << n):
        if state.bit_count() % 2 == 0:
            continue
        count, h, q, u = data(state)
        dh, dq, du, bh, bq, bu = 0, 0, 0, 0, 0, 0
        for i in range(n):
            if not state >> i & 1:
                continue
            left, right = (i-1) % n, (i+1) % n
            for endpoint in (left, right):
                destination = state ^ (1 << i) ^ (1 << endpoint)
                _, hd, qd, ud = data(destination)
                dh += h-hd
                dq += q-qd
                du += u-ud
                if h:
                    assert hd <= 2*h
                    largest_ratio = max(largest_ratio, hd/h)
            destination = state ^ (1 << left) ^ (1 << right)
            _, hd, qd, ud = data(destination)
            bh += hd-h
            bq += qd-q
            bu += ud-u
            if h:
                assert hd <= 2*h
                assert h >= n-2
                largest_ratio = max(largest_ratio, hd/h)
        assert dh == n*(count-1)
        assert dq == (count-3)*h
        assert du == 24*h
        assert bh == n-2*count
        assert bq <= 3*h
        assert bu == -24*h+2*(n-2)*(n-1)*count
        checked += 1
    return {"n": n, "odd_states_checked": checked, "max_h_destination_ratio": largest_ratio,
            "all_exact_checks_passed": True}


if __name__ == "__main__":
    result = {
        "generic_gap_polynomial_identities": [polynomial_check(k) for k in range(3, 18, 2)],
        "finite_state_identities_and_rejection_envelope": [state_check(n) for n in (6, 8, 10, 12)],
    }
    print(json.dumps(result, indent=2))
    Path(__file__).with_name("barw_polynomial_audit_results.json").write_text(json.dumps(result, indent=2)+"\n")
