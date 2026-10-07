#!/usr/bin/env python3
"""Owned finite-bit heat-seed/cutoff-Euler/importance/Clifford compiler.

Exact rational decisions and outward intervals; measurements alone use floats.
The scientific Euler/statistical/Gibbs bound is reported separately from the
numerical law certificate. A bounded replay is not Monte Carlo validation.
S03 normal/interval primitives are copied in vendor/; no peer file is executed.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse, datetime, importlib.util, itertools, json, math, random
import resource, secrets, time

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('owned_normal',HERE/'vendor/certified_normal.py')
normal=importlib.util.module_from_spec(spec); spec.loader.exec_module(normal)
ar=normal.base; IV=ar.IV; iv=ar.iv

def ceilq(x): return -((-x.numerator)//x.denominator)
def bitbudget(x):
    p=0
    while F(1,1<<p)>x: p+=1
    return p
def near(x,p):
    y=x*(1<<p)+F(1,2)
    return F(y.numerator//y.denominator,1<<p)
def dot(x,y): return sum((a*b for a,b in zip(x,y)),F(0))
def norm2(x): return dot(x,x)
def eye(v=1): return [[F(v if i==j else 0) for j in range(3)] for i in range(3)]
def mm(A,B): return [[sum((A[i][t]*B[t][j] for t in range(3)),F(0)) for j in range(3)] for i in range(3)]
def mv(A,x): return [dot(row,x) for row in A]
def rows(A): return max(sum(map(abs,row),F(0)) for row in A)
def det(A):
    if len(A)==1: return A[0][0]
    return sum(((-1)**j)*A[0][j]*det([r[:j]+r[j+1:] for r in A[1:]]) for j in range(len(A)))
def psd(A):
    return all(det([[A[i][j] for j in I] for i in I])>=0
               for size in range(1,4) for I in itertools.combinations(range(3),size))
def inverse(A):
    d=det(A); assert d!=0
    return [[F((-1)**(i+j))*det([[A[r][c] for c in range(3) if c!=i]
                               for r in range(3) if r!=j])/d for j in range(3)] for i in range(3)]

def exp_bounds(x,p):
    """Range-reduced rational Taylor enclosure, absolute width <=2^-p."""
    x=F(x)
    if x==0: return F(1),F(1)
    if x<-(p+2): return F(0),F(1,1<<(p+2))  # e>=2
    j=0; t=x
    while abs(t)>F(1,2): t/=2; j+=1
    guard=j+ceilq(2*max(x,F(0)))+(j+1).bit_length()+16
    tol=F(1,1<<(p+guard)); term=total=F(1); n=0
    while True:
        rem=2*abs(term*t/F(n+1))
        if 2*rem<=tol: break
        n+=1; term=term*t/F(n); total+=term
    Q=1<<(p+guard)
    def out(a,b):
        return F((a*Q).numerator//(a*Q).denominator,Q),F(ceilq(b*Q),Q)
    lo,hi=out(max(F(0),total-rem),total+rem)
    for _ in range(j): lo,hi=out(lo*lo,hi*hi)
    assert 0<=lo<=hi and hi-lo<=F(1,1<<p)
    ar.ledger.add('owned_exp_series_terms',n)
    return lo,hi

def exp_iv(x):
    x=iv(x)
    return IV(exp_bounds(x.lo,IV.P+8)[0],exp_bounds(x.hi,IV.P+8)[1])
def log_scalar(x):
    assert x>0
    z=(x-1)/(x+1); assert abs(z)<1
    term=z; total=F(0); n=0; tol=F(1,1<<(IV.P+8))
    while True:
        total+=term/F(2*n+1)
        tail=2*abs(term*z*z)/(F(2*n+3)*(1-z*z))
        if tail<=tol: break
        term*=z*z; n+=1
    ar.ledger.add('owned_log_series_terms',n+1)
    return IV(2*total-tail,2*total+tail)
def log_iv(x):
    x=iv(x)
    return IV(log_scalar(x.lo).lo,log_scalar(x.hi).hi)
def cosh_iv(x): return (exp_iv(x)+exp_iv(-x))/2
def sinch_iv(x):
    x=iv(x)
    if x.hi<=1: return ar.even_series_iv(x,'sinch')
    assert x.lo>0
    return (exp_iv(x)-exp_iv(-x))/(2*x)

def root_spd(D,p):
    """Fast bounded-domain Newton, certified by residual and PSD floor."""
    assert psd([[D[i][j]-F(3,4)*int(i==j) for j in range(3)] for i in range(3)])
    gamma=F(1)
    while gamma*gamma<rows(D): gamma*=2
    X=eye(gamma); q=F(1,1<<p); P=p+24
    for iteration in range(1,25):
        inv=inverse(X); A=mm(D,inv); B=mm(inv,D)
        Y=[[X[i][j]/2+(A[i][j]+B[i][j])/4 for j in range(3)] for i in range(3)]
        X=[[near(Y[i][j],P) for j in range(3)] for i in range(3)]
        assert all(X[i][j]==X[j][i] for i in range(3) for j in range(3))
        residual=rows([[z-D[i][j] for j,z in enumerate(row)] for i,row in enumerate(mm(X,X))])
        if residual<=q and psd([[X[i][j]-F(1,2)*int(i==j) for j in range(3)] for i in range(3)]):
            # X E+E sqrt(D)=X²-D; both floors >=1/2, so ||E||op<=residual.
            ar.ledger.add('owned_spd_root_iterations',iteration)
            return X,residual,iteration
    raise ArithmeticError('SPD root residual guard failed; no output')

class Bits:
    def __init__(self,seed): self.rng=None if seed is None else random.Random(seed); self.used=0; self.transcript=[]
    def draw(self,n):
        self.used+=n
        answer=secrets.randbits(n) if self.rng is None else self.rng.getrandbits(n)
        self.transcript.append({'bits':n,'integer':answer})
        return answer

class Compiler:
    def __init__(self,N,T,R,eps,seed,A=None,b=None):
        self.N=N; self.k=math.isqrt(math.isqrt(N)); assert self.k**4==N and N>=4096
        self.T=T; self.R=R; self.eps=eps; self.bits=Bits(seed)
        self.M=F(1,10); self.B=F(1,5); self.Lambda=1+self.M; self.Lc=1+2*self.M
        self.A=[[F(1,10),F(0),F(0)],[F(0),F(-2,25),F(0)],[F(0),F(0),F(3,100)]] if A is None else A
        self.b=[F(1,10),F(1,20),F(-1,20)] if b is None else b
        assert len(self.A)==3 and all(len(row)==3 for row in self.A)
        assert all(self.A[i][j]==self.A[j][i] for i in range(3) for j in range(3)) and len(self.b)==3
        self.C=[[self.A[i][j]+self.Lambda*int(i==j) for j in range(3)] for i in range(3)]
        assert norm2(self.b)<=self.B*self.B
        for sign in [-1,1]: assert psd([[self.M*int(i==j)+sign*self.A[i][j] for j in range(3)] for i in range(3)])
        self.Tc=sum(self.C[i][i] for i in range(3)); self.r02=1/(16*(self.Lc+1))
        self.L=12; self.normalL=8; self.s=self.k**3; self.d0=1-self.Lambda/(2*self.k*self.k)
        assert self.d0>=F(1,2)
        self.zbound=ceilq(2*(self.Lambda+1)); self.p0=F(1,(1<<self.zbound)*self.L**3)
        self.eb=bitbudget(eps/(128*R)); self.K=ceilq(F(self.eb+8)/self.p0)
        rho=2*self.L; self.Lseed=rho*(self.Lambda/4+F(1,12))+F(rho**3,48)
        self.seed_p=bitbudget(eps/(1024*R*self.K*(2*self.L*self.Lseed+4)))
        self.p=max(48,self.seed_p)
        assert self.p<=128
        self.normal_p=min(64,max(48,bitbudget(eps/(4096*R*T*(self.k+1)))))
        # Rational public Lipschitz bounds (r0>1/8 for this admitted M).
        self.La=(self.Lc*(1+3*self.r02)/2+8*self.Lc)/(self.k*self.k)+64*self.B/self.s
        self.Lsig=(6*self.Lc+64*(3*self.Lc+1))/self.s
        amp_log=self.La+2*self.normalL*self.Lsig*T
        # sqrt(T)<=T: deliberately conservative, polynomial precision budget.
        self.amp_pow=ceilq(2*amp_log+1); self.amp=1<<self.amp_pow
        self.path_p=max(self.p,bitbudget(eps/(8192*R*T*self.amp*(self.k*self.k+1))))
        self.p=max(self.p,bitbudget(eps/(8192*R*T*self.amp*(self.k+1))))
        self.path_p=max(self.path_p,self.p)
        self.normal_p=max(self.normal_p,bitbudget(eps/(8192*R*T*self.amp*(self.k*self.k+1)*(self.normalL+1)*(self.Lc+1))))
        assert self.normal_p<=128, 'Configured normal component precision exceeded; no certificate emitted'
        self.stats={'seed_attempts':0,'seed_full_evaluations':0,'seed_upper_rejections':0,
                    'normal_calls':0,'normal_bits':0,'cdf_requests':0,'cdf_terms':0,
                    'matrix_roots':0,'max_root_residual':F(0),'exhausted_seeds':0}
        self.precision()
        delta=iv(F(1,2))-log_iv(cosh_iv(iv(1)))
        assert delta.lo>F(1,16), 'Acquire the rational f(1) lower constant before use'

    def precision(self): IV.precision(self.path_p+self.N.bit_length()+32)
    def density(self,x):
        self.precision(); r2=norm2(x)
        if r2==0: return iv(1)
        rad=ar.sqrt_iv(r2); y=rad/(2*self.k)
        f=y*y/2-log_iv(cosh_iv(y))
        ell=log_iv(sinch_iv(y))-r2*self.Lambda/(16*self.d0)-self.N*f
        val=exp_iv(ell)
        lo=max(F(0),val.lo); hi=min(F(1),val.hi)
        assert hi-lo<=F(1,1<<self.p)
        return IV(lo,hi,raw=True)

    def seed(self):
        Q=1<<self.p
        for attempt in range(1,self.K+1):
            self.stats['seed_attempts']+=1
            x=[F(2*self.bits.draw(self.p)+1-Q,Q)*self.L for _ in range(3)]
            u=F(self.bits.draw(self.p),Q); r2=norm2(x)
            # Certified scalar envelope; reject without a costly log-cosh evaluation.
            if r2<=4*self.k*self.k: fbound=r2*r2/256
            else: fbound=self.k*self.k*r2/64
            upper_log=r2/(24*self.k*self.k)-self.Lambda*r2/(16*self.d0)-fbound
            _,upper=exp_bounds(upper_log,self.p+8)
            if u>upper:
                self.stats['seed_upper_rejections']+=1; continue
            self.stats['seed_full_evaluations']+=1
            enc=self.density(x); alpha=(enc.lo+enc.hi)/2
            n=min(Q,max(0,(alpha*Q).numerator//(alpha*Q).denominator))
            if u<F(n,Q):
                m,me=self.bloch(x)
                return self.seed_contract(m), {'attempts':attempt,'field_R':x,
                    'acceptance_interval':enc.json(),'precontract_bloch_error_upper':me,'exhausted':False}
        self.stats['exhausted_seeds']+=1
        return [F(0)]*3,{'attempts':self.K,'exhausted':True}

    def bloch(self,x):
        self.precision(); r2=norm2(x)
        if r2==0: return [F(0)]*3,F(0)
        rad=ar.sqrt_iv(r2); y=rad/(2*self.k); e=exp_iv(2*y); tanh=(e-1)/(e+1)
        factor=tanh/rad; boxes=[factor*xi for xi in x]
        m=[near((z.lo+z.hi)/2,self.path_p) for z in boxes]
        err=sum((z.hi-z.lo for z in boxes),F(0))/2+F(3,1<<(self.path_p+1))
        assert norm2(m)<1
        return m,err
    def seed_contract(self,m):
        c=min(F(1),max(F(0),2-16*norm2(m)/self.r02))
        out=[near(c*x,self.path_p) for x in m]
        assert norm2(out)<=self.r02/9+F(1,1<<(self.path_p-3))
        return out
    def retract(self,m):
        r2=norm2(m)
        if r2<=self.r02: return m
        return [x*self.r02/r2 for x in m]
    def V(self,m):
        m=self.retract(m); quad=dot(m,mv(self.C,m))
        return F(self.N*(self.N-1),4*self.s*self.s)*quad+F(self.N*self.Tc,4*self.s*self.s)+F(self.N,2*self.s)*dot(self.b,m)
    def coefficients(self,m):
        chi=min(F(1),max(F(0),3-4*norm2(m)/self.r02))
        if chi==0: return [F(0)]*3,eye(0),F(0),0
        P=[[F(int(i==j))-m[i]*m[j] for j in range(3)] for i in range(3)]
        cross=[[F(0),-m[2],m[1]],[m[2],F(0),-m[0]],[-m[1],m[0],F(0)]]
        trans=list(map(list,zip(*cross))); U=mm(mm(P,self.C),P); W=mm(mm(cross,self.C),trans)
        D=[[U[i][j]-W[i][j] for j in range(3)] for i in range(3)]
        root,residual,it=root_spd(D,self.path_p)
        self.stats['matrix_roots']+=1; self.stats['max_root_residual']=max(self.stats['max_root_residual'],residual)
        quad=dot(m,mv(self.C,m)); field=dot(self.b,m)
        drift=[chi*(F(self.N-1,2*self.s*self.s)*(z-quad*m[i])+F(1,2*self.s)*(self.b[i]-field*m[i])) for i,z in enumerate(mv(self.C,m))]
        self.precision(); factor_iv=ar.sqrt_iv(F(1,2*self.T))/self.s
        factor=(factor_iv.lo+factor_iv.hi)/2
        noise=[[chi*factor*z for z in row] for row in root]
        return drift,noise,residual,it

    def one_normal(self):
        n=self.normal_p+ceilq(F(self.normalL*self.normalL))+8
        u=self.bits.draw(n); data=normal.generate(F(self.normalL),self.normal_p,u)
        assert data['exact_fair_random_bit_count']==n
        self.stats['normal_calls']+=1; self.stats['normal_bits']+=n
        self.stats['cdf_requests']+=data['cdf_request_count']; self.stats['cdf_terms']+=data['cdf_integral_taylor_terms']
        return F(data['output_rational'])
    def path(self):
        m,seed=self.seed(); ell=F(0); maxr2=norm2(m)
        for _ in range(self.T):
            ell+=self.V(m)/self.T
            drift,noise,residual,it=self.coefficients(m)
            z=[self.one_normal() for i in range(3)]
            inc=mv(noise,z)
            m=[near(m[i]+drift[i]/self.T+inc[i],self.path_p) for i in range(3)]
            maxr2=max(maxr2,norm2(m))
        m=self.retract(m)
        return m,ell,{'seed':seed,'maximum_grid_norm_squared':maxr2}

    def choose(self,states,logs):
        p=self.p; Q=1<<p; highest=max(logs); ints=[]; errors=[]
        for ell in logs:
            lo,hi=exp_bounds(ell-highest,p+8)
            n=(F(lo+hi,2)*Q).numerator//(F(lo+hi,2)*Q).denominator
            if ell==highest: n=Q
            assert n>=0
            ints.append(n); errors.append(max(abs(F(n,Q)-lo),abs(F(n,Q)-hi)))
        denom=sum(ints); b=denom.bit_length(); attempts=0
        while True:
            u=self.bits.draw(b); attempts+=1
            if u<denom: break
            if attempts>=128:
                u=0; break  # arbitrary positive fallback; its probability is charged
        total=0
        for i,n in enumerate(ints):
            total+=n
            if u<total: break
        # A maximal unscaled weight is exactly1; normalized TV<=sum abs errors.
        return i,{'integer_weights':ints,'denominator':denom,'exact_integer_choice':u,
                  'random_integer_attempts':attempts,'categorical_TV_error_upper':sum(errors),
                  'integer_selector_cap_failure_upper':F(1,1<<128)}

    def pauli_emissions(self,m,count):
        # Tiny inward dyadic rounding gives an exact positive octahedron point.
        P=self.path_p; D=1<<P
        local=[near(x,P) for x in m]; assert sum(map(abs,local),F(0))<1
        weights=[abs(x) for x in local]
        entries=[int(w*D) for w in weights]; entries.append(D-sum(entries))
        assert sum(entries)==D and all(n>=0 for n in entries)
        gate_options=[['H'],['H','S'],[]]
        choices=[]; gate_count=0
        for _ in range(count):
            u=self.bits.draw(P); total=0
            for axis,n in enumerate(entries):
                total+=n
                if u<total: break
            if axis==3:
                sign=self.bits.draw(1); gates=['X'] if sign else []
                label='I/2 independently sampled +/-Z'
            else:
                gates=list(gate_options[axis])
                if local[axis]<0: gates.insert(0,'X')
                label=('X','Y','Z')[axis]+('+' if local[axis]>=0 else '-')
            choices.append({'branch':label,'gates_in_application_order':gates}); gate_count+=len(gates)
        blocherr=sum(abs(a-b) for a,b in zip(local,m))
        return {'method':'Independent Pauli-octahedron draws at each site; ideal Clifford interface',
            'dyadic_local_Bloch':local,'common_denominator':D,'Pauli_axis_integer_weights':entries,
            'sites_requested':self.N,'sites_transcript_executed':count,
            'complete_N_site_transcript':count==self.N,'local_ideal_gate_count_executed':gate_count,
            'maximum_ideal_Clifford_gates_per_site':3,
            'description_rounding_product_trace_upper':self.k*self.k*blocherr,
            'gate_transcript':choices,'physical_hardware_execution':False}

    def numerical_budget(self):
        q=F(1,1<<self.p); qp=F(1,1<<self.path_p); qn=F(1,1<<self.normal_p)
        # Continuous uniform cube -> dyadic centers, acceptance -> dyadic midpoint law.
        seedcoin=self.R*self.K*((2*self.L*self.Lseed+4)*q)
        seedexhaust=self.R*F(1,1<<(self.eb+8))
        if self.L>=2*self.k:
            # The whole omitted radius is in the Gaussian region. Acquire
            # f(y0)/y0² directly; monotonicity controls all y>=y0.
            self.precision(); y0=F(self.L,2*self.k)
            f0=iv(y0*y0/2)-log_iv(cosh_iv(iv(y0)))
            delta0=f0.lo/(y0*y0); assert delta0>=F(1,16)
            c=self.k*self.k*delta0/4+self.Lambda/(16*self.d0)-F(1,24*self.k*self.k)
            assert c>0
            multiplier=max(1,ceilq(1/c)**2)*(1<<self.zbound)
            exponent=(c*self.L*self.L/2).numerator//(c*self.L*self.L/2).denominator
            exterior=min(F(1),F(multiplier,1<<exponent)); lowtail=F(0)
        else:
            lowtail=F(256*(1<<self.zbound),1<<(self.L**4//512))
            exterior=F(1,1<<100) if self.N//64>=100+self.zbound+12 else min(F(1),F(4096*(1<<self.zbound),1<<(self.N//64)))
        seedtail=self.R*(lowtail+exterior)
        # Upper bound on pointwise path coupling on the retained Gaussian draw set.
        # Seed map has Lipschitz<=4; m(R) has Lipschitz<=1/(2k).
        init=6*self.L*q/self.k+8*qp
        one_step=8*qp+F(12*(self.Lc+1),self.s)*(qn+qp)*self.normalL
        pathdelta=self.amp*(init+self.T*one_step)
        Vlip=(self.Lc+self.B)*self.k*self.k  # r0<=1, retract 1-Lipschitz
        logdelta=Vlip*pathdelta
        assert logdelta<F(1,8)
        categorical_from_path=4*logdelta
        branch=self.k*self.k*pathdelta
        tail,degree=normal.tail_upper(F(self.normalL))
        normalbad=3*self.R*self.T*tail
        selection=self.R*2*q+F(1,1<<128)
        total=seedcoin+seedexhaust+seedtail+normalbad+categorical_from_path+branch+selection
        return {'certificate_scope':'Numerical average-state error to continuous full-heat-seed exact-normal Euler importance law at the SAME R,T, plus ideal Clifford output rounding',
            'seed_coin_coupling_upper':seedcoin,'seed_exhaustion_upper':seedexhaust,
            'full_heat_seed_cube_tail_union_upper':seedtail,'normal_tail_union_upper':normalbad,
            'retained_path_Bloch_coupling_upper':pathdelta,'retained_logweight_coupling_upper':logdelta,
            'resampling_path_TV_upper':categorical_from_path,'product_branch_trace_upper':branch,
            'dyadic_selection_upper':selection,'total_before_output_rounding_upper':total,
            'requested_numerical_epsilon':self.eps,'passes_numerical_budget':total<=self.eps,
            'normal_tail_positive_Taylor_degree':degree,
            'warning':'No statistical R^-1/2, Euler-to-SDE, or SDE-to-Gibbs error is included in this numerical bound.'}

def stringize(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,list): return [stringize(z) for z in x]
    if isinstance(x,dict): return {k:stringize(v) for k,v in x.items()}
    return x

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--N',type=int,default=4096)
    ap.add_argument('--steps',type=int,default=1); ap.add_argument('--proposals',type=int,default=4)
    ap.add_argument('--epsilon',default='1/1000'); ap.add_argument('--seed',type=int)
    ap.add_argument('--emit-count',type=int,default=4096); ap.add_argument('--out',required=True)
    ap.add_argument('--A',help='Nine comma-separated rational symmetric matrix entries, row order; fixed public M=1/10')
    ap.add_argument('--b',help='Three comma-separated rational field entries; fixed public B=1/5')
    args=ap.parse_args(); assert args.steps>=1 and args.proposals>=1
    ar.ledger=ar.Ledger(); start=time.perf_counter(); cpu=time.process_time()
    A=None if args.A is None else [list(map(F,args.A.split(',')))[3*i:3*i+3] for i in range(3)]
    b=None if args.b is None else list(map(F,args.b.split(',')))
    c=Compiler(args.N,args.steps,args.proposals,F(args.epsilon),args.seed,A,b)
    budget=c.numerical_budget(); assert budget['passes_numerical_budget']
    assert not any(isinstance(z,float) for z in budget.values()), 'No floating certificate allowed'
    states=[]; logs=[]; paths=[]
    for _ in range(c.R):
        m,ell,path=c.path(); states.append(m); logs.append(ell); paths.append(path)
    idx,choice=c.choose(states,logs); output=c.pauli_emissions(states[idx],min(c.N,args.emit_count))
    total=budget['total_before_output_rounding_upper']+output['description_rounding_product_trace_upper']
    assert total<=c.eps
    data={'worker':'c07_s02','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status':'CERTIFIED_NUMERICAL_CUTOFF_EULER_PIPELINE; FULL_GIBBS_STATISTICAL_BUDGET_SEPARATE',
        'parameter_contract':{'N':c.N,'A':c.A,'b':c.b,'M':c.M,'B':c.B,'Lambda':c.Lambda,'r0_squared':c.r02},
        'run_contract':{'T':c.T,'R':c.R,'cube_L':c.L,'seed_cap_K':c.K,
            'seed_grid_bits':c.p,'Euler_coordinate_bits':c.path_p,'normal_error_bits':c.normal_p,
            'path_amplification_upper':c.amp,'source':'OS secrets.randbits, theorem assumes iid fair bits' if args.seed is None else 'seeded replay, not iid evidence','seed':args.seed},
        'numerical_error_certificate':budget,'total_numerical_error_with_local_output_upper':total,
        'chosen_proposal_index':idx,'states':states,'logweights':logs,'paths':paths,
        'importance_selection':choice,'local_output':output,
        'random_prefix_transcript':c.bits.transcript,
        'unexecuted_scientific_guarantee':{'Gibbs_comparison':'Owned source stopped theorem plus cutoff/contracted seed comparison; explicit certificate may be vacuous for small N.',
            'Euler_systematic':'Must add proved public C(M,B)*(1/T+N^-1/4/sqrt(T)), or the more conservative S03 sqrt(N/T) theorem.',
            'statistical':'Must add exp(B²/2)*sqrt(K2/R), with certified public K2; empirical sample variance is not substituted.',
            'full_scientific_error_numeric':'UNKNOWN in this numerical compiler artifact; separately acquired bounds required.'},
        'costs':{'random_bits_used':c.bits.used,**c.stats,**ar.ledger.snapshot(),
                 'arithmetic_count_limit':'Counters/maximum integer sizes track explicit primitive calls, not all owned Fraction/GCD operations.',
                 'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,
                 'process_peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
        'limits':['Finite-bit program acquires the specified bounded Euler law, not exact Brownian paths.',
                  'Finite replay is not accuracy or Monte Carlo evidence for the continuous scientific theorem.',
                  'Ideal Clifford gates/reset and fair bits are explicit device/random-source interfaces.',
                  'Large N can use a compressed per-site gate generator; a partial transcript is flagged.',
                  'Priority, external mathematical certification, energy and physical hardware runtime UNKNOWN.'],
        'attribution':['S02 exact generator/stopped theorem', 'S03 copied interval/normal primitives, cutoff/Euler/moment bridge and Pauli output insight',
                       'S01 quartic moment audit; L08 scalar envelopes', 'root/S08/S03 sharper Euler scaling pending full integration']}
    path=Path(args.out); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(stringize(data),indent=2)+'\n')
    print(json.dumps({'output':str(path),'status':data['status'],'N':c.N,'R':c.R,'T':c.T,
        'full_emission_transcript':output['complete_N_site_transcript'],'seed_attempts':c.stats['seed_attempts'],
        'normal_calls':c.stats['normal_calls'],'normal_bits':c.stats['normal_bits'],
        'numerical_error_upper':str(total),'wall_seconds':data['costs']['wall_seconds']}))

if __name__=='__main__': main()
