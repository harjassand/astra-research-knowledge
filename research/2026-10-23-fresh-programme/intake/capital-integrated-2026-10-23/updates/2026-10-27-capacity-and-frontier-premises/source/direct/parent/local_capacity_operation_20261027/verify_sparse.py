"""Reconstruct every large sparse residual independently from proposed y only."""
from fractions import Fraction as F
from pathlib import Path
import sys,math,json,time,hashlib
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
SRC=HERE.parents[1]/'alternative/interacting_rare_operation_20261027/direct_variational'
sys.path.insert(0,str(SRC))
import sparse_galerkin as candidate

def decode(x):return F(int(x['num_hex'],16),int(x['den_hex'],16))

def check(delta,m=24):
    start=time.perf_counter()
    theta=[F(17+(7*i%13),100) for i in range(m)]
    clocks=[F(11+(3*i%7),10) for i in range(m-1)]
    rho=math.prod(theta);b=(1<<m)-1
    rates=[];creation=[]
    for i,alpha in enumerate(clocks):
        t,s=theta[i:i+2];c=alpha*t*s/(1+t*s);creation.append(c)
        bare=[c,alpha*s/(t+s),alpha*t/(t+s),alpha/(1+t*s)]
        rates.append([[r*(1+delta*outside) for r in bare] for outside in (0,1)])
    Ra=sum(creation);gap=2*min(creation);Rmax=(1+delta)*sum(clocks)
    result,(op,vectors,gram,_)=candidate.certify(theta,clocks,delta,return_internal=True)
    weights={}
    def weight(x):
        if x not in weights:weights[x]=math.prod(theta[i] for i in range(m) if x>>i&1)
        return weights[x]
    def inner(x,y):return sum((weight(s)*v*y.get(s,F(0)) for s,v in x.items()),F(0))
    u={0:rho,b:F(-1)}
    lower=(1+rho)/(2*Rmax);upper=(1+rho)/gap;checks=[]
    for k in range(1,len(vectors)):
        _,_,coef,_=candidate.galerkin_at_degree(op,vectors,k,gram)
        trial={}
        for a,v in zip(coef,vectors[:k]):
            for s,z in v.items():trial[s]=trial.get(s,F(0))+F(op.D,op.W)*a*z
        trial={s:v for s,v in trial.items() if v}
        support=set(trial)|set(u)
        for s in trial:support.update(s^(3<<i) for i in range(m-1))
        hy={};res={}
        for s in support:
            val=F(0);fs=trial.get(s,F(0))
            for i in range(m-1):
                difference=fs-trial.get(s^(3<<i),F(0))
                if not difference:continue
                outside=(s>>(i-1 if i else 2))&1;pair=(s>>i)&3
                val+=rates[i][outside][pair]*difference
            hy[s]=val;res[s]=u.get(s,F(0))-val
        assert inner(res,{s:F(1) for s in res})==0
        L=(2*inner(u,trial)-inner(trial,hy))/rho
        U=L+inner(res,res)/(rho*gap)
        receipt=result['degrees'][k-1]
        assert L==decode(receipt['raw_Galerkin_lower'])
        assert U==decode(receipt['raw_residual_upper'])
        lower=max(lower,L);upper=min(upper,U)
        checks.append({'degree':k,'trial_support':len(trial),'full_residual_support':len(support),
          'independent_raw_lower_and_upper':'EXACT_MATCH'})
    plo,phi=rho/(Ra*upper),rho/(Ra*lower)
    assert plo==decode(result['p_lower']) and phi==decode(result['p_upper'])
    assert upper/lower<=1+F(1,1000)
    return {'M':m,'delta':str(delta),'checks':checks,'full_even_state_count':2**(m-1),
      'p_lower_approx':float(plo),'p_upper_approx':float(phi),
      'relative_width':float(upper/lower-1),'result':'PASS',
      'seconds_including_independent_fraction_verification':time.perf_counter()-start}

def main():
    code=SRC/'sparse_galerkin.py';before=hashlib.sha256(code.read_bytes()).hexdigest()
    m=int(sys.argv[1]) if len(sys.argv)>1 else 24
    out=[check(d,m) for d in ((F(0),F(1,20),F(1,2)) if m==24 else (F(1,2),))]
    after=hashlib.sha256(code.read_bytes()).hexdigest();assert before==after
    result={'scope':'Independent full sparse backward residual reconstruction from candidate trials; no whole-state solve or physical claim',
      'candidate_source_sha256':before,'records':out}
    name='SPARSE_LARGE_CHECK.json' if m==24 else f'SPARSE_M{m}_CHECK.json'
    (HERE/name).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
