"""Raw acquisition of the shared-port, one-mode-module composition theorem."""
from fractions import Fraction as F
from math import prod
from rank_one_modules import construct as one_mode, rational, ceil, fall


def _acquire(reactions,x0,lam=1,mu=1):
    x0=tuple(x0);n=len(x0);lam,mu=rational(lam),rational(mu)
    if not n or any(type(x) is not int or x<0 for x in x0):raise ValueError('Invalid counts.')
    raw=[]
    for y,z,kappa in reactions:
        y,z=tuple(y),tuple(z)
        if len(y)!=n or len(z)!=n or any(type(x) is not int or x<0 for x in y+z):raise ValueError('Invalid complex.')
        kappa=rational(kappa)
        if y!=z:raw.append((y,z,kappa))
    dynamic={i for i in range(1,n) if any(y[i]!=z[i] for y,z,k in raw)}
    fixed=set(range(1,n))-dynamic
    graph={i:{i} for i in dynamic}
    for y,z,k in raw:
        touched={i for i in dynamic if y[i] or z[i]}
        if not touched:raise ValueError('A nonzero conservative reaction must use a nonport dynamic species.')
        for i in touched:graph[i]|=touched
    left=set(dynamic);blocks=[]
    while left:
        seed=min(left);seen={seed};todo=[seed]
        while todo:
            for i in graph[todo.pop()]:
                if i not in seen:seen.add(i);todo.append(i)
        left-=seen;blocks.append(sorted(seen))
    if not blocks:return dict(kind='bounded',raw=raw,x0=x0,lam=lam,mu=mu,blocks=[],t=F(2),head=ceil((lam+1)/(mu/2))+1,nu=F(1))
    assembled=[]
    for block in blocks:
        indices=[0]+block+sorted(fixed)
        local=[]
        for y,z,k in raw:
            if any(y[i]!=z[i] for i in block):
                if any((y[i] or z[i]) for i in dynamic-set(block)):raise ValueError('Cross-module dependence.')
                local.append((tuple(y[i] for i in indices),tuple(z[i] for i in indices),k))
        cert=one_mode(local,tuple(x0[i] for i in indices),lam,mu)
        assembled.append(dict(indices=indices,reactions=local,cert=cert))
    live=[b for b in assembled if b['cert']['kind']=='rank_one_profile']
    bounded=[b for b in assembled if b['cert']['kind']!='rank_one_profile']
    if not live:
        span=sum(abs(b['cert']['v'][0])*(b['cert']['outside_high']-b['cert']['outside_low'])
                 for b in bounded if b['cert']['kind']=='bounded_outside')
        acut=ceil((lam+1)/(mu/2))
        return dict(kind='bounded',raw=raw,x0=x0,lam=lam,mu=mu,blocks=assembled,t=F(2),head=acut+span+1,nu=F(1))
    p=max([b['cert']['p'] for b in live]+[y[0] for b in bounded for y,z,k in b['reactions']]+[1])
    jumpmax=max(abs(z[0]-y[0]) for y,z,k in raw);shift=jumpmax+1
    big=F(p*jumpmax)*shift**(p+1)
    for b in live:
        b['cert']=one_mode(b['reactions'],tuple(x0[i] for i in b['indices']),lam,mu,p,shift)
    cost=sum((b['cert']['C'] for b in live),F(0))
    # Bounded modes retain their entire acquired coordinate interval.
    for b in bounded:
        c=b['cert'];bounds=list(c['x0'])
        if c['kind']=='bounded_outside':
            for i in range(1,len(bounds)):
                bounds[i]=max(c['x0'][i]+c['v'][i]*c['outside_low'],c['x0'][i]+c['v'][i]*c['outside_high'])
        b['outside_bounds']=bounds
        cost+=big*mu
        for y,z,k in b['reactions']:
            if z[0]<y[0]:cost+=big*k*prod(bounds[i]**y[i] for i in range(1,len(y)))
    minimum=max(min(g['m'] for g in b['cert']['groups']) for b in live)

    def bounded_down(b,a,weight):
        c=b['cert'];total=F(0)
        for y,z,k in b['reactions']:
            if z[0]<y[0] and a>=y[0]:
                total+=weight(a,z[0]-y[0])*k*fall(a,y[0])*prod(b['outside_bounds'][i]**y[i] for i in range(1,len(y)))
        return total

    def domination_cost(b,a,weight,factor):
        """cost <= factor*sum selected rates + returned constant, for every q."""
        c=b['cert'];result=F(0)
        for g in c['groups']:
            if a<g['m']:continue
            ratio=F(0)
            for y,z,kappa in g['bad']:
                if a<y[0]:continue
                kk=(y[0]-g['m'])//c['r']
                cc=kappa/g['selected'][2]*2**g['b']*prod((c['offset'][i]+c['v'][i])**y[i] for i in range(1,len(y)) if c['v'][i]>0)
                ratio+=weight(a,z[0]-y[0])*cc*(a+shift)**(c['r']*kk)
            threshold=max(c['Z0'],1+ceil(ratio/factor))
            for y,z,kappa in g['bad']:
                if a<y[0]:continue
                upper=kappa*fall(a,y[0])*prod((c['offset'][i]+c['v'][i]*threshold)**y[i]
                                             if c['v'][i]>0 else fall(c['x0'][i],y[i]) for i in range(1,len(y)))
                result+=weight(a,z[0]-y[0])*upper
        return result

    differences=[]
    for a in range(minimum):
        def old_weight(aa,jump):return sum(differences[aa+jump:aa],F(0))
        bound=mu*a*(differences[a-1] if a else 0)
        for b in live:bound+=domination_cost(b,a,old_weight,F(1))
        for b in bounded:bound+=bounded_down(b,a,old_weight)
        differences.append(max(F(1),(1+bound)/lam))
    heads=[sum(differences[a:],F(0)) for a in range(minimum)]+[F(0)]
    gmax=F(1,shift**p);ee=mu*gmax/(2*(cost+1))+2*lam*heads[0]
    eta=min(F(1,2),F(1,4)/(ee+1));t=1+eta;death=mu*(1-1/t)
    epsilon=death/(2*(cost+1));delta=2*lam*eta
    assert 1+epsilon*gmax+delta*heads[0]<=F(3,2)
    entry=F(0)
    for a in range(minimum,minimum+jumpmax):
        def entry_weight(aa,jump):
            dest=aa+jump
            return heads[dest] if 0<=dest<minimum else F(0)
        for b in live:
            # Each linkage gets its own exact allowance c_l/(a+s)^(p+1).
            c=b['cert']
            for group in c['groups']:
                tmp=dict(b);tmpcert=dict(c);tmpcert['groups']=[group];tmp['cert']=tmpcert
                factor=epsilon*group['c']/(2*delta*(a+shift)**(p+1))
                entry+=delta*domination_cost(tmp,a,entry_weight,factor)
        for b in bounded:entry+=delta*bounded_down(b,a,entry_weight)
    if minimum:entry+=delta*mu*minimum*heads[minimum-1]
    acut=max(minimum+jumpmax,ceil(4*lam*eta/death),1)
    denominator=(acut-1+shift)**(p+1)
    for b in live:
        c=b['cert'];g=min(c['groups'],key=lambda x:x['m']);y,z,k=g['selected']
        coefficient=g['c']*k*g['catalyst']*F(fall(minimum,g['m']),2**g['b'])
        assert coefficient>0
        qcut=max(c['Z0'],1)
        while epsilon*coefficient*(qcut+1)**g['b']<2*(entry+2*lam*eta)*denominator:qcut*=2
        b['qcut']=qcut
    span=sum(abs(b['cert']['v'][0])*(b['cert']['outside_high']-b['cert']['outside_low'])
             for b in bounded if b['cert']['kind']=='bounded_outside')
    head=acut+sum(b['cert']['r']*b['qcut'] for b in live)+span+1
    return dict(kind='shared_profile',raw=raw,x0=x0,lam=lam,mu=mu,blocks=assembled,
                live=live,bounded=bounded,p=p,shift=shift,B=big,C=cost,M=minimum,
                head_values=heads,eta=eta,t=t,epsilon=epsilon,delta=delta,E=entry,
                Acut=acut,head=head,nu=lam*eta/2,zeta=lam*eta/3)


