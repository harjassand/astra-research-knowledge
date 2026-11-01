"""Finite rational scalar-return receiver. Not a practical sample-efficiency claim.

Only the adapter sees source reports. Receiver sees scalar rational means, never
hidden coordinates. Emulator estimates MUST NOT be represented as sampled means.
"""
from fractions import Fraction as F
from math import isqrt

class TerminalFailure(RuntimeError): pass
class BudgetRefused(RuntimeError): pass


def ceil_log2(x):
    x=F(x)
    if x<=1: return 0
    p=max(0,x.numerator.bit_length()-x.denominator.bit_length())
    if (x.denominator<<p)<x.numerator: p+=1
    return p


def required_shots(alpha,beta):
    # ln(2/beta)<=ceil(log2(2/beta)); no transcendental computation.
    if not (0<F(alpha) and 0<F(beta)<1):raise ValueError('invalid calibration tolerances')
    n=8*F(alpha)**-2*ceil_log2(2/F(beta))
    return (n.numerator+n.denominator-1)//n.denominator


def zeros(n,m): return [[F(0) for _ in range(m)] for _ in range(n)]
def transpose(a): return [list(row) for row in zip(*a)]
def mm(a,b): return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]
def mv(a,v): return [sum((x*y for x,y in zip(row,v)),F(0)) for row in a]
def add(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,c): return [[c*x for x in row] for row in a]
def quad(a,v): return sum((x*y for x,y in zip(v,mv(a,v))),F(0))


def psd(a,strict=False):
    """Exact symmetric Schur-complement test, including zero-pivot handling."""
    n=len(a)
    if any(a[i][j]!=a[j][i] for i in range(n) for j in range(n)): return False
    s=[r[:] for r in a]
    for j in range(n):
        d=s[j][j]
        if d<0 or (strict and d==0): return False
        if d==0:
            if any(s[j][i]!=0 for i in range(j+1,n)): return False
            continue
        for i in range(j+1,n):
            for h in range(i,n):
                s[h][i]=s[i][h]=s[i][h]-s[i][j]*s[j][h]/d
    return True


