"""Independent selective information-contract checks; no kinetic trajectory.

Reads the frozen source rates but not the producer LP function. Three selected
LPs are independently assembled in the original eV mean convention, then solved
with HiGHS IPM. All stored primal witnesses are re-evaluated. This is a floating
audit, not an exact source-rate or universal numerical certificate.
"""
from pathlib import Path
import os, sys, json, time, resource, hashlib, re
from fractions import Fraction
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
resource.setrlimit(resource.RLIMIT_CPU, (30,35))
resource.setrlimit(resource.RLIMIT_AS, (1024**3,1024**3))
START=time.monotonic(); CPU=time.process_time()
import numpy as np
from scipy.optimize import linprog
D=Path(__file__).resolve().parent
B=D.parent
sys.path.insert(0,str(B/'source/state_contraction'))
import contract_on2 as source
data=json.loads((B/'RESULTS.json').read_text())
E=np.asarray(source.EN-source.EN[0],float)
O=np.asarray(source.EO-source.EO[0],float)
mu=float(data['mean_excitation_eV']); n=len(E); e=E/max(E)
def features(name):
    if name=='mean_only':return np.empty((0,n))
    if name=='full_population':return np.eye(n)[:-1]
    if name=='moments_2_3_4':return np.array([e**j for j in [2,3,4]])
    if name=='chebyshev_2_3_4':
        x=2*e-1
        return np.array([(1+(2*x*x-1))/2,(1+(4*x*x*x-3*x))/2,(1+(8*x**4-8*x*x+1))/2])
    cuts={'equal_level_thresholds':[15,30,45], 'equal_energy_thresholds':data['equal_energy_thresholds'], 'selected_thresholds':data['selected_thresholds']}[name]
    return np.array([[float(i>=c) for i in range(n)] for c in cuts])
cache={}
def coefficient(T,var,output):
    key=(T,var)
    if key not in cache:
        k=np.asarray(source.rates(T,var),float)
        cache[key]={'R':k.sum(axis=1),'M':np.sum(k*(O[None,:]-E[:,None]),axis=1)}
    return cache[key][output]
checks={'normalization':0.,'original_mean_eV':0.,'negative_population':0.,'observation_violation':0.,'objective_relative_error':0.,'saved_response_relative_error':0.}
for row in data['rows']:
    p=np.array(row['p']);q=np.array(row['q']);f=features(row['design']);k=coefficient(row['T_K'],row['variant'],row['output'])
    checks['normalization']=max(checks['normalization'],abs(p.sum()-1),abs(q.sum()-1))
    checks['original_mean_eV']=max(checks['original_mean_eV'],abs(E@p-mu),abs(E@q-mu))
    checks['negative_population']=max(checks['negative_population'],max(0,-min(p.min(),q.min())))
    if len(f):checks['observation_violation']=max(checks['observation_violation'],max(0,float(np.max(np.abs(f@(p-q))))-2*row['epsilon']))
    scale=max(float(np.max(abs(k))),1e-300)
    checks['objective_relative_error']=max(checks['objective_relative_error'],abs(k@(p-q)-row['diameter'])/scale)
    checks['saved_response_relative_error']=max(checks['saved_response_relative_error'],abs(k@p-row['response_p'])/scale,abs(k@q-row['response_q'])/scale)
assert max(checks.values())<1e-9,checks

