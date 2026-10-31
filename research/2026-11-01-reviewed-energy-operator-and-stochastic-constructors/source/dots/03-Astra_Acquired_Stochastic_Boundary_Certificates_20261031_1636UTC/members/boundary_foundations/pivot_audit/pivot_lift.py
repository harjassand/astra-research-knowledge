"""Exact raw-list certificate for a catalytic star lift of a one-species core.
Research mathematics only. Standard-library rational checker; SymPy constructs
rational functions/polynomial tail witnesses. No simulation or floating solver.
"""
from fractions import Fraction as F
from math import prod, ceil
import json, hashlib
import sympy as S

def weak_reversible(edges):
    verts=set(x for e in edges for x in e)
    reach={v:{v} for v in verts}
    for u,v in edges: reach[u].add(v)
    for k in verts:
        for i in verts:
            if k in reach[i]: reach[i]|=reach[k]
    return all(u in reach[v] for u,v in edges)

def recognize(species,reactions):
    n=len(species)
    assert all(len(r[0])==len(r[1])==n and F(r[2])>0 for r in reactions)
    assert all(all(type(x)==int and x>=0 for x in r[0]+r[1]) for r in reactions)
    rs=[(tuple(u),tuple(v),F(k)) for u,v,k in reactions if tuple(u)!=tuple(v)]
    if not weak_reversible([(u,v) for u,v,k in rs]):
        return {'accepted':False,'reason':'full reaction graph not weakly reversible'}
    trials=[]
    for p in range(n):
        core=[]; alpha=[F(0)]*n; beta=[F(0)]*n; neutral=[]; bad=[]
        aa=tuple(2 if j==p else 0 for j in range(n))
        for idx,(u,v,k) in enumerate(rs):
            if all(u[j]==v[j]==0 for j in range(n) if j!=p):
                core.append((u[p],v[p],k)); continue
            caught=False
            for j in range(n):
                if j==p: continue
                ab=tuple(int(z==p)+int(z==j) for z in range(n))
                if u==aa and v==ab: alpha[j]+=k; caught=True; break
                if u==ab and v==aa: beta[j]+=k; caught=True; break
            if caught: continue
            if u[p]==v[p] and sum(u)==sum(v): neutral.append(idx)
            else: bad.append(idx)
        missing=[j for j in range(n) if j!=p and not(alpha[j]>0 and beta[j]>0)]
        if not bad and not missing and weak_reversible([(u,v) for u,v,k in core]):
            return {'accepted':True,'pivot':p,'species':species,'core':core,
                    'alpha':alpha,'beta':beta,'neutral_indices':neutral,'reactions':rs}
        trials.append({'pivot':p,'bad':bad,'missing_star':missing})
    return {'accepted':False,'reason':'no acquired pivot-star decomposition','trials':trials}

def q(x): return S.Rational(x.numerator,x.denominator) if isinstance(x,F) else S.Rational(x)
def ff(a,k): return S.prod(a-j for j in range(k))
def ratio(a,j,c):
    if j>=0: return S.prod((a+k)/(a+c+k) for k in range(j))
    return S.prod((a+c-k)/(a-k) for k in range(1,-j+1))
def g_int(a,c,g0):
    if a==0:return g0
    return prod((F(k)/(F(k)+c) for k in range(1,a)),start=F(1))

def construct(rec,t=F(2)):
    assert rec['accepted'] and t>1
    p=rec['pivot'];core=rec['core'];alpha=sum(rec['alpha']);betas=[b for j,b in enumerate(rec['beta']) if j!=p]
    # The one-species case can simply omit the star term.
    bmin=min(betas) if betas else None
    if not core: return {'finite_shells':True,'reason':'every jump conserves total count'}
    M=max(u for u,v,k in core)
    if M==1:
        mu=sum(k for u,v,k in core if u==1)
        c=min(F(1),mu*(1-1/t)/(2*alpha)) if alpha else F(1)
    else:c=F(1)
    inflows=[v for u,v,k in core if u==0]
    g0=F(1)+max([t**v*g_int(v,c,F(1)) for v in inflows],default=F(0))
    a=S.symbols('a');P=S.factor(sum(q(k)*ff(a,u)*(q(t)**(v-u)*ratio(a,v-u,q(c))-1) for u,v,k in core))
    H=S.factor(P+q(c*alpha)*a)
    numerator,denominator=S.fraction(S.cancel(H+1))
    if S.Poly(denominator,a).LC()<0:numerator=-numerator;denominator=-denominator
    R=max(2,M+1);z=S.symbols('z');tries=0
    while True:
        nc=S.Poly(numerator.subs(a,z+R),z).all_coeffs()
        dc=S.Poly(denominator.subs(a,z+R),z).all_coeffs()
        tries+=1
        if all(x<=0 for x in nc) and any(x<0 for x in nc) and all(x>=0 for x in dc) and dc[-1]>0:break
        R*=2
    def base(a0):
        ga=g_int(a0,c,g0)
        return sum(k*F(prod(range(a0-u+1,a0+1))) * (t**(v-u)*g_int(a0+v-u,c,g0)/ga-1)
                   for u,v,k in core if a0>=u)
    H0=base(0)
    assert (not inflows and H0==0) or H0<0
    eps=min(F(1),-H0) if inflows else F(1)
    exceptions=[]
    for av in range(1,R):
        hv=base(av)+(c*alpha*av if av>=2 else F(0))
        coeff=c*av/(av+c)*(bmin or F(1))
        B=max(-1,ceil((hv+eps)/coeff)) if bmin is not None else 0
        # All states with bsum>B have quotient at most -eps.
        exceptions.append({'a':av,'H':hv,'b_slope_min':coeff,'B':B})
    # A finite safe Foster constant from H(a)-negative b term <=H(a).
    C=F(0)
    for row in exceptions:
        if row['B']>=0:
            C=max(C,t**(row['a']+row['B'])*g_int(row['a'],c,g0)*max(F(0),row['H']+eps))
    return {'finite_shells':False,'t':t,'c':c,'g0':g0,'M':M,'alpha':alpha,'beta_min':bmin,
            'P':str(P),'H':str(H),'tail_numerator':str(numerator),'tail_denominator':str(denominator),
            'R':R,'shifted_numerator_coeffs':[str(x) for x in nc],
            'shifted_denominator_coeffs':[str(x) for x in dc], 'radius_trials':tries,
            'epsilon':eps,'foster_C':C,'zero_face_quotient':H0,'zero_face_conservative':not inflows,
            'exceptions':exceptions}