def acquire(reactions,x0,lam=1,mu=1):
    cert=_acquire(reactions,x0,lam,mu)
    bounds=list(cert['x0']);offset_bounds=list(cert['x0']);bounds[0]=cert['head'];slope=1
    for b in cert['blocks']:
        c=b['cert']
        if c['kind']=='rank_one_profile':
            slope=max(slope,ceil(F(c['s'],c['r'])))
            for j,index in enumerate(b['indices'][1:],1):
                if c['v'][j]>0:
                    bounds[index]=c['offset'][j]+c['v'][j]*cert['head']
                    offset_bounds[index]=c['offset'][j]
        elif c['kind']=='bounded_outside':
            for j,index in enumerate(b['indices'][1:],1):
                bounds[index]=max(c['x0'][j]+c['v'][j]*c['outside_low'],c['x0'][j]+c['v'][j]*c['outside_high'])
                offset_bounds[index]=bounds[index]
    offset=sum(offset_bounds[1:]);rho=1+(cert['t']-1)/2**slope
    assert rho**slope<=cert['t']
    rate=cert['lam']+cert['mu']*cert['head']
    for y,z,k in cert['raw']:rate+=k*prod(xx**yy for xx,yy in zip(bounds,y))
    hbar=F(3,2) if cert['kind']=='shared_profile' else F(1)
    zeta=cert.get('zeta',cert['nu']);coef=hbar*(zeta+rate)
    cert.update(zeta=zeta,count_offset=offset,count_slope=slope,rho=rho,
                head_count_bounds=tuple(bounds),head_rate_bound=rate,
                head_drift_bound=dict(coefficient=coef,base=cert['t'],exponent=cert['head']+1),
                stationary_total_moment_bound=dict(coefficient=coef/zeta,
                     powers=[(rho,offset),(cert['t'],cert['head']+1)]))
    return cert


