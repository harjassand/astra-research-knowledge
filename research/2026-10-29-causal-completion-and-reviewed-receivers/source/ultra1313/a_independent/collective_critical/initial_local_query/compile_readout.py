"""Outward finite canonical charge-readout compiler, with no many-body oracle.

The source is the frozen real frustrated trimer/connected trimer-chain class.
All-K/all-M assertions are the analytic proofs, not these finite executions.
This code performs matrix-function/scalar acquisitions and selects an explicit
accuracy gate. It emits a positive dyadic FIVE-outcome law and no random draws.
Python-flint/Arb encloses arithmetic; fair-bit sampling is a separate primitive.
"""
import time
PROCESS_START = time.perf_counter()
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import math
import platform
import sys
from flint import arb, arb_mat, fmpq, ctx

AFTER_IMPORTS = time.perf_counter()
HERE = Path(__file__).resolve().parent
ctx.prec = 2048


def b(x):
    if isinstance(x, arb):
        return x
    x = F(x)
    return arb(fmpq(x.numerator, x.denominator))


def fq(x):
    return F(str(x.fmpq()))


def exact_upper(x):
    return b(fq(x.upper()))


def exact_lower(x):
    return b(fq(x.lower()))


def record(x):
    assert x.is_finite()
    # Do not materialize the denominator of exp(-10^30) as a Fraction.
    # The exact dyadic endpoint pair has polynomial-size exponent metadata.
    lm,le = x.lower().man_exp()
    um,ue = x.upper().man_exp()
    return {'ball': x.str(40),
            'lower_dyadic': {'mantissa':str(lm),'exponent':str(le)},
            'upper_dyadic': {'mantissa':str(um),'exponent':str(ue)}}


def identity(n):
    return arb_mat([[int(i == j) for j in range(n)] for i in range(n)])


def trace(A):
    return sum((A[i, i] for i in range(A.nrows())), b(0))


def native_input(M):
    assert M >= 3
    T = [[F(0) for j in range(M)] for i in range(M)]
    core = [[3, 1, -4], [1, 3, -4], [-4, -4, 8]]
    internal = set()
    for start in range(0, M-2, 3):
        for i in range(3):
            for j in range(3):
                T[start+i][start+j] = F(core[i][j])
        internal.update((start, start+1))
    eps = F(1, 100000)
    for i in range(M-1):
        if i not in internal:
            T[i][i] += eps
            T[i+1][i+1] += eps
            T[i][i+1] -= eps
            T[i+1][i] -= eps
    assert all(sum(row) == 0 for row in T)
    assert all(T[i][j] == T[j][i] for i in range(M) for j in range(M))
    # These bounds are proved in the frozen all-M source construction, not
    # inferred from a floating eigensolve. M3 has the exact stronger input.
    lam = F(2) if M == 3 else 4*eps/F(M*M)
    upper = F(12) if M == 3 else F(12)+4*eps
    return T, lam, upper