# Independent primal/dual reassembly. The equality rows use eV, not e=E/Emax.
eq=np.zeros((4,2*n));eq[0,:n]=1;eq[1,n:]=1;eq[2,:n]=E;eq[3,n:]=E
rhs=np.array([1,1,mu,mu]); audits=[]
for name in ['selected_thresholds','chebyshev_2_3_4','moments_2_3_4']:
    row=max((x for x in data['rows'] if x['design']==name and x['epsilon']==1e-6),key=lambda x:x['normalized_diameter'])
    k=coefficient(row['T_K'],row['variant'],row['output']);f=features(name);scale=max(abs(k))
    obj=np.concatenate((-k,k))/scale
    diff=np.concatenate((f,-f),axis=1);ineq=np.concatenate((diff,-diff),axis=0);bounds=np.full(len(ineq),2e-6)
    sol=linprog(obj,A_ub=ineq,b_ub=bounds,A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs-ipm',options={'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10,'ipm_optimality_tolerance':1e-12})
    assert sol.success,sol.message
    slack=obj-eq.T@sol.eqlin.marginals-ineq.T@sol.ineqlin.marginals
    dual=rhs@sol.eqlin.marginals+bounds@sol.ineqlin.marginals
    a={'design':name,'T_K':row['T_K'],'variant':row['variant'],'output':row['output'],
       'reported_diameter':row['diameter'],'independent_diameter':-sol.fun*scale,
       'objective_disagreement_scaled':abs(-sol.fun*scale-row['diameter'])/scale,
       'max_equality_residual_original_eV':float(max(abs(eq@sol.x-rhs))),
       'max_inequality_violation':float(max(0,max(ineq@sol.x-bounds))),
       'dual_sign_violation':float(max(0,max(sol.ineqlin.marginals))),
       'dual_feasibility_violation':float(max(0,-min(slack))),
       'stationarity_residual':float(max(abs(slack-sol.lower.marginals))),
       'primal_dual_gap_scaled':float(abs(sol.fun-dual)),
       'dual_equality':sol.eqlin.marginals.tolist(),'dual_inequality':sol.ineqlin.marginals.tolist()}
    assert max(a[x] for x in ['objective_disagreement_scaled','max_equality_residual_original_eV','max_inequality_violation','dual_sign_violation','dual_feasibility_violation','stationarity_residual','primal_dual_gap_scaled'])<1e-8,a
    audits.append(a)

# Exact population construction from the decimal source energy assignments.
txt=(B/'source/mode_evidence/2017_numeric_assignments.txt').read_text()
raw={int(i):Fraction(v.replace('D','E')) for i,v in re.findall(r'(?im)^\s*En2_onn_3Asec\((\d+)\)\s*=\s*([-+0-9.EeDd]+)',txt)}
energy=[raw[i]-raw[0] for i in range(n)]; mean=Fraction('0.06417802570979354')
states=[]
for j in [1,21]:
    p=[Fraction(0)]*n;p[j]=mean/energy[j];p[0]=1-p[j]
    assert sum(p)==1 and sum(x*y for x,y in zip(energy,p))==mean and min(p)>=0
    exact_features=[sum(p[i] for i in range(c,n)) for c in data['selected_thresholds']]
    assert exact_features==[0,0,0]
    values={variant:float(coefficient(3000,variant,'M')@np.array([float(x) for x in p])) for variant in ['literal','corrected_index']}
    states.append({'support':[0,j],'population_nonzero':[str(p[0]),str(p[j])],'exact_mean_eV':str(mean),'selected_features':list(map(str,exact_features)),'M_at3000':values})
assert all(x>0 for x in states[0]['M_at3000'].values())
assert all(x<0 for x in states[1]['M_at3000'].values())

# Exhaustive mean-polytope vertices: mean<E1, hence only supports {0,j} occur.
assert 0<mu<E[1]
global_sign=[]
for T in [1500,1686.4595074210936,1700,1900,2100,2500,3000]:
    for var in ['literal','corrected_index']:
        k=coefficient(T,var,'M')
        vals=[(float((1-mu/E[j])*k[0]+mu/E[j]*k[j]),j) for j in range(1,n)]
        lo=min(vals);hi=max(vals)
        global_sign.append({'T_K':T,'variant':var,'minimum':lo[0],'minimum_second_state':lo[1],'maximum':hi[0],'maximum_second_state':hi[1]})

out={'status':'PASS','scope':__doc__,'source_result_sha256':hashlib.sha256((B/'RESULTS.json').read_bytes()).hexdigest(),
     'stored_primal_witness_count':len(data['rows']),'stored_checks':checks,'independent_LPs':audits,
     'exact_mean_same_threshold_sign_pair':states,'global_M_sign_by_vertices':global_sign,
     'sign_scope':'Population feasibility and common selected-threshold observations are exact rational assertions; numerical source output signs use the saved QCT fit and are not interval-certified physical rates.',
     'costs':{'wall_s':time.monotonic()-START,'CPU_s':time.process_time()-CPU,'max_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'independent_LP_count':len(audits)},
     'limitations':['No independent reconstruction of underlying QCT potential or fit.','Only three representative optima replayed; every saved primal witness re-evaluated.','No exact rational dual certificate for source-rate functions.','No entropy or dynamic reachability constraints imposed.']}
(D/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','stored_primal_witness_count','stored_checks','exact_mean_same_threshold_sign_pair','costs']},indent=2))
