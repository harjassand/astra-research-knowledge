import sys,json,copy,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.linalg import expm
sys.path.insert(0,str(Path(__file__).parent))
import acquire_effective_qubit as a

def run():
    cases=[];checks=0
    for n,site,ep,lam in [(1,0,F(1,100),10**8),(4,2,F(1,100),10**8),(16,8,F(1,100),10**8),(16,8,F(1,10000),10**12),(10**12,5*10**11,F(1,100),10**8),(10**9,5*10**8,F(1,10000),10**12)]:
        start=time.perf_counter();r=a.acquire(n,site,F(21,20),lam,ep);dt=time.perf_counter()-start
        assert r['status']=='PASS' and a.verify_channel(r);checks+=2
        assert F(*r['total_error_upper'])<=ep;checks+=1
        D=F(*r['coefficient_rational']);cp=r['channel'];X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);I=np.eye(2)
        G=-1j*(np.kron(I,X)-np.kron(X.T,I))+2*float(D)*(np.kron(Z,Z)-np.eye(4))
        E=expm(G);J=np.array([[E[(i%2)+2*(j%2),(i//2)+2*(j//2)] for j in range(4)] for i in range(4)])
        Jcp=np.array(a.decoded(cp['choi']).evalf(18),complex)
        err=float(np.linalg.norm(Jcp-J,ord='nuc'))
        # This is a floating diagnostic upper proxy, not the certificate proof.
        assert err<=float(ep/8)+1e-12;checks+=1
        cases.append(dict(n=n,site=site,epsilon=str(ep),lambda_value=lam,radius=r['radius'],local_sites=r['local_sites'],seconds=dt,
          total_error_upper=str(F(*r['total_error_upper'])),numerical_choi_trace_error=err,Taylor_degree=cp['Taylor_degree'],scaling_power=cp['scaling_power']))
    r=a.acquire(4,2,F(21,20),10**8,F(1,100));assert a.verify_record(r);checks+=1
    for field,value in [('radius',999),('coefficient_rational',[1,1]),('total_error_upper',[0,1])]:
        bad=copy.deepcopy(r);bad[field]=value;assert not a.verify_record(bad);checks+=1
    bad=copy.deepcopy(r);bad['channel']['choi'][0][0][0]+=1;assert not a.verify_channel(bad);checks+=1
    bad=copy.deepcopy(r);bad['channel']['ldl_positive_diagonal'][0]=[-1,1];assert not a.verify_channel(bad);checks+=1
    for args in [(0,0,1,10**8,F(1,100)),(4,4,1,10**8,F(1,100)),(4,1,-1,10**8,F(1,100)),(4,1,2,10**8,F(1,100)),(4,1,1,0,F(1,100)),(4,1,1,1,0)]:
        try:a.acquire(*args)
        except ValueError:checks+=1
        else:raise AssertionError('malformed admitted')
    assert a.acquire(4,1,F(21,20),100,F(1,100))['status']=='ABORT';checks+=1
    for value in [None,[],{},[1],[[1]],'not a matrix',[[[1,1,0,1]]*5 for _ in range(5)]]:
        bad=copy.deepcopy(r);bad['channel']['choi']=value;assert not a.verify_channel(bad);checks+=1
    for value in [[True,1],[1,0],['1',1],[],None]:
        bad=copy.deepcopy(r);bad['known_program']['clock_rate']=value;assert not a.verify_record(bad);checks+=1
    for malformed in [None,[],True,'record']:
        assert not a.verify_record(malformed);checks+=1
    for field,value in [('local_sites',False),('local_sites',0.0),('numerical_channel_error_upper',True)]:
        r1=a.acquire(1,0,F(21,20),10**8,F(1,100));bad=copy.deepcopy(r1);bad[field][0]=value
        assert not a.verify_record(bad);checks+=1
    local=[]
    for n in [4,8,16]:
      for site in [0,n//2,n-1]:
       full=a.covariance_entry(n,site,F(1,41))
       for R in range(3):
        left=max(0,site-R);right=min(n-1,site+R);v=a.covariance_entry(right-left+1,site-left,F(1,41))
        bound=F(0) if left==0 and right==n-1 else 2*F(1,20)**(R+1)/F(19,20)
        assert abs(v-full)<=bound;checks+=1
        local.append(dict(n=n,site=site,R=R,error=str(abs(v-full)),bound=str(bound)))
    return dict(scope='Exact CP/TP/rational and malformed/tamper tests plus floating diagnostics; no executed quantum gate synthesis.',checks=checks,cases=cases,locality_checks=local)
if __name__=='__main__':
    out=run();Path(__file__).with_name('effective_qubit_checks.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',out['checks']);print([(c['n'],c['seconds'],c['radius']) for c in out['cases']])
