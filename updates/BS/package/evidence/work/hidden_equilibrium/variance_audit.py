"""Numerical second-moment audit of the pinned seven-time witness.

Uses only NumPy plus Python stdlib. This is NOT an interval proof and does not
recompute the tiny mean by catastrophically cancelling huge word coefficients.
The rigorous negative mean remains conditional on the original certificate.
"""
from pathlib import Path
from fractions import Fraction
import json
import itertools
import time
import numpy as np

ROOT = Path(__file__).resolve().parent
D = np.longdouble

def scalar(x):
    f = Fraction(str(x))
    # Fraction.__float__ scales arbitrarily large numerator/denominator safely.
    return D(float(f))

def arr(x):
    if isinstance(x, list):
        return np.array([arr(z) for z in x], dtype=D)
    return scalar(x)

def expm(Q, t):
    # Input has ||tQ||_infinity below 0.003. 30 Taylor terms suffice.
    ans = np.eye(len(Q), dtype=D)
    term = ans.copy()
    for k in range(1, 31):
        term = term @ Q * (t/k)
        ans += term
    return ans

def raw(central, future):
    z = np.zeros((len(central), 11), dtype=D)
    z[:, 0] = central == 0
    for k in range(5):
        z[:, k+1] = (central == 0) & (future == k+1)
        z[:, k+6] = central == k+1
    return z

def run():
    start = time.monotonic()
    seed = json.loads((ROOT/'certificate.txt').read_text())
    wit = json.loads((ROOT/'witness.txt').read_text())
    Q,H,L = (arr(seed[k]) for k in ['Q','H','L'])
    C,Dm,K = (arr(wit[k]) for k in ['feature_matrix','facet_residual_matrix','K'])
    alpha = arr(wit['quadratic_coefficients'])
    const = {k:scalar(v) for k,v in wit['constants'].items()}
    h,t,tau = (const[k] for k in ['h','t','tau'])
    words = np.array(list(itertools.product(range(6), repeat=7)), dtype=np.uint8)
    bm,bp = raw(words[:,3],words[:,2]),raw(words[:,3],words[:,4])
    fm,fp = bm @ C.T,bp @ C.T
    dm,dp = bm @ Dm.T,bp @ Dm.T
    gm = raw(words[:,1],words[:,0]) @ C.T - fm @ K.T
    gp = raw(words[:,5],words[:,6]) @ C.T - fp @ K.T
    p0 = (words[:,3]==0).astype(D)
    s2 = fm[:,1]*fp[:,1]+fm[:,2]*fp[:,2]
    sq = (alpha[0]*p0+alpha[1]/2*(fm[:,1]+fp[:,1])
          +alpha[2]/2*(fm[:,2]+fp[:,2])+alpha[3]*fm[:,1]*fp[:,1]
          +alpha[4]/2*(fm[:,1]*fp[:,2]+fm[:,2]*fp[:,1]))
    rh = np.sum(dm*dp,axis=1)
    rt = np.sum(gm*gp,axis=1)
    W = (sq+72*(p0-s2)+(45000*h+tau)*(p0+s2)+tau*p0
         +const['Lambda']*rh+const['Mu']*rt)
    times = arr(wit['observation_times'])
    labels = np.array([0]*5+[1,2,3,4,5])
    prob = np.ones((len(words),10),dtype=D)/10
    prob *= words[:,0,None] == labels[None,:]
    for j,dt in enumerate(np.diff(times),1):
        prob = prob @ expm(Q,dt)
        prob *= words[:,j,None] == labels[None,:]
    prob = prob.sum(axis=1)
    second = np.dot(prob,W*W)
    # Mean W is about 1e-6 whereas terms in its naive sum reach 1e13:
    # do not interpret any numerical dot(prob,W) as the mean.
    R = W.max()-W.min()
    delta = const['raw_target_gap']
    logterm = np.log(D(80)) # two confidence events at alpha=.05
    # Planning estimates, not nonasymptotic sample guarantees.
    radius_leading = 2*second*logterm/delta**2
    radius_linear = 7*R*logterm/(3*delta)
    res = {
        'status':'NUMERICAL_DIAGNOSTIC_NOT_INTERVAL_CERTIFIED',
        'source_revision':'8aed7fd74eb14622ed5a0a3635a799374296e32a',
        'num_words':len(words),
        'word_probability_mass':str(prob.sum()),
        'min_word_probability':str(prob.min()),
        'QH_minus_HL_max':str(np.max(np.abs(Q@H-H@L))),
        'raw_min_W':str(W.min()),'raw_max_W':str(W.max()),
        'raw_range':str(R),'raw_second_moment':str(second),
        'raw_guaranteed_gap_from_source':str(delta),
        'empirical_Bernstein_leading_planning_n':str(radius_leading),
        'empirical_Bernstein_linear_planning_n':str(radius_linear),
        'source_Hoeffding_n':str(8*(const['M']/delta)**2*np.log(D(40))),
        'elapsed_seconds':time.monotonic()-start,
        'numpy_version':np.__version__,
        'longdouble_precision':str(np.finfo(D)),
        'cautions':[
            'No interval certificate for second moment or range.',
            'Leading planning n ignores confidence control of sample variance.',
            'Universal empirical-Bernstein test remains valid using certified source range.',
            'iid stationary windows assumed, independence not supplied by overlapping trajectory.',
            'A supplied seed and statistic do not establish acquisition of either from data.'
        ]
    }
    (ROOT/'variance_results.json').write_text(json.dumps(res,indent=2)+'\n')
    print(json.dumps(res,indent=2))

if __name__=='__main__':
    run()
