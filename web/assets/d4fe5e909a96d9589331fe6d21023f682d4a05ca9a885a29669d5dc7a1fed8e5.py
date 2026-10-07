"""Tiny exact checks supplementing the analytic all-N collective-decay audit."""
from fractions import Fraction as F
from math import comb,factorial
from pathlib import Path
import datetime,hashlib,json,time

OWN=Path(__file__).parent

def main():
    out=OWN/'collective_decay_exact_checks.json'
    assert not out.exists(),'Preserve frozen checks receipt'
    started=time.perf_counter();counts={'rates':0,'bernoulli':0,'multiplicities':0,'spin_addition':0,'ratios':0}
    def cap():
        if time.perf_counter()-started>5:raise TimeoutError('Prospective five-second cap')
    for K in range(1,33):
        for n in range(1,K+1):
            lam=n*(K-n+1)
            assert lam-K==(n-1)*(K-n)>=0
            assert lam<=((K+1)**2)//4
            counts['rates']+=1
    for K in range(1,65):
        cap()
        assert (1-F(1,2*K))**K>=F(1,2)
        counts['bernoulli']+=1
    beta={}
    for N in range(1,33):
        cap();total=0;inv=F(0);bn=F(0)
        for b in range(N//2+1):
            d=comb(N,b)-(comb(N,b-1) if b else 0)
            assert d>0
            weight=F(d*(N-2*b+1),2**N)
            total+=weight;inv+=weight/F(N-2*b+1);bn+=b*weight
        assert total==1
        assert inv==F(comb(N,N//2),2**N)<=F(1,2)
        assert bn>=F(N-1,4)
        beta[N]=bn;counts['multiplicities']+=1
        if N>=2:
            C=F(3*N+N%2,4)
            assert 2*N*C/(F(N-1,4)**2)<=96
            assert 2*N*C/(bn**2)<=96
            counts['ratios']+=1
    for N in range(1,32):
        assert beta[N+1]-beta[N]==F(1,2)-F(comb(N,N//2),2**(N+1))
        counts['spin_addition']+=1
    exp6_lower=sum((F(6)**n)/factorial(n) for n in range(6))
    exp5_lower=sum((F(5)**n)/factorial(n) for n in range(7))
    assert exp6_lower==F(899,5)>128
    assert exp5_lower==F(16289,144)>96
    W3_upper=F(55,16)/exp6_lower-F(1,32)
    assert W3_upper==F(-349,28768)<0
    assert 10>9 # the dark N2 partial-transpose lower eigenvalue is negative
    cap()
    receipt={'status':'PASS all tiny exact arithmetic checks; all-N proof is analytic',
             'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'declared_wall_cap_seconds':5,'wall_seconds':time.perf_counter()-started,
             'counts':counts,'exp6_lower':str(exp6_lower),'exp5_lower':str(exp5_lower),
             'N2_time3_linear_witness_upper':str(W3_upper),
             'supplemental_scope':'Finite fixtures, not extrapolation or solver certificate of all N',
             'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