def inverse(a):
    n=len(a)
    s=[row[:]+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        p=next((i for i in range(j,n) if s[i][j]),None)
        if p is None: raise ArithmeticError('singular matrix')
        s[j],s[p]=s[p],s[j]
        d=s[j][j];s[j]=[x/d for x in s[j]]
        for i in range(n):
            if i!=j:
                c=s[i][j];s[i]=[x-c*y for x,y in zip(s[i],s[j])]
    return [r[n:] for r in s]


def sqrt_upper(x,eta):
    """Rational outward sqrt with additive gap <=eta; exact integer sqrt."""
    if x<0: raise ArithmeticError('negative certified squared norm')
    if not x: return F(0)
    p=ceil_log2(1/F(eta));s=1<<p
    y=x*s*s;r=isqrt(y.numerator//y.denominator)
    if r*r*y.denominator<y.numerator:r+=1
    return F(r,s)


class BinaryMeanAdapter:
    """Genuine finite calibration: callback returns one fresh +/-1 report.

    max_total_episodes is an explicit safety budget. Refusal does not pretend
    any mean was sampled. The full fixed n is checked BEFORE requesting reports.
    Conditional unbiasedness and physical preparation remain source premises.
    """
    calibration_mode='actual_one_bit_samples'
    def __init__(self,report,max_total_episodes=None):
        self.report=report;self.max_total_episodes=max_total_episodes
        self.actual_episodes=0;self.attempted_episodes=0;self.actual_descriptor_controls=0
    def estimate(self,kind,key,alpha,beta_job,shots,epoch):
        if not isinstance(shots,int) or shots<required_shots(alpha,beta_job):
            raise ValueError('shot count below proved calibration budget')
        if self.max_total_episodes is not None and self.attempted_episodes+shots>self.max_total_episodes:
            raise BudgetRefused(f'calibration requires {shots} fresh episodes; configured budget refuses')
        total=0
        for _ in range(shots):
            self.attempted_episodes+=1
            self.actual_descriptor_controls+=sum(map(len,key)) if kind=='gram' else len(key[1])
            z=self.report(kind,key)
            self.actual_episodes+=1
            if z not in (-1,1):raise TerminalFailure('source report is not one-bit +/-1')
            total+=int(z)
        return F(total,shots)


class Receiver:
    def __init__(self,alphabet,H,epsilon,delta,readouts,adapter):
        self.alphabet=tuple(alphabet);self.H=H;self.epsilon=F(epsilon);self.delta=F(delta)
        self.readouts=tuple(readouts);self.adapter=adapter
        if H<1 or not self.alphabet or len(set(self.alphabet))!=len(self.alphabet):raise ValueError('invalid alphabet/horizon')
        if not (0<self.epsilon<=1 and 0<self.delta<1) or not self.readouts:raise ValueError('invalid tolerances/readouts')
        self.tau=self.epsilon/(128*H*H);self.lam=self.tau*self.tau
        self.W=sum(len(self.alphabet)**j for j in range(H+1));self.beta=self.delta/(self.W+1)**32
        self.W1=1+len(self.alphabet)*self.W
        self.E=ceil_log2(self.W)+1
        self.Nmax=self.E*(self.W1*self.W1+len(self.readouts)*self.W1+1)
        self.words=[()];self.cache={};self.failed=None;self.ready=False
        self.acquisition={'mean_jobs':0,'cache_hits':0,'theoretical_required_episodes':0,
                          'actual_episodes':0,'attempted_episodes':0,'actual_descriptor_controls':0,'dictionary_additions':0,
                          'builds':0,'rejected_evaluations':0,'prefix_leverage_tests':0,
                          'rejected_matrix_vector_products':0,'rejected_certificate_quadratic_forms':0,
                          'calibration_mode':getattr(adapter,'calibration_mode','UNDECLARED'),
                          'max_rational_bitheight':0,'tolerance_bitheight':sum(x.numerator.bit_length()+x.denominator.bit_length() for x in (self.epsilon,self.delta))}
        self.deployment={'requests':0,'accepted':0,'matrix_vector_products':0,'certificate_quadratic_forms':0,'max_rational_bitheight':0}
        self.job_log=[]

    def fail(self,reason):
        self.failed=str(reason);raise TerminalFailure(self.failed)

    def _track(self,x):
        if isinstance(x,list):
            for y in x:self._track(y)
        else:
            x=F(x);self.acquisition['max_rational_bitheight']=max(self.acquisition['max_rational_bitheight'],x.numerator.bit_length()+x.denominator.bit_length())

    def _mean(self,kind,key):
        if kind=='gram':key=tuple(sorted(key))
        ck=(self.epoch,kind,key)
        if ck in self.cache:
            self.acquisition['cache_hits']+=1;return self.cache[ck]
        if self.acquisition['mean_jobs']>=self.Nmax:self.fail('proved lifetime job ceiling exceeded')
        self.acquisition['mean_jobs']+=1
        self.acquisition['theoretical_required_episodes']+=self.shots
        self.job_log.append({'epoch':self.epoch,'kind':kind,'key':key,'alpha':self.alpha,'beta_job':self.beta_job,'shots':self.shots})
        try:
            raw=self.adapter.estimate(kind,key,self.alpha,self.beta_job,self.shots,self.epoch)
            if not isinstance(raw,(int,F)):self.fail('adapter must return a finite exact rational, not float')
            value=F(raw)
            if not -1<=value<=1:self.fail('empirical mean outside [-1,1]')
        except (BudgetRefused,TerminalFailure) as exc:
            self.failed=str(exc);raise
        except Exception as exc:
            self.fail('scalar adapter failed: '+str(exc))
        finally:
            self.acquisition['actual_episodes']=getattr(self.adapter,'actual_episodes',0)
            self.acquisition['attempted_episodes']=getattr(self.adapter,'attempted_episodes',0)
            self.acquisition['actual_descriptor_controls']=getattr(self.adapter,'actual_descriptor_controls',0)
        self._track(value);self.cache[ck]=value;return value

    def _gram(self,u,v):return self._mean('gram',(u,v))

    def _build(self):
        m=len(self.words)
        b=1<<(m-1).bit_length();self.epoch=b;self.alpha=self.lam*self.lam/(4096*b);self.t=b*self.alpha/self.lam
        # At most Nmax jobs: their allocations sum to <=beta. Each precision
        # epoch has a common n-shot denominator, including cached means.
        self.beta_job=self.beta/self.Nmax;self.shots=required_shots(self.alpha,self.beta_job)
        self.acquisition['builds']+=1
        G=[[self._gram(u,v) for v in self.words] for u in self.words]
        self.A=add(G,[[self.lam*int(i==j) for j in range(m)] for i in range(m)])
        if not psd(self.A,strict=True):self.fail('Ahat failed exact SPD guard')
        self.Ainv=inverse(self.A);self.M={};self.S={}
        for a in self.alphabet:
            nxt=[w+(a,) for w in self.words]
            K=[[self._gram(u,v) for v in nxt] for u in self.words]
            HH=[[self._gram(u,v) for v in nxt] for u in nxt]
            M=scale(mm(self.Ainv,K),1/(1+4*self.t));MT=transpose(M)
            S=add(add(HH,scale(add(mm(transpose(K),M),mm(MT,K)),-1)),mm(mm(MT,self.A),M))
            S=add(S,scale(self.A,4*self.t/(1-self.t)))
            if not psd(S):self.fail('residual upper matrix failed exact PSD guard')
            self.M[a]=M;self.S[a]=S;self._track(M);self._track(S)
        self.h={r:[self._mean('readout',(r,w)) for w in self.words] for r in self.readouts}
        self._track(self.Ainv);self.ready=True

    def _evaluate(self,word,readout):
        z=[F(i==0) for i in range(len(self.words))];cert=self.tau+2*self.t
        eta=self.epsilon/(64*self.H)
        for a in word:
            cert+=sqrt_upper(quad(self.S[a],z),eta)
            z=mv(self.M[a],z)
        bitheight=max(x.numerator.bit_length()+x.denominator.bit_length() for x in z+[cert])
        value=sum((x*y for x,y in zip(self.h[readout],z)),F(0))
        return {'value':value,'certificate':cert,'dictionary_size':len(self.words),'word':word,'readout':readout,'evaluation_bitheight':bitheight}

    def request(self,word,readout):
        if self.failed is not None:raise TerminalFailure('latched: '+self.failed)
        word=tuple(word)
        if len(word)>self.H or any(a not in self.alphabet for a in word) or readout not in self.readouts:raise ValueError('request outside fixed contract')
        self.deployment['requests']+=1
        try:
            while True:
                if not self.ready:self._build()
                answer=self._evaluate(word,readout)
                if answer['certificate']<=self.epsilon:
                    self.deployment['max_rational_bitheight']=max(self.deployment['max_rational_bitheight'],answer['evaluation_bitheight'])
                    self.deployment['accepted']+=1
                    self.deployment['matrix_vector_products']+=len(word)
                    self.deployment['certificate_quadratic_forms']+=len(word)
                    return answer
                self.acquisition['max_rational_bitheight']=max(self.acquisition['max_rational_bitheight'],answer['evaluation_bitheight'])
                self.acquisition['rejected_evaluations']+=1
                self.acquisition['rejected_matrix_vector_products']+=len(word)
                self.acquisition['rejected_certificate_quadratic_forms']+=len(word)
                witness=None
                for j in range(len(word)+1):
                    w=word[:j]
                    if w in self.words:continue
                    self.acquisition['prefix_leverage_tests']+=1
                    v=[self._gram(u,w) for u in self.words]
                    lower=self._gram(w,w)-quad(self.Ainv,v)-8*self.t
                    if lower>self.lam:witness=w;break
                if witness is None:self.fail('rejected request has no novel lower-certified prefix')
                if len(self.words)>=self.W:self.fail('descriptor ceiling reached')
                self.words.append(witness);self.acquisition['dictionary_additions']+=1;self.ready=False
        except (ArithmeticError,TerminalFailure,BudgetRefused) as exc:
            self.failed=str(exc);raise
