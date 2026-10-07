"""Charged inverse-square-scale certificate for a supplied diagonal PSD table.

Only rational arithmetic enters the returned certificates. Decimal logs in
main are bounded diagnostic comparisons, never trusted as a theorem premise.
The general matrix-entropy proof is c09_s01's, independently audited here.
The square-root mean/range comparison is proved in revision03.
"""
from fractions import Fraction as F
from pathlib import Path
from decimal import Decimal, localcontext
import argparse
import hashlib
import json
import math
import time


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[1], a[1] - b[0]


def scale(a, c):
    c = F(c)
    return (a[0]*c, a[1]*c) if c >= 0 else (a[1]*c, a[0]*c)


def positive_square(a):
    assert 0 <= a[0] <= a[1]
    return a[0]*a[0], a[1]*a[1]


def power_two(e):
    return F(1 << e) if e >= 0 else F(1, 1 << -e)


def unit_log(z, width):
    """Exact positive-series enclosure for 1<=z<=2."""
    assert 1 <= z <= 2 and width > 0
    t = (z - 1)/(z + 1)
    lo = F(0)
    n = 0
    power = t
    while True:
        tail = 2*power/((2*n+1)*(1-t*t))
        if tail <= width:
            return (lo, lo+tail), n
        lo += 2*power/(2*n+1)
        power *= t*t
        n += 1


def log_interval(x, width=F(1, 1 << 45)):
    x = F(x)
    if x <= 0:
        raise ValueError('log input must be positive')
    e = x.numerator.bit_length()-x.denominator.bit_length()
    z = x/power_two(e)
    if z < 1:
        e -= 1
        z *= 2
    elif z >= 2:
        e += 1
        z /= 2
    assert 1 <= z < 2
    local_width = width/(2*(abs(e)+1))
    lz, nz = unit_log(z, local_width)
    l2, n2 = unit_log(F(2), local_width)
    ans = add(lz, scale(l2, e))
    assert ans[1]-ans[0] <= width
    return ans, nz+n2


