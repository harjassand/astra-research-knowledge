"""Astra chemistry: NCL-product sulfur traffic vs dual-function write-once cap.

Everything except citation-listed isolated chemical precedents is a conditional
kinetic model. No PNA/DNA-integrated acylation or molecular rates were measured.
"""
from dataclasses import dataclass
import math
import numpy as np
from scipy.linalg import solve, expm
from scipy.special import gammaln
from scipy.optimize import brentq, minimize_scalar

@dataclass(frozen=True)
class Donor:
    k: float = .02           # intended amide hazard from free donor
    w: float = 4e-8          # background permanent wrong bond from free donor
    b: float = 2e-5          # acyl excursion to EACH completed-site thiol
    r: float = 1.            # release from product thioester back to free donor
    x: float = 2e-4          # irreversible wrong acyl transfer from product thioester
    h: float = .01           # reagent becomes unavailable while S-acylated
    lam: float = .005        # free reagent hydrolysis/removal; parent unchanged

def absorbing(j: int, R: Donor):
    assert j >= 0 and min(vars(R).values()) >= 0 and R.r + R.x + R.h > 0
    Q = np.array([[-R.k-R.w-R.lam-j*R.b,j*R.b], [R.r,-R.r-R.x-R.h]])
    output=np.array([[R.k,R.w,R.lam], [0,R.x,R.h]])
    p=solve(-Q,output)[0]
    t=solve(-Q,np.ones(2))[0]
    return p,t

def reduced(j,R):
    g=R.r+R.x+R.h
    denom=R.k+R.w+R.lam+j*R.b*(R.x+R.h)/g
    return np.array([R.k,R.w+j*R.b*R.x/g,R.lam+j*R.b*R.h/g])/denom

def stage_correct_eventually(j,R):
    # Harmless reagent loss in either donor state restarts the same competent parent
    return R.k/(R.k+R.w+j*R.b*R.x/(R.r+R.x+R.h))

def log_full_correct(L,R,product_sulfur_remaining=1):
    assert L>=1 and 0<=product_sulfur_remaining<=1
    rho0=R.w/R.k
    slope=product_sulfur_remaining*R.b*R.x/(R.k*(R.r+R.x+R.h))
    jj=np.arange(L,dtype=float)
    log_direct=float(-np.log1p(rho0+slope*jj).sum())
    if slope>0 and (1+rho0)/slope < 1e7:
        z=(1+rho0)/slope
        log_gamma=float(-L*math.log(slope)+gammaln(z)-gammaln(z+L))
        assert abs(log_gamma-log_direct)<max(1e-6,abs(log_direct)*1e-4),(log_gamma,log_direct)
    return log_direct

def mask_protection_survival(t, *, a,b,c_U):
    """A=free unfinished aminothiol; H=reversible 2-FPBA protected; D=irreversible thiol cap.
    Starts at protective binding equilibrium, with 2-FPBA maintained during capping.
    """
    Q=np.array([[-a-c_U,a],[b,-b]],float)
    initial=np.array([b/(a+b),a/(a+b)])
    return float(initial@expm(Q*t)@np.ones(2))

def mask_good_pair(t,*,a,b,c_U,c_P):
    return mask_protection_survival(t,a=a,b=b,c_U=c_U)*(-math.expm1(-c_P*t))

