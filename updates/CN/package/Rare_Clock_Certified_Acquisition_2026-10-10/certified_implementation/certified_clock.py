"""Finite-bit Brown/Cox first-hit clock with integer outward log enclosures.

No floating-point value participates in the sampler or certificate. The theorem
assumes independent unbiased input bits. CounterTape is only a deterministic,
domain-separated replay fixture, not an assertion of information-theoretic IID.
"""
from fractions import Fraction as F
from dataclasses import dataclass
from collections import defaultdict
import hashlib, json, math, time, os
from pathlib import Path


def ceil(x): return -(-x.numerator // x.denominator)
def ceildiv(a,b): return -(-a//b)
def pow2ceil_ratio(x):
    b=0
    while F(1,1<<b)>x: b+=1
    return b

def exact_fraction(x):
    if isinstance(x,float): raise TypeError('Floating-point input is not certified input')
    if isinstance(x,str) and '0x' in x.lower():
        pieces=x.split('/')
        if len(pieces)==1:return F(int(pieces[0],0))
        if len(pieces)==2:return F(int(pieces[0],0),int(pieces[1],0))
        raise ValueError('Invalid hexadecimal rational')
    return F(x)

def rational_text(x):
    # Python's decimal-string safety limit must not reject a valid exact time.
    # Hex integer formatting is linear and has no decimal conversion limit.
    if max(x.numerator.bit_length(),x.denominator.bit_length())>10000:
        return f'{x.numerator:#x}/{x.denominator:#x}'
    return str(x)

@dataclass(frozen=True)
class Budget:
    p: tuple
    rates: tuple
    eps: F = F(1,4)
    delta: F = F(1,20)
    def __post_init__(self):
        p=tuple(map(exact_fraction,self.p)); rates=tuple(map(exact_fraction,self.rates))
        eps=exact_fraction(self.eps); delta=exact_fraction(self.delta)
        if not p or len(p)!=len(rates): raise ValueError('Nonempty matching dimensions required')
        if any(not 0<x<1 for x in p) or any(x<=0 for x in rates): raise ValueError('Invalid CTMC parameters')
        if not 0<eps<F(1,2) or not 0<delta<F(1,2): raise ValueError('Require 0 < epsilon, delta < 1/2')
        pairs=sorted(zip(rates,p)); rates=tuple(x[0] for x in pairs);p=tuple(x[1] for x in pairs)
        # A bounded dyadic input gate makes each Bernoulli draw exact and bounded.
        if any(x.denominator & (x.denominator-1) for x in p): raise ValueError('This implementation gate requires dyadic probabilities')
        n=len(p);q=math.prod(p);w=tuple((1-p[i])*math.prod(p[i+1:]) for i in range(n))
        kappa=tuple(1+sum(((1-p[j])*rates[j] for j in range(i)),F())/rates[i] for i in range(n))
        h=eps/(2+2*eps); L=0
        while 4*n*F(3,8)**L>delta/4:L+=1
        R=tuple(ceil(6*k*L/h**2) for k in kappa)
        capell=0
        while n*F(1,2)**capell>delta/64:capell+=1
        K=tuple(24*r+capell+1 for r in R)
        J=1+sum(r+2*k for r,k in zip(R,K))
        eta=min(eps/100,delta/(512*sum(R)));a=delta/(64*J)
        b=pow2ceil_ratio(eta*a*a/16)
        P=b+32
        while True:
            N=(P+8)//3+1
            C=(b+2)*(10*N+2)+2
            if F(C,1<<P)<=eta*a/16 and 3**(2*N+1)>=3*(1<<P):break
            P+=8
        vals=locals()
        for key in ('p','rates','eps','delta','n','q','w','kappa','h','L','R','K','J','eta','a','b','P','N','C','capell'):
            object.__setattr__(self,key,vals[key])
        assert sum(w)+q==1
        assert eta<=F(1,8)
        assert (1+h)/(1-h)*(1+eta)**2<=1+eps
        assert (1-h)/(1+h)/(1+eta)**2>=1-eps
        assert F(1,1<<b)/a+F(C,1<<P)<=eta*a/8
    def report(self):
        return {k: encode(getattr(self,k)) for k in ('p','rates','eps','delta','n','q','w','kappa','h','L','R','K','J','eta','a','b','P','N','capell')} | {
          'expected_exponential_call_upper_bound':1+sum(5*r+2 for r in self.R),
          'max_main_uniform_bits':self.J*self.b,
          'max_main_bernoulli_bits':sum(max(r,k)*sum(p.denominator.bit_length()-1 for p in self.p[:i]) for i,(r,k) in enumerate(zip(self.R,self.K))),
          'failure_bounds': {
              'uniform_cell_endpoint_rejection':rational_text(self.delta/16),
              'small_branch_interval_ambiguity':rational_text(15*self.eta*sum(self.R)),
              'poisson_count_caps':rational_text(self.n*F(1,2)**self.capell),
              'large_branch_concentration':rational_text(4*self.n*F(3,8)**self.L),
              'total':rational_text(self.delta/16+15*self.eta*sum(self.R)+self.n*F(1,2)**self.capell+4*self.n*F(3,8)**self.L)}
        }

def display_float(x):
    # Presentation must never turn a successful exact large-scale acquisition
    # into an exception. None means outside the binary64 display range.
    try:return float(x)
    except OverflowError:return None

def encode(x):
    if isinstance(x,F):return rational_text(x)
    if isinstance(x,(tuple,list)):return [encode(y) for y in x]
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    return x

class CounterTape:
    """Deterministic SHA256 counter fixture. Uniform-bit interface can be replaced."""
    def __init__(self,seed,label):
        self.key=(seed+'\x00'+label).encode();self.counter=0;self.pool=0;self.available=0;self.bits=0
        self.hash=hashlib.sha256()
    def _next_block(self):
        block=hashlib.sha256(self.key+self.counter.to_bytes(8,'big')).digest()
        self.counter+=1;self.hash.update(block)
        return block
    def getbits(self,k):
        while self.available<k:
            block=self._next_block()
            self.pool=(self.pool<<256)|int.from_bytes(block,'big');self.available+=256
        self.available-=k
        ans=self.pool>>self.available
        self.pool&=(1<<self.available)-1;self.bits+=k
        return ans
    def evidence(self):return {'bits_consumed':self.bits,'blocks_generated':self.counter,'generated_block_sha256':self.hash.hexdigest()}

class TapeBank:
    def __init__(self,seed):self.seed=seed;self.streams={}
    def stream(self,label):
        if label not in self.streams:self.streams[label]=CounterTape(self.seed,label)
        return self.streams[label]
    def evidence(self):return {k:v.evidence() for k,v in sorted(self.streams.items())}

class OSRecordedTape(CounterTape):
    """OS-backed bits with the exact generated blocks preserved for replay."""
    def __init__(self,label):super().__init__('',label);self.raw=bytearray()
    def _next_block(self):
        block=os.urandom(32);self.raw.extend(block)
        self.counter+=1;self.hash.update(block)
        return block

class OSRecordedBank(TapeBank):
    def __init__(self):super().__init__('')
    def stream(self,label):
        if label not in self.streams:self.streams[label]=OSRecordedTape(label)
        return self.streams[label]
    def save(self,directory):
        directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
        doc={'source':'os.urandom','contract':'The probability theorem assumes independent unbiased bits. OS entropy is a practical source, not a proved physical independence certificate.','streams':{}}
        for i,(label,tape) in enumerate(sorted(self.streams.items())):
            name=f'{i:02d}.bin';(directory/name).write_bytes(tape.raw)
            doc['streams'][label]={'file':name,**tape.evidence()}
        (directory/'manifest.json').write_text(json.dumps(doc,indent=2)+'\n')
        return doc

class PrefixReplayTape(CounterTape):
    def __init__(self,label,data,bit_limit):super().__init__('',label);self.data=data;self.bit_limit=bit_limit
    def _next_block(self):
        block=self.data[32*self.counter:32*(self.counter+1)]
        if len(block)!=32:raise ValueError('Recorded prefix exhausted')
        self.counter+=1;self.hash.update(block);return block
    def getbits(self,k):
        if self.bits+k>self.bit_limit:raise ValueError('Replay exceeds recorded bit-request prefix')
        return super().getbits(k)

class PrefixReplayBank(TapeBank):
    def __init__(self,directory):
        super().__init__('');self.directory=Path(directory)
        self.manifest=json.loads((self.directory/'manifest.json').read_text())
    def stream(self,label):
        if label not in self.streams:
            row=self.manifest['streams'][label]
            data=(self.directory/row['file']).read_bytes()
            if hashlib.sha256(data).hexdigest()!=row['generated_block_sha256']:
                raise ValueError('Recorded prefix hash mismatch')
            self.streams[label]=PrefixReplayTape(label,data,row['bits_consumed'])
        return self.streams[label]

class BitCallbackTape:
    """Adapter for a caller-supplied getbits(k) source.

    Independent unbiased returned bits are the probability theorem's explicit
    source assumption. A finite test cannot certify that source assumption.
    """
    def __init__(self,getbits):self.provider=getbits;self.bits=0;self.hash=hashlib.sha256()
    def getbits(self,k):
        x=self.provider(k)
        if type(x) is not int or not 0<=x<(1<<k):raise ValueError('Bit source violated range/type contract')
        self.bits+=k;self.hash.update(k.to_bytes(8,'big')+x.to_bytes((k+7)//8,'big'))
        return x
    def evidence(self):return {'bits_consumed':self.bits,'encoded_request_sha256':self.hash.hexdigest()}

class BitCallbackBank:
    """Factory(label) returns an independent getbits(k) callback per stream."""
    def __init__(self,factory):self.factory=factory;self.streams={}
    def stream(self,label):
        if label not in self.streams:self.streams[label]=BitCallbackTape(self.factory(label))
        return self.streams[label]
    def evidence(self):return {k:v.evidence() for k,v in sorted(self.streams.items())}

class AcquisitionFailure(Exception): pass

class ExpCells:
    def __init__(self,budget):
        self.budget=budget;self.F=1<<budget.P;self.calls=0;self.endpoint_rejections=0
        self.log2=self._logv(2,1)
    def _logv(self,num,den):
        """Enclose log(num/den), 1 <= num/den <= 2, in units 2^-P."""
        assert den<=num<=2*den
        zn=num-den;zd=num+den
        lo=self.F*zn//zd;hi=ceildiv(self.F*zn,zd)
        zl=zn*zn;zh=zd*zd;slo=shi=0
        for j in range(self.budget.N):
            d=2*j+1;slo+=lo//d;shi+=ceildiv(hi,d)
            lo=lo*zl//zh;hi=ceildiv(hi*zl,zh)
        # For z <= 1/3, omitted 2*atanh tail < 3*(1/3)^(2N+1).
        tail=ceildiv(3*self.F,3**(2*self.budget.N+1))
        return 2*slo,2*shi+tail
    def cell_from_integer(self,k):
        B=self.budget;D=1<<B.b
        if not 0<=k<D:raise ValueError('Uniform cell index out of range')
        if F(k,D)<B.a or F(k+1,D)>1-B.a:
            self.endpoint_rejections+=1;raise AcquisitionFailure('uniform_endpoint')
        odd=2*k+1;e=odd.bit_length()-1;d=B.b+1-e
        vl,vh=self._logv(odd,1<<e)
        lo=d*self.log2[0]-vh;hi=d*self.log2[1]-vl
        radius=ceildiv(self.F,2*k)
        lo=max(0,lo-radius);hi+=radius
        # This is a runtime certificate, not a floating-point tolerance.
        if lo<=0 or (hi-lo)*B.eta.denominator>lo*B.eta.numerator:
            raise AssertionError('Derived exponential-cell width contract failed')
        return (lo+hi)//2,lo,hi
    def draw(self,tape):
        self.calls+=1
        return self.cell_from_integer(tape.getbits(self.budget.b))


def poisson_count(cells,tape,rlo,rhi,cap):
    """Exact count for every ideal-uniform extension of these finite cells.

    rlo/rhi are intensities multiplied by 2^P. Inconclusive comparison is a
    charged acquisition failure, never a guessed branch.
    """
    alo=ahi=0
    for count in range(cap):
        _,lo,hi=cells.draw(tape);alo+=lo;ahi+=hi
        if ahi<=rlo:continue
        if alo>rhi:return count
        raise AcquisitionFailure('poisson_interval_ambiguity')
    raise AcquisitionFailure('poisson_count_cap')


def marks(cells,tape,B,i,count):
    # Only at most 2^i groups are used in this n=4 acquisition. This is NOT
    # product-generator construction, and no 2^n algorithm claim is made here.
    # Only observed rate groups are stored; at most min(count,2^i) groups occur.
    groups=defaultdict(lambda:[0,0,0])
    for _ in range(count):
        rate=B.rates[i]
        for j in range(i):
            p=B.p[j];k=p.denominator.bit_length()-1
            if tape.getbits(k)>=p.numerator:rate+=B.rates[j]
        point,lo,hi=cells.draw(tape)
        row=groups[rate];row[0]+=point;row[1]+=lo;row[2]+=hi
    return tuple(sum((F(row[k],cells.F)/rate for rate,row in groups.items()),F()) for k in range(3))


def acquire(B,seed=None,reference=False,reference_mark_cap=200000,tape_bank=None,reference_tape_bank=None):
    if tape_bank is None and seed is None:raise ValueError('Provide a bit-source bank or an explicit fixture seed')
    if reference and tape_bank is not None and reference_tape_bank is None:
        raise ValueError('Custom-source reference requires a matching replay bank')
    bank=tape_bank if tape_bank is not None else TapeBank(seed)
    cells=ExpCells(B);start=time.perf_counter()
    strata=[];out=F();failure=None
    try:
        Wpoint,Wlo,Whi=cells.draw(bank.stream('W'))
        for i in range(B.n):
            fac=B.w[i]/B.q
            rp=fac*Wpoint;rlo=fac*Wlo;rhi=fac*Whi
            large=rp>=2*B.R[i]*cells.F
            if large:
                if rlo<B.R[i]*cells.F:raise AssertionError('Compression threshold is not certified')
                count=B.R[i]
                vals=marks(cells,bank.stream(f'{i}/compressed_marks'),B,i,count)
                val=rp/cells.F*vals[0]/count
            else:
                count=poisson_count(cells,bank.stream(f'{i}/arrivals'),rlo,rhi,B.K[i])
                vals=marks(cells,bank.stream(f'{i}/exact_marks'),B,i,count)
                val=vals[0]
            out+=val
            strata.append({'index':i,'branch':'compressed' if large else 'small','intensity_interval':[rlo/cells.F,rhi/cells.F],
                            'marks':count,'output':val})
    except AcquisitionFailure as exc:
        failure=str(exc);out=F()
    main_calls=cells.calls;main_evidence=bank.evidence()
    assert main_calls<=B.J
    result={'seed':seed,'execution_source':'caller-supplied bit callbacks' if tape_bank is not None else 'deterministic SHA256 replay fixture','output':rational_text(out),'output_float_display_only':display_float(out),'failure':failure,'strata':encode(strata),
            'main_exponential_cells':main_calls,'main_bits':sum(x['bits_consumed'] for x in main_evidence.values()),
            'main_tape_evidence':main_evidence,'main_seconds':time.perf_counter()-start}
    if reference and failure is None:
        # Independent proof-reference arrivals/marks for compressed strata;
        # small strata use their identical main tapes. W is the same finite cell.
        refbank=reference_tape_bank if reference_tape_bank is not None else TapeBank(seed);refcells=ExpCells(B)
        wp,wl,wh=refcells.draw(refbank.stream('W'))
        assert (wp,wl,wh)==(Wpoint,Wlo,Whi)
        total_lo=total_hi=F();total_marks=0;rows=[];ref_failure=None
        try:
            for i in range(B.n):
                fac=B.w[i]/B.q
                available=reference_mark_cap-total_marks
                if available<=0:raise AcquisitionFailure('reference_work_cap')
                cnt=poisson_count(refcells,refbank.stream(f'{i}/arrivals'),fac*Wlo,fac*Whi,available)
                total_marks+=cnt
                _,lo,hi=marks(refcells,refbank.stream(f'{i}/exact_marks'),B,i,cnt)
                total_lo+=lo;total_hi+=hi
                rows.append({'index':i,'marks':cnt,'interval':[lo,hi]})
        except AcquisitionFailure as exc:ref_failure=str(exc)
        rr={'failure':ref_failure,'total_marks':total_marks,'exponential_cells':refcells.calls,'strata':encode(rows),'tape_evidence':refbank.evidence()}
        if ref_failure is None:
            # Enforce the advertised replay contract rather than silently
            # accepting an independently resampled small branch.
            ref_evidence=refbank.evidence()
            for row in strata:
                if row['branch']=='small':
                    for role in ('arrivals','exact_marks'):
                        label=f"{row['index']}/{role}"
                        if main_evidence[label]!=ref_evidence[label]:
                            raise ValueError('Reference small-stream replay evidence mismatch: '+label)
            rr['shared_small_stream_evidence_matches']=True
            if total_lo==0:rel=F() if out==0 else None
            else:rel=max(abs(out/total_lo-1),abs(out/total_hi-1))
            rr|={'exact_H_interval':encode([total_lo,total_hi]),'relative_error_upper_bound':encode(rel),
                  'within_requested_epsilon_for_every_tape_extension':rel is not None and rel<=B.eps,
                  'relative_error_float_display_only':display_float(rel) if rel is not None else None}
        result['same_tape_reference']=rr
    result['total_seconds']=time.perf_counter()-start
    return result


def default_budget():return Budget(('1/8','1/16','1/32','1/16'),('1','2','4','8'))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--budget-only',action='store_true');parser.add_argument('--reference',action='store_true');parser.add_argument('--seed',default='rare-clock-certified-20261010-v1')
    sources=parser.add_mutually_exclusive_group();sources.add_argument('--os-recorded');sources.add_argument('--replay-recorded')
    args=parser.parse_args();B=default_budget()
    report={'budget':B.report()}
    if not args.budget_only:
        if args.os_recorded:
            bank=OSRecordedBank();report['run']=acquire(B,tape_bank=bank,reference=args.reference)
            report['source_manifest']=bank.save(args.os_recorded)
        elif args.replay_recorded:
            report['run']=acquire(B,tape_bank=PrefixReplayBank(args.replay_recorded),reference=args.reference)
        else:report['run']=acquire(B,args.seed,reference=args.reference)
    print(json.dumps(report,indent=2))
