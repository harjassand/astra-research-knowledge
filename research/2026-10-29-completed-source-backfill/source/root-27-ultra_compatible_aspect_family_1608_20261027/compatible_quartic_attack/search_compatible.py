"""Direct differential-compatible Jensen search, no SOS feasibility solver."""
import pathlib,json,time,argparse
import numpy as np
from scipy.optimize import minimize
from compatible_core import FourierProblem,half_square,derivative_check,ROOT

def run(starts=16,cutoff=1,iterations=600):
    freq=[(1,0),(0,1),(1,1),(1,-1)]if cutoff==1 else half_square(cutoff)
    problem=FourierProblem(freq);rng=np.random.default_rng(701+cutoff)
    out={'status':'RESTRICTED_COMPATIBLE_FOURIER_SEARCH_NO_GLOBAL_QC_ASSERTION',
        'derivative_check':derivative_check(),'frequency_count':len(freq),'runs':[]}
    path=ROOT/f'data/fourier_cutoff{cutoff}.json'
    for i in range(starts):
        start=time.monotonic();p=rng.normal(size=4*len(freq))
        opt=minimize(problem.evaluate,p,jac=True,method='L-BFGS-B',options={'maxiter':iterations,'ftol':1e-14,'gtol':2e-10,'maxls':50})
        rec=problem.evaluate(opt.x,details=True)
        rec.update({'start':i,'iterations':int(opt.nit),'function_evaluations':int(opt.nfev),
            'success':bool(opt.success),'message':str(opt.message),'seconds':time.monotonic()-start})
        out['runs'].append(rec);path.write_text(json.dumps(out,indent=2))
        print(cutoff,i,rec['objective_scaled'],rec['original_gap'],rec['gradient_norm'],rec['seconds'],flush=True)
    out['best_start']=min(range(len(out['runs'])),key=lambda i:out['runs'][i]['objective_scaled'])
    path.write_text(json.dumps(out,indent=2));return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--starts',type=int,default=16);p.add_argument('--cutoff',type=int,default=1);p.add_argument('--iterations',type=int,default=600);a=p.parse_args();run(a.starts,a.cutoff,a.iterations)
