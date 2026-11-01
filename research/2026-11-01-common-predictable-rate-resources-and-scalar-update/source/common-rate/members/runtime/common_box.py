"""Author construction for predictable channel-rate boxes; whole review pending.
Standard-library, exact rational scalar acquisition. No stationary-law claim.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from copy import deepcopy

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

def _limits(max_nodes,max_depth,max_atom_bits,max_string_chars):
    for name,value in [('nodes',max_nodes),('depth',max_depth),('atom bits',max_atom_bits),('string characters',max_string_chars)]:
        if type(value)is not int or value<0:raise Unsupported('nonnegative exact integer '+name+' budget')

def _check_tree(x,*,max_nodes=200000,max_depth=64,max_atom_bits=1000000,max_string_chars=1000000,encoded=False):
    """Iterative finite expanded-tree admission; aliases are charged each visit.
    Cycles are refused. Exact built-in containers/atoms only. This limits logical
    work, not all Python heap overhead or trusted raw-constructor arithmetic.
    """
    _limits(max_nodes,max_depth,max_atom_bits,max_string_chars)
    stack=[(x,0,False)];active=set();nodes=0;scheduled=1
    while stack:
        value,depth,leaving=stack.pop()
        if leaving:active.remove(id(value));continue
        nodes+=1
        if nodes>max_nodes:raise BudgetRefusal('finite-tree node budget')
        if depth>max_depth:raise BudgetRefusal('finite-tree depth budget')
        typ=type(value)
        if typ is int:
            if abs(value).bit_length()>max_atom_bits:raise BudgetRefusal('integer atom bit budget')
        elif typ is F and not encoded:
            if max(value.numerator.bit_length(),value.denominator.bit_length())>max_atom_bits:raise BudgetRefusal('rational atom bit budget')
        elif typ is str:
            if len(value)>max_string_chars:raise BudgetRefusal('string character budget')
        elif typ is dict or typ is list or (typ is tuple and not encoded):
            if id(value) in active:raise Unsupported('cyclic receiving tree')
            children=2*len(value) if typ is dict else len(value)
            scheduled+=children
            if scheduled>max_nodes:raise BudgetRefusal('finite-tree expanded node budget')
            active.add(id(value));stack.append((value,depth,True))
            if typ is dict:
                for key,child in reversed(list(value.items())):
                    if type(key)is not str:raise Unsupported('exact string dictionary keys required')
                    stack.append((child,depth+1,False));stack.append((key,depth+1,False))
            else:
                for child in reversed(value):stack.append((child,depth+1,False))
        else:raise Unsupported('unsupported receiving atom or container type')
    return nodes

def _hex_integer(text,max_atom_bits):
    if type(text)is not str:raise Unsupported('exact hexadecimal string required')
    body=text[1:] if text.startswith('-') else text
    if not body.startswith('0x') or len(body)<=2 or any(c not in '0123456789abcdef' for c in body[2:]):
        raise Unsupported('canonical hexadecimal integer required')
    if len(body)-2>(max_atom_bits+3)//4:raise BudgetRefusal('hexadecimal atom bit budget')
    value=int(text,16)
    if abs(value).bit_length()>max_atom_bits:raise BudgetRefusal('hexadecimal atom bit budget')
    if hex(value)!=text:raise Unsupported('noncanonical hexadecimal integer')
    return value

def decode(x,*,max_nodes=200000,max_depth=64,max_atom_bits=1000000,max_string_chars=1000000):
    """Bounded wire-tree decoding; malformed values have controlled refusals."""
    _check_tree(x,max_nodes=max_nodes,max_depth=max_depth,max_atom_bits=max_atom_bits,max_string_chars=max_string_chars,encoded=True)
    def visit(value):
        if type(value)is list:return [visit(v) for v in value]
        if type(value)is dict:
            if 'QHEX' in value:
                if set(value)!={'QHEX'} or type(value['QHEX'])is not list or len(value['QHEX'])!=2:raise Unsupported('two-entry rational tag required')
                a,b=value['QHEX'];num=_hex_integer(a,max_atom_bits);den=_hex_integer(b,max_atom_bits)
                if den<=0:raise Unsupported('positive rational denominator required')
                out=F(num,den)
                if hex(out.numerator)!=a or hex(out.denominator)!=b:raise Unsupported('reduced canonical rational required')
                return out
            if 'ZHEX' in value:
                if set(value)!={'ZHEX'}:raise Unsupported('exclusive integer tag required')
                out=_hex_integer(value['ZHEX'],max_atom_bits)
                if abs(out).bit_length()<=4096:raise Unsupported('small integer must use canonical JSON decimal')
                return out
            return {k:visit(v) for k,v in value.items()}
        return value
    try:return visit(x)
    except (Unsupported,BudgetRefusal):raise
    except (RecursionError,MemoryError) as exc:raise BudgetRefusal('decoder runtime resource refusal') from exc
    except (ValueError,TypeError,KeyError,IndexError,ArithmeticError) as exc:raise Unsupported('malformed numeric wire tree') from exc

def _scan_json(payload,max_nodes,max_depth,max_string_chars):
    """Pre-parser lexical depth/token guard. JSON grammar remains json.loads'."""
    depth=0;tokens=0;quoted=False;escape=False;word=False;chars=0
    for c in payload:
        if quoted:
            if not escape and c==34:quoted=False;continue
            chars+=1
            if chars>max_string_chars:raise BudgetRefusal('wire string byte budget')
            if escape:escape=False
            elif c==92:escape=True
            continue
        if c==34:
            quoted=True;chars=0;word=False;tokens+=1
        elif c in (91,123):
            depth+=1;word=False;tokens+=1
            if depth>max_depth:raise BudgetRefusal('wire nesting budget')
        elif c in (93,125):
            depth-=1;word=False
            if depth<0:raise Unsupported('malformed JSON nesting')
        elif c in (9,10,13,32,44,58):word=False
        elif not word:word=True;tokens+=1
        if tokens>max_nodes:raise BudgetRefusal('wire token budget')
    if quoted or depth:raise Unsupported('incomplete JSON text')

