from pathlib import Path
import numpy as np
import math,json,itertools

# Independent 2-block construction with a genuinely interacting count energy.
# Not copied from the principal's single-block diagnostic.
blocks=[(0,1,2),(3,4,5)]
N=6
states=list(itertools.product([0,1],repeat=N))
lookup={x:i for i,x in enumerate(states)}
keys=list(itertools.product(range(4),repeat=2))
key_index={k:i for i,k in enumerate(keys)}
which=np.array([key_index[tuple(sum(x[i] for i in V) for V in blocks)] for x in states])
fibers=[np.flatnonzero(which==j) for j in range(len(keys))]
G=np.zeros((64,16)); H=np.zeros((64,16)); R=np.zeros((16,64))
for j,inds in enumerate(fibers):
    G[inds,j]=1/math.sqrt(len(inds)); H[inds,j]=1/len(inds); R[j,inds]=1
P=G@G.T; Q=np.eye(64)-P
neighbors={i:tuple(j for j in V if j!=i) for V in blocks for i in V}
types=[0,1,0,1,0,1]
b=np.array([[.7,1.2,.9,1.8],[1.4,.8,1.7,1.1]])


def energy(k,h):
    # Both nonconvex single-block and nonzero cross-block interaction.
    s1=2*k[0]-3; s2=2*k[1]-3
    return -.12*(s1*s1+s2*s2)-.09*s1*s2-h*(s1-s2)

def setup(h,drive,kappa):
    E=np.array([energy(keys[j],h) for j in which])
    p=np.exp(-E-E.max()); p/=sum(p)
    pb=np.array([sum(p[inds]) for inds in fibers])
    A=np.zeros((64,64)); F=np.zeros((64,64)); B=np.zeros((64,64))
    exitmax=0
    avals=[]
    Jmax=0
    for row,x in enumerate(states):
        for V in blocks:
            for ia in range(len(V)):
                for ib in range(ia+1,len(V)):
                    i,j=V[ia],V[ib]
                    if x[i]!=x[j]:
                        y=list(x);y[i],y[j]=y[j],y[i]; col=lookup[tuple(y)]
                        F[row,col]-=kappa;F[row,row]+=kappa
        for i in range(N):
            pattern=2*x[neighbors[i][0]]+x[neighbors[i][1]]
            a=1+drive*(.13*(pattern-1.5)+.07*types[i])
            avals.append(a)
            y=list(x); y[i]=1-y[i]; col=lookup[tuple(y)]
            dE=E[col]-E[row]; Jmax=max(Jmax,abs(dE))
            rate=b[types[i],pattern]*a*math.exp(-dE/2)
            B[row,col]-=rate;B[row,row]+=rate
        exitmax=max(exitmax,B[row,row])
    A=F+B
    sqrtp=np.sqrt(p)
    Bs=sqrtp[:,None]*B/sqrtp[None,:]
    As=sqrtp[:,None]*A/sqrtp[None,:]
    assert np.max(abs(Bs-Bs.T))<1e-12
    assert np.max(abs(As-As.T))<1e-12
    A0=G.T@Bs@G
    C=P@Bs@P+Q@As@Q
    Bbar=R@B.T@H
    assert np.max(abs(Bbar.sum(axis=0)))<1e-12
    # Generator columns for macro probabilities; compare exact uniform averages.
    Ebar=R@np.diag(p)@B@R.T
    assert np.max(abs(Ebar-Ebar.T))<1e-12
    def pinvhalf(M):
        vals,vecs=np.linalg.eigh((M+M.T)/2)
        cutoff=1e-10*max(1,float(max(abs(vals))))
        inv=np.zeros_like(vals); inv[vals>cutoff]=vals[vals>cutoff]**-.5
        return (vecs*inv)@vecs.T
    A0is=pinvhalf(A0)
    cc_actual=float(np.linalg.norm(Q@Bs@G@A0is,2)**2)
    A11is=pinvhalf(Q@As@Q)
    d_actual=float(np.linalg.norm(A11is@Q@Bs@G@A0is,2))
    bpmax=float(np.max(b)*max(avals)); bpmin=float(np.min(b)*min(avals))
    CE=math.exp(Jmax/2); Ls=2*(2+1)*bpmax
    cc_bound=2*CE*Ls**2/bpmin
    gamma=3*kappa
    assert cc_actual<=cc_bound+1e-10
    assert d_actual<=math.sqrt(cc_bound/gamma)+1e-9
    assert np.max(abs(G.T@As@G-A0))<1e-10
    # Independent hypergeometric mean-rate construction for each type/site.
    max_hyper=0.
    def fall(a,n):
        if a<0 or n>a: return 0
        v=1
        for t in range(n):v*=a-t
        return v
    for j,k in enumerate(keys):
        for r,V in enumerate(blocks):
            kr=k[r];m=3
            for sign in [+1,-1]:
                if not 0<=kr+sign<=m:continue
                k2=list(k);k2[r]+=sign; j2=key_index[tuple(k2)]
                rate=0.
                for i in V:
                    for alpha in itertools.product([0,1],repeat=2):
                        ones=sum(alpha);pattern=2*alpha[0]+alpha[1]
                        if sign==1:
                            prob=fall(kr,ones)*fall(m-kr-1,2-ones)/fall(m-1,2)
                            central=(m-kr)/m
                        else:
                            prob=fall(kr-1,ones)*fall(m-kr,2-ones)/fall(m-1,2)
                            central=kr/m
                        a=1+drive*(.13*(pattern-1.5)+.07*types[i])
                        rate+=central*prob*b[types[i],pattern]*a*math.exp(-(energy(tuple(k2),h)-energy(k,h))/2)
                max_hyper=max(max_hyper,abs(rate+Bbar[j2,j]))
    assert max_hyper<1e-12
    return {'p':p,'pb':pb,'A':A,'As':As,'C':C,'Bbar':Bbar,'cc_actual':cc_actual,'cc_bound':cc_bound,'d_actual':d_actual,'d_bound':math.sqrt(cc_bound/gamma),'max_hyper_error':max_hyper,'J':Jmax}

