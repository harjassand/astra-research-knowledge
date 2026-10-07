"""Finite digital bin archive for every Gaussian I<=C<=bI, including correlation.

Scalar triangle CDF/encoder/decoder arithmetic is reused with attribution from
c09_s03/gaussian_compander_codec.py, audited and copied before any execution.
The new covariance derivative budget and tuple compiler are proved in rev03.
No physical Gaussian sampler or continuous-TV digital output is implemented.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import math
import time


def triangle_cdf(t, j, J):
    t = F(t)
    if not (0 <= t <= 1) or not (0 <= j < J) or J < 3:
        raise ValueError('bad triangle')
    x = J*t
    if j == 0:
        if x <= 1:
            return x-x*x/2
        if x <= J-1:
            return F(1, 2)
        return F(1, 2)+(x-(J-1))**2/2
    if x <= j-1:
        return F(0)
    if x <= j:
        return (x-(j-1))**2/2
    if x <= j+1:
        return 1-(j+1-x)**2/2
    return F(1)


def encode_coordinate(k, p, J, bits):
    N = 1 << p
    if not 0 <= k < N or not 0 <= bits < 2*N:
        raise ValueError('bad input/random tape')
    q, rem = divmod(J*(2*k+1), 2*N)
    return (q+1) % J if bits < rem else q % J


def decode_coordinate(j, p, J, bits):
    N = 1 << p
    D = 1 << (2*p+1)
    if not 0 <= j < J or not 0 <= bits < D:
        raise ValueError('bad archive/random tape')
    lo, hi, steps = 0, N-1, 0
    while lo < hi:
        mid = (lo+hi)//2
        threshold = triangle_cdf(F(mid+1, N), j, J)*D
        assert threshold.denominator == 1
        if bits < threshold.numerator:
            hi = mid
        else:
            lo = mid+1
        steps += 1
    return lo, steps


def pack(labels, J):
    result = 0
    for j in reversed(labels):
        if not 0 <= j < J:
            raise ValueError('bad label')
        result = result*J+j
    return result


def unpack(code, modes, J):
    if not 0 <= code < J**modes:
        raise ValueError('bad archive code')
    labels = []
    for _ in range(modes):
        code, j = divmod(code, J)
        labels.append(j)
    assert code == 0
    return labels


def encode_bins(bins, p, J, independent_bits):
    if len(bins) != len(independent_bits):
        raise ValueError('wrong tape count')
    return pack([encode_coordinate(k,p,J,r) for k,r in zip(bins,independent_bits)], J)


def decode_bins(code, modes, p, J, independent_bits):
    if len(independent_bits) != modes:
        raise ValueError('wrong tape count')
    pairs = [decode_coordinate(j,p,J,r) for j,r in zip(unpack(code,modes,J),independent_bits)]
    return [x for x,_ in pairs], sum(steps for _,steps in pairs)


def plan(modes, covariance_upper, epsilon):
    upper, epsilon = F(covariance_upper), F(epsilon)
    if modes < 1 or upper < 1 or not 0 < epsilon < 1:
        raise ValueError('invalid covariance/precision contract')
    ell = math.isqrt(upper.numerator//upper.denominator)
    if ell*ell < upper:
        ell += 1
    b = F(ell*ell)
    q = 194*modes*b/epsilon
    J = max(3, math.isqrt(q.numerator//q.denominator))
    if J*J < q:
        J += 1
    p = 0
    while (1 << p)*epsilon < modes*J:
        p += 1
    ideal = F(97)*modes*b/(J*J)
    midpoint = F(modes*J, 2*(1 << p))
    assert ideal+midpoint <= epsilon
    return {'m': modes, 'C_upper': str(upper), 'public_integer_compander_width': ell,
            'b': str(b), 'epsilon': str(epsilon), 'J': J, 'p': p,
            'acquired_input_bits': modes*p, 'output_bits': modes*p,
            'archive_total_dimension': str(J**modes), 'archive_bits': (J**modes-1).bit_length(),
            'encoder_random_bits': modes*(p+1), 'decoder_random_bits': modes*(2*p+1),
            'ideal_TV_upper': str(ideal), 'midpoint_TV_upper': str(midpoint),
            'total_TV_upper_rational': str(ideal+midpoint),
            'total_TV_upper_float_display_only': float(ideal+midpoint)}


def pairings_moment(indices, covariance):
    if not indices:
        return F(1)
    if len(indices) % 2:
        return F(0)
    first = indices[0]
    answer = F(0)
    for j in range(1, len(indices)):
        rest = indices[1:j]+indices[j+1:]
        answer += covariance[first][indices[j]]*pairings_moment(rest,covariance)
    return answer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('correlated_covariance_checks.json'))
    args = parser.parse_args()
    start = time.perf_counter()
    checks = 0
    # All small mixed-radix archives and probability thresholds.
    for J in (3, 5, 8):
        for modes in (1, 2, 3):
            for code in range(J**modes):
                assert pack(unpack(code,modes,J),J) == code
                checks += 1
    for J in (3, 5):
        for p in (1, 2, 4):
            N, D = 1 << p, 1 << (2*p+1)
            for k in range(N):
                counts = [0]*J
                for r in range(2*N):
                    counts[encode_coordinate(k,p,J,r)] += 1
                q, rem = divmod(J*(2*k+1),2*N)
                assert counts[q % J] == 2*N-rem and counts[(q+1) % J] == rem
                checks += 1
            for j in range(J):
                old = F(0)
                for k in range(N):
                    now = triangle_cdf(F(k+1,N),j,J)
                    a, b = old*D, now*D
                    assert a.denominator == b.denominator == 1 and a <= b
                    for r in (a.numerator, b.numerator-1):
                        if a <= r < b:
                            out, steps = decode_coordinate(j,p,J,r)
                            assert out == k and steps <= p
                            checks += 1
                    old = now
                assert old == 1
    # Exact correlated input-bin fixture: diagonal joint law, NOT a product.
    J, p = 3, 2
    N, D = 1 << p, 1 << (2*p+1)
    labels = [[F(0) for _ in range(J)] for _ in range(J)]
    for k in range(N):
        q, rem = divmod(J*(2*k+1),2*N)
        probs = [F(0)]*J
        probs[q % J] += F(2*N-rem,2*N)
        probs[(q+1) % J] += F(rem,2*N)
        for i in range(J):
            for j in range(J):
                labels[i][j] += probs[i]*probs[j]/N
    assert sum(map(sum,labels)) == 1
    marginal = [sum(row) for row in labels]
    dependence = sum(abs(labels[i][j]-marginal[i]*marginal[j]) for i in range(J) for j in range(J))/2
    assert dependence > 0
    transition = [[triangle_cdf(F(k+1,N),j,J)-triangle_cdf(F(k,N),j,J) for k in range(N)] for j in range(J)]
    output = [[sum(labels[i][j]*transition[i][a]*transition[j][b]
                   for i in range(J) for j in range(J)) for b in range(N)] for a in range(N)]
    assert sum(map(sum,output)) == 1
    om = [sum(row) for row in output]
    output_dependence = sum(abs(output[a][b]-om[a]*om[b]) for a in range(N) for b in range(N))/2
    assert output_dependence > 0
    for code in range(J*J):
        for r1 in (0,D//2,D-1):
            for r2 in (0,D//2,D-1):
                bins, steps = decode_bins(code,2,p,J,[r1,r2])
                assert len(bins)==2 and all(0<=x<N for x in bins) and steps<=2*p
                checks += 1
    # Exact Wick-moment identities underlying the correlated Gaussian budget.
    moments = []
    # C=I+3 vv^T for rational unit v; C has eigenvalues exactly 1,4.
    for vx, vy in [(F(1),F(0)),(F(3,5),F(4,5)),(F(4,5),F(-3,5))]:
        c00, c01, c11 = 1+3*vx*vx, 3*vx*vy, 1+3*vy*vy
        determinant = c00*c11-c01*c01
        assert determinant == 4
        for v, h in [(c00,c11/determinant),(c11,c00/determinant)]:
            covariance = [[v,F(1)],[F(1),h]]
            m22 = pairings_moment([0,0,1,1],covariance)
            m42 = pairings_moment([0,0,0,0,1,1],covariance)
            assert m22 == v*h+2 and m42 == 3*v*v*h+12*v
            # Exact third bracket <=28b for b=4.
            b = F(4)
            third = 2*b*h+4*v*h+4+(6*v*v*h+12*v)/b
            assert third <= 28*b and 1<=v<=b and 0<h<=1
            moments.append({'variance':str(v),'precision':str(h),'EX2W2':str(m22),'EX4W2':str(m42),'third_bracket':str(third)})
            checks += 2
    plans = [plan(2, F(4), F(1,1000)),plan(8, F(4), F(1,1000)),plan(32, F(5,2), F(1,100))]
    result = {'status':'PASS_FINITE_EXACT_COMPILER_AND_MOMENT_CHECKS','exact_checks':checks,
              'correlated_fixture':{'J':J,'p':p,'label_dependence_TV':str(dependence),
                                   'decoded_dependence_TV':str(output_dependence),
                                   'scope':'NonGaussian rational bin-law fixture checks that the tensor decoder retains input-induced label correlations; it is not a Gaussian convergence fixture.'},
              'exact_joint_Gaussian_moments':moments,'plans':plans,
              'elapsed_seconds':time.perf_counter()-start,
              'scope':'Exact integer probability compiler, finite rational correlations/Wick identities, and analytic-plan arithmetic. No physical Gaussian instrument, dense MI evaluation, continuous-TV digital output, or formal theorem verification.'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'checks':checks,'plans':plans,
                      'elapsed_seconds':result['elapsed_seconds'],'output':str(args.output)},indent=2))


if __name__ == '__main__':
    main()
