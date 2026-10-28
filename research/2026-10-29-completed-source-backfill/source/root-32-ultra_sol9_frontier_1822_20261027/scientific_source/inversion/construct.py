"""Reproducible synthetic construction; no physical measurements are loaded.

Runtime: work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python
All rates, pulse maps and detector laws are declared inputs. Binomial records
are synthetic draws from their exact scalar forward means, not acquired data.
"""
from pathlib import Path
import json, math, time
import numpy as np
import sympy as sp
from scipy.linalg import expm, logm
from scipy.optimize import minimize
from scipy.optimize import brentq
from scipy.stats import norm, chi2

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'outputs'
OUT.mkdir(exist_ok=True)
RNG=np.random.default_rng(202610280903)

def save(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')

def finite(x):
    x=float(x)
    return x if np.isfinite(x) else ('-Infinity' if x<0 else 'Infinity')

def rational_construction():
    cases=[]
    for n in range(2,8):
        for repeat in range(3):
            rr=np.random.default_rng(177*n+repeat)
            cols=[]
            for i in range(n):
                v=list(map(int,rr.integers(1,20,n)));v[i]+=n*25
                cols.append([sp.Rational(x,sum(v)) for x in v])
            P=sp.Matrix(n,n,lambda j,i:cols[i][j])
            pp=list(map(int,rr.integers(1,12,n)))
            p=sp.Matrix([sp.Rational(x,sum(pp)) for x in pp])
            aa=[sp.Rational(int(x),20) for x in rr.integers(3,20,n)]
            beta=sp.Rational(1,37);gamma=sp.Rational(29,37)
            one=sp.ones(n,1);R=[]
            for i in range(n):
                r=sp.eye(n);r[i,i]-=aa[i];R.append(r)
            y0=beta+gamma
            E=[beta+gamma*(one.T*P*R[i]*p)[0] for i in range(n)]
            L=[beta+gamma*(one.T*R[j]*P*p)[0] for j in range(n)]
            ell=sp.Matrix([y0-e for e in E])
            pair=sp.Matrix(n,n,lambda j,i:beta+gamma*(one.T*R[j]*P*R[i]*p)[0])
            C=sp.Matrix(n,n,lambda j,i:pair[j,i]-E[i]-L[j]+y0)
            B=C*sp.diag(*[1/x for x in ell]);c=B.T.inv()*one
            recoveredP=sp.diag(*c)*B;g=(c.T*ell)[0]
            recoveredp=sp.diag(*c)*ell/g
            assert recoveredP==P and recoveredp==p and g==gamma and y0-g==beta
            assert [1/x for x in c]==aa
            rvec=sp.Matrix([y0-x for x in L])
            assert B*sp.diag(*ell)*c==rvec
            cases.append({'n':n,'repeat':repeat,'exact_recovered':True,'det_P':str(P.det())})
    # A singular operator can still satisfy the stronger full-data rank test.
    P=sp.Matrix([[sp.Rational(2,3)]*2,[sp.Rational(1,3)]*2])
    a=sp.Matrix([sp.Rational(2,5),sp.Rational(4,5)])
    p=sp.Matrix([sp.Rational(1,4),sp.Rational(3,4)])
    gamma=sp.Rational(4,5);B=sp.diag(*a)*P;ell=gamma*sp.diag(*a)*p
    M=B.T.col_join(B*sp.diag(*ell));d=sp.ones(2,1).col_join(gamma*sp.diag(*a)*P*p)
    c=(M.T*M).inv()*M.T*d
    assert M.rank()==2 and sp.diag(*c)*B==P
    return {'exact_cases':cases,'singular_case':{'P':str(P),'stacked_rank':M.rank(),'c':str(c)}}

def ring_generator(forward=4.,backward=1.,kill=None):
    cycle=[0,3,1,4,2,5];Q=np.zeros((6,6))
    for i in range(6):
        u,v=cycle[i],cycle[(i+1)%6]
        Q[v,u]=forward;Q[u,v]=backward
    np.fill_diagonal(Q,-Q.sum(axis=0))
    if kill is not None:Q-=np.diag(kill)
    return Q

EDGES=[(0,1),(1,2),(2,0),(1,0),(2,1),(0,2)]

def design_means(P,p,aE,aL,beta,gamma,groups=None,detector=None):
    n=len(p);labels=range(len(aE));one=np.ones(n)
    if groups is None:groups=[[i] for i in labels]
    RE=[];RL=[]
    for i,g in enumerate(groups):
        re=np.eye(n);rl=np.eye(n)
        re[g,g]-=aE[i];rl[g,g]-=aL[i];RE.append(re);RL.append(rl)
    def read(x):
        s=float(one@x)
        return beta+gamma*s if detector is None else detector(s)
    vals=[read(P@p)];names=['baseline']
    for i in labels:vals.append(read(P@RE[i]@p));names.append(f'early_{i}')
    for j in labels:vals.append(read(RL[j]@P@p));names.append(f'late_{j}')
    for i,j in EDGES:vals.append(read(RL[j]@P@RE[i]@p));names.append(f'pair_{i}_to_{j}')
    return np.array(vals),names

def contrast_map(k=3):
    T=np.zeros((len(EDGES),1+2*k+len(EDGES)))
    for e,(i,j) in enumerate(EDGES):
        T[e,0]=1;T[e,1+i]=-1;T[e,1+k+j]=-1;T[e,1+2*k+e]=1
    return T

T=contrast_map();SGN=np.array([1,1,1,-1,-1,-1])

def affinity(C):
    if np.any(C<=0):return None
    return float(SGN@np.log(C))

def confidence(C,eps):
    lo=np.maximum(0,C-4*eps);hi=C+4*eps
    amin=-np.inf if np.any(lo[:3]<=0) else np.log(lo[:3]).sum()-np.log(hi[3:]).sum()
    amax=np.inf if np.any(lo[3:]<=0) else np.log(hi[:3]).sum()-np.log(lo[3:]).sum()
    return {'A_lower':finite(amin),'A_upper':finite(amax),'reject_reversible':bool(amin>0 or amax<0),'contrast_lower':lo.tolist(),'contrast_upper':hi.tolist()}

def asymptotic_full_record(mu,m):
    C=T@mu;A=affinity(C)
    if A is None:return None
    gradient=T.T@(SGN/C)
    se=float(np.sqrt(np.sum(gradient**2*mu*(1-mu)/m)))
    return {'A':A,'standard_error':se,'normal_99_percent_interval':[A-norm.ppf(.995)*se,A+norm.ppf(.995)*se],
            'scope':'ordinary same-record delta method; asymptotic, not a finite-sample guarantee'}

def reversible_null_fit(counts,m):
    """Ordinary same-record likelihood, null enlarged to cycle-product equality.

    Variables are the 13 raw means, not a supplied hidden generator. Numerical
    convergence is reported, never treated as a global optimum certificate.
    """
    empirical=counts/m
    C=T@empirical
    def nll(mu):
        return float(-np.sum((counts/m)*np.log(mu)+(1-counts/m)*np.log1p(-mu)))
    def jac(mu):return -(counts/m)/mu+(1-counts/m)/(1-mu)
    def eq(mu):
        c=T@mu
        if np.any(c<=0):return 1e6+np.minimum(c,0).sum()*1e9
        return float(SGN@np.log(c))
    def eqjac(mu):return T.T@(SGN/(T@mu))
    constraints=[{'type':'eq','fun':eq,'jac':eqjac},
                 {'type':'ineq','fun':lambda mu:T@mu-1e-9,'jac':lambda mu:T}]
    starts=[empirical.copy()]
    # A reversible contrast seed obtained by replacing each pair of directed
    # contrasts by its geometric mean while leaving shared singles unchanged.
    c0=C.copy()
    for f,r in [(0,3),(1,4),(2,5)]:c0[f]=c0[r]=np.sqrt(max(C[f]*C[r],1e-12))
    alt=empirical.copy();alt[7:]=c0-empirical[0]+empirical[1+np.array([i for i,j in EDGES])]+empirical[4+np.array([j for i,j in EDGES])]
    starts.append(np.clip(alt,1e-6,1-1e-6))
    fits=[]
    for start in starts:
        z=minimize(nll,start,jac=jac,method='SLSQP',bounds=[(1e-8,1-1e-8)]*len(empirical),
                   constraints=constraints,options={'maxiter':2000,'ftol':1e-10})
        fits.append(z)
    good=[z for z in fits if z.success and abs(eq(z.x))<1e-6 and np.all(T@z.x>0)]
    z=min(good or fits,key=lambda x:x.fun)
    dev=2*m*(nll(z.x)-nll(empirical))
    return {'success':bool(z.success),'message':str(z.message),'constraint_residual':eq(z.x),
            'fitted_means':z.x.tolist(),'fitted_contrasts':(T@z.x).tolist(),
            'binomial_deviance':float(dev),'asymptotic_chi_square_1_p':float(chi2.sf(max(dev,0),1)),
            'all_starts':[{'success':bool(z0.success),'objective':float(z0.fun),'iterations':int(z0.nit)} for z0 in fits],
            'scope':'ordinary same-record numerical constrained likelihood; null is a superset of reversible hidden generators; p value asymptotic only; no global optimality claim'}

def exact_sign_certificate(counts,m):
    """Exact rational sign and a rational check of the Hoeffding tail budget.

    For this fixed design epsilon=1/500, 2*m*epsilon^2=8. A positive Taylor
    partial sum lower-bounds exp(8), certifying 26*exp(-8)<1/100. Logs are
    used only to display the interval endpoint, never to decide its sign.
    """
    assert m==1000000 and len(counts)==13
    epsilon=sp.Rational(1,500);t=2*m*epsilon**2
    exp_lower=sum(t**k/sp.factorial(k) for k in range(41))
    alpha_upper=sp.Rational(26,1)/exp_lower
    assert alpha_upper<sp.Rational(1,100)
    T_exact=sp.Matrix(T.astype(int).tolist())
    C=T_exact*sp.Matrix([sp.Rational(int(k),m) for k in counts])
    lowerf=[x-4*epsilon for x in C[:3]]
    upperr=[x+4*epsilon for x in C[3:]]
    F=sp.prod(lowerf);R=sp.prod(upperr);positive=bool(min(lowerf)>0 and F>R)
    return {'mean_epsilon_exact':str(epsilon),'confidence_error_budget_exact':'1/100',
            'exp8_positive_Taylor_terms':41,'exact_Hoeffding_union_bound_upper':str(alpha_upper),
            'confidence_error_bound_display':float(alpha_upper),
            'contrasts_exact':[str(x) for x in C],
            'forward_lower_product_exact':str(F),'reverse_upper_product_exact':str(R),
            'product_difference_exact':str(F-R),'reject_reversible_exact_sign':positive,
            'A_lower_display_only':float(sp.log(F/R)) if min(lowerf)>0 else '-Infinity',
            'scope':'exact rational sign and analytic IID bounded-trial tail bound; synthetic record is not an acquired experiment or a finite-bit IID guarantee'}

def synthetic_cycle():
    Q=ring_generator();tau=.3;P=expm(Q*tau)
    p=np.array([.3,.25,.2,.1,.08,.07])
    # Early and late efficiencies deliberately differ; the cycle cancels both.
    aE=np.array([.75,.92,.84]);aL=np.array([.91,.78,.87])
    beta=.03;gamma=.9;m=1000000;alpha=.01
    mu,names=design_means(P,p,aE,aL,beta,gamma)
    C=T@mu;Ap=affinity(np.array([P[j,i] for i,j in EDGES]))
    assert abs(affinity(C)-Ap)<1e-10
    counts=RNG.binomial(m,mu);hat=counts/m;Chat=T@hat
    eps=math.sqrt(math.log(2*len(mu)/alpha)/(2*m))
    record={'source':'synthetic binomial, not experimental',
            'inputs':{'Q':Q.tolist(),'tau':tau,'p':p.tolist(),'early_efficiencies':aE.tolist(),'late_efficiencies':aL.tolist(),'beta':beta,'gamma':gamma,'m_per_setting':m,'alpha':alpha},
            'setting_names':names,'exact_means':mu.tolist(),'synthetic_counts':counts.tolist(),
            'exact_contrasts':C.tolist(),'empirical_contrasts':Chat.tolist(),'exact_P_selected':P[:3,:3].tolist(),
            'exact_cycle_affinity':Ap,'empirical_cycle_affinity':affinity(Chat),
            'hoeffding_epsilon':eps,'confidence':confidence(Chat,eps),
            'exact_finite_confidence_sign':exact_sign_certificate(counts,m),
            'total_preparations':int(len(mu)*m),'total_terminal_readouts':int(len(mu)*m),'total_loss_pulses':int(18*m),
            'full_record_delta_comparator':asymptotic_full_record(hat,m),
            'full_record_likelihood_comparator':reversible_null_fit(counts,m)}
    # Distribution-free certificate degradation with deterministic mean drift.
    record['systematic_error_sweep']=[{'per_setting_mean_error_budget':e,**confidence(Chat,eps+e)} for e in [0,.0001,.0003,.0005,.001,.002,.005]]
    # Independent synthetic repeated records quantify this one model only.
    repetitions=2000;rep_counts=RNG.binomial(m,mu,size=(repetitions,len(mu)));repC=(rep_counts/m)@T.T
    repA=np.log(repC)@SGN
    rejected=np.array([confidence(c,eps)['reject_reversible'] for c in repC])
    record['repeated_synthetic_model']={'repetitions':repetitions,'all_contrasts_positive':bool(np.all(repC>0)),
                                      'affinity_bias':float(repA.mean()-Ap),'affinity_RMSE':float(np.sqrt(np.mean((repA-Ap)**2))),
                                      'rigorous_interval_rejections':int(rejected.sum()),
                                      'scope':'finite synthetic model diagnostic, not proof of power or physical validation'}
    return record

def reversible_controls():
    out=[]
    for r in range(30):
        n=int(RNG.integers(4,15));weights=RNG.uniform(.1,1,(n,n));weights=(weights+weights.T)/2;np.fill_diagonal(weights,0)
        pi=RNG.uniform(.2,2,n);pi/=pi.sum()
        Q=weights/pi[None,:];np.fill_diagonal(Q,0);np.fill_diagonal(Q,-Q.sum(0))
        # State-dependent killing is symmetric in the same reversible measure.
        if r%2:Q-=np.diag(RNG.uniform(0,1,n))
        p=RNG.uniform(.1,2,n);p/=p.sum();ae=RNG.uniform(.2,1,3);al=RNG.uniform(.2,1,3)
        P=expm(Q*float(RNG.uniform(.005,.05)))
        mu,_=design_means(P,p,ae,al,.03,.9);A=affinity(T@mu)
        assert abs(A)<2e-9
        out.append({'n':n,'state_dependent_killing':bool(r%2),'cycle_affinity_numerical':A})
    return out

def falsifiers():
    n=6;P=sp.eye(n)*sp.Rational(4,5)
    for i in range(n):P[(i+1)%n,i]=P[(i-1)%n,i]=sp.Rational(1,10)
    p=sp.Matrix([sp.Rational(i,21) for i in range(1,7)])
    groups=[[0,1],[2,3],[4,5]];C=sp.zeros(3)
    for j in range(3):
        for i in range(3):C[j,i]=sum(P[y,x]*p[x] for y in groups[j] for x in groups[i])
    ratio=(C[1,0]*C[2,1]*C[0,2])/(C[0,1]*C[1,2]*C[2,0])
    assert ratio==sp.Rational(16,5) and P==P.T
    Q=np.zeros((6,6))
    for i in range(6):Q[(i+1)%6,i]=Q[(i-1)%6,i]=1
    np.fill_diagonal(Q,-2);ctmc=[]
    pn=np.arange(1,7)/21
    for tau in [.001,.01,.1,.3]:
        mu,_=design_means(expm(Q*tau),pn,np.array([.6,.8,.7]),np.array([.9,.7,.8]),.03,.9,groups=groups)
        ctmc.append({'tau':tau,'false_coarse_affinity':affinity(T@mu)})
    # Nonlinear detector can fail even with resolved states and reversible P.
    P3=np.array([[.7,.2,.1],[.2,.6,.2],[.1,.2,.7]])
    mu,_=design_means(P3,np.array([.15,.55,.3]),np.array([.4,.8,.6]),np.array([.4,.8,.6]),0,1,detector=lambda x:x*x)
    return {'unresolved_groups':{'full_symmetric_P':str(P),'p':str(p),'groups':groups,'exact_false_cycle_ratio':str(ratio),'exact_false_affinity':float(sp.log(ratio)),'reversible_CTMCS':ctmc},
            'nonlinear_detector':{'law':'y=s^2','full_symmetric_P':P3.tolist(),'scalar_means':mu.tolist(),'false_cycle_affinity':affinity(T@mu)}}

def floating_full_tomography():
    n=5;rates=RNG.uniform(.05,.6,(n,n));np.fill_diagonal(rates,0)
    Q=rates.copy();np.fill_diagonal(Q,-Q.sum(0));Lambda=float(max(-np.diag(Q)));tau=.2/Lambda
    P=expm(Q*tau);p=RNG.uniform(.5,1.5,n);p/=p.sum();a=RNG.uniform(.3,.9,n);g=.9;b=.03
    E=np.eye(n)-np.diag(a);ell=g*a*p;B=np.diag(a)@P;c=np.linalg.solve(B.T,np.ones(n));Phat=np.diag(c)@B
    recoveredgamma=float(c@ell);recoveredp=c*ell/recoveredgamma;Qhat=logm(Phat).real/tau
    assert np.max(np.abs(Phat-P))<1e-12 and np.max(np.abs(Qhat-Q))<1e-10
    return {'Q':Q.tolist(),'tau':tau,'Lambda':Lambda,'a':a.tolist(),'p':p.tolist(),'gamma':g,'beta':b,
            'P_max_absolute_error':float(np.max(np.abs(Phat-P))),'Q_max_absolute_error':float(np.max(np.abs(Qhat-Q))),
            'p_max_absolute_error':float(np.max(np.abs(recoveredp-p))),'gamma_absolute_error':abs(recoveredgamma-g),
            'scope':'declared-model floating reconstruction only; exact algebra is separate'}

def one_state_operation():
    """Four-setting return-revival operation and exact signed-mean certificate."""
    n=8;Q=np.zeros((n,n))
    for i in range(n):Q[(i+1)%n,i]=1.;Q[(i-1)%n,i]=.05
    np.fill_diagonal(Q,-Q.sum(0));p=np.array([.4]+[.6/7]*7)
    ae=.85;al=.9;beta=.03;gamma=.92;t1=4.;t2=8.;m=100000
    E=np.eye(n);L=np.eye(n);E[0,0]-=ae;L[0,0]-=al
    mu=[];returns=[]
    for t in [t1,t2]:
        P=expm(Q*t);returns.append(float(P[0,0]))
        mu += [beta+gamma*np.ones(n)@L@P@p,
               beta+gamma*np.ones(n)@L@P@E@p]
    mu=np.array(mu);signs=np.array([1,-1,-1,1]);D=float(signs@mu)
    assert abs(D-gamma*ae*al*p[0]*(returns[1]-returns[0]))<1e-12
    counts=RNG.binomial(m,mu);phat=counts/m;Dhat=float(signs@phat)
    de=sp.Rational(1,100);Dhat_exact=sum(int(s)*sp.Rational(int(k),m) for s,k in zip(signs,counts))
    exponent=sp.Rational(m,2)*de**2
    exp_lower=sum(exponent**j/sp.factorial(j) for j in range(41))
    alpha_upper=1/exp_lower
    assert alpha_upper<sp.Rational(1,100)
    exact_lower=Dhat_exact-de
    # Ordinary convex constrained binomial likelihood. One scalar Lagrange
    # multiplier solves the KKT equations for the linear null signs@mu<=0.
    def at_lambda(lam):
        if abs(lam)<1e-12:return phat.copy()
        k=lam*signs
        return 2*phat/(1+k+np.sqrt((1+k)**2-4*k*phat))
    if Dhat>0:
        high=1.
        while signs@at_lambda(high)>0:high*=2
        lam=brentq(lambda x:signs@at_lambda(x),0,high,xtol=1e-14)
        null=at_lambda(lam)
    else:lam=0.;null=phat.copy()
    dev=float(2*m*np.sum(phat*np.log(phat/null)+(1-phat)*np.log((1-phat)/(1-null))))
    se=float(np.sqrt(np.sum(phat*(1-phat))/m))
    record={'source':'synthetic binomial, not experimental',
            'inputs':{'Q':Q.tolist(),'p':p.tolist(),'early_efficiency':ae,'late_efficiency':al,'beta':beta,'gamma':gamma,'t1':t1,'t2':t2,'m_per_setting':m},
            'setting_names':['late_t1','early_and_late_t1','late_t2','early_and_late_t2'],
            'exact_means':mu.tolist(),'synthetic_counts':counts.tolist(),'P00_at_delays':returns,
            'true_D':D,'observed_D':Dhat,'observed_D_exact':str(Dhat_exact),
            'exact_confidence':{'subtraction_d_exact':str(de),'D_lower_exact':str(exact_lower),
                                'D_lower_display':float(exact_lower),'reject_reversible_exact_sign':bool(exact_lower>0),
                                'Hoeffding_exp_argument':str(exponent),'positive_Taylor_terms':41,
                                'exact_error_upper':str(alpha_upper),'error_upper_display':float(alpha_upper),
                                'scope':'exact rational signed-mean bound under independent bounded observations, not a finite-bit IID guarantee or physical measurement'},
            'total_preparations':4*m,'total_terminal_readouts':4*m,'total_loss_pulses':6*m,
            'ordinary_same_record_analysis':{'point_estimate':Dhat,'standard_error':se,
                                            'normal_one_sided_99_percent_lower':Dhat-norm.ppf(.99)*se,
                                            'constrained_null_means':null.tolist(),'Lagrange_multiplier':lam,
                                            'linear_constraint_residual':float(signs@null),'binomial_deviance':dev,
                                            'asymptotic_one_sided_chi_bar_square_p':float(.5*chi2.sf(max(dev,0),1)),
                                            'scope':'same four raw records and all nuisance promises; convex null with analytic KKT reduction and numerical scalar root; p value and normal interval asymptotic only; no advantage claimed'},
            'systematic_budget_threshold_exact':str(exact_lower/4),
            'lag_selection_scope':'predeclared demonstration pair chosen from the declared model; physical lag discovery and multiple-testing/scanning costs are not acquired'}
    # Two sharp false witnesses if physical premises are dropped.
    q=np.array([[-.1,.1,0],[.1,-10.1,10],[0,10,-10]])
    pcoarse=np.array([.01,.98,.01]);group=np.array([1.,1.,0.])
    coarse_times=[.5,10.]
    coarse_returns=[float(group@expm(q*t)@(pcoarse*group)) for t in coarse_times]
    record['reversible_unresolved_group_falsifier']={'symmetric_Q':q.tolist(),'p':pcoarse.tolist(),'group':[0,1],
                                                   'times':coarse_times,'group_return_joint':coarse_returns,
                                                   'false_revival':coarse_returns[1]-coarse_returns[0],
                                                   'scope':'microscopically reversible; unresolved transient macrostate invalidates theorem'}
    tlo,thi=.5,2.;aa=.5;ll=.6
    false=aa*(1-ll)*(math.exp(-tlo)-math.exp(-thi))
    record['reversible_natural_loss_falsifier']={'one_state_subgenerator':-1,'early_efficiency':aa,'late_efficiency':ll,
                                              'times':[tlo,thi],'false_four_setting_D':false,
                                              'eight_setting_C_difference':aa*ll*(math.exp(-thi)-math.exp(-tlo)),
                                              'scope':'diagonal reversible decay fakes the four-setting shortcut; eight-setting inclusion-exclusion repairs it'}
    return record

def ordinal_monotone_detector_operation():
    """A stronger detector nuisance model, using a sufficient crossed order."""
    n=32;rates=np.array([1.]+[31/5]*31);Q=np.zeros((n,n))
    for i in range(n):Q[(i+1)%n,i]=rates[i]
    np.fill_diagonal(Q,-rates)
    pi=np.array([1/6]+[5/186]*31);p=np.array([8/31]+[23/961]*31)
    ae=17/20;al=9/10;m=100000;times=[3.,6.]
    assert np.max(np.abs(Q@pi))<1e-12 and abs(p.sum()-1)<1e-12
    theta=17/155
    assert np.max(np.abs(p-((1-theta)*pi+theta*np.eye(n)[0])))<1e-12
    assert abs(theta-ae*p[0]/2)<1e-12
    E=np.eye(n);L=np.eye(n);E[0,0]-=ae;L[0,0]-=al
    population=[];returns=[]
    for t in times:
        P=expm(Q*t);returns.append(float(P[0,0]))
        population.extend([float(np.ones(n)@L@P@p),float(np.ones(n)@L@P@E@p)])
    population=np.array(population)
    # This law is used only by the synthetic data generator. The analysis uses
    # only its strict monotonicity, never its inverse or derivative.
    mu=.01+.98*population**2
    counts=RNG.binomial(m,mu);emp=counts/m
    # Positive order contrasts are late(t1)-late(t2), both(t2)-both(t1).
    pairs=[(0,2),(3,1)]
    exact_diff=[sp.Rational(int(counts[a])-int(counts[b]),m) for a,b in pairs]
    d=sp.Rational(3,400);exponent=m*d*d
    exp_lower=sum(exponent**j/sp.factorial(j) for j in range(41))
    alpha_upper=2/exp_lower
    assert alpha_upper<sp.Rational(1,100)
    margins=[x-d for x in exact_diff]
    component=[]
    for a,b in pairs:
        pooled=(emp[a]+emp[b])/2
        if emp[a]>emp[b]:
            kl=sum(emp[z]*math.log(emp[z]/pooled)+(1-emp[z])*math.log((1-emp[z])/(1-pooled)) for z in [a,b])
            dev=2*m*kl
        else:dev=0.
        component.append({'ordered_setting_indices':[a,b],'empirical_difference':float(emp[a]-emp[b]),
                          'null_pooled_mean':float(pooled),'binomial_deviance':float(dev),
                          'asymptotic_one_sided_p':float(.5*chi2.sf(max(dev,0),1)) if dev>0 else 1.})
    record={'source':'synthetic binomial, not experimental',
            'inputs':{'Q':Q.tolist(),'stationary_pi':pi.tolist(),'nonstationary_p':p.tolist(),
                      'early_efficiency_exact':'17/20','late_efficiency_exact':'9/10',
                      'detector_law_used_only_to_generate':'1/100+(49/50)*s^2',
                      't1':times[0],'t2':times[1],'m_per_setting':m},
            'setting_names':['late_t1','early_and_late_t1','late_t2','early_and_late_t2'],
            'underlying_populations':population.tolist(),'exact_means':mu.tolist(),'synthetic_counts':counts.tolist(),
            'P00_at_delays':returns,'exact_order_differences_display':[float(mu[a]-mu[b]) for a,b in pairs],
            'empirical_order_differences_exact':[str(x) for x in exact_diff],
            'exact_confidence':{'per_difference_subtraction_exact':str(d),
                                'positive_margins_exact':[str(x) for x in margins],
                                'positive_margins_display':[float(x) for x in margins],
                                'both_orderings_certified':bool(min(margins)>0),
                                'Hoeffding_exp_argument':str(exponent),'positive_Taylor_terms':41,
                                'exact_simultaneous_error_upper':str(alpha_upper),'error_upper_display':float(alpha_upper),
                                'scope':'simultaneous exact-rational sign plus analytic IID bounded-trial confidence, conditional on fixed strictly increasing total detector and other physical premises; synthetic record is not physical or finite-bit IID validation'},
            'total_preparations':4*m,'total_terminal_readouts':4*m,'total_loss_pulses':6*m,
            'ordinary_same_record_comparator':{'null':'union of the two nonpositive-order halfspaces; supplied no hidden rates, initial population or detector law',
                                              'component_pooled_MLE_fits':component,
                                              'union_null_best_fit_deviance':float(min(x['binomial_deviance'] for x in component)),
                                              'asymptotic_intersection_union_p':float(max(x['asymptotic_one_sided_p'] for x in component)),
                                              'scope':'standard ordinary pooled-binomial likelihood on exactly the same records; p values asymptotic only; no advantage claimed'},
            'systematic_mean_bias_limit_per_setting_exact':str(min(margins)/2),
            'physical_access':'only state0 selective loss and aggregate total count assumed; all31 intermediate states inaccessible',
            'lag_and_prep_selection':'chosen from declared model, not discovered or acquired in a real specimen; actual search/preparation/validation costs remain unacquired'}
    return record

if __name__=='__main__':
    started=time.perf_counter()
    exact=rational_construction();save('exact_reconstruction.json',exact)
    record=synthetic_cycle();save('synthetic_cycle_record.json',record)
    controls=reversible_controls();save('reversible_controls.json',controls)
    bad=falsifiers();save('essential_premise_falsifiers.json',bad)
    full=floating_full_tomography();save('full_tomography_float.json',full)
    one=one_state_operation();save('one_state_record.json',one)
    ordinal=ordinal_monotone_detector_operation();save('ordinal_one_state_record.json',ordinal)
    summary={'status':'CONDITIONAL_OPERATION_CONSTRUCTED; MISSION_NOT_ACHIEVED',
             'exact_rational_reconstruction_cases':len(exact['exact_cases']),
             'cycle_affinity_true':record['exact_cycle_affinity'],
             'cycle_affinity_estimated':record['empirical_cycle_affinity'],
             'rigorous_99_percent_interval':record['confidence'],
             'exact_finite_confidence_sign':record['exact_finite_confidence_sign'],
             'preparations':record['total_preparations'],'loss_pulses':record['total_loss_pulses'],
             'ordinary_likelihood':{k:v for k,v in record['full_record_likelihood_comparator'].items() if k not in ['fitted_means','fitted_contrasts']},
             'ordinary_delta':record['full_record_delta_comparator'],
             'reversible_model_controls':len(controls),
             'max_reversible_abs_affinity':float(max(abs(x['cycle_affinity_numerical']) for x in controls)),
             'unresolved_group_false_ratio':bad['unresolved_groups']['exact_false_cycle_ratio'],
             'nonlinear_detector_false_affinity':bad['nonlinear_detector']['false_cycle_affinity'],
             'one_state_operation':{'true_D':one['true_D'],'observed_D':one['observed_D'],
                                    'exact_confidence':one['exact_confidence'],
                                    'preparations':one['total_preparations'],'loss_pulses':one['total_loss_pulses'],
                                    'ordinary_same_record_analysis':one['ordinary_same_record_analysis'],
                                    'systematic_budget_threshold_exact':one['systematic_budget_threshold_exact']},
             'ordinal_monotone_detector_operation':{'exact_confidence':ordinal['exact_confidence'],
                                                    'preparations':ordinal['total_preparations'],'loss_pulses':ordinal['total_loss_pulses'],
                                                    'ordinary_same_record_comparator':ordinal['ordinary_same_record_comparator'],
                                                    'systematic_mean_bias_limit_per_setting_exact':ordinal['systematic_mean_bias_limit_per_setting_exact']},
             'elapsed_seconds':time.perf_counter()-started}
    save('RESULTS.json',summary);print(json.dumps(summary,indent=2))