def run():
    R=Donor()
    for j in (0,1,4,25,100,999):
        probs,_=absorbing(j,R)
        assert np.allclose(probs,reduced(j,R),rtol=1e-12,atol=1e-13)
        assert abs(probs.sum()-1)<1e-12
        eventual=probs[0]/(probs[0]+probs[1])
        assert math.isclose(eventual,stage_correct_eventually(j,R),rel_tol=1e-12)
    print('NCL sulfur sink CTMC identity PASS; donor-loss restarts do not alter wrong/correct odds')
    for L in (20,100,256,500,1000,2000):
        p_ncl=math.exp(log_full_correct(L,R))
        p_selfsilenced=math.exp(log_full_correct(L,R,0))
        p_99pct_capped=math.exp(log_full_correct(L,R,.01))
        print('physical toy',L,'NCL',p_ncl,'fully thiol-silenced',p_selfsilenced,'1% residual sulfur',p_99pct_capped)
    # Chemical-route crossover comparison: can a self-silencing reaction with more
    # background permanent errors still be better due removal of product-S traffic?
    r0=2e-6; slope=2e-7; cap_ratio=5e-5
    def log_ncl(L):return -sum(math.log1p(r0+slope*j) for j in range(L))
    def log_cap(L):return -L*math.log1p(cap_ratio)
    first=next(L for L in range(1,2000) if log_cap(L)>log_ncl(L))
    print('Crossover in second conditional comparison: length',first)
    for L in (100,300,first,500,1000):
        print('comparison length',L,'NCL',math.exp(log_ncl(L)),'covalently silenced alternate',math.exp(log_cap(L)))
    # Even when all S-acyl excursions eventually reverse (x=h=0), expected
    # excursion COUNT until intended chemistry is quadratic in chain length.
    N=1000;b_over_k=0.01
    excursions=b_over_k*N*(N-1)/2
    assert excursions==4995
    print('Expected product-thiol excursions (no wrong/loss), L=1000,b/k=.01:',excursions)
    # Chemical state-selective reversible mask + permanent cap. Exact CTMC.
    # On a successful NCL site: N-acyl Cys has an exposed SH (cap rate c_P).
    # On unfinished site: aminothiol gets reversible 2-FPBA shield (on=a, off=b).
    # Free unfinished site's SH can still be irreversibly capped (rate c_U).
    a=2.;c_U=c_P=.1
    for b in (0.,1e-6,1e-5,.0001,.001,.01):
        # Require product cap failure <=5e-6, so duration is fixed at earliest admissible
        t=math.log(1/(5e-6))/c_P
        p_survive=mask_protection_survival(t,a=a,b=b,c_U=c_U)
        p_pair=mask_good_pair(t,a=a,b=b,c_U=c_U,c_P=c_P)
        print('mask-off',b,'duration',t,'unfinished survives',p_survive,'pair success',p_pair,'1000 pairs',p_pair**1000)
    # Find permitted spontaneous mask-off for given two-site error budget
    t=math.log(1/5e-6)/c_P
    limit=brentq(lambda b:mask_protection_survival(t,a=a,b=b,c_U=c_U)-(1-5e-6),0,.01)
    print('mask-off ceiling for 5e-6 unfinished damage:',limit,'mean protected lifetime s:',1/limit)
    # Confirm natural gross harm formula by independently integrating the F occupancy flux.
    # dS/dt = -c_U*P(unmasked,t): compare finite difference of matrix solution.
    for b in (1e-4,.001):
        for t in (1,100):
            Q=np.array([[-a-c_U,a],[b,-b]],float)
            ini=np.array([b/(a+b),a/(a+b)])
            vec=ini@expm(Q*t)
            dS=(mask_protection_survival(t+1e-4,a=a,b=b,c_U=c_U)-mask_protection_survival(t-1e-4,a=a,b=b,c_U=c_U))/(2e-4)
            assert abs(dS+c_U*vec[0]) <1e-7
    print('CTMC derivative/flux identity PASS')
    # Direct write-once irreversible chemistry must protect its OWN new failure channels:
    # stable wrong attachment ratio, reagent hydrolysis, and product-DNA footprint.
    # Explicitly no claim those are acquired for 6-acyloxy-FPBA barcoded substrates.

    # Second distinct physical architecture: 6-acyloxy-FPBA reagent. Formation of
    # thiazolidino-boronate (TzB) is a reversible covalent NCys-capture; intramolecular
    # N-acyl transfer later yields stable N-acyl thiazolidine (both handles consumed).
    # Its chemical NCys association occurs without needing a correct DNA barcode.
    # Only if wrong-matched TzB reverses rapidly enough does DNA recognition help.
    k2=5000. # published order of magnitude M^-1 s^-1 for isolated KL42-associated NCys capture
    c_commit=math.log(2)/(0.3*3600) # approximate apparent pH 6 product half-time; illustrative for model
    cWrong=1e-9 # EACH of 255 free wrong donors at 1 nM, illustrative
    lambda_w=255*k2*cWrong
    lambda_c=.1 # illustrative fast correct-DNA docking/capture per second
    f_c=.5  # favorable correct TzB commitment probability before reversal
    eps=.99**(-1/1000)-1
    f_w_ceiling=eps*(lambda_c/lambda_w)*f_c
    rw_min=c_commit*(1/f_w_ceiling-1)
    print('256-way NCys reagent capture: wrong aggregate encounter hazard',lambda_w)
    per_wrong_limit=eps*lambda_c/(255*k2)
    min_matching_capture=lambda_w/eps
    print('If correct and wrong TzB have IDENTICAL commitment/reversal, wrong donor concentration must be <=',per_wrong_limit,'M per identity; at 1 nM each, correct capture must be >=',min_matching_capture,'per second')
    print('single correct dock/capture 0.1/s, assumed correct commit chance 0.5')
    print('target wrong thiazolidine commit fraction <=',f_w_ceiling,
          'required wrong precursor reversal/s >=',rw_min,
          'ratio over correct reversal',rw_min/c_commit)
    for correct_docking in (.01,.1,1.):
        bound=eps*(correct_docking/lambda_w)*f_c
        required=max(0,c_commit*(1/bound-1))
        print('correct capture rate',correct_docking,'wrong TzB reversal req',required)
    # Markov renewal equation includes occupancy time in BOTH correct/wrong
    # reversible covalent intermediates; intermediate DNA dissociation on its own
    # does not alter chemistry unless it actually changes reversal/commitment.
    def ligation_renewal(alpha_c,alpha_w,cc,rc,cw,rw):
        A=alpha_c*cc/(cc+rc);B=alpha_w*cw/(cw+rw)
        p=A/(A+B)
        T=(1+alpha_c/(cc+rc)+alpha_w/(cw+rw))/(A+B)
        return p,T
    p_sel,t_sel=ligation_renewal(lambda_c,lambda_w,c_commit,c_commit,c_commit,rw_min)
    assert abs(p_sel**1000-.99)<1e-10
    print('two-step 256-donor model conditional result P1000',p_sel**1000,
          'mean elapsed seconds per completed site',t_sel)
    # Wrong TzB and correct TzB with identical kinetics yield no proofreading:
    for off in (1e-4,.001,.1,1,10):
        p,_=ligation_renewal(lambda_c,lambda_w,c_commit,off,c_commit,off)
        assert abs(p-lambda_c/(lambda_c+lambda_w))<1e-11
    print('Two-step no-postcapture-discrimination theorem PASS')
    # One MC on a deliberately higher-error model validates the renewal ratio,
    # and does not share the matrix or gamma reduction algorithm.
    rng=np.random.default_rng(1221)
    testR=Donor(k=.3,w=.01,b=.04,r=.3,x=.2,h=.04,lam=.1)
    j=5;N=14000
    outcomes=np.zeros(2,int)
    for _ in range(N):
        state=0
        for steps in range(20000):
            if state==0:
                hazards=[testR.k,testR.w,testR.lam,j*testR.b]
                nxt=rng.choice(4,p=np.array(hazards)/sum(hazards))
                if nxt==0: outcomes[0]+=1;break
                if nxt==1: outcomes[1]+=1;break
                if nxt==2: continue # lost reagent replaced; parent unaffected
                state=1
            else:
                hazards=[testR.r,testR.x,testR.h]
                nxt=rng.choice(3,p=np.array(hazards)/sum(hazards))
                if nxt==1:outcomes[1]+=1;break
                # detached or hydrolyzed S-acyl donor; replace as needed
                state=0
        else:raise RuntimeError('excess MC steps')
    exact=stage_correct_eventually(j,testR)
    sample=outcomes[0]/N;stderr=math.sqrt(exact*(1-exact)/N)
    assert abs(sample-exact)<5*stderr,(sample,exact,stderr)
    print('stochastic donor recycling validation: measured',sample,'exact',exact,'PASS')

    print('ALL VERIFIED; no experimental kinetic claims made')

if __name__=='__main__':run()
