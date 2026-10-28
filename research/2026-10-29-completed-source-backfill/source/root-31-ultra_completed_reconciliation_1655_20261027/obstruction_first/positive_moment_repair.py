"""Joint diagnostic repair of the witness using all-length trace positivity.

Search stage uses continuous weights. A successful LP is not an integer
counting-spectrum certificate and must not be reported as one.
"""
import pathlib,sys,json,math,time
import construct_moment_witness as w
from scipy.optimize import least_squares
import mpmath as mp
mp.mp.dps=90;mp.iv.dps=75
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as F
ROOT=pathlib.Path(__file__).resolve().parent


def run():
    v=1.1;cap=1.09;limit=10**9
    stop=math.ceil(math.log(3*limit/2)/math.log(v/cap))+1
    grid=np.linspace(-cap,cap,601);grid=grid[np.abs(grid)>.015];ng=len(grid)
    # Midpoints of actual validated I/P intervals, transformed exactly.
    z={}
    for n in range(4,9):
        for p in range(2):
            j=json.loads((ROOT/f'data/trace_n{n}_p{p}_b12.json').read_text());z[n,p]=(F(j['trace_lower'])+F(j['trace_upper']))/2
    targetJ=np.array([float((z[n,0]+3*z[n,1])/4)for n in range(4,9)])
    targetN=np.array([float((z[n,0]-z[n,1])/4)for n in range(4,9)])
    ns=np.arange(4,9);fixed=2*v**ns
    scaleJ=np.maximum(np.abs(targetJ),1);scaleN=np.maximum(np.abs(targetN),1)
    # Optimize weighted masses w_i=count_i*x_i^4. Direct count variables made
    # important M8 columns fall below HiGHS' small-matrix threshold; independently
    # computed equality residuals rejected that first apparent solver success.
    mat=grid[None,:]**(ns[:,None]-4)
    aeq=np.zeros((10,2*ng));aeq[:5,:ng]=mat/scaleJ[:,None];aeq[5:,ng:]=mat/scaleN[:,None]
    beq=np.r_[(targetJ-fixed)/scaleJ,targetN/scaleN]
    rows=[];rhs=[]
    for n in range(9,stop+1):
        power=(grid/v)**n/grid**4
        # Both extremal characters: Z_I=J+3N and Z_P=J-N. Every SO(3)
        # twist of a spin0+spin1 representation lies between these endpoints.
        if n%2:
            rows.append(-np.r_[power,3*power]);rhs.append(1.99)
        rows.append(-np.r_[power,-power]);rhs.append(1.99)
    rows.append(np.r_[1/grid**4,1/grid**4]/limit);rhs.append(1.)
    start=time.monotonic()
    cost=1+np.random.default_rng(271029).random(2*ng)
    solutions=[]
    for trial in range(4):
        result=linprog(cost,A_eq=aeq,b_eq=beq,A_ub=np.array(rows),b_ub=np.array(rhs),bounds=(0,None),method='highs',options={'threads':1,'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
        if result.success:solutions.append(result.x)
        cost=1+np.random.default_rng(271030+trial).random(2*ng)
    out={'status':'CONTINUOUS_WEIGHT_DIAGNOSTIC_ONLY','success':bool(result.success),'message':result.message,'tail_stop':stop,'seconds':time.monotonic()-start}
    if result.success:
        result.x=np.mean(solutions,axis=0)
        take=np.flatnonzero(result.x>1e-7);out['atoms']=[{'sector':'J'if i<ng else 'N','value':float(grid[i%ng]),'weight':float(result.x[i]/grid[i%ng]**4)}for i in take];out['max_equality_residual']=float(np.max(np.abs(aeq@result.x-beq)));out['minimum_positivity_slack']=float(np.min(np.array(rhs)-np.array(rows)@result.x));out['sum_weights']=float(sum(r['weight']for r in out['atoms']))
        assert out['max_equality_residual']<1e-6,out
    (ROOT/'data/positive_moment_repair_lp.json').write_text(json.dumps(out,indent=2));print(out)
    return out


def exact_repair():
    lp=json.loads((ROOT/'data/positive_moment_repair_lp.json').read_text());assert lp['success'] and lp['max_equality_residual']<1e-6
    boxes={};z={}
    for n in range(4,9):
        for p in range(2):
            j=json.loads((ROOT/f'data/trace_n{n}_p{p}_b12.json').read_text());lo,hi=F(j['trace_lower']),F(j['trace_upper']);boxes[n,p]=(lo,hi);z[n,p]=(lo+hi)/2
    targets={'J':{n:(z[n,0]+3*z[n,1])/4 for n in range(4,9)},'N':{n:(z[n,0]-z[n,1])/4 for n in range(4,9)}}
    spectra={};moments={}
    for sector in ['J','N']:
        atoms=[a for a in lp['atoms']if a['sector']==sector];counts=np.array([math.ceil(a['weight'])for a in atoms],dtype=np.int64);x0=np.array([a['value']*(a['weight']/c)**.25 for a,c in zip(atoms,counts)])
        ns=np.arange(4,9);target=targets[sector];fixed=[(2,F(11,10))]if sector=='J'else[]
        goals=[mp.mpf(target[n].numerator)/target[n].denominator-sum(c*(mp.mpf(x.numerator)/x.denominator)**n for c,x in fixed)for n in range(4,9)]
        ys=np.array([float(x)for x in goals]);scale=np.maximum(np.abs(ys),1.)
        def res(x):return (np.sum(counts[None,:]*x[None,:]**ns[:,None],axis=1)-ys)/scale
        def jac(x):return counts[None,:]*ns[:,None]*x[None,:]**(ns[:,None]-1)/scale[:,None]
        fit=least_squares(res,x0,jac=jac,bounds=(-1.099,1.099),xtol=2e-15,ftol=2e-15,gtol=2e-15,max_nfev=5000,x_scale='jac')
        print('integer-count refinement',sector,fit.message,'residual',res(fit.x),'nodes',fit.x,flush=True)
        roots=mp.matrix([mp.mpf(float(x))for x in fit.x]);scales=[max(abs(x),1)for x in goals]
        for iteration in range(80):
            err=mp.matrix([(sum(int(c)*x**n for c,x in zip(counts,roots))-goal)/scale for n,goal,scale in zip(range(4,9),goals,scales)])
            if max(abs(x)for x in err)<mp.mpf('1e-75'):break
            jacobian=mp.matrix([[int(c)*n*x**(n-1)/scale for c,x in zip(counts,roots)]for n,scale in zip(range(4,9),scales)])
            change=-jacobian.T*mp.lu_solve(jacobian*jacobian.T,err)
            step=mp.mpf(1)
            while any(abs(x+step*d)>=mp.mpf('1.099')for x,d in zip(roots,change)):step/=2
            roots+=step*change
        else:raise ArithmeticError('high-precision moment refinement did not converge')
        den=10**36;spectrum=fixed+[(int(c),F(int(mp.nint(x*den)),den))for c,x in zip(counts,roots)]
        assert all(abs(x)<F(1099,1000)for c,x in spectrum[len(fixed):])
        spectra[sector]=spectrum;moments[sector]={n:sum(c*x**n for c,x in spectrum)for n in range(4,9)}
    checks=[]
    for n in range(4,9):
        for p,value in [(0,moments['J'][n]+3*moments['N'][n]),(1,moments['J'][n]-moments['N'][n])]:
            lo,hi=boxes[n,p];assert lo<value<hi
            checks.append({'n':n,'twist':p,'value':str(value),'lower_margin':str(value-lo),'upper_margin':str(hi-value)})
    # Finite directed checks plus an analytic tail give ALL integer lengths,
    # not a selected finite positivity fixture.
    iv=mp.iv;v=iv.mpf(11)/10;total=sum(c for s in spectra.values()for c,x in s)
    maxrest=max([abs(x)for c,x in spectra['J'][1:]]+[abs(x)for c,x in spectra['N']])
    cap_r=F(math.ceil(1000*maxrest),1000);assert cap_r<F(11,10)
    cap=iv.mpf(cap_r.numerator)/cap_r.denominator
    stop=math.ceil(math.log(3*total/2)/math.log(1.1/float(cap_r)))+1
    tail=2-3*total*(cap/v)**stop;assert float(tail.a)>0
    terms={s:[(c,iv.mpf(x.numerator)/x.denominator/v)for c,x in ss]for s,ss in spectra.items()}
    powers={s:[iv.mpf(1)for c,x in ss]for s,ss in spectra.items()}
    minimum=None;min_at=None
    for n in range(1,stop):
        sums={}
        for s in ['J','N']:
            for i,(c,x)in enumerate(terms[s]):powers[s][i]*=x
            sums[s]=sum(c*p for (c,x),p in zip(terms[s],powers[s]))
        if n>=4:
            for label,value in [('I',sums['J']+3*sums['N']),('P',sums['J']-sums['N'])]:
                lo=math.nextafter(float(value.a),-math.inf)
                if lo<=0:raise AssertionError(('all-length positivity failed',n,label,lo))
                if minimum is None or lo<minimum:minimum=lo;min_at=[n,label]
    out={'status':'EXACT_RATIONAL_MOMENTS_AND_ALL_LENGTH_POSITIVITY','J_spectrum':[{'multiplicity':c,'eigenvalue':str(x)}for c,x in spectra['J']],'N_spectrum_one_copy':[{'multiplicity':c,'eigenvalue':str(x)}for c,x in spectra['N']],'largest_eigenvalue':'11/10','largest_multiplicity':2,'moment_checks':checks,'dimension_J':sum(c for c,x in spectra['J']),'dimension_N_one_copy':sum(c for c,x in spectra['N']),'positivity':{'all_integer_lengths_at_least':4,'directed_finite_stop_exclusive':stop,'rest_modulus_cap':str(cap_r),'minimum_normalized_trace_lower':minimum,'minimum_at':min_at,'tail_normalized_margin_lower':math.nextafter(float(tail.a),-math.inf),'tail_argument':'2-3*(dimJ+dimN)*(cap/1.1)^n>0, monotone for n>=stop'},'scope':'Finite real SO(3)-equivariant self-adjoint transfer operator. All I/P and hence every SO(3) twisted trace positive at every integer n>=4. Does not construct the local spin-two kernel or one common all-temperature physical Hamiltonian family.'}
    (ROOT/'data/moment_counting_witness_positive.json').write_text(json.dumps(out,indent=2));print(out['status'],out['dimension_J'],out['dimension_N_one_copy'],out['positivity']);print('SPECTRA',{s:[(c,float(x))for c,x in ss]for s,ss in spectra.items()});return out

if __name__=='__main__':
    if '--exact' in sys.argv:exact_repair()
    else:run()