def sqrt_interval(x, bits=45):
    x = F(x)
    if x < 0:
        raise ValueError('negative square root')
    den = 1 << bits
    q = math.isqrt((x.numerator << (2*bits))//x.denominator)
    lo = F(q, den)
    hi = lo if q*q*x.denominator == x.numerator*den*den else F(q+1, den)
    assert lo*lo <= x <= hi*hi and hi-lo <= F(1, den)
    return lo, hi


def serial_interval(a):
    return {'lower_rational': str(a[0]), 'upper_rational': str(a[1]),
            'width_rational': str(a[1]-a[0]), 'upper_float_display_only': float(a[1])}


def certify(table, cap=F(64), bits=45):
    ps = [F(x) for x in table['probabilities']]
    rows = [[F(x) for x in row] for row in table['diagonal_fields']]
    if not ps or len(ps) != len(rows) or sum(ps) != 1 or min(ps) < 0:
        raise ValueError('invalid reference probabilities')
    modes = len(rows[0])
    if modes < 1 or any(len(row) != modes or min(row) < 0 for row in rows):
        raise ValueError('invalid PSD diagonal fields')
    cap = F(cap)
    if cap <= 0 or bits < 1:
        raise ValueError('invalid cap/precision')
    means = [sum(p*row[i] for p, row in zip(ps, rows)) for i in range(modes)]
    trace_mean = sum(means)
    cache = {}
    series_terms = 0

    def logged(x):
        nonlocal series_terms
        if x not in cache:
            ans, count = log_interval(x, F(1, 1 << bits))
            cache[x] = ans
            series_terms += count
        return cache[x]

    raw = (F(0), F(0))
    for p, row in zip(ps, rows):
        if p:
            for a in row:
                if a:
                    raw = add(raw, scale(logged(a), p*a))
    centered = (F(0), F(0))
    for a in means:
        if a:
            centered = add(centered, scale(logged(a), a))
    entropy = sub(raw, centered)
    entropy = (max(F(0), entropy[0]), max(F(0), entropy[1]))
    assert entropy[1]-entropy[0] <= 2*trace_mean*F(1, 1 << bits)
    active = [i for i, a in enumerate(means) if a]
    kapp = max([F(1)] + [row[i]/means[i] for p, row in zip(ps, rows)
                                       if p for i in active])
    envelope = scale(logged(kapp), trace_mean/2)
    bound_candidates = {'matrix_entropy_upper': entropy[1]/2,
                        'trace_profile_upper': cap*trace_mean/4,
                        'joint_order_envelope_upper': envelope[1]}
    log_cap=logged(1+cap)
    g_cap=scale(sub(scale(log_cap,(1+cap)/cap),(F(1),F(1))),F(1,2))
    g_cap=(max(F(0),g_cap[0]),max(F(0),g_cap[1]))
    bound_candidates['peer_fixed_reference_trace_upper']=g_cap[1]*trace_mean
    root_report = {'common_zero_coordinates': [i for i in range(modes) if i not in active]}
    if active:
        root_bits = bits
        while True:
            root_means = [(F(0), F(0)) for _ in range(modes)]
            for p, row in zip(ps, rows):
                if p:
                    for i in active:
                        root_means[i] = add(root_means[i], scale(sqrt_interval(row[i], root_bits), p))
            s_lower = min(root_means[i][0] for i in active)
            if s_lower > 0:
                break
            root_bits *= 2
        beta = max(row[i] for p, row in zip(ps, rows) if p for i in active)
        r_upper = sqrt_interval(beta, root_bits)[1]
        v_upper = r_upper/s_lower
        assert v_upper >= 1
        if v_upper == 1:
            b_upper = F(2)
        else:
            ln_v = logged(v_upper)
            direct_upper = (2*v_upper*v_upper*ln_v[1]-v_upper*v_upper+1)/(v_upper-1)**2
            # Stable upper: b(v)=4 int_0^1(1-t)[1+log(1+t(v-1))]dt
            # <=2(1+log v) for v>=1. Avoid cancellation when v is near 1.
            b_upper = min(direct_upper, 2+2*ln_v[1])
            assert b_upper >= 2
        sum_squares = (F(0), F(0))
        for i in active:
            sum_squares = add(sum_squares, positive_square(root_means[i]))
        variance = sub((trace_mean, trace_mean), sum_squares)
        variance = (max(F(0), variance[0]), max(F(0), variance[1]))
        bound_candidates['square_root_mean_range_upper'] = b_upper*variance[1]/2
        cap_coefficient = sub(scale(log_cap, (1+cap)**2/(cap*cap)),
                              (F(1)+1/cap+F(1,2), F(1)+1/cap+F(1,2)))
        cap_coefficient = (max(F(0),cap_coefficient[0]), max(F(0),cap_coefficient[1]))
        bound_candidates['peer_correct_weight_root_variance_upper'] = 2*cap_coefficient[1]*variance[1]
        root_report.update({'root_precision_bits': root_bits,
                            'root_mean_intervals': [serial_interval(x) for x in root_means],
                            's_lower': str(s_lower), 'r_upper': str(r_upper),
                            'ratio_upper': str(v_upper), 'b_upper': str(b_upper),
                            'root_variance_interval': serial_interval(variance),
                            'peer_H_L_interval': serial_interval(cap_coefficient),
                            'peer_G_L_interval': serial_interval(g_cap)})
    else:
        bound_candidates['square_root_mean_range_upper'] = F(0)
    encoded = {'probabilities': [str(p) for p in ps],
               'diagonal_fields': [[str(a) for a in row] for row in rows]}
    return {'status': 'EXACT_RATIONAL_INTERVAL_UPPER_CERTIFICATE',
            'source_sha256': hashlib.sha256(json.dumps(encoded,sort_keys=True).encode()).hexdigest(),
            'K': len(ps), 'm': modes, 'cap': str(cap), 'log_precision_bits': bits,
            'full_scalar_inputs_read': len(ps)*(modes+1), 'mean_field': [str(x) for x in means],
            'trace_mean': str(trace_mean), 'entropy_interval': serial_interval(entropy),
            'joint_order_kappa': str(kapp), 'root_certificate': root_report,
            'candidate_upper_rationals': {k: str(v) for k,v in bound_candidates.items()},
            'integrated_information_upper_rational': str(min(bound_candidates.values())),
            'integrated_information_upper_float_display_only': float(min(bound_candidates.values())),
            'unique_log_arguments': len(cache), 'positive_series_terms': series_terms,
            'scope': 'Supplied finite diagonal PSD table; true continuous-source dT/T^2 MI upper. Also applies to digital-label MI by data processing. Dense matrix acquisition, unknown probabilities, physical sampling and N75 gate not implemented.'}


def certify_partition(table, labels, bits=45):
    """Conditional-cell entropy acquisition; downstream Gaussian sampling ideal.

    c09_s01's full simulation proof is independently audited. This computes
    its local entropy premise for a fixed supplied multidimensional diagonal
    partition, and our new root mean/range certificate in each cell.
    """
    ps = [F(x) for x in table['probabilities']]
    rows = table['diagonal_fields']
    if len(labels) != len(ps) or len(rows) != len(ps):
        raise ValueError('partition length mismatch')
    groups = {}
    for i,(p,j) in enumerate(zip(ps,labels)):
        if p:
            groups.setdefault(j,[]).append(i)
    cells = []
    total_upper = F(0)
    total_lower = F(0)
    for j, indices in sorted(groups.items()):
        weight = sum(ps[i] for i in indices)
        conditional = {'probabilities':[str(ps[i]/weight) for i in indices],
                       'diagonal_fields':[rows[i] for i in indices]}
        report = certify(conditional, cap=1, bits=bits)
        raw_upper = F(report['entropy_interval']['upper_rational'])
        raw_lower = F(report['entropy_interval']['lower_rational'])
        # These branches certify entropy, unlike cap-dependent MI branches.
        envelope_upper = 2*F(report['candidate_upper_rationals']['joint_order_envelope_upper'])
        root_upper = 2*F(report['candidate_upper_rationals']['square_root_mean_range_upper'])
        h_upper = min(raw_upper,envelope_upper,root_upper)
        total_upper += weight*h_upper
        total_lower += weight*raw_lower
        cells.append({'label':j,'source_rows':indices,'reference_weight':str(weight),
                      'mean_field':report['mean_field'],'conditional_entropy_upper':str(h_upper),
                      'conditional_certificate':report})
    return {'D_nonempty':len(groups),'archive_bits':max(0,(len(groups)-1).bit_length()),
            'fixed_encoder_labels':labels,'conditional_entropy_interval':serial_interval((total_lower,total_upper)),
            'cells':cells,
            'downstream_scope':'Under supplied domination C and scale density w(T)<=c_w/T^2, c09_s01 simulation has TV^2<=k C c_w H_upper/4. Decoder Gaussian sampling remains ideal; this is an acquired finite conditional-field premise, not a digital Gaussian generator.'}


def decimal_entropy(table):
    with localcontext() as ctx:
        ctx.prec = 110
        def dec(x):
            x = F(x)
            return Decimal(x.numerator)/Decimal(x.denominator)
        ps = [dec(p) for p in table['probabilities']]
        rows = [[dec(a) for a in row] for row in table['diagonal_fields']]
        means = [sum(p*row[i] for p,row in zip(ps,rows)) for i in range(len(rows[0]))]
        ans = sum(p*a*a.ln() for p,row in zip(ps,rows) for a in row if a)
        return ans-sum(a*a.ln() for a in means if a)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--table', type=Path)
    parser.add_argument('--cap', default='64')
    parser.add_argument('--bits', type=int, default=45)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('entropy_table_checks.json'))
    args = parser.parse_args()
    start = time.perf_counter()
    if args.table:
        fixtures = [json.loads(args.table.read_text())]
    else:
        fixtures = [
            {'probabilities':['1/2','1/3','1/6'], 'diagonal_fields':[['1/4','1','4'],['1','4','1'],['4','1/4','1/4']]},
            {'probabilities':['1/2','1/2'], 'diagonal_fields':[['0','2','0'],['2','0','0']]},
            {'probabilities':['127/128','1/128'], 'diagonal_fields':[['0'],['128']]},
            {'probabilities':['1/5','4/5'], 'diagonal_fields':[['0','0'],['0','0']]},
            {'probabilities':['1/3','2/3'], 'diagonal_fields':[['1','4'],['1','4']]},
        ]
    reports = []
    for table in fixtures:
        report = certify(table, F(args.cap), args.bits)
        reference = decimal_entropy(table)
        interval = report['entropy_interval']
        with localcontext() as ctx:
            ctx.prec = 110
            def dec(x):
                x = F(x)
                return Decimal(x.numerator)/Decimal(x.denominator)
            assert dec(interval['lower_rational'])-Decimal('1e-95') <= reference
            assert reference <= dec(interval['upper_rational'])+Decimal('1e-95')
            for name in ['joint_order_envelope_upper','square_root_mean_range_upper']:
                assert reference/2 <= dec(report['candidate_upper_rationals'][name])+Decimal('1e-95')
        report['decimal_entropy_diagnostic'] = str(reference)
        reports.append(report)
    # Independent special-case entropy identity with varying null spaces.
    if not args.table:
        log2, _ = log_interval(F(2), F(1,1 << args.bits))
        interval = reports[1]['entropy_interval']
        assert F(interval['lower_rational']) <= 2*log2[1]
        assert F(interval['upper_rational']) >= 2*log2[0]
        assert reports[1]['root_certificate']['common_zero_coordinates'] == [2]
        assert reports[3]['integrated_information_upper_rational'] == '0'
    result = {'status': 'PASS_ADMITTED_TABLE_CERTIFICATES', 'reports': reports,
              'elapsed_seconds': time.perf_counter()-start,
              'evidence_scope': 'Certified output uses rational positive-series remainder bounds. Decimal special-case comparisons are finite diagnostics, not a proof of matrix entropy theorem.'}
    if not args.table:
        partition_reports = [certify_partition(fixtures[0],labels,args.bits)
                             for labels in ([0,0,0],[0,0,1],[0,1,2])]
        for a,b in zip(partition_reports,partition_reports[1:]):
            assert F(b['conditional_entropy_interval']['upper_rational']) <= F(a['conditional_entropy_interval']['upper_rational'])
        assert partition_reports[-1]['conditional_entropy_interval']['upper_rational'] == '0'
        result['fixed_partition_certificates'] = partition_reports
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'tables': len(reports),
                      'upper_displays': [r['integrated_information_upper_float_display_only'] for r in reports],
                      'elapsed_seconds': result['elapsed_seconds'], 'output': str(args.output)},indent=2))


if __name__ == '__main__':
    main()
