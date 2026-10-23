"""Exact conditional sign certificates for FROZEN computed coefficient vectors.

The rational certificate treats each independently recomputed binary64 M_v as an
exact number. It certifies the finite linear model with those frozen values, not
the transcendental source evaluation, source potential or physical coefficient.
Also selectively verifies the post-primary control's recorded adverse pairs and
one independently assembled optimum; no kinetic trajectory.
"""
from pathlib import Path
from fractions import Fraction
import os,sys,json,time,resource,re,hashlib
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
resource.setrlimit(resource.RLIMIT_CPU,(30,35));resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
start=time.monotonic();cpu=time.process_time()
import numpy as np
from scipy.optimize import linprog
D=Path(__file__).resolve().parent; B=D.parent
sys.path.insert(0,str(B/'source/state_contraction'));import contract_on2 as source
txt=(B/'source/mode_evidence/2017_numeric_assignments.txt').read_text()
raw={int(i):Fraction(v.replace('D','E')) for i,v in re.findall(r'(?im)^\s*En2_onn_3Asec\((\d+)\)\s*=\s*([-+0-9.EeDd]+)',txt)}
EE=[raw[i]-raw[0] for i in range(60)];mu=Fraction('0.06417802570979354')
E=np.array(list(map(float,EE)));O=np.asarray(source.EO-source.EO[0],float)
assert 0<mu<EE[1]
cache={}
def coeff(T,var,kind):
    key=(T,var)
    if key not in cache:
        k=np.asarray(source.rates(T,var),float)
        cache[key]={'R':k.sum(1),'M':(k*(O[None,:]-E[:,None])).sum(1)}
    return cache[key][kind]
sign=[]
for T in [1500,1686.4595074210936,1700,1900,2100,2500,3000]:
    for var in ['literal','corrected_index']:
        v=coeff(T,var,'M');f=[Fraction(float(x)) for x in v]
        slopes=[(f[j]-f[0])/EE[j] for j in range(1,60)]
        jmax=1+max(range(59),key=lambda j:slopes[j]);s=slopes[jmax-1];a=f[0]
        slacks=[a+s*EE[j]-f[j] for j in range(60)]
        assert min(slacks)>=0
        upper=a+s*mu
        # The {0,jmax} population attains the affine upper exactly.
        val=(1-mu/EE[jmax])*f[0]+mu/EE[jmax]*f[jmax]
        assert val==upper
        sign.append({'T_K':T,'variant':var,'frozen_coefficients':list(map(str,f)),
                     'affine_intercept':str(a),'affine_slope':str(s),
                     'all60_majorant_inequalities_exact':True,'attaining_support':[0,jmax],
                     'upper_exact':str(upper),'upper_float':float(upper),
                     'negative_for_all_fixed_mean_populations':upper<0})
r=json.loads((B/'STRONG_CONTROL_RESULTS.json').read_text());degrees=r['winner']['degrees'];e=E/max(E);F=np.array([e**j for j in degrees]);n=60
primal={'normalization':0.,'mean_eV':0.,'feature_excess':0.,'negative_population':0.,'objective_scaled_error':0.}
for row in r['rows']:
    p=np.array(row['p']);q=np.array(row['q']);k=coeff(row['T_K'],row['variant'],row['output']);s=max(abs(k))
    primal['normalization']=max(primal['normalization'],abs(p.sum()-1),abs(q.sum()-1))
    primal['mean_eV']=max(primal['mean_eV'],abs(E@p-float(mu)),abs(E@q-float(mu)))
    primal['feature_excess']=max(primal['feature_excess'],float(max(0,max(abs(F@(p-q)))-2*row['epsilon'])))
    primal['negative_population']=max(primal['negative_population'],float(max(0,-min(min(p),min(q)))))
    primal['objective_scaled_error']=max(primal['objective_scaled_error'],abs(k@(p-q)-row['diameter'])/s)
assert max(primal.values())<1e-9
row=max((x for x in r['rows'] if x['epsilon']==1e-6),key=lambda x:x['normalized_diameter'])
k=coeff(row['T_K'],row['variant'],row['output']);scale=max(abs(k));c=np.r_[-k,k]/scale
eq=np.zeros((4,120));eq[0,:60]=1;eq[1,60:]=1;eq[2,:60]=E;eq[3,60:]=E;rhs=np.array([1,1,float(mu),float(mu)])
dif=np.c_[F,-F];ineq=np.r_[dif,-dif];bound=np.full(6,2e-6)
sol=linprog(c,A_ub=ineq,b_ub=bound,A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs-ipm',options={'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10,'ipm_optimality_tolerance':1e-12})
assert sol.success
slack=c-eq.T@sol.eqlin.marginals-ineq.T@sol.ineqlin.marginals;dual=rhs@sol.eqlin.marginals+bound@sol.ineqlin.marginals
audit={'degrees':degrees,'T_K':row['T_K'],'variant':row['variant'],'output':row['output'],
       'independent_diameter':float(-sol.fun*scale),'reported_diameter':row['diameter'],
       'objective_disagreement_scaled':abs(-sol.fun*scale-row['diameter'])/scale,
       'equality_residual_eV':float(max(abs(eq@sol.x-rhs))),
       'inequality_violation':float(max(0,max(ineq@sol.x-bound))),
       'dual_sign_violation':float(max(0,max(sol.ineqlin.marginals))),
       'dual_feasibility_violation':float(max(0,-min(slack))),
       'stationarity_residual':float(max(abs(slack-sol.lower.marginals))),
       'duality_gap_scaled':float(abs(sol.fun-dual))}
# A valid dual certificate uses reconstructed nonnegative slack. The solver's
# separately returned bound marginal is redundant; its discrepancy is retained.
assert max(audit[j] for j in ['objective_disagreement_scaled','equality_residual_eV','inequality_violation','dual_sign_violation','dual_feasibility_violation','duality_gap_scaled'])<1e-8
out={'status':'PASS_RECONSTRUCTED_DUAL_WITH_REPORTED_MARGINAL_DISCREPANCY','scope':__doc__,'exact_frozen_sign_certificates':sign,
     'strong_control_source_sha256':hashlib.sha256((B/'STRONG_CONTROL_RESULTS.json').read_bytes()).hexdigest(),
     'strong_control_80_primal_checks':primal,'independent_strong_control_LP':audit,
     'costs':{'wall_s':time.monotonic()-start,'CPU_s':time.process_time()-cpu,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'new_LP_count':1}}
(D/'FROZEN_SIGN_AND_CONTROL.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'strong_control_primal':primal,'independent_strong_control_LP':audit,'costs':out['costs'],'native_sign':[{k:s[k] for k in ['T_K','variant','upper_float','negative_for_all_fixed_mean_populations']} for s in sign if s['T_K'] in [1686.4595074210936,1700]]},indent=2))