def exp_sym(M,t):
    vals,vecs=np.linalg.eigh((M+M.T)/2)
    return (vecs*np.exp(-vals*t))@vecs.T

def evolve_probability(q,model,t,kind):
    if kind=='true':
        sp=np.sqrt(model['p']);return sp*(exp_sym(model['As'],t)@(q/sp))
    if kind=='coarse':
        qmacro=R@q
        sp=np.sqrt(model['pb'])
        # Positive weighted macro generator; Bbar is already column convention.
        M=model['Bbar']*sp[None,:]/sp[:,None]
        assert np.max(abs(M-M.T))<1e-12
        # Bbar constructed as positive forward generator, so same sign as A.
        qmacro=sp*(exp_sym(M,t)@(qmacro/sp))
        return H@qmacro
    raise ValueError(kind)

kappa=100000.
models=[setup(h,drive,kappa) for h,drive in [(0,0),(.05,.8),(-.03,-.6)]]
T=[.2,.3,.7]
p0=models[0]['p'].copy();true=p0.copy();coarse=p0.copy()
K=0.
for j,(model,t) in enumerate(zip(models,T)):
    if j:K+=.5*float(np.max(np.log(models[j-1]['p']/model['p'])))
    true=evolve_probability(true,model,t,'true')
    coarse=evolve_probability(coarse,model,t,'coarse')
assert abs(sum(true)-1)<1e-9 and min(true)>-1e-10
assert abs(sum(coarse)-1)<1e-9 and min(coarse)>-1e-10
actual_tv=float(np.sum(abs(R@(true-coarse)))/2)
d=max(m['d_actual'] for m in models)
cert=math.exp(K)*d/(2*math.sqrt(1-d))
# For all |g|<=1, mean error <= certificate (W0=1).
assert 2*actual_tv<=cert+1e-8
result={'status':'PASS','microscopic_states':64,'blocks':2,'macro_states':16,'count_energy_cross_coupling':-.09,'kappa':kappa,'cases':[{k:float(m[k]) for k in ['cc_actual','cc_bound','d_actual','d_bound','max_hyper_error','J']} for m in models],'changing_energy_test':{'K_jump':K,'worst_actual_d':d,'observed_macro_TV':actual_tv,'all_bounded_observable_error':2*actual_tv,'action_certificate_W0_1':cert},'scope':'Finite independent multi-block diagnostic; not physical data, an infinite-size proof or a novelty result.'}
Path(__file__).with_name('check_multiblock_relative_energy_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