def receive_wire(raw,payload,max_bytes=10000000,*,max_nodes=200000,max_depth=64,max_atom_bits=1000000,max_string_chars=1000000):
    if type(payload)is not bytes or type(max_bytes)is not int or max_bytes<0:raise Unsupported('bytes and nonnegative integer byte budget')
    _limits(max_nodes,max_depth,max_atom_bits,max_string_chars)
    if len(payload)>max_bytes:raise BudgetRefusal('wire byte budget')
    _scan_json(payload,max_nodes,max_depth,max_string_chars)
    def no_float(token):raise Unsupported('floating/nonfinite JSON number not admitted')
    def decimal(token):
        # Canonical large integers use hexadecimal tags, not Python's decimal
        # conversion-limit bypass. At most4096bits are legitimate here.
        if len(token.lstrip('-'))>1234:raise Unsupported('large JSON integer must use hexadecimal tag')
        out=int(token)
        if abs(out).bit_length()>min(4096,max_atom_bits):raise BudgetRefusal('decimal atom bit budget')
        return out
    def pairs(items):
        out={}
        for key,value in items:
            if key in out:raise Unsupported('duplicate JSON key')
            out[key]=value
        return out
    try:
        parsed=json.loads(payload,parse_float=no_float,parse_constant=no_float,parse_int=decimal,object_pairs_hook=pairs)
        claimed=decode(parsed,max_nodes=max_nodes,max_depth=max_depth,max_atom_bits=max_atom_bits,max_string_chars=max_string_chars)
        if canonical_bytes(claimed)!=payload:raise Unsupported('noncanonical wire')
        return receive(raw,claimed,max_nodes=max_nodes,max_depth=max_depth,max_atom_bits=max_atom_bits,max_string_chars=max_string_chars)
    except (Unsupported,BudgetRefusal):raise
    except (RecursionError,MemoryError) as exc:raise BudgetRefusal('wire runtime resource refusal') from exc
    except (ValueError,TypeError,KeyError,IndexError,ArithmeticError,UnicodeError) as exc:raise Unsupported('malformed JSON wire') from exc

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

