"""Source-faithful bounded-projection online scalar-return receiver.

No hidden vectors. Source data enter only through calibrated scalar adapters.
Small exact active-face proposals are capped at m<=4 and accepted only after an
exact FW-gap check. Generic rounded FW has an explicit pre-execution budget.
"""
from fractions import Fraction as F
from itertools import combinations,product
from receiver import (TerminalFailure,BudgetRefused,BinaryMeanAdapter,ceil_log2,
                      required_shots,mv,inverse,quad,psd,sqrt_upper)

def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def ceil_fraction(x):return (x.numerator+x.denominator-1)//x.denominator

def _round_zero(x,D):
    a=abs(x.numerator)*D//x.denominator
    return F(a if x>=0 else -a,D)

def _work():
    return {'qp_calls':0,'proposal_linear_solves':0,'proposal_accepts':0,
            'fw_gap_checks':0,'rounded_fw_steps':0,'theoretical_fw_iteration_caps':0,
            'max_coefficient_bitheight':0,'rollout_steps':0,'residual_forms':0,
            'correction_forms':0,'prefix_distance_solves':0}

def _merge(a,b):
    for k,v in b.items():
        if k.startswith('max_'):a[k]=max(a.get(k,0),v)
        else:a[k]=a.get(k,0)+v


class BoundedProjectionReceiver:
    def __init__(self,alphabet,H,epsilon,delta,adjoints,adapter,
                 max_fw_iterations=10000,use_small_proposals=True):
        self.alphabet=tuple(alphabet);self.H=H;self.epsilon=F(epsilon);self.delta=F(delta)
        self.adjoints=dict(adjoints);self.adapter=adapter
        if not self.alphabet or len(set(self.alphabet))!=len(self.alphabet) or H<1:raise ValueError('invalid alphabet/horizon')
        if not 0<self.epsilon<=1 or not 0<self.delta<1:raise ValueError('invalid tolerances')
        if set(self.adjoints)!=set(self.alphabet) or any(self.adjoints.get(self.adjoints[a])!=a for a in self.alphabet):raise ValueError('adjoint labels must be a supplied involution')
        if max_fw_iterations is not None and max_fw_iterations<0:raise ValueError('negative optimizer budget')
        self.max_fw_iterations=max_fw_iterations;self.use_small_proposals=use_small_proposals
        self.lam=self.epsilon/(128*H**4)
        self.W=1
        for _ in range(H):self.W=1+len(self.alphabet)*self.W
        self.W1=1+len(self.alphabet)*self.W;self.E=1+ceil_log2(self.W)
        self.Jmax=(self.E+1)*(self.W1+1)**2
        self.beta=self.delta/(self.W+1)**64;self.beta_job=self.beta/self.Jmax
        self.words=[()];self.cache={};self.job_log=[];self.failed=None;self.ready=False
        self.acquisition={'mean_jobs':0,'cache_hits':0,'theoretical_required_episodes':0,
            'actual_episodes':0,'attempted_episodes':0,'actual_descriptor_controls':0,
            'builds':0,'dictionary_additions':0,'rejected_evaluations':0,
            'calibration_mode':getattr(adapter,'calibration_mode','UNDECLARED'),
            'input_tolerance_bitheight':sum(x.numerator.bit_length()+x.denominator.bit_length() for x in (self.epsilon,self.delta)),**_work()}
        self.deployment={'requests':0,'accepted':0,**_work()}
        self.optimizer_log=[]

    def _fail(self,message):
        self.failed=str(message);raise TerminalFailure(self.failed)

    def _mean(self,u,v):
        if len(u)>self.H+1 or len(v)>self.H+1:self._fail('descriptor outside proved moment universe')
        key=tuple(sorted((u,v)));ck=(self.epoch,key)
        if ck in self.cache:
            self.acquisition['cache_hits']+=1;return self.cache[ck]
        if self.acquisition['mean_jobs']>=self.Jmax:self._fail('lifetime mean-job ceiling exceeded')
        self.acquisition['mean_jobs']+=1;self.acquisition['theoretical_required_episodes']+=self.shots
        self.job_log.append({'epoch':self.epoch,'key':key,'alpha':self.alpha,'beta_job':self.beta_job,'shots':self.shots})
        try:
            raw=self.adapter.estimate('gram',key,self.alpha,self.beta_job,self.shots,self.epoch)
            if not isinstance(raw,(F,int)):self._fail('scalar adapter must return exact rational means')
            value=F(raw)
            if not -1<=value<=1:self._fail('mean outside binary-report range')
        except (TerminalFailure,BudgetRefused) as exc:
            self.failed=str(exc);raise
        except Exception as exc:self._fail('scalar adapter failed: '+str(exc))
        finally:
            for k in ('actual_episodes','attempted_episodes','actual_descriptor_controls'):
                self.acquisition[k]=getattr(self.adapter,k,0)
        self.cache[ck]=value;return value

    def _build(self):
        m=len(self.words);self.B=m;self.epoch=1<<(m-1).bit_length();b=self.epoch
        self.alpha=self.lam/(128*(b+4)*b*b)
        self.shots=required_shots(self.alpha,self.beta_job)
        self.G=[[self._mean(u,v) for v in self.words] for u in self.words]
        self.A=[[self.G[i][j]+(m*self.alpha if i==j else 0) for j in range(m)] for i in range(m)]
        if not psd(self.A):self._fail('repaired empirical Gram failed PSD guard')
        self.K={};self.HH={}
        for a in self.alphabet:
            successor=[w+(a,) for w in self.words]
            self.K[a]=[[self._mean(u,v) for v in successor] for u in self.words]
            self.HH[a]=[[self._mean(u,v) for v in successor] for u in successor]
        self.acquisition['builds']+=1;self.ready=True

    def _gap(self,c,k,work):
        work['fw_gap_checks']+=1
        grad=[2*(x-y) for x,y in zip(mv(self.A,c),k)]
        j=max(range(self.B),key=lambda i:abs(grad[i]))
        s=[F(0)]*self.B;s[j]=F(-self.B if grad[j]>0 else self.B)
        gap=dot(grad,[x-y for x,y in zip(c,s)])
        if gap<0:self._fail('negative exact FW gap')
        return gap,s

    def _proposal(self,k,work):
        """Constant-size scalar-only accelerator; NOT the generic optimizer."""
        n=self.B;candidates=[]
        def solve(A,rhs):
            work['proposal_linear_solves']+=1
            try:return mv(inverse(A),rhs)
            except ArithmeticError:return None
        c=solve(self.A,k)
        if c is not None and sum(map(abs,c))<=n:candidates.append(c)
        for size in range(1,n+1):
            for support in combinations(range(n),size):
                for signs in product((-1,1),repeat=size):
                    matrix=[[self.A[i][j] for j in support]+[F(signs[h])] for h,i in enumerate(support)]
                    matrix.append([F(s) for s in signs]+[F(0)])
                    sol=solve(matrix,[k[i] for i in support]+[F(n)])
                    if sol is None or any(s*x<0 for s,x in zip(signs,sol)):continue
                    c=[F(0)]*n
                    for i,x in zip(support,sol):c[i]=x
                    if sum(map(abs,c))<=n:candidates.append(c)
        if not candidates:return None
        return min(candidates,key=lambda c:quad(self.A,c)-2*dot(k,c))

    def _solve(self,k,work):
        m=self.B;work['qp_calls']+=1
        delta=m*m*self.alpha;C=16*m**3;theta=delta/C
        hmax=delta*delta/(24*C*m*m);D=1<<ceil_log2(1/hmax)
        R=8*m**3;cap=ceil_fraction(4*C*F(R)/(delta*delta))+1
        work['theoretical_fw_iteration_caps']+=cap
        c=[F(0)]*m;gap,_=self._gap(c,k,work);path='zero'
        if gap>delta and self.use_small_proposals and m<=4:
            proposal=self._proposal(k,work)
            if proposal is not None:
                c=[_round_zero(x,D) for x in proposal]
                gap,_=self._gap(c,k,work)
                if gap<=delta:work['proposal_accepts']+=1;path='capped_active_face_proposal'
        if gap>delta:
            if self.max_fw_iterations is not None and cap>self.max_fw_iterations:
                raise BudgetRefused(f'rounded FW proof cap {cap} exceeds configured per-solve budget {self.max_fw_iterations}; no fallback steps executed')
            path='rounded_fw'
            for _ in range(cap):
                gap,s=self._gap(c,k,work)
                if gap<=delta:break
                c=[_round_zero((1-theta)*x+theta*y,D) for x,y in zip(c,s)]
                work['rounded_fw_steps']+=1
            gap,_=self._gap(c,k,work)
            if gap>delta:self._fail('rounded FW iteration cap exhausted')
        if sum(map(abs,c))>m:self._fail('optimizer returned infeasible coefficients')
        work['max_coefficient_bitheight']=max(work['max_coefficient_bitheight'],max(x.numerator.bit_length()+x.denominator.bit_length() for x in c))
        self.optimizer_log.append({'m':m,'gap':gap,'delta':delta,'grid_denominator_bits':D.bit_length(),'proof_iteration_cap':cap,'path':path})
        if len(self.optimizer_log)>256:self.optimizer_log.pop(0)  # bounded deployment diagnostics
        return c,gap

    def _rollout(self,word,work):
        cs=[[F(i==0) for i in range(self.B)]];norms=[]
        eta=self.epsilon/(128*self.H*self.H*(self.B+1))
        for a in word:
            d=cs[-1];c,_=self._solve(mv(self.K[a],d),work)
            rad=quad(self.HH[a],d)-2*dot(c,mv(self.K[a],d))+quad(self.G,c)+4*self.B*self.B*self.alpha
            if rad<0:self._fail('negative residual upper radicand')
            norms.append(sqrt_upper(rad,eta));cs.append(c)
            work['rollout_steps']+=1;work['residual_forms']+=1
        return cs,norms

    def _evaluate(self,word,work):
        if not word:return {'value':self.G[0][0],'certificate':self.alpha,'word':word,'dictionary_size':self.B}
        forward,R=self._rollout(word,work)
        dualword=tuple(self.adjoints[a] for a in reversed(word))
        backward,S=self._rollout(dualword,work);l=len(word)
        estimate=dot(self.G[0],forward[-1])
        for i,a in enumerate(word,1):
            cross=[x-y for x,y in zip(mv(self.K[a],forward[i-1]),mv(self.G,forward[i]))]
            estimate+=dot(backward[l-i],cross);work['correction_forms']+=1
        cert=(self.B+2*l*self.B*self.B)*self.alpha
        cert+=sum((R[i-1]*sum(S[:l-i],F(0)) for i in range(1,l+1)),F(0))
        return {'value':max(F(-1),min(F(1),estimate)),'certificate':cert,'word':word,'dictionary_size':self.B}

    def _witness(self,word,work):
        reverse=tuple(self.adjoints[a] for a in reversed(word));seen=set(self.words)
        for route in (word,reverse):
            for j in range(1,len(route)+1):
                prefix=route[:j]
                if prefix in seen:continue
                seen.add(prefix);work['prefix_distance_solves']+=1
                k=[self._mean(v,prefix) for v in self.words];norm=self._mean(prefix,prefix)
                c,gap=self._solve(k,work)
                value=quad(self.A,c)-2*dot(c,k)+norm
                lower=value-gap-(self.B+4)*self.B*self.B*self.alpha
                if lower>self.lam/2:return prefix
        return None

    def request(self,word):
        if self.failed is not None:raise TerminalFailure('latched: '+self.failed)
        word=tuple(word)
        if len(word)>self.H or any(a not in self.alphabet for a in word):raise ValueError('request outside fixed task contract')
        self.deployment['requests']+=1;work=_work()
        try:
            while True:
                if not self.ready:self._build()
                result=self._evaluate(word,work)
                if result['certificate']<=self.epsilon:
                    _merge(self.deployment,work);self.deployment['accepted']+=1;return result
                self.acquisition['rejected_evaluations']+=1
                witness=self._witness(word,work)
                _merge(self.acquisition,work);work=_work()
                if witness is None:self._fail('rejected task has no certified novel prefix')
                if witness in self.words or len(self.words)>=self.W:self._fail('descriptor uniqueness/ceiling guard')
                self.words.append(witness);self.acquisition['dictionary_additions']+=1;self.ready=False
        except Exception as exc:
            _merge(self.acquisition,work);self.failed=str(exc)
            raise