def matrix_acquisition(T, lam, upper):
    start = time.perf_counter()
    M = len(T)
    I = identity(M)
    P = arb_mat([[b(F(1, M)) for j in range(M)] for i in range(M)])
    TT = arb_mat([[b(x) for x in row] for row in T])
    ell = max(F(1), upper)
    mu = min(F(1), lam)
    A = (TT+P)/b(ell)
    Y = I
    residual = b(1-mu/ell)
    n = 0
    tail_target = b(F(1, 2**300))
    # Exact polynomial residual squares; interval operations enclose that
    # polynomial, with analytic spectral tails added only at the end.
    while (b(ell).sqrt()*residual).upper() > tail_target:
        Y = (Y*(3*I-A*Y*Y))/2
        residual = residual*residual
        n += 1
        assert n <= 128
    root0 = b(ell).sqrt()*A*Y-P
    inv0 = Y/b(ell).sqrt()-P
    root_tail = exact_upper(b(ell).sqrt()*residual)
    inv_tail = exact_upper(residual/b(mu).sqrt())
    root = arb_mat([[root0[i,j]+arb(0,root_tail) for j in range(M)]
                    for i in range(M)])
    invroot = arb_mat([[inv0[i,j]+arb(0,inv_tail) for j in range(M)]
                       for i in range(M)])
    # Width checks are part of this deterministic implementation contract.
    max_rad = max(root[i,j].rad().upper() for i in range(M) for j in range(M))
    max_irad = max(invroot[i,j].rad().upper() for i in range(M) for j in range(M))
    assert max_rad < b(F(1, 2**240)), ('sqrt width',n,max_rad)
    assert max_irad < b(F(1, 2**220)), ('inverse sqrt width',n,max_irad)
    sqrt_trace = trace(root)
    invS = (TT+P).inv()
    diag = [root[i,i] for i in range(M)]
    mean = sum(diag,b(0))/M
    centered = arb_mat([[x-mean] for x in diag])
    pressure = (centered.transpose()*invS*centered)[0,0]
    assert pressure.lower() > 0
    # Physical unit charge vector (e0-e1)/sqrt(2). The query is later scaled
    # by M^(1/4), so it sees the per-site (K/M)^(1/4) charge scale.
    quad = (root[0,0]+root[1,1]-root[0,1]-root[1,0])/2
    assert quad.lower() > 0
    return {'T': TT, 'I': I, 'P': P, 'sqrtT': root,
            'invrootT': invroot, 'sqrt_trace': sqrt_trace,
            'pressure': pressure, 'query_sqrtT_form': quad,
            'matrix_receipt': {
                'M': M, 'proved_gap_lower': str(lam),
                'proved_norm_upper': str(upper), 'precision_bits': ctx.prec,
                'newton_schulz_iterations': n,
                'square_root_tail': record(root_tail),
                'inverse_root_tail': record(inv_tail),
                'max_square_root_entry_radius': record(max_rad),
                'max_inverse_root_entry_radius': record(max_irad),
                'Tr_sqrtT': record(sqrt_trace),
                'diag_pressure_d_Tplus_d': record(pressure),
                'unit_query_w_sqrtT_w': record(quad),
                'seconds': time.perf_counter()-start}}


def theta_bound(M, d, gmax, sqrtK, alpha):
    r = (-arb.pi()**2/(M*(gmax/sqrtK+alpha))).exp()
    return (d*(r.log1p()-(-r).log1p())).expm1()


def error_receiver(K, M, lam, upper, data, outcomes=5):
    U = b(1)
    beta = b(1)
    d = M-1
    sk = b(K).sqrt()
    kquart = sk.sqrt()
    S = data['sqrt_trace']
    TrT = trace(data['T'])
    C = (2*U/M).sqrt()*S
    cexpr = 2*U.sqrt()*(S+b(upper).sqrt())/(b(M).sqrt()*b(lam))
    cbar = int(cexpr.upper().ceil().fmpz())
    R = 8*K+4
    eps = b(cbar)/b(R).sqrt()
    if eps.upper() > b(F(1, 2)):
        return None, {'K_bits': K.bit_length()-1,
                      'failure': 'lower-operator epsilon gate'}
    aa = (1-eps)/R
    gmax = (M*U/(2*b(lam))).sqrt()
    alpha = b(M)/(4*K)
    thetaC = theta_bound(M,d,gmax,sk,alpha)
    thetaA = theta_bound(M,d,gmax,sk,b(0))
    C4 = b(F(M+15,12))
    Aclt = C4*d*(d+2)/2+3*d
    a0 = 4/(arb.pi()**2*M*M)
    tau = 1/(8*arb.pi()**2*d*M*M)
    logB = b(2).log()+b(F(d,2))*(4/a0).log()-b(F(M,2))*b(M).log()
    Eclt = Aclt/K+(logB-tau*K).exp()
    Rdet = (data['I']+(M/(4*sk))*(2/(M*U)).sqrt()*data['sqrtT']).det().sqrt()
    delta = thetaC+Eclt*(1+thetaA)*Rdet
    if delta.upper() >= b(F(1,2)):
        return None, {'K_bits': K.bit_length()-1,
                      'failure': 'trial delta gate'}
    gamma = (alpha+2*delta)/(1-delta)
    TrGinv = (2/(M*U)).sqrt()*S
    l1 = sum((abs(x) for row in INPUTS[M] for x in row),F(0))
    Rup = b(l1)/M*(gmax*gmax/4+2*K*gamma)+U*sk*TrGinv*delta/(1-delta)
    Etr = C*sk+Rup
    D = math.comb(K+d,d)
    Eup = exact_upper(Etr+2*b(D).log()/beta)
    L = 4*K*(U*(1-eps)/(M*R)).sqrt()*S \
        -(1-eps)*b(8*K)/R*TrT-U*data['pressure']/4
    Llo = exact_lower(L)
    Bfast = Eup-Llo
    assert Bfast.lower() > 0
    Dexc = Eup/b(lam)
    if Dexc.upper() >= b(2*K):
        Dexc = b(2*K)
    bmax = (aa*K*b(upper)).sqrt()
    tnorm = b(M).sqrt().sqrt()

    def err(t):
        return t*Bfast.sqrt()/(U.sqrt()*kquart) \
            +d*bmax/(2*U.sqrt())*t*t \
            *(8*((Dexc+1)/K).sqrt()+b(F(8,3))*t/kquart)

    errors = [err(h*tnorm) for h in range(1,outcomes)]
    tv = sum((b(F(outcomes-h,outcomes))*errors[h-1]
              for h in range(1,outcomes)),b(0))
    return {'M': M,'K': K,'D': D,'C': C,'cbar': cbar,
            'epsilon': eps,'a': aa,'gmax': gmax,'Eclt': Eclt,
            'thetaC': thetaC,'thetaA': thetaA,'Rdet': Rdet,
            'delta': delta,'gamma': gamma,'Rup': Rup,
            'Etr': Etr,'Eup': Eup,'Llower': Llo,'Bfast': Bfast,
            'Dexc': Dexc,'errors': errors,'tv': tv}, \
           {'K_bits':K.bit_length()-1,'finite_instrument_tv_upper':str(fq(tv.upper()))}