def exact_generator(rec,cert,x):
    a=x[rec['pivot']];N=sum(x);V=cert['t']**N*g_int(a,cert['c'],cert['g0'])
    out=F(0)
    for u,v,k in rec['reactions']:
        if any(xx<yy for xx,yy in zip(x,u)):continue
        intensity=k*prod(prod(range(xx-yy+1,xx+1)) for xx,yy in zip(x,u))
        xp=tuple(xx-yy+zz for xx,yy,zz in zip(x,u,v))
        Vp=cert['t']**sum(xp)*g_int(xp[rec['pivot']],cert['c'],cert['g0'])
        out+=intensity*(Vp-V)
    return V,out

def encode(o):
    if isinstance(o,F):return str(o)
    raise TypeError(type(o))

def demo():
    # Two linkage classes: {0,A} and {2A,3A,A+B,A+C}. Non-complex balance:
    # 0<->A forces a=1; 2A<->3A with rates2,1 forces a=2.
    sp=['A','B','C'];R=[((0,0,0),(1,0,0),1),((1,0,0),(0,0,0),1),
       ((2,0,0),(3,0,0),2),((3,0,0),(2,0,0),1),
       ((2,0,0),(1,1,0),F(2,3)),((1,1,0),(2,0,0),F(5,7)),
       ((2,0,0),(1,0,1),F(3,2)),((1,0,1),(2,0,0),F(7,5)),
       # High-order neutral reaction and reverse: neither A nor N changes.
       ((0,2,1),(0,1,2),3),((0,1,2),(0,2,1),F(4,3))]
    rec=recognize(sp,R);assert rec['accepted'] and rec['pivot']==0
    cert=construct(rec)
    total=0
    for a in range(26):
      for b in range(26):
       for c in range(10):
        V,LV=exact_generator(rec,cert,(a,b,c));assert LV<=-cert['epsilon']*V+cert['foster_C'];total+=1
    # The two-species product-form baseline, and no-zero-complex core.
    baseline=recognize(['A','B'],[r[:2]+(r[2],) for r in [((0,0),(1,0),1),((1,0),(0,0),1),((2,0),(1,1),1),((1,1),(2,0),1)]])
    cb=construct(baseline);assert cb['c']==F(1,4)
    boundary=recognize(['A','B'],[((2,0),(3,0),1),((3,0),(2,0),1),((2,0),(1,1),1),((1,1),(2,0),1)])
    cc=construct(boundary);assert cc['zero_face_conservative']
    for a in range(1,20):
      for b in range(20):
        V,LV=exact_generator(boundary,cc,(a,b));assert LV<=-cc['epsilon']*V+cc['foster_C']
    # Neutral extension does not change the quotient at any count, exact proof by increments.
    rec_without=recognize(sp,R[:-2])
    for x in [(0,200,100),(1,40,30),(2,100,150),(20,30,40)]:
        assert exact_generator(rec,cert,x)==exact_generator(rec_without,cert,x)
    # A satellite immigration breaks the model and must not silently be accepted.
    bad=recognize(sp,R+[((0,0,0),(0,1,0),1),((0,1,0),(0,0,0),1)])
    assert not bad['accepted']
    # Renaming/permuting the species must acquire the same pivot, not a supplied one.
    perm=[2,0,1];Rp=[(tuple(u[j] for j in perm),tuple(v[j] for j in perm),k) for u,v,k in R]
    rr=recognize([sp[j] for j in perm],list(reversed(Rp)));assert rr['accepted'] and rr['pivot']==1
    result={'status':'exact certificate and finite challenges passed','example_species':sp,'example_reactions':R,
      'certificate':cert,'baseline_certificate':cb,'no_zero_core_certificate':cc,
      'exact_grid_states':total,'noncomplex_balance_witness':'0<->A requires a=1; 2A<->3A requires a=2',
      'rejected_mutation':bad,'renamed_pivot':rr['pivot'],
      'scope':'All-population theorem follows from rational polynomial coefficient witness plus symbolic generator identity; finite grids are challenges only.'}
    print(json.dumps(result,default=encode,indent=2))
if __name__=='__main__':demo()