def receive(raw,claimed,*,max_nodes=200000,max_depth=64,max_atom_bits=1000000,max_string_chars=1000000):
    _check_tree(claimed,max_nodes=max_nodes,max_depth=max_depth,max_atom_bits=max_atom_bits,max_string_chars=max_string_chars)
    expected=construct(raw)
    try:matches=canonical_bytes(expected)==canonical_bytes(claimed)
    except (RecursionError,MemoryError) as exc:raise BudgetRefusal('canonical receiving runtime resource refusal') from exc
    except (ValueError,TypeError,KeyError,IndexError,ArithmeticError) as exc:raise Unsupported('malformed canonical claim') from exc
    if not matches:raise Unsupported('canonical certificate mismatch')
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
    q=rat(q)
    if q<=0 or type(k)is not int:raise Unsupported('positive rational base and exact integer exponent required')
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
    out={'status':'FACTORED_RESOURCE_TAIL_RECIPE','max_count_upper':{'op':'min','args':[1,{'op':'mul','args':[F(4,3),{'op':'pow','base':p['t'],'exponent':-level},{'op':'add','args':[{'op':'mul','args':[p['Htot'],{'op':'pow','base':p['t'],'exponent':N0}]},{'op':'mul','args':[T,deepcopy(p['CF_expression'])]}]}]}]},'box_sha256':p['raw']['canonical_box_sha256']}
    if event_threshold is not None:
        integer_budget(event_threshold,'event threshold');r=p['raw'];rate=r['lam_hi']+r['mu_hi']*level+r['Srate_hi']*level**2
        out['event_count_upper']={'op':'min','args':[1,{'op':'add','args':[deepcopy(out['max_count_upper']),{'op':'POISSON_UPPER_TAIL','mean':rate*T,'threshold':event_threshold}]}]}
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

def receive_resource_budget(raw,claimed,*,initial_total_upper_bound,horizon,failure,max_nodes=200000,max_depth=64,max_atom_bits=1000000,max_string_chars=1000000):
    """Bind arithmetic receipt to a separately supplied CLIENT request.
    This does not certify the observation contract of its count upper bound.
    Same-author checking, not an independent implementation.
    """
    if type(claimed)is not dict:raise Unsupported('budget dictionary required')
    _check_tree(claimed,max_nodes=max_nodes,max_depth=max_depth,max_atom_bits=max_atom_bits,max_string_chars=max_string_chars)
    try:expected=resource_budget(construct(raw),initial_total_upper_bound,horizon,failure)
    except (Unsupported,BudgetRefusal):raise
    except (ValueError,TypeError,KeyError,IndexError,ArithmeticError) as exc:raise Unsupported('malformed external resource request') from exc
    try:matches=canonical_bytes(expected)==canonical_bytes(claimed)
    except (RecursionError,MemoryError) as exc:raise BudgetRefusal('resource receiving runtime resource refusal') from exc
    except (ValueError,TypeError,KeyError,IndexError,ArithmeticError) as exc:raise Unsupported('malformed resource claim') from exc
    if not matches:raise Unsupported('resource budget or external request mismatch')
    return {'status':'SAME_AUTHOR_EXTERNALLY_BOUND_RESOURCE_BUDGET_RECEIVED','budget_sha256':digest(expected),'box_sha256':expected['box_sha256']}

class RiskLedger:
    """Trusted model-level predictable episode allocation; no reset/independence.
    Only admitted episodes inherit the familywise conditional union guarantee.
    Public properties/snapshots are immutable; single-owner sequential API.
    Private-state introspection attacks and unsynchronized concurrent calls are
    outside this ordinary in-process contract.
    """
    __slots__=('_total','_spent','_allocations')
    def __init__(self,total):
        total=rat(total)
        if not 0<total<1:raise ValueError('total failure budget in (0,1)')
        self._total=total;self._spent=F(0);self._allocations=()
    @property
    def total(self):return self._total
    @property
    def spent(self):return self._spent
    @property
    def allocations(self):return self._allocations
    def reserve(self,requested):
        try:
            a=rat(requested)
            if not 0<a<1 or self.spent+a>self.total:raise Unsupported('episode risk budget')
        except (Unsupported,TypeError,ValueError):
            return {'status':'REJECT_NO_ALLOCATION','spent':self.spent,'remaining':self.total-self.spent}
        new_allocations=self._allocations+(a,)
        new_spent=self._spent+a
        self._allocations=new_allocations;self._spent=new_spent
        return {'status':'ADMIT_EPISODE_RISK','episode':len(self.allocations)-1,'failure':a,'spent':self.spent,'remaining':self.total-self.spent}