def compile_case(M):
    start = time.perf_counter()
    T,lam,upper = native_input(M)
    INPUTS[M] = T
    data = matrix_acquisition(T,lam,upper)
    (HERE/f'MATRIX_M{M}.json').write_text(json.dumps(data['matrix_receipt'],indent=2)+'\n')
    attempts = []
    out = None
    for Kbits in range(64,513,16):
        val,attempt = error_receiver(2**Kbits,M,lam,upper,data)
        attempts.append(attempt)
        if val is not None and val['tv'].upper() < b(F(1,100)):
            out = val
            break
    assert out is not None
    K = out['K']
    sk = b(K).sqrt()
    G = (b(M)/2).sqrt()*data['invrootT']
    z = 4*sk/M
    p0 = ((data['I']+z*(G+data['P'])).det()/(1+z))**F(-1,2)
    assert p0.lower() > 0
    # Query theta=(q0-q1)/(sqrt(2)*(K/M)^(1/4)), five-outcome Fejer POVM.
    variance = 2*(out['a']*K).sqrt()*data['query_sqrtT_form']
    n = 5
    probs = []
    for j in range(n):
        prob = (1+2*sum((b(F(n-h,n))*(-h*h*variance/2).exp()
                         *b(F(2*h*j,n)).cos_pi()
                         for h in range(1,n)),b(0)))/n
        assert prob.lower() > 0 and prob.upper() < 1
        probs.append(prob)
    assert sum(probs,b(0)).contains(1)
    bits = 48
    den = 2**bits
    numerators = [int((p.mid()*den).floor().fmpz()) for p in probs[:-1]]
    numerators.append(den-sum(numerators))
    assert min(numerators) >= 0 and sum(numerators) == den
    round_tv = sum((max(abs(F(a,den)-fq(p.lower())),
                        abs(F(a,den)-fq(p.upper())))
                    for a,p in zip(numerators,probs)),F(0))/2
    total_tv = out['tv']+b(round_tv)
    assert total_tv.upper() < b(F(1,100))
    input_body = {'M':M,'T':[[str(x) for x in row] for row in T],
                  'U':1,'beta':1,'K_each':str(K),
                  'gap_lower':str(lam),'norm_upper':str(upper)}
    input_raw = (json.dumps(input_body,sort_keys=True,indent=2)+'\n').encode()
    (HERE/f'INPUT_M{M}.json').write_bytes(input_raw)
    fields = ('C','epsilon','Eclt','thetaC','thetaA','Rdet','delta','gamma',
              'Rup','Etr','Eup','Llower','Bfast','Dexc')
    result = {'input':f'INPUT_M{M}.json','input_sha256':hashlib.sha256(input_raw).hexdigest(),
       'source_scope':'Unchanged finite canonical Hamiltonian, U=beta=1; native trimer or connected bounded-range frustrated trimer chain.',
       'M':M,'K_each':str(K),'K_bit_length':K.bit_length(),
       'one_flavor_hilbert_dimension_bits':out['D'].bit_length(),
       'two_flavor_hilbert_dimension_log2_lower':2*(out['D'].bit_length()-1),
       'matrix_acquisition':data['matrix_receipt'],'accuracy_gate_attempts':attempts,
       'bounds':{name:record(out[name]) for name in fields},
       'trial_norm_proxy_p0':record(p0),
       'trial_norm_interval':record(p0+arb(0,exact_upper(p0*out['delta']))),
       'free_energy_interval':{'lower':str(fq((out['Llower']-2*b(out['D']).log()).lower())),
                               'upper':str(fq(out['Etr'].upper()))},
       'query':'theta=(q_0-q_1)/(sqrt(2)*(K/M)^(1/4)); p_j=|sum_l=0..4 exp[il(theta-2pi*j/5)]|^2/25',
       'gaussian_theta_variance':record(variance),
       'proxy_probabilities':list(map(record,probs)),
       'dyadic_table':{'bits':bits,'denominator':str(den),'numerators':numerators},
       'arithmetic_table_tv_upper':str(round_tv),
       'finite_instrument_tv_theorem':record(out['tv']),
       'finite_instrument_tv_total':record(total_tv),
       'harmonic_characteristic_errors':list(map(record,out['errors'])),
       'ordinary_bare_pair_law':[1,0,0,0,0],
       'actual_first_outcome_upper':str(fq((probs[0]+total_tv).upper())),
       'fair_bit_sampling_cost_per_output':{'fair_bits':bits,'comparisons_upper':n,
                                          'unknown_normalizers':0,'rejection_proposals':0},
       'manybody_states_enumerated':0,'permanents':0,'random_draws':0,
       'seconds_case':time.perf_counter()-start,
       'limits':['No exact/full Gibbs or continuous charge sampler.',
                 'No fixed-density or practical many-body advantage claim.',
                 'Ordinary harmonic methods predict the same proxy; error acquisition is the constructed link.',
                 'No RNG realization is offered as an iid-bit theorem.']}
    return result


