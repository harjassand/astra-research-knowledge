"""Frozen finite-table information-selection experiment. No kinetic trajectory."""
from pathlib import Path
import os,sys,json,time,hashlib,resource
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
resource.setrlimit(resource.RLIMIT_CPU,(120,125))
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
START=time.monotonic(); CPU=time.process_time()
import numpy as np
from scipy.optimize import linprog
D=Path(__file__).resolve().parent
SOURCE=D/'source'/'state_contraction'
sys.path.insert(0,str(SOURCE))
import contract_on2 as source
E=np.asarray(source.EN-source.EN[0],float)
EO=np.asarray(source.EO-source.EO[0],float)
N=len(E); MEAN=0.06417802570979354; e=E/E.max()
Aeq=np.zeros((4,2*N))
Aeq[0,:N]=1;Aeq[1,N:]=1;Aeq[2,:N]=e;Aeq[3,N:]=e
beq=np.array([1,1,MEAN/E.max(),MEAN/E.max()])
OPTIONS={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9}
COUNTS={'lp':0,'source_evaluations':0}; MAX_CHECKS={'equality':0.,'inequality':0.,'duality_gap':0.,'negative_population':0.}

def response(T,variant):
    COUNTS['source_evaluations']+=1
    k=np.asarray(source.rates(T,variant),float)
    return {'R':k.sum(1),'M':(k*(EO[None,:]-E[:,None])).sum(1)}

def diameter(k,B,eps,keep=False):
    scale=float(np.max(np.abs(k)))
    cost=np.r_[-k,k]/scale
    if len(B):
        C=np.c_[B,-B]; A=np.r_[C,-C]; b=np.full(2*len(B),2*eps)
    else:A=None;b=None
    sol=linprog(cost,A_ub=A,b_ub=b,A_eq=Aeq,b_eq=beq,bounds=(0,None),method='highs',options=OPTIONS)
    COUNTS['lp']+=1
    if not sol.success: raise RuntimeError(sol.message)
    err_eq=float(np.max(np.abs(Aeq@sol.x-beq)))
    err_ub=float(max(0,np.max(A@sol.x-b))) if A is not None else 0.
    neg=float(max(0,-sol.x.min()))
    dual=float(beq@sol.eqlin.marginals+(b@sol.ineqlin.marginals if b is not None else 0))
    gap=abs(float(sol.fun)-dual)
    for key,val in [('equality',err_eq),('inequality',err_ub),('negative_population',neg),('duality_gap',gap)]: MAX_CHECKS[key]=max(MAX_CHECKS[key],val)
    if max(err_eq,err_ub,neg,gap)>2e-7: raise AssertionError((err_eq,err_ub,neg,gap))
    out={'diameter':max(0.,-float(sol.fun)*scale),'scaled_duality_gap':gap,'max_primal_residual':max(err_eq,err_ub,neg)}
    if keep:
        p=sol.x[:N];q=sol.x[N:]
        out.update(p=p.tolist(),q=q.tolist(),response_p=float(k@p),response_q=float(k@q),feature_gap=(B@(p-q)).tolist() if len(B) else [])
    return out

def thresholds(cuts):return np.asarray([(np.arange(N)>=i).astype(float) for i in cuts]) if cuts else np.zeros((0,N))
train=[]
for T in [1700,2300,2700]:
    for name,k in response(T,'corrected_index').items():
        train.append((T,name,k,diameter(k,[],0)['diameter']))

design_start=time.monotonic();design_cpu=time.process_time()
selected=[];design_records=[]
for step in range(3):
    records=[]
    for cut in range(1,N):
        if cut in selected:continue
        B=thresholds(sorted(selected+[cut]))
        vals=[diameter(k,B,1e-6)['diameter']/base for T,name,k,base in train]
        records.append({'cut':cut,'worst':max(vals),'values':vals})
    winner=min(records,key=lambda r:(r['worst'],r['cut']))
    selected.append(winner['cut']);selected.sort()
    design_records.append({'step':step+1,'selected':selected[:],'winner':winner,'candidates':records})
design_cost={'wall_s':time.monotonic()-design_start,'cpu_s':time.process_time()-design_cpu,'lp_count_after_design':COUNTS['lp']}
energy_cuts=sorted(set(int(np.searchsorted(e,x)) for x in [.25,.5,.75]))
cheb=[]
for degree in [2,3,4]:
    coeff=np.zeros(degree+1);coeff[-1]=1
    cheb.append((1+np.polynomial.chebyshev.chebval(2*e-1,coeff))/2)
designs={'mean_only':np.zeros((0,N)),
    'moments_2_3_4':np.array([e**i for i in [2,3,4]]),
    'chebyshev_2_3_4':np.array(cheb),
    'equal_level_thresholds':thresholds([15,30,45]),
    'equal_energy_thresholds':thresholds(energy_cuts),
    'selected_thresholds':thresholds(selected),
    'full_population':np.eye(N)[:N-1]}
(D/'DESIGN_LOCK.json').write_text(json.dumps({'selected_thresholds':selected,'equal_energy_thresholds':energy_cuts,'design_records':design_records,'design_cost':design_cost,'preregistration_sha256':hashlib.sha256((D/'PREREGISTRATION.txt').read_bytes()).hexdigest()},indent=2)+'\n')

rows=[]; eval_start=time.monotonic();eval_cpu=time.process_time()
for T in [1500,1900,2100,2500,3000]:
    for variant in ['literal','corrected_index']:
        for output,k in response(T,variant).items():
            base=diameter(k,[],0)['diameter']
            for eps in [0.,1e-8,1e-6,1e-4]:
                for name,B in designs.items():
                    r=diameter(k,B,eps,True)
                    r.update(T_K=T,variant=variant,output=output,epsilon=eps,design=name,extra_observables=len(B),normalized_diameter=r['diameter']/base,baseline_diameter=base)
                    rows.append(r)
eval_cost={'wall_s':time.monotonic()-eval_start,'cpu_s':time.process_time()-eval_cpu}
summary=[]
for eps in [0.,1e-8,1e-6,1e-4]:
    for name in designs:
        rr=[r for r in rows if r['epsilon']==eps and r['design']==name]
        summary.append({'epsilon':eps,'design':name,'max_normalized_diameter':max(r['normalized_diameter'] for r in rr),'median_normalized_diameter':float(np.median([r['normalized_diameter'] for r in rr])),'R_worst':max(r['normalized_diameter'] for r in rr if r['output']=='R'),'M_worst':max(r['normalized_diameter'] for r in rr if r['output']=='M')})
out={'scope':__doc__,'source_files':{str(p.relative_to(D)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [SOURCE/'contract_on2.py',SOURCE.parent/'mode_evidence/2017_numeric_assignments.txt']},'mean_excitation_eV':MEAN,'selected_thresholds':selected,'equal_energy_thresholds':energy_cuts,'design_cost':design_cost,'evaluation_cost':eval_cost,'resources':{'wall_s':time.monotonic()-START,'cpu_s':time.process_time()-CPU,'max_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'enforced_CPU_soft_s':120,'enforced_address_space_bytes':1024**3,'unknown':'total inference, source-production, experiment-design and integration costs'},'counts':COUNTS,'max_checks':MAX_CHECKS,'summary':summary,'rows':rows,'limitations':['Mathematical observation/noise contract; not measured instrument costs.','Both source variants are model fits; no empirical validation.','No admissible population dynamics, reverse rates, full entropy constraint or complete cycle.','Floating LP checks are not rational positivity certificates.','No independent receiving use or amplification established.']}
(D/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['selected_thresholds','equal_energy_thresholds','resources','counts','max_checks','summary']},indent=2))
