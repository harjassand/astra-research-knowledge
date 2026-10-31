import copy
import itertools
import json
from pathlib import Path
import random
import time
import sympy as sp
from learn import acquire,encode,evaluate,exact,fixture,metric,sum_kernel,inner,encode_matrix
from verify import verify


def run():
    count=0; started=time.perf_counter()
    mats,b,c=fixture(n=6,groups=3,noise=sp.Rational(1,1000))
    model=acquire(mats,b,c,6,sp.Rational(1,1000))
    record=encode(model)
    check=lambda r:verify(mats,b,c,r,expected_length=6,expected_tolerance=sp.Rational(1,1000))
    assert check(record);count+=1
    worst=sp.Rational(0)
    for length in range(7):
        for word in itertools.product(range(2),repeat=length):
            error=abs(exact(mats,b,c,model['pi'],word)-evaluate(model,word))
            assert error**2<=model['quadratic_error_bound_squared']
            worst=max(worst,error);count+=1
    for key,value in [('alpha','0'),('quadratic_error_bound_squared','0'),('tolerance','1/100000000000000000000'),('length',True)]:
        bad=copy.deepcopy(record);bad[key]=value;assert not check(bad);count+=1
    bad=copy.deepcopy(record);bad['operators'][0][0][0][0]+=1
    assert not check(bad);count+=1
    for value in [True,1.0,'1']:
        bad=copy.deepcopy(record);bad['basis'][0][0][0]=value
        assert not check(bad);count+=1
    easier=encode(acquire(mats,b,c,0,sp.Rational(1,1000)))
    assert not check(easier);count+=1
    easier=encode(acquire(mats,b,c,6,sp.Rational(1,10)))
    assert not check(easier);count+=1
    zero=sp.zeros(len(b),1)
    zm=acquire(mats,zero,c,7,sp.Rational(1,10))
    assert verify(mats,zero,c,encode(zm),expected_length=7,expected_tolerance=sp.Rational(1,10));count+=1
    assert evaluate(zm,[0,1,0,1])==0;count+=1
    assert not verify([None],b,c,record,expected_length=6,expected_tolerance=sp.Rational(1,1000));count+=1
    # Demonstrate why stochasticity cannot substitute for the acquired metric.
    A=sp.Matrix([[sp.Rational(99,100),sp.Rational(1,100)]]*2)
    pi,_,_=metric([A])
    assert pi==sp.Matrix([sp.Rational(99,100),sp.Rational(1,100)]);count+=1
    assert max((A.T*A).eigenvals())>1;count+=1
    x=sp.Matrix([1,-2]);assert inner(A*x,A*x,pi)<=inner(x,x,pi);count+=1
    try:metric([A,sp.Matrix([[sp.Rational(1,2)]*2]*2)])
    except ValueError:count+=1
    else:raise AssertionError('incompatible equilibria admitted')
    # Gapless bound and the second-order leading coefficient.
    assert sum_kernel(30,sp.Rational(1))==435;count+=1
    sharp=[]
    for denominator in [100,1000]:
        e=sp.Rational(1,denominator);g=sp.Rational(1,4)
        A=sp.Matrix([[1-e**2/g,e],[e,1-g]])
        assert sorted(A.eigenvals())==[1-g-e**2/g,sp.Rational(1)];count+=1
        for length in [2,4,12]:
            err=(A**length)[0,0]-A[0,0]**length
            bound=e**2*sum_kernel(length,1-g)
            assert 0<err<=bound;count+=1
            sharp.append({'leakage':str(e),'length':length,'actual_over_bound':float(err/bound)})
    # Holdouts at the main fixture's full declared horizon.
    mats,b,c=fixture()
    model=acquire(mats,b,c,30,sp.Rational(1,100000))
    assert verify(mats,b,c,encode(model),expected_length=30,expected_tolerance=sp.Rational(1,100000));count+=1
    rng=random.Random(443)
    words=[[0]*30,[1]*30,[0,1]*15,[1,0]*15]+[[rng.randrange(2) for _ in range(30)] for _ in range(8)]
    maxerr=sp.Rational(0);direct_seconds=reduced_seconds=0
    for word in words:
        tic=time.perf_counter();truth=exact(mats,b,c,model['pi'],word);direct_seconds+=time.perf_counter()-tic
        tic=time.perf_counter();got=evaluate(model,word);reduced_seconds+=time.perf_counter()-tic
        error=abs(truth-got);maxerr=max(maxerr,error)
        assert error**2<=model['quadratic_error_bound_squared'];count+=1
    Path('fixture_input.json').write_text(json.dumps({'matrices':[encode_matrix(A) for A in mats],
        'b':encode_matrix(b),'c':encode_matrix(c),'length':30,'absolute_error':'1/100000',
        'scope':'Raw rational kernels/observables only; hidden generator coordinates are not learner inputs.'},indent=2)+'\n')
    result={'scope':'Exact author tests and small illustrative timings only; not independent review or strong-baseline superiority.',
            'checks':count,'exhaustive_words':127,'full_horizon_holdouts':len(words),
            'small_fixture_rank':record['ledger']['rank'],'main_fixture_rank':model['ledger']['rank'],
            'main_max_error':str(maxerr),'main_bound_squared':str(model['quadratic_error_bound_squared']),
            'tightness_cases':sharp,'main_query_seconds':{'full_direct_total':direct_seconds,'reduced_total':reduced_seconds},
            'elapsed_seconds':time.perf_counter()-started}
    return result


if __name__=='__main__':
    out=run();Path('tests_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