def sample_compiled_table(fair_integer, numerators, bits=48):
    """Exact pushforward of an acquired uniform B-bit integer; no RNG oracle."""
    assert isinstance(fair_integer,int) and 0 <= fair_integer < 2**bits
    assert all(isinstance(a,int) and a>=0 for a in numerators)
    assert sum(numerators)==2**bits
    boundary = 0
    for j,a in enumerate(numerators):
        boundary += a
        if fair_integer < boundary:
            return j
    raise AssertionError('unreachable normalized integer table')


INPUTS = {}


def main():
    cases = [compile_case(M) for M in (3,32)]
    # Test every interval endpoint of the FINITE pushforward without generating
    # any random trajectory or exhaustive fair-bit tape.
    for c in cases:
        nums = c['dyadic_table']['numerators']
        lower = 0
        for j,a in enumerate(nums):
            if a:
                assert sample_compiled_table(lower,nums) == j
                assert sample_compiled_table(lower+a-1,nums) == j
            lower += a
    result = {'operation':'Acquired finite canonical collective-charge readout law',
       'precision_bits':ctx.prec,'python':platform.python_version(),
       'cases':cases,'sample_table_endpoint_checks':20,
       'seconds_after_imports':time.perf_counter()-AFTER_IMPORTS,
       'seconds_process_internal':time.perf_counter()-PROCESS_START,
       'scope':'Outward coefficient/normalization/error and exact dyadic-law acquisition. No many-body dynamics, thermal Monte Carlo, physical measurement, full Gibbs-state approximation or novel generic oscillator method.'}
    (HERE/'READOUT_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'M_cases':[c['M'] for c in cases],
       'selected_K_bits':[c['K_bit_length']-1 for c in cases],
       'total_TV_bounds':[c['finite_instrument_tv_total']['ball'] for c in cases],
       'first_outcome_proxy':[c['proxy_probabilities'][0]['ball'] for c in cases],
       'matrix_seconds':[c['matrix_acquisition']['seconds'] for c in cases],
       'seconds_after_imports':result['seconds_after_imports'],
       'seconds_process_internal':result['seconds_process_internal'],
       'random_draws':0,'manybody_states_enumerated':0},indent=2))


if __name__ == '__main__':
    main()
