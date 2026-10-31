"""Independent adversarial checks; no saved author artifact is overwritten."""
import copy, json, sys, time
from fractions import Fraction as F
from pathlib import Path
import sympy as sp
sys.path.insert(0,str(Path(__file__).parent))
import acquire_effective_qubit as a

def run():
    checks=0; cases=[]
    for n,site,q,lam,ep in [(1,0,F(1),10**8,F(1,100)),(3,0,F(41,39),10**8,F(1,100)),(5,2,F(39,41),10**12,F(1,10000)),(10**30,10**29,F(21,20),10**12,F(1,10000))]:
        tic=time.perf_counter();r=a.acquire(n,site,q,lam,ep)
        assert r['status']=='PASS' and a.verify_record(r) and a.verify_channel(r);checks+=3
        assert F(*r['combined_error_upper'])<=ep;checks+=1
        assert F(*r['channel']['CP_channel_error_upper'])==F(*r['numerical_channel_error_upper']);checks+=1
        cases.append({'n':str(n),'site':str(site),'q':str(q),'radius':r['radius'],'seconds':time.perf_counter()-tic})
    r=a.acquire(1,0,'21/20',10**8,'1/100')
    for x in [None,[],0,'x',True,{'status':'PASS'}, {'status':'ABORT'}]:
        assert not a.verify_record(x) and not a.verify_channel(x);checks+=2
    for field,ix,val in [('local_sites',0,False),('local_sites',0,0.0),('numerical_channel_error_upper',0,True),('reserved_gate_error',0,1.0)]:
        bad=copy.deepcopy(r);bad[field][ix]=val
        assert not a.verify_record(bad);checks+=1
    for field,val in [('task','source output too'),('scope','verified physical truth'),('radius',99),('total_error_upper',[0,1]),('combined_error_upper',[0,1])]:
        bad=copy.deepcopy(r);bad[field]=val
        assert a.verify_channel(bad) and not a.verify_record(bad);checks+=2
    for val in [None,[],[[0]],a.encoded(sp.eye(5))]:
        bad=copy.deepcopy(r);bad['channel']['choi']=val
        assert not a.verify_channel(bad);checks+=1
    for val in [True,1.0,'1']:
        bad=copy.deepcopy(r);bad['channel']['choi'][0][0][0]=val
        assert not a.verify_channel(bad);checks+=1
    for val in [0,-1,True]:
        bad=copy.deepcopy(r);bad['channel']['choi'][0][0][1]=val
        assert not a.verify_channel(bad);checks+=1
    J=sp.diag(sp.Rational(1,2),sp.Rational(1,2),sp.Rational(1,2),sp.Rational(1,2),1)
    bad={'channel':{'choi':a.encoded(J),'ldl_unit_lower':a.encoded(sp.eye(5)),'ldl_positive_diagonal':[[1,2]]*4+[[1,1]]}}
    assert not a.verify_channel(bad);checks+=1
    for args in [(True,0,1,10**8,F(1,100)),(2,True,1,10**8,F(1,100)),(2,0,True,10**8,F(1,100)),(2,0,1,False,F(1,100)),(2,0,1,10**8,False),(2,0,0,10**8,F(1,100)),(2,0,1,10**8,F(-1,100)),(2,0,1,10**8,F(1)),(2,0,F(100),10**8,F(1,100))]:
        try:a.acquire(*args)
        except (ValueError,TypeError):checks+=1
        else:raise AssertionError('invalid input admitted')
    assert a.acquire(2,0,1,F(1,2),F(1,100))['status']=='ABORT';checks+=1
    for n in range(1,9):
        for site in [0,n//2,n-1]:
            assert a.covariance_entry(n,site,F(1,40))==a.covariance_entry(n,site,F(-1,40));checks+=1
    return {'scope':'Independent exact/adversarial checks only; no gate backend or physical-law verification.','checks':checks,'cases':cases}
if __name__=='__main__':print(json.dumps(run(),indent=2))
