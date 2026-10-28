"""Exact nonzero characteristic receiver, no SDP/Newton acquisition."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations_with_replacement as cw,product
import json,math,time,runpy
START=time.monotonic()
import sympy as s
import numpy as np
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[2]; COMP=OUT.parent/'support_gram_compiler'
inp=runpy.run_path(str(COMP/'verify_grams_independently.py'),run_name='frozen_literal_input')
a=s.symbols('a0:4'); U=s.symbols('u0:4')
def sym(q):return s.Rational(q.numerator,q.denominator)
def rat(v):return Q(int(v.p),int(v.q))
def expr(p):return sum(sym(v)*s.prod(x**n for x,n in zip(a,e)) for e,v in p.items())
F=expr(inp['F']); p=expr(inp['p']); T=sum(x*x for x in a); q=a[0]*a[3]-a[1]*a[2]
kap=Q(1,20000000); eps=Q(1,100); ee=eps-kap; sig=Q(1,34); C=Q(33,400)
gam=Q(1,400000)-24*kap; mu=Q(1,25000)-7*kap
B=[Q(1,3),-Q(1,5),Q(1,7),Q(2,5)]; BS=105; BI=[int(x*BS) for x in B]; SCALE=BS**3
def mon(ii):return tuple(ii.count(j) for j in range(4))
def add(e,f):return tuple(x+y for x,y in zip(e,f))
def feat(ai,xi):return mon(ai)+mon(xi)
basis=[mon(ii) for d in range(1,5) for ii in cw(range(4),d)]; ix={e:i for i,e in enumerate(basis)}
f180=[feat(ai,(j,)) for ai in cw(range(4),3) for j in range(4)]+[feat(ai,xi) for ai in cw(range(4),2) for xi in cw(range(4),2)]
f26=[feat((i,),(j,)) for i in range(4) for j in range(4)]+[feat((),ii) for ii in cw(range(4),2)]
def row(e):
    out=[0]*69; al,be=e[:4],e[4:]
    for kk in product(*(range(n+1) for n in al)):
        v=(-1)**sum(be)*BS**(3-sum(al))
        for n,k,b in zip(al,kk,BI):v*=math.comb(n,k)*b**(n-k)*BS**k
        out[ix[add(kk,be)]]+=v
    return out
def congr(features,g):
    k=np.asarray([row(e) for e in features],dtype=object)
    return k.T@np.asarray(g,dtype=object)@k
def diag(features,w):
    k=np.asarray([row(e) for e in features],dtype=object)
    return k.T@(np.asarray(w,dtype=object)[:,None]*k)
def polynomial(g,den):
    out={}
    for i,e in enumerate(basis):
        for j in range(i,69):
            v=int(g[i,j])*(1 if i==j else 2)
            if v:
                ex=add(e,basis[j]);out[ex]=out.get(ex,Q(0))+Q(v,den)
    return {e:v for e,v in out.items() if v}
def shift(expr):
    raw={e:rat(v) for e,v in s.Poly(expr,*a,domain=s.QQ).terms()}; out={}
    for al,c in raw.items():
        for kk in product(*(range(n+1) for n in al)):
            v=c
            for n,k,b in zip(al,kk,B):v*=math.comb(n,k)*b**(n-k)
            out[kk]=out.get(kk,Q(0))+v
    return {e:v for e,v in out.items() if v}

def graph_gram():
    start=time.monotonic()
    old=json.loads((ROOT/'work/sol8_opportunity_selection_20261027/rational_selector/EXACT_RATIONAL_SUPPORT.json').read_text())
    new=json.loads((COMP/'EXACT26_SUPPORT_GRAM.json').read_text()); ir={e:i for i,e in enumerate(f180)}; v=[0]*180
    for i in range(4):
        for j,k,sign in [(3,0,1),(2,1,-1),(1,2,-1),(0,3,1)]:v[ir[feat((i,i,j),(k,))]]+=sign
        v[ir[feat((i,i),(0,3))]]+=1;v[ir[feat((i,i),(1,2))]]-=1
    assert sum(x*x for x in v)==24
    dr=old['gram_denominator']; fac=int(kap*dr)
    rh=[[old['gram_integer_matrix'][i][j]-fac*v[i]*v[j] for j in range(180)] for i in range(180)]
    ir={e:i for i,e in enumerate(f26)}; lv=[0]*26
    for i,j,sign in [(3,0,1),(2,1,-1),(1,2,-1),(0,3,1)]:lv[ir[feat((i,),(j,))]]=sign
    lv[ir[feat((),(0,3))]]=1;lv[ir[feat((),(1,2))]]=-1
    assert sum(x*x for x in lv)==6
    canon=[[lv[i]*lv[j] for j in range(26)] for i in range(26)]
    for i,j,sign in [(0,15,1),(1,14,-1),(4,11,-1),(5,10,1)]:canon[i][j]+=sign;canon[j][i]+=sign
    dn=new['gram_denominator']; fac=int(kap*dn)
    gh=[[new['gram_numerators'][i][j]-fac*canon[i][j] for j in range(26)] for i in range(26)]
    residual=[ee-2*C*sig,sig*(2*ee-C*sig),ee*sig*sig];assert min(residual)>0
    mats=[congr(f180,rh),congr(f26,gh)]; factors=[Q(1,dr*SCALE*SCALE),sig**2/(dn*SCALE*SCALE)]
    third=np.zeros((69,69),dtype=object)
    for i in range(4):third+=congr([tuple(v+(j==i) for j,v in enumerate(e[:4]))+e[4:] for e in f26],gh)
    mats.append(third);factors.append(2*sig/(dn*SCALE*SCALE))
    af=[feat(ii,(j,)) for ii in cw(range(4),2) for j in range(4)]
    ww=[1 if ii[0]==ii[1] else 2 for ii in cw(range(4),2) for j in range(4)]
    mats.extend([diag(af,ww),diag(f26[:16],[1]*16),diag([feat((),(i,)) for i in range(4)],[1]*4)])
    factors.extend([v/SCALE**2 for v in residual]);den=math.lcm(*(v.denominator for v in factors));g=np.zeros((69,69),dtype=object)
    for mat,v in zip(mats,factors):g+=mat*(v.numerator*(den//v.denominator))
    assert np.array_equal(g,g.T)
    return g,den,{'RH_margin':str(gam),'G26H_margin':str(mu),'residual':list(map(str,residual)),
                  'construction_seconds':time.monotonic()-start}

def bound69():
    k=[]
    for e in basis:
        d=sum(e)
        if d<=2:
            v=[Q(0)]*69;v[ix[e]]=1
        else:
            ii=[j for j,n in enumerate(e) for _ in range(n)]
            v=[Q(x,SCALE) for x in row(feat(tuple(ii[:d-2]),tuple(ii[d-2:])))]
        k.append(v)
    assert all(k[i][i]==1 and not any(k[i][i+1:]) for i in range(69))
    inv=[[Q(0)]*69 for _ in range(69)]
    for i in range(69):
        inv[i][i]=1;nz=[j for j in range(i) if k[i][j]]
        for j in range(i):inv[i][j]=-sum((k[i][t]*inv[t][j] for t in nz),Q(0))
    assert all(sum((k[i][t]*inv[t][j] for t in range(69)),Q(0))==(i==j) for i in range(69) for j in range(69))
    n1=max(sum(abs(inv[i][j]) for i in range(69)) for j in range(69));ni=max(sum(map(abs,r)) for r in inv)
    m0=min(ee*sig**2,mu*sig**2,2*sig*mu,gam);b=m0/(n1*ni)
    return b,{'selected_minimum_weight':str(m0),'inverse_norm1':str(n1),'inverse_norminf':str(ni),'lower':str(b)}

def main():
    H=F-sym(kap)*q*q;E=H+sym(ee)*T;pH=p-2*sym(kap)*q*T*T;D=(T+sym(sig))**2;kk=pH/D
    at=dict(zip(a,map(sym,B)));cof=s.Matrix([s.diff(q,t) for t in a]);grad=s.Matrix([s.diff(E,t) for t in a])
    kv=kk.subs(at);M=(s.hessian(E,a)-kv*s.hessian(q,a)).subs(at);r=s.Matrix([s.diff(kk,t).subs(at) for t in a]);cb=cof.subs(at)
    hh=M.inv()*r;normal=s.Matrix([-v for v in hh]+[1-(cb.T*hh)[0]]);nq=list(map(rat,normal))
    qB=rat(q.subs(at));z0=B+[qB];t0=rat(E.subs(at));j0=s.Matrix(list((grad-kk*cof).subs(at))+[kv]);slope=rat((j0.T*normal)[0])
    gradk=s.Matrix([s.diff(kk,t) for t in a]);J=s.Matrix.vstack(s.hessian(E,a)-cof*gradk.T-kk*s.hessian(q,a),gradk.T).subs(at)
    assert J.T*normal==s.zeros(4,1)
    assert normal[4]-(cb.T*s.Matrix(list(normal[:4])))[0]==1
    inp['positive_ldl']([[rat(v) for v in row] for row in M.tolist()])
    metric=J*M.inv()*J.T+2*sym(kap)*s.eye(5)
    inp['positive_ldl']([[rat(v) for v in row] for row in metric.tolist()])
    N=D*(-3*H-sym(ee)*T+sum(s.diff(E,a[i])*sym(B[i]) for i in range(4)))+pH*(sym(qB)+q-sum(cof[i]*sym(B[i]) for i in range(4)))
    zero=shift(D*sym(t0)-N)
    first=shift(D*sym(slope)-D*sum(s.diff(E,a[i])*normal[i] for i in range(4))+pH*(sum(cof[i]*normal[i] for i in range(4))-normal[4]))
    assert all(sum(e)>=2 for e in zero) and all(sum(e)>=2 for e in first)
    g,den,construction=graph_gram();assert polynomial(g,den)==zero
    bound,bd=bound69();pairs={}
    for i,e in enumerate(basis):
        for j in range(i,69):pairs.setdefault(add(e,basis[j]),[]).append((i,j))
    assert len(pairs)==490
    delta=[[Q(0)]*69 for _ in range(69)]
    for e,v in first.items():
        i,j=min(pairs[e],key=lambda ij:(abs(sum(basis[ij[0]])-sum(basis[ij[1]])),ij))
        if i==j:delta[i][i]+=v
        else:delta[i][j]+=v/2;delta[j][i]+=v/2
    dd=math.lcm(*(x.denominator for rr in delta for x in rr));di=np.asarray([[int(x*dd) for x in rr] for rr in delta],dtype=object)
    assert polynomial(di,dd)==first
    L=sum(map(abs,first.values()));assert L>0 and sum(abs(x) for rr in delta for x in rr)<=L
    qn=nq[0]*nq[3]-nq[1]*nq[2];radius=min(bound/(2*L),Q(1,2)/(1+abs(qn)),Q(1));lam=Q(1)
    while lam>radius:lam/=10
    zz=[x+lam*y for x,y in zip(z0,nq)];tt=t0+lam*slope;val=tt+kap*sum(x*x for x in zz)
    gap=zz[4]-zz[0]*zz[3]+zz[1]*zz[2];assert gap==lam-lam*lam*qn and gap!=0
    assert bound-lam*L>=bound/2
    assert t0+kap*sum(x*x for x in z0)==rat(F.subs(at))+eps*sum(x*x for x in B)
    (OUT/'BASE69_GRAM.json').write_text(json.dumps({'status':'EXACT69_GRAPH_GRAM','basis':basis,'center':list(map(str,B)),
        'gram_denominator':den,'gram_numerators':g.tolist(),'PD_lower_bound':str(bound),'construction':construction,'bound':bd},indent=2)+'\n')
    (OUT/'DELTA69_GRAM.json').write_text(json.dumps({'status':'EXACT69_DIRECTION_GRAM','basis':basis,'gram_denominator':dd,
        'gram_numerators':di.tolist(),'operator_norm_upper_bound':str(L)},indent=2)+'\n')
    result={'status':'EXACT_NONZERO_CONTACT_SEGMENT_ACQUIRED','B':list(map(str,B)),'epsilon':str(eps),'kappa':str(kap),'e':str(ee),'sigma':str(sig),
        'z0':list(map(str,z0)),'normal':list(map(str,nq)),'base_t':str(t0),'slope':str(slope),'radius':str(radius),'display_radius':float(radius),
        'selected_lambda':str(lam),'selected_z':list(map(str,zz)),'selected_t':str(tt),'selected_G_value':str(val),'display_G_value':float(val),
        'off_graph_gap':str(gap),'display_off_graph_gap':float(gap),'base_Gram_lower_bound':str(bound),'direction_Gram_operator_bound':str(L),
        'segment_Gram_lower_bound':str(bound/2),'Hessian_V_rank':int(J.rank()),'seconds':time.monotonic()-START,
        'scope':'For all |lambda|<=radius, V(z0+lambda*n)=base_t+lambda*slope exactly. '
        'G adds kappa norm^2. No SDP/Newton/optimization; source certificates charged. Scientific imports included, stdlib/startup excluded.'}
    (OUT/'RECEIVER.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','display_radius','selected_lambda','display_G_value','display_off_graph_gap','base_Gram_lower_bound','Hessian_V_rank','seconds']},indent=2),flush=True)

if __name__=='__main__':main()
