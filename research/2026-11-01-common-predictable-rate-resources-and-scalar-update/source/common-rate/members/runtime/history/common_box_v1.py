"""Author construction for predictable channel-rate boxes; whole review pending.
Standard-library, exact rational scalar acquisition. No stationary-law claim.
"""
from fractions import Fraction as F
from hashlib import sha256
import json

class Unsupported(ValueError): pass
class BudgetRefusal(RuntimeError): pass

def rat(x):
    if type(x) not in (int,F): raise Unsupported('exact integer/Fraction required')
    return F(x)

def ceilq(x): return -((-x.numerator)//x.denominator)
def encode(x):
    if isinstance(x,F): return {'QHEX':[hex(x.numerator),hex(x.denominator)]}
    if type(x)is int and abs(x).bit_length()>4096:return {'ZHEX':hex(x)}
    if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [encode(v) for v in x]
    return x

def canonical_bytes(x): return (json.dumps(encode(x),sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x): return sha256(canonical_bytes(x)).hexdigest()

def decode(x):
    if isinstance(x,list):return [decode(v) for v in x]
    if isinstance(x,dict):
        if set(x)=={'QHEX'}:
            a,b=x['QHEX']
            if type(a)is not str or type(b)is not str:raise Unsupported('rational hex strings')
            return F(int(a,16),int(b,16))
        if set(x)=={'ZHEX'}:
            if type(x['ZHEX'])is not str:raise Unsupported('integer hex string')
            return int(x['ZHEX'],16)
        return {k:decode(v) for k,v in x.items()}
    return x

def receive_wire(raw,payload,max_bytes=10000000):
    if type(payload)is not bytes or type(max_bytes)is not int or max_bytes<0:raise Unsupported('bytes and nonnegative integer byte budget')
    if len(payload)>max_bytes:raise BudgetRefusal('wire byte budget')
    claimed=decode(json.loads(payload))
    if canonical_bytes(claimed)!=payload:raise Unsupported('noncanonical wire')
    return receive(raw,claimed)

def recognize(raw):
    if type(raw) not in (list,tuple) or not raw: raise Unsupported('nonempty channel box list')
    if type(raw[0]) not in (list,tuple) or len(raw[0])!=4: raise Unsupported('source,target,lower,upper rows')
    if type(raw[0][0]) not in (list,tuple): raise Unsupported('source complex sequence')
    m=len(raw[0][0]); ch={}
    if m<3: raise Unsupported('at least A and two satellites')
    for row in raw:
        if type(row) not in (list,tuple) or len(row)!=4: raise Unsupported('four-entry row')
        u,v,lo,hi=row
        if type(u) not in (list,tuple) or type(v) not in (list,tuple) or len(u)!=m or len(v)!=m: raise Unsupported('complex dimensions')
        if any(type(z)is not int or z<0 for z in tuple(u)+tuple(v)): raise Unsupported('nonnegative integer complexes')
        lo,hi=rat(lo),rat(hi)
        if not 0<lo<=hi or tuple(u)==tuple(v): raise Unsupported('strictly positive finite interval/nontrivial channel')
        key=(tuple(u),tuple(v));old=ch.get(key,(F(0),F(0)));ch[key]=(old[0]+lo,old[1]+hi)
    if any((v,u) not in ch for u,v in ch): raise Unsupported('positive reverse channel required')
    zero=(0,)*m;ups=[v for u,v in ch if u==zero]
    if len(ups)!=1 or sum(ups[0])!=1: raise Unsupported('one sole reversible port')
    one=ups[0];A=one.index(1);two=tuple(2*z for z in one);sat=tuple(i for i in range(m) if i!=A)
    if (one,zero) not in ch: raise Unsupported('port reverse missing')
    lam_lo,lam_hi=ch[(zero,one)];mu_lo,mu_hi=ch[(one,zero)]
    def hub(u): return u[A]==0 and sum(u)==2 and max(u)<=1
    def arm(u): return u[A]==1 and sum(u)==2
    hubs=set();internal=[];kl={i:F(0) for i in sat};ku=kl.copy()
    for (u,v),(lo,hi) in sorted(ch.items()):
        if (u,v) in ((zero,one),(one,zero)): continue
        if sum(u)!=2 or sum(v)!=2 or not ((hub(u) and (v==two or arm(v))) or (hub(v) and (u==two or arm(u)))): raise Unsupported('conservative binary hub-active architecture')
        hh=u if hub(u) else v;hubs.add(hh);internal.append((u,v,lo,hi))
        if arm(u):
            i=next(i for i in sat if u[i]);kl[i]+=lo;ku[i]+=hi
    if not hubs or any(kl[i]<=0 for i in sat): raise Unsupported('nonempty graph/all satellites have a positive arm')
    if any((two,hh) not in ch or (hh,two) not in ch for hh in hubs): raise Unsupported('every hub amplified reversibly')
    channels=tuple((u,v,lo,hi) for (u,v),(lo,hi) in sorted(ch.items()))
    return dict(m=m,A=A,n=len(sat),sat=sat,edges=tuple(sorted(tuple(i for i,z in enumerate(hh) if z) for hh in hubs)),channels=channels,
       lam_lo=lam_lo,lam_hi=lam_hi,mu_lo=mu_lo,mu_hi=mu_hi,
       a_hi=sum((ch[(two,hh)][1] for hh in hubs),F(0)),b_lo=min(ch[(hh,two)][0] for hh in hubs),
       s_hi=max(sum((hi for (u,v),(lo,hi) in ch.items() if u==hh),F(0)) for hh in hubs),
       kmin_lo=min(kl.values()),kmax_hi=max(ku.values()),Srate_hi=sum((hi for u,v,lo,hi in internal),F(0)),
       canonical_box_sha256=digest(channels))

def construct(raw):
    r=recognize(raw);n=r['n'];M=max(2,ceilq(12*r['s_hi']/r['b_lo']));q=F(M+1,M);aw=2*M;W=2*M+2
    g=r['kmin_lo']*(1-q**-2)/(q-1);h=r['b_lo']/(4*(q-1));Cstep=(4*M+4)*3**6
    CA=Cstep*(r['a_hi']+r['kmax_hi'])+18*r['mu_hi']*M;CH=Cstep*r['s_hi'];d=F(1,8*(3*M+3)**2)
    T=max(1,ceilq(4*CA/g),ceilq(4*CH*len(r['edges'])/h));B=1+n*T;R=(B+1)**2/d
    K=max(2,ceilq(4*2**n*CH*R/h));Pbar=(K+1)**n;RA=Pbar*CA*(B+1);RQ=Pbar*CH*(B+1)**2
    delta=F(1,4);eta=delta/(4*n);hh=eta**(n-1)/(2*n);epsC=min(F(1,4),hh**2/2,hh/8);gamma=delta*hh/8
    sstar=min(g,h)*d*epsC/4;Cbirth=r['lam_hi']*(1+Pbar)+r['mu_hi']**2/4
    eps=min(F(1),sstar/(16*Cbirth));t=1+eps;D=r['mu_lo']*(1-1/t);Fwd=2*r['a_hi']+r['kmax_hi']
    e=min(F(1,4),D/(4*(Fwd+1)));H=1+eps*(1+Pbar);dA=F(1,8*(3*M+1)**2)
    thresholds=(F(2),4*RA/D,RQ/(e*r['b_lo']),1+4*r['mu_hi']*H/(g*dA),
                4*(Cbirth*eps+1)/(D*gamma),2*(Cbirth*eps+1)/(e*r['b_lo']*gamma**2))
    Nstar=ceilq(max(thresholds));nu=min(r['lam_lo'],F(1),sstar/8);Htot=1+Pbar+H;zeta=nu/Htot
    CF_prefactor=(zeta+r['lam_hi']+r['mu_hi']*Nstar+r['Srate_hi']*Nstar**2)*Htot
    p=dict(status='PENDING_COMMON_PREDICTABLE_BOX_CERTIFICATE',raw=r,M=M,q=q,aw=aw,W=W,g=g,h=h,Cstep=Cstep,CA=CA,CH=CH,d=d,T=T,B=B,R=R,K=K,Pbar=Pbar,RA=RA,RQ=RQ,
       delta=delta,eta=eta,hh=hh,epsC=epsC,gamma=gamma,sstar=sstar,Cbirth=Cbirth,eps=eps,t=t,D=D,Fwd=Fwd,e=e,H=H,dA=dA,Nstar=Nstar,nu=nu,Htot=Htot,zeta=zeta,CF_prefactor=CF_prefactor,
       independent_sets_enumerated=0,CF_expression={'coefficient':CF_prefactor,'base':t,'exponent':Nstar+1},
       lyapunov_recipe={'sum':'nonempty independent I','face_weight':'K^(n-|I|)','resource':'2M*A+(2M+2)*NearMass+(M+1)*FarMass','tail':'(1-q^(-(J+M)))/(J+M)','other':'1-e*A/(N+1)+H*inactive_indicator','mask_bound':2**n})
    return p

def receive(raw,claimed):
    expected=construct(raw)
    if canonical_bytes(expected)!=canonical_bytes(claimed): raise Unsupported('canonical certificate mismatch')
    return {'status':'SAME_AUTHOR_CANONICAL_RECEIVED_NOT_INDEPENDENT','box_sha256':expected['raw']['canonical_box_sha256'],'certificate_sha256':digest(expected)}

def integer_budget(x,name):
    if type(x)is not int or x<0: raise ValueError(name+' must be nonnegative integer')
    return x

def state(p,x):
    if type(x) not in (list,tuple) or len(x)!=p['raw']['m'] or any(type(a)is not int or a<0 for a in x): raise ValueError('count state')
    return tuple(x)

def faces(p,max_masks=100000):
    integer_budget(max_masks,'max_masks');r=p['raw'];n=r['n']
    if 2**n>max_masks: raise BudgetRefusal('face enumeration budget')
    out=[]
    for mask in range(1,2**n):
        I=frozenset(r['sat'][j] for j in range(n) if mask>>j&1)
        if any(u in I and v in I for u,v in r['edges']):continue
        near={v for edge in r['edges'] for v in edge if v not in I and any(u in I for u in edge)}
        weights=tuple(p['aw'] if i==r['A'] else 0 if i in I else p['W'] if i in near else p['M']+1 for i in range(r['m']))
        out.append((weights,p['K']**(n-len(I))))
    return tuple(out)

def power(q,k,max_exponent=20000,max_bits=200000):
    integer_budget(max_exponent,'max_exponent');integer_budget(max_bits,'max_bits')
    bits=abs(k)*(q.numerator.bit_length()+q.denominator.bit_length())
    if abs(k)>max_exponent or bits>max_bits: raise BudgetRefusal('rational power budget')
    return q**k

def multiplier(p,x,fs=None,max_exponent=20000,max_bits=200000):
    x=state(p,x);fs=faces(p) if fs is None else fs;N=sum(x);r=p['raw'];A=x[r['A']]
    out=1-p['e']*A/(N+1)+(p['H'] if A==0 and not any(x[u]*x[v] for u,v in r['edges']) else 0)
    for weights,w in fs:
        k=sum(a*b for a,b in zip(weights,x))+p['M']
        out+=w*(1-power(p['q'],-k,max_exponent,max_bits))/k
    return out

def propensity(u,x):
    out=1
    for a,b in zip(u,x):
        if b<a:return 0
        for j in range(a):out*=b-j
    return out

def worst_scaled_drift(p,x,fn):
    """Exact max over the entire product box, with endpoint witness per channel."""
    x=state(p,x);fx=fn(x);total=F(0);witness=[]
    for u,v,lo,hi in p['raw']['channels']:
        y=tuple(a-b+c for a,b,c in zip(x,u,v));prop=propensity(u,x)
        if not prop: witness.append(lo);continue
        coeff=prop*(p['t']**(sum(v)-sum(u))*fn(y)-fx)
        k=hi if coeff>0 else lo;total+=k*coeff;witness.append(k)
    return total,tuple(witness)

class RateGuard:
    """Model-level admitted rates; invalid requests KEEP the previous rates.
    Predictability is a controller obligation, not inferred from a vector.
    No physical rate/actuator certification is performed.
    """
    def __init__(self,raw):
        self._raw=recognize(raw)
        self._active=tuple((lo+hi)/2 for u,v,lo,hi in self._raw['channels'])
        self.accepted=0;self.rejected=0
    @property
    def active(self): return self._active
    @property
    def box_sha256(self): return self._raw['canonical_box_sha256']
    def select(self,request):
        try:
            if type(request) not in (tuple,list) or len(request)!=len(self._active): raise Unsupported('wrong channel count')
            proposed=tuple(rat(k) for k in request)
            if any(not lo<=k<=hi for k,(u,v,lo,hi) in zip(proposed,self._raw['channels'])):raise Unsupported('outside acquired box')
        except (Unsupported,TypeError,ValueError):
            self.rejected+=1;return {'status':'REJECT_KEEP_PREVIOUS','box_sha256':self.box_sha256,'active_sha256':digest(self._active)}
        self._active=proposed;self.accepted+=1
        return {'status':'ADMIT_MODEL_RATES','box_sha256':self.box_sha256,'active_sha256':digest(self._active)}
    def intensities(self,x):
        # This exact model mapping, not an actuator assertion, earns the bounds.
        if type(x) not in (tuple,list) or len(x)!=self._raw['m'] or any(type(a)is not int or a<0 for a in x):raise ValueError('count state')
        return tuple(k*propensity(u,x) for k,(u,v,lo,hi) in zip(self._active,self._raw['channels']))

def tail_recipe(p,N0,horizon,level,event_threshold=None):
    integer_budget(N0,'received initial total upper bound');integer_budget(level,'level');T=rat(horizon)
    if T<0: raise ValueError('nonnegative horizon')
    # Symbolic powers are deliberate. This is not a numeric tail computation.
    out={'status':'FACTORED_RESOURCE_TAIL_RECIPE','max_count_upper':{'op':'min','args':[1,{'op':'mul','args':[F(4,3),{'op':'pow','base':p['t'],'exponent':-level},{'op':'add','args':[{'op':'mul','args':[p['Htot'],{'op':'pow','base':p['t'],'exponent':N0}]},{'op':'mul','args':[T,p['CF_expression']]}]}]}]},'box_sha256':p['raw']['canonical_box_sha256']}
    if event_threshold is not None:
        integer_budget(event_threshold,'event threshold');r=p['raw'];rate=r['lam_hi']+r['mu_hi']*level+r['Srate_hi']*level**2
        out['event_count_upper']={'op':'min','args':[1,{'op':'add','args':[out['max_count_upper'],{'op':'POISSON_UPPER_TAIL','mean':rate*T,'threshold':event_threshold}]}]}
        out['event_count_scope']='reaction firings only; level exit counted by the first term; controller overhead excluded'
    return out

def fixture():
    n=5;m=n+1;z=lambda *ix:tuple(ix.count(i) for i in range(m))
    rows=[(z(),z(0),F(1,2),F(3)),(z(0),z(),F(1,3),F(2))]
    for j,(u,v) in enumerate(((1,2),(1,3),(2,3),(4,5))):
        H=z(u,v);rows.extend([(z(0,0),H,F(1,2),F(2)),(H,z(0,0),F(1),F(3))])
        for i in range(1,m):
            rows.extend([(z(0,i),H,F(1,2),F(2)),(H,z(0,i),F(1,3),F(2 if j+i!=1 else 3))])
    return rows

def ceil_log2_at_least_one(x):
    """Least nonnegative k with 2^k>=x; costs depend on rational bit length."""
    x=rat(x)
    if x<=0: raise ValueError('positive ratio')
    if x<=1:return 0
    k=max(0,x.numerator.bit_length()-x.denominator.bit_length())
    if F(1<<k)<x:k+=1
    return k

def poisson_dyadic_threshold(mean,failure):
    """P(Pois(mean)>=m)<=failure via E2^P=exp(mean)<=2^(2ceil(mean))."""
    v=rat(mean);a=rat(failure)
    if v<0 or not 0<a<1:raise ValueError('mean>=0 and 0<failure<1')
    vc=ceilq(v);k=ceil_log2_at_least_one(1/a)
    return dict(threshold=2*vc+k,mean=v,mean_ceiling=vc,dyadic_confidence_bits=k,failure=a)

def resource_budget(p,N0,horizon,failure):
    """Actually acquired integer caps, no huge profile/final-power expansion.
    N0 must be a received history-measurable U>=current total count.
    No full state/Psi observation is needed. The API does not certify sensing.
    Conditional guarantee: P(max N>=R or firings>=m | past)<=failure.
    """
    integer_budget(N0,'received initial total upper bound');tt=rat(horizon);alpha=rat(failure)
    if tt<0 or not 0<alpha<1:raise ValueError('horizon>=0, 0<failure<1')
    half=alpha/2;block=ceilq(1/p['eps']);L=max(N0,p['Nstar']+1) if tt else N0
    ratio=F(4,3)*(p['Htot']+p['CF_prefactor']*tt)/half
    k=ceil_log2_at_least_one(ratio);RF=L+block*k
    arrival=poisson_dyadic_threshold(p['raw']['lam_hi']*tt,half);RP=N0+arrival['threshold']
    R=min(RF,RP);method='COMMON_FOSTER_LOG_HORIZON' if RF<RP else 'ORDINARY_IMMIGRATION_POISSON'
    r=p['raw'];Lambda=r['lam_hi']+r['mu_hi']*R+r['Srate_hi']*R**2
    firing=poisson_dyadic_threshold(Lambda*tt,half)
    return dict(status='ACQUIRED_INTEGER_RESOURCE_BUDGET_PENDING_THEOREM_REVIEW',box_sha256=r['canonical_box_sha256'],initial_total_upper_bound=N0,horizon=tt,failure=alpha,
                count_level=R,firing_level=firing['threshold'],selected_count_cap=method,
                foster_count_level=RF,immigration_count_level=RP,
                foster_receipt=dict(common_exponent_base=L,bernoulli_block=block,dyadic_bits=k,ratio=ratio),
                arrival_receipt=arrival,firing_receipt=firing,total_rate_cap=Lambda,
                guarantee='conditional on continuing history: P(max_count>=count_level OR reaction_firings>=firing_level)<=failure',
                excludes='controller decision/observation costs and unverified physical resources')

def receive_resource_budget(raw,claimed):
    """Reacquire from raw box, then compare full requested budget receipt.
    Same-author checking, not an independent implementation.
    """
    if type(claimed)is not dict:raise Unsupported('budget dictionary required')
    expected=resource_budget(construct(raw),claimed['initial_total_upper_bound'],claimed['horizon'],claimed['failure'])
    if canonical_bytes(expected)!=canonical_bytes(claimed):raise Unsupported('resource budget mismatch')
    return {'status':'SAME_AUTHOR_RESOURCE_BUDGET_RECEIVED','budget_sha256':digest(expected),'box_sha256':expected['box_sha256']}

class RiskLedger:
    """Trusted model-level predictable episode allocation; no reset/independence.
    Only admitted episodes inherit the familywise conditional union guarantee.
    """
    def __init__(self,total):
        total=rat(total)
        if not 0<total<1:raise ValueError('total failure budget in (0,1)')
        self.total=total;self.spent=F(0);self.allocations=[]
    def reserve(self,requested):
        try:
            a=rat(requested)
            if not 0<a<1 or self.spent+a>self.total:raise Unsupported('episode risk budget')
        except (Unsupported,TypeError,ValueError):
            return {'status':'REJECT_NO_ALLOCATION','spent':self.spent,'remaining':self.total-self.spent}
        self.spent+=a;self.allocations.append(a)
        return {'status':'ADMIT_EPISODE_RISK','episode':len(self.allocations)-1,'failure':a,'spent':self.spent,'remaining':self.total-self.spent}
