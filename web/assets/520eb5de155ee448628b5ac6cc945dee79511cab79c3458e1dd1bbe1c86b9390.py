"""Cheap exact algebra fixtures for notes20/21, not an all-N numerical proof."""
from fractions import Fraction as F
from math import comb,factorial
from pathlib import Path
import datetime,hashlib,json,time

OWN=Path(__file__).parent

def main():
    out=OWN/'collective_thermal_exact_checks.json';assert not out.exists()
    start=time.perf_counter();counts={'detailed_balance_edges':0,'stationary_identities':0,'geometric_rest_moments':0,'inverse_filter_identities':0}
    for nu in [F(1,10),F(1),F(10)]:
        q=nu/(nu+1)
        assert (nu+F(1,2))**2-nu*(nu+1)==F(1,4)
        for K in range(1,13):
            if time.perf_counter()-start>5:raise TimeoutError('Prospective five-second cap')
            Z=sum(q**r for r in range(K+1));pi=[q**r/Z for r in range(K+1)]
            for r in range(K):
                b=nu*(K-r)*(r+1);d=(nu+1)*(r+1)*(K-r)
                assert pi[r]*b==pi[r+1]*d
                assert b>=K*nu and d>=K*(nu+1)
                counts['detailed_balance_edges']+=1
            E=sum(r*pi[r] for r in range(K+1))
            R=sum(r*(K-r+1)*pi[r] for r in range(K+1))
            assert R==nu*(K-2*E)
            assert 0<=E<=F(K,2)
            assert pi[-1]>=q**K/(K+1)
            counts['stationary_identities']+=1
            assert (1-q**(K+1))/((K+1)*(1-q))==Z/(K+1)
            for r in range(K+1):
                beta_integral=F(factorial(r)*factorial(K-r),factorial(K+1))
                assert comb(K,r)*beta_integral==F(1,K+1)
                assert F(K+1)*q**r*comb(K,r)*beta_integral/Z==pi[r]
                counts['geometric_rest_moments']+=1
            for x in [F(0),F(1,7),F(1,2),F(1)]:
                a=1-(1-q)*x;p=q*x/a
                assert p/(q+(1-q)*p)==x
                assert q/(q+(1-q)*p)==a
                counts['inverse_filter_identities']+=1
    nu=F(1,100);q=nu/(nu+1);Z=1+q+q*q
    beta=F(1,4);jbar=F(3,4);Delta=beta*beta/2-2*nu*jbar
    assert Delta==F(13,800)>0
    R=F(3,2)*q*(1+q)/Z
    E=F(1,4)+F(3,4)*(q+2*q*q)/Z
    W=R-beta*E+beta*beta/2
    assert W==F(-6025,329696)<-Delta
    wall=time.perf_counter()-start;assert wall<5
    receipt={'status':'PASS all tiny exact thermal/representation checks; infinite statements analytic',
             'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'declared_wall_cap_seconds':5,
             'wall_seconds':wall,'counts':counts,'N2_nu1over100_Delta':str(Delta),
             'N2_nu1over100_stationary_W':str(W),
             'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