def make_state(cert,a,coordinates):
    x=list(cert['x0']);x[0]=a
    for b,q in zip(cert['blocks'],coordinates):
        c=b['cert']
        if c['kind']=='rank_one_profile':
            vals=[c['offset'][i]+c['v'][i]*q for i in range(1,len(c['v']))]
        elif c['kind']=='bounded_outside':
            zz=c['outside_low']+q
            vals=[c['x0'][i]+c['v'][i]*zz for i in range(1,len(c['v']))]
        else:vals=list(c['x0'][1:])
        for i,value in zip(b['indices'][1:],vals):x[i]=value
    return tuple(x)


def norm(cert,a,coordinates):
    value=a
    for b,q in zip(cert['blocks'],coordinates):
        c=b['cert']
        if c['kind']=='rank_one_profile':value+=c['r']*q
        elif c['kind']=='bounded_outside':
            va=c['v'][0];width=c['outside_high']-c['outside_low']
            value+=-va*q+max(va,0)*width
    return value


def parts(cert,a):
    g=F(1,(a+cert['shift'])**cert['p'])
    hh=cert['head_values'][a] if a<cert['M'] else F(0)
    return g,hh,1+cert['epsilon']*g+cert['delta']*hh


def actual_check(cert,a,coordinates):
    x=make_state(cert,a,coordinates);gg,hh,h=parts(cert,a);t=cert['t']
    lg=cert['lam']*(parts(cert,a+1)[0]-gg);lh=cert['lam']*(parts(cert,a+1)[1]-hh)
    tilted=cert['lam']*(t*parts(cert,a+1)[2]-h)
    if a:
        g1,h1,v1=parts(cert,a-1)
        lg+=cert['mu']*a*(g1-gg);lh+=cert['mu']*a*(h1-hh);tilted+=cert['mu']*a*(v1/t-h)
    for y,z,k in cert['raw']:
        rate=k*prod(fall(xx,yy) for xx,yy in zip(x,y))
        if rate:
            ga,ha,va=parts(cert,a+z[0]-y[0])
            lg+=rate*(ga-gg);lh+=rate*(ha-hh);tilted+=rate*(va-h)
    service=F(0)
    for b,q in zip(cert['blocks'],coordinates):
        c=b['cert']
        if c['kind']=='rank_one_profile' and q>=c['Z0']:
            xx=(a,)+tuple(x[i] for i in b['indices'][1:])
            for group in c['groups']:
                y,z,k=group['selected']
                service+=group['c']*k*prod(fall(zz,yy) for zz,yy in zip(xx,y))/(a+cert['shift'])**(cert['p']+1)
    assert lg<=-service+cert['C']*a
    if a<cert['M']:assert lh<=-1
    else:assert cert['delta']*lh<=cert['epsilon']*service/2+cert['E']*int(a<cert['M']+cert['shift']-1)
    assert 1<=h<=F(3,2)
    if norm(cert,a,coordinates)>=cert['head']:assert tilted<=-cert['nu']
    return tilted
