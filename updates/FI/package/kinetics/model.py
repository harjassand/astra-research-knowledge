"""Energy acquisition and factor compiler for a declared pairwise heat-bath law."""
from fractions import Fraction as F
from math import isqrt,lcm
from itertools import product
import numpy as np
from scipy.linalg import eigh
from tt_ops import product as ttproduct,add,rounded


def fpow2(k):return F(2**k) if k>=0 else F(1,2**(-k))
def fsqrt(x):
    a,b=isqrt(x.numerator),isqrt(x.denominator)
    if a*a!=x.numerator or b*b!=x.denominator:raise ValueError('Nonrational pair factor')
    return F(a,b)
def ffmat(a):return np.array(a,dtype=object)
def zeros(q):return np.full((q,q),F(0),dtype=object)
def eye(q):
    A=zeros(q)
    for j in range(q):A[j,j]=F(1)
    return A

def fixture(B=3,m=4,rarity=1,cross=F(3,2),seed=71,field_scale=1,clock_scale=1):
    """Authored disordered modular gate, not an independently selected molecule."""
    rng=np.random.default_rng(seed);n=B*m;edges={};fields=[];nus=[]
    for b in range(B):
        # Disordered cycle plus chords; external field and site clocks break closure.
        local=set(tuple(sorted((i,(i+1)%m))) for i in range(m))
        if m>=4:local.add((0,m//2))
        if m>=6:local.add((1,m-2))
        for i,j in sorted(local):edges[(b*m+i,b*m+j)]=fpow2(rarity*int(rng.integers(2,5)))
        # One weak frustrated internal bond, not a homogeneous ferromagnetic ring.
        if b==1 and m>=4:edges[(b*m+1,b*m+2)]=fpow2(-rarity)
        for i in range(m):
            fields.append(fpow2(field_scale*int(rng.integers(-1,2))))
            nus.append(fpow2(int(rng.integers(-1,2)))*F(clock_scale))
    for b in range(B-1):edges[(b*m,(b+1)*m)]=F(cross)
    # Relabel all non-target coordinates; target remains coordinate zero.
    perm=np.concatenate(([0],rng.permutation(np.arange(1,n))))
    ee={tuple(sorted((int(perm[i]),int(perm[j])))):v for (i,j),v in edges.items()}
    ff=[None]*n;nn=[None]*n
    for i in range(n):ff[int(perm[i])]=fields[i];nn[int(perm[i])]=nus[i]
    return {'n':n,'edges':ee,'fields':ff,'nu':nn,'kappa':F(1),'target':0,'metadata':dict(B=B,m=m,rarity=rarity,cross=str(cross),seed=seed,field_scale=field_scale,clock_scale=str(clock_scale))}

def weight(truth,x):
    v=F(1)
    for i,h in enumerate(truth['fields']):
        if (x>>i)&1:v*=h
    for (i,j),t in truth['edges'].items():
        if ((x>>i)&1)==((x>>j)&1):v*=t
    return v

def acquire(truth):
    n=truth['n'];answers={};clocks={}
    def query(x):
        y=weight(truth,x);answers[x]=str(y);return y
    w0=query(0);single=[query(1<<i) for i in range(n)];edges={}
    for i in range(n):
        for j in range(i+1,n):
            t=fsqrt(query((1<<i)|(1<<j))*w0/(single[i]*single[j]))
            if t!=1:edges[(i,j)]=t
    fields=[]
    for i in range(n):
        h=single[i]/w0
        for (j,k),t in edges.items():
            if i==j or i==k:h*=t
        fields.append(h)
    # Synthetic exact answer under energy-equalizing intervention, not a laboratory result.
    nu=[];baseline_rates=[]
    for i in range(n):
        rate=(truth['clock_tables'][i][0] if 'clock_tables' in truth else truth['nu'][i])/2
        clocks[i]=str(rate);baseline_rates.append(rate);nu.append(2*rate)
    learned={'n':n,'edges':edges,'fields':fields,'nu':nu,'kappa':truth['kappa'],'target':truth['target']}
    if 'clock_tables' in truth:
        learned['clock_contexts']={};learned['clock_tables']={}
        clocks={}
        for i in range(n):
            ctx=sorted(j if i==a else a for a,j in edges if i==a or i==j)
            learned['clock_contexts'][i]=ctx;learned['clock_tables'][i]=[]
            assert ctx==truth['clock_contexts'][i]
            for z,aa in enumerate(truth['clock_tables'][i]):
                rate=baseline_rates[i] if z==0 else aa/2
                clocks[f'{i}:{z}']=str(rate);learned['clock_tables'][i].append(2*rate)
    assert edges==truth['edges'] and fields==truth['fields'] and nu==truth['nu']
    return learned,{'energy_queries':len(answers),'balanced_clock_queries':len(clocks),'weights':answers,'balanced_rates':clocks,'scope':'exact synthetic coefficient acquisition under declared pairwise and intervention-invariant heat-bath law'}

def partition(model,threshold=F(2)):
    n=model['n'];parent=list(range(n))
    def root(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    for (i,j),v in model['edges'].items():
        if max(v,1/v)>=threshold:
            parent[root(i)]=root(j)
    groups={}
    for i in range(n):groups.setdefault(root(i),[]).append(i)
    out=sorted(groups.values(),key=lambda a:(0 not in a,min(a)))
    return out

class Compiler:
    def __init__(self,model,groups):
        self.model=model;self.groups=groups;self.B=len(groups)
        if self.B<2:raise ValueError('No nontrivial factorization at this threshold')
        self.loc={x:(b,i) for b,g in enumerate(groups) for i,x in enumerate(g)}
        self.cross=[];self.internal=[[] for _ in groups]
        for (i,j),v in model['edges'].items():
            b,s=self.loc[i];c,t=self.loc[j]
            if b==c:self.internal[b].append((s,t,v))
            else:self.cross.append((b,s,c,t,v))
        self.R=F(1)
        for *_,v in self.cross:self.R*=max(v,1/v)
        self.bits=[];self.mass=[];self.prob=[];self.rootprob=[];self.refraw=[];self.refsym=[]
        for b,g in enumerate(groups):
            q=1<<len(g);bits=np.array([[(a>>i)&1 for i in range(len(g))] for a in range(q)],int);self.bits.append(bits)
            mass=[]
            for a in range(q):
                v=F(1)
                for s,i in enumerate(g):
                    if bits[a,s]:v*=model['fields'][i]
                for s,t,h in self.internal[b]:
                    if bits[a,s]==bits[a,t]:v*=h
                mass.append(v)
            den=lcm(*(v.denominator for v in mass));mi=[int(v*den) for v in mass];self.mass.append(mi)
            p=[F(v,sum(mi)) for v in mi];self.prob.append(p);rp=np.sqrt(np.array(p,float));self.rootprob.append(rp)
            C=self.local_weighted(b,[F(1)]*q)
            if model['target'] in g:
                ti=g.index(model['target'])
                for a in range(q):C[a,a]+=model['kappa']*int(bits[a,ti])
            self.refraw.append(C);self.refsym.append(rp[:,None]*np.array(C,float)/rp[None,:])
        self.R_mass=self.R;self.R_clock=F(1)
        if 'clock_tables' in model:
            for b,g in enumerate(groups):
                for ss,i in enumerate(g):
                    for a in range(len(self.bits[b])):
                        amin=self.clock_value(b,a,ss,None)
                        for z,val in enumerate(model['clock_tables'][i]):
                            if all(((z>>j)&1)==self.bits[b][a,self.loc[node][1]] for j,node in enumerate(model['clock_contexts'][i]) if self.loc[node][0]==b):self.R_clock=max(self.R_clock,val/amin)
        self.R*=self.R_clock
        self.rawterms=self.make_terms();self.terms=[]
        for term in self.rawterms:self.terms.append([p[:,None]*np.array(M,float)/p[None,:] for M,p in zip(term,self.rootprob)])
        self.wterms=self.cross_terms(range(len(self.cross)))
        self.source=None
        for vs in self.wterms:
            z=ttproduct([np.array(v,float)*p for v,p in zip(vs,self.rootprob)])
            self.source=z if self.source is None else add(self.source,z)
        self.source=rounded(self.source,64,1e-15)
        self.Z=sum(self.prod_expect(vs) for vs in self.wterms)
        self.evals=[];self.evecs=[]
        for b,C in enumerate(self.refsym):
            lam,U=eigh((C+C.T)/2)
            if model['target'] not in groups[b]:lam[0]=0.0
            if lam.min()<-1e-8:raise ValueError('Invalid reference eigenvalues')
            self.evals.append(np.maximum(lam,0));self.evecs.append(U)
    def prod_expect(self,vs):
        v=F(1)
        for p,f in zip(self.prob,vs):v*=sum(a*b for a,b in zip(p,f))
        return v
    def clock_value(self,b,a,s,outside):
        i=self.groups[b][s]
        if 'clock_tables' not in self.model:return self.model['nu'][i]
        ctx=self.model['clock_contexts'][i];tab=self.model['clock_tables'][i]
        if outside is None:
            vals=[val for z,val in enumerate(tab) if all(((z>>j)&1)==self.bits[b][a,self.loc[node][1]] for j,node in enumerate(ctx) if self.loc[node][0]==b)]
            return min(vals)
        z=0
        for j,node in enumerate(ctx):
            c,t=self.loc[node];bit=int(self.bits[b][a,t]) if c==b else outside[(c,t)];z|=bit<<j
        return tab[z]
    def local_weighted(self,b,d,outside=None):
        q=len(self.bits[b]);M=zeros(q);g=self.groups[b];mass=self.mass[b]
        for a in range(q):
            for s,i in enumerate(g):
                ap=a^(1<<s);rate=self.clock_value(b,a,s,outside)*mass[ap]*d[ap]/(mass[a]*d[a]+mass[ap]*d[ap]);z=d[a]*rate;M[a,a]+=z;M[a,ap]-=z
        return M
    def cross_terms(self,ids):
        terms=[[np.full(len(bits),F(1),dtype=object) for bits in self.bits]]
        for e in ids:
            b,s,c,t,v=self.cross[e];a=(1+v)/(2*min(F(1),v));h=(v-1)/(2*min(F(1),v));new=[]
            for vs in terms:
                vv=[x.copy() for x in vs];vv[b]*=a;new.append(vv)
                vv=[x.copy() for x in vs];vv[b]*=h*(2*self.bits[b][:,s]-1);vv[c]*=2*self.bits[c][:,t]-1;new.append(vv)
            terms=new
        return terms
    def make_terms(self):
        out=[]
        for b in range(self.B):
            inc=[i for i,e in enumerate(self.cross) if b==e[0] or b==e[2]];rest=[i for i in range(len(self.cross)) if i not in inc]
            nb=set((e[2],e[3]) if e[0]==b else (e[0],e[1]) for i in inc for e in [self.cross[i]])
            # Kinetic dependence can cross a block even without an energy bond.
            for i in self.groups[b]:
                for node in self.model.get('clock_contexts',{}).get(i,[]):
                    if self.loc[node][0]!=b:nb.add(self.loc[node])
            nb=sorted(nb)
            for z in product((0,1),repeat=len(nb)):
                zz=dict(zip(nb,z));d=[F(1)]*len(self.bits[b]);projs=[np.ones(len(bits),dtype=object) for bits in self.bits]
                for (c,t),a in zz.items():projs[c]*=(self.bits[c][:,t]==a).astype(int)
                for i in inc:
                    bb,s,c,t,v=self.cross[i]
                    if bb!=b:bb,s,c,t=c,t,bb,s
                    for a in range(len(d)):d[a]*=(v if self.bits[b][a,s]==zz[(c,t)] else F(1))/min(F(1),v)
                M=self.local_weighted(b,d,zz)
                for vs in self.cross_terms(rest):
                    term=[np.diag(v*p) for v,p in zip(vs,projs)];term[b]=M.copy();out.append(term)
        tb,ts=self.loc[self.model['target']]
        for vs in self.cross_terms(range(len(self.cross))):
            term=[np.diag(v) for v in vs];term[tb]*=self.model['kappa'];term[tb]=np.diag(self.bits[tb][:,ts])@term[tb];out.append(term)
        return out

def discover_partition(model,max_local_bits=6):
    """Search thresholds of acquired bond contrasts; never expand an oversized block.
    The score is a transparent heuristic, not a globally optimal partition theorem.
    """
    import math
    values=sorted(set(max(v,1/v) for v in model['edges'].values()))
    thresholds=values+[max(values)*2] if values else [F(2)]
    candidates=[]
    for threshold in thresholds:
        gs=partition(model,threshold)
        if len(gs)<2 or max(map(len,gs))>max_local_bits:continue
        loc={i:b for b,g in enumerate(gs) for i in g};cross=[v for (i,j),v in model['edges'].items() if loc[i]!=loc[j]]
        R=F(1)
        for v in cross:R*=max(v,1/v)
        score=math.log(sum(2**(3*len(g)) for g in gs))+math.log(float(R))+len(cross)*math.log(2)
        candidates.append({'threshold':str(threshold),'groups':gs,'R':str(R),'cross_edges':len(cross),'heuristic_log_cost':score})
    if not candidates:raise ValueError('No admitted small-block factorization')
    best=min(candidates,key=lambda r:r['heuristic_log_cost'])
    return best['groups'],{'selected':best,'candidates':candidates,'scope':'energy-derived heuristic; not an optimal separator search'}


def add_context_clock(truth,slow=F(1,100)):
    """Same energies and all-zero-context clocks; hidden mobility differs on mixed contacts.
    Full context tables are disclosed ONLY through the balancing-query interface.
    """
    truth={**truth};truth['clock_contexts']={};truth['clock_tables']={}
    for i in range(truth['n']):
        nei=sorted(j if i==a else a for a,j in truth['edges'] if i==a or i==j)
        strong=[j for j,node in enumerate(nei) if max(truth['edges'][tuple(sorted((i,node)))],1/truth['edges'][tuple(sorted((i,node)))])>=2]
        tab=[]
        for z in range(1<<len(nei)):
            bb=[(z>>j)&1 for j in strong];mixed=bool(bb) and min(bb)!=max(bb)
            tab.append(truth['nu'][i]*(slow if mixed else F(1)))
        truth['clock_contexts'][i]=nei;truth['clock_tables'][i]=tab
    truth['metadata']={**truth['metadata'],'mixed_contact_clock_factor':str(slow)}
    return truth


def from_transcript(n,trans,target=0,kappa=F(1)):
    if trans.get('clock_interface')=='unknown-support-degree-two-reverse':
        from reverse_tomography import recover_reverse
        return recover_reverse(n,trans,target,kappa)[0]
    if trans.get('clock_interface')=='unknown-support-degree-two':
        from kinetic_tomography import recover
        return recover(n,trans['weights'],trans['balanced_rates'],target,kappa)[0]
    data={int(k):F(v) for k,v in trans['weights'].items()};w0=data[0];ss=[data[1<<i] for i in range(n)];edges={}
    for i in range(n):
        for j in range(i+1,n):
            t=fsqrt(data[(1<<i)|(1<<j)]*w0/(ss[i]*ss[j]))
            if t!=1:edges[(i,j)]=t
    fields=[]
    for i in range(n):
        h=ss[i]/w0
        for (a,b),t in edges.items():
            if i==a or i==b:h*=t
        fields.append(h)
    cr=trans['balanced_rates'];context=any(':' in str(k) for k in cr)
    nu=[2*F(cr[f'{i}:0'] if context else cr[str(i)]) for i in range(n)]
    out=dict(n=n,edges=edges,fields=fields,nu=nu,target=target,kappa=kappa)
    if context:
        out['clock_contexts']={};out['clock_tables']={}
        for i in range(n):
            ctx=sorted(j if i==a else a for a,j in edges if i==a or i==j);out['clock_contexts'][i]=ctx
            out['clock_tables'][i]=[2*F(cr[f'{i}:{z}']) for z in range(1<<len(ctx))]
    return out
