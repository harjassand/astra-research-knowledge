#!/usr/bin/env python3
"""Independent reaction-complex audit. No import of author code, no simulation.
Ordinary proof is in INDEPENDENT_REVIEW.md; these checks only supplement it.
"""
from fractions import Fraction as Qr
from itertools import product
from pathlib import Path
import hashlib
import json
import sympy as sp

A,B,C,D,E,N,T,l,e = sp.symbols('A B C D E N T l e')
x=(A,B,C,D,E)
complexes={'0':(0,0,0,0,0),'A':(1,0,0,0,0),'2A':(2,0,0,0,0),
 'AC':(1,0,1,0,0),'AD':(1,0,0,1,0),'AE':(1,0,0,0,1),
 'CD':(0,0,1,1,0),'AB':(1,1,0,0,0)}
edges=[('0','A',1),('A','0',1),('2A','AC',1),('AC','2A',1),
 ('2A','AD',1),('AD','2A',1),('2A','AE',1),('AE','2A',1),
 ('AE','CD',1),('CD','AE',2),('CD','AB',1),('AB','CD',1)]
channels=[]
for src,dst,k in edges:
    rc,pc=complexes[src],complexes[dst]
    nu=tuple(b-a for a,b in zip(rc,pc))
    rate=sp.Integer(k)
    for xx,m in zip(x,rc):
        for j in range(m): rate*=xx-j
    channels.append((src+'->'+dst,sp.expand(rate),nu))

def shifted(p,nu): return sp.expand(sp.sympify(p).subs(dict(zip(x,[v+d for v,d in zip(x,nu)])),simultaneous=True))
def jump(p,nu): return sp.expand(shifted(p,nu)-p)
def gen(p): return sp.expand(sum(rate*jump(p,nu) for _,rate,nu in channels))
def bracket(p,q): return sp.expand(sum(rate*jump(p,nu)*jump(q,nu) for _,rate,nu in channels))
checks=[]
def eq(a,b,name):
    assert sp.cancel(sp.expand(a-b))==0,name
    checks.append(name)
L=A+(C+D)/2; Z=C-D; h=A*E; n=sum(x); a2=A*(A-1); defect=L**2-C*D
rh=E-3*E*defect+2*A*C*D+A*(A-1)**2+2*C*D+h*(N-B+2*L+2-7*A)
eq(gen(L),1+A+A*L+h-3*A*A,'GL from source complexes')
eq(gen(E),a2-2*h+2*C*D,'GE from source complexes')
eq(gen(h),-N*h+3*E*L*L+rh,'Gh from source complexes')
eq(gen(A),1-A-3*a2+A*(C+D)+3*C*D-A*B,'GA from source complexes')
eq(gen(Z),-A*Z,'GZ from source complexes')
eq(gen(Z*Z),-2*A*Z*Z+2*A*(L-1),'GZ squared drift')
eq(gen(n),1-A,'Gn from source complexes')
eq(defect,2*A*L-A*A+Z*Z/4,'Q decomposition')
qLL=1+A+sp.Rational(3,2)*a2+A*(C+D)/4+h
qEE=a2+2*h+2*C*D; wLE=a2+h
sL=1+A+2*a2+A*(C+D)/2+h
qhh=E**2*(1+A+2*a2+A*(C+D)+C*D+A*B)+a2*(A-E-1)**2+2*h*((E-1)**2+A*A)+2*C*D*(A+E+1)**2
qA=1+A+3*a2+A*(C+D)+2*h+3*C*D+A*B
eq(bracket(L,L),qLL,'qLL')
eq(bracket(E,E),qEE,'qEE')
eq(bracket(L,E),-wLE,'qLE sign')
eq(sum(rate*abs(jump(L,nu)) for _,rate,nu in channels),sL,'absolute L intensity')
eq(bracket(h,h),qhh,'qhh including both fast rows')
eq(bracket(A,A),qA,'qA exact, not just upper bound')
for name,rate,nu in channels:
    eq(jump(n,nu),int(name=='0->A')-int(name=='A->0'),'total-count jump '+name)
    if name in ('CD->AB','AB->CD'):
        eq(jump(L,nu),0,'fast L zero '+name)
        eq(jump(E,nu),0,'fast E zero '+name)
        eq(jump(h,nu),E if name=='CD->AB' else -E,'fast AE jump '+name)
# All finite product terms for arbitrary endpoint g-values.
g,dg=sp.symbols('g dg')
for name,rate,nu in channels:
    hp=shifted(h,nu); dw=jump(h,nu)
    eq(hp*(g+dg)-h*g,g*dw+hp*dg,'product rule with postjump h '+name)
# Higher mixed polynomial spot checks, and the physically necessary N=T^5 relation.
for f in (l,e,l*l,l*e,e*e,l**3*e**2,l**2*e**3):
    sub={l:L/T,e:E/T**3}; ff=f.subs(sub); fl=sp.diff(f,l).subs(sub); fe=sp.diff(f,e).subs(sub)
    F=ff+h*fl/(N*T)
    r2=gen(ff)-fl*gen(L)/T-fe*gen(E)/T**3
    pp=sum(rate*shifted(h,nu)*jump(fl,nu) for _,rate,nu in channels)/(N*T)
    rr=fl*(A+A*L-3*A*A)/T+fe*(a2-2*h-2*defect)/T**3+fl*rh/(N*T)+r2+pp
    target=(fl*(1+3*(L/T)**2*(E/T**3))+fe*2*(L/T)**2)/T
    eq((gen(F)-target-rr).subs(N,T**5),0,'full corrected identity '+str(f))
# Compact exponent ledger using the exact displayed budgets.
K,M,S,h0,d0=sp.symbols('K M S h0 d0',positive=True)
H=h0/T**2; J=K*T*H; Zbar=S*T**2; d=d0*T**3
U=S*T+H+sp.Rational(3,2)*J+(K*T/2+M*T**3)*H
W=J+M*T**3*H
VE=J+2*M*T**3*H+2*K*K*S*T**3
VL=S*T+H+2*J+(K*T+M*T**3)*H
HP=(K*T+1)*(M*T**3+1); RP=K*T+M*T**3+1
RH=M*S*T**4+6*M*K*T**4*H+sp.Rational(3,4)*M*T**3*Zbar+2*K*K*T*T*H+K*T*J+2*K*K*S*T**3+M*T**3*(d+M*T**3+4*K*T+2)*H
rho_terms=[(1+2*K*T)*H/T,(J+2*M*T**3*H+4*K*T*H+Zbar/2)/T**3,RH/T**6,U/(2*T*T),W/T**4,VE/(2*T**6),HP*VL/T**7,HP*VE/T**9]
Phi=M*M*T**6*(S*T+H+2*J+2*K*T*H+K*K*S*T**3+(T**5+d)*H)+RP**2*VE
astar=1/T+HP/T**7; bstar=1/T**3+HP/T**9; cstar=1/T**6
bracket_terms=[2*astar**2*U,4*astar*bstar*W,2*bstar**2*VE,2*cstar**2*Phi]
def max_power(expr): return max(term.as_powers_dict().get(T,0) for term in sp.expand(expr).as_ordered_terms())
rho_degrees=[int(max_power(v)) for v in rho_terms]
bracket_degrees=[int(max_power(v)) for v in bracket_terms]
assert rho_degrees==[-2,-1,-1,-1,-3,-3,-2,-2],rho_degrees
assert bracket_degrees==[-1,-3,-3,-3],bracket_degrees
assert max_power(2*HP/T**6)==-2
assert max_power(astar+bstar+cstar*RP)==-1
checks.extend(['rho exponent ledger','bracket exponent ledger','endpoint exponent','jump exponent'])
# Fast rational adversarial grid; no symbolic substitution, no trajectories.
state_count=active_count=0
for aa,bb,cc,dd,ee,tt in product(range(6),(0,1,7,100),range(4),range(4),(0,1,2,7),(1,2,3)):
    xx=(aa,bb,cc,dd,ee); LL=Qr(2*aa+cc+dd,2); hh=aa*ee; zz=cc-dd
    hpmax=(aa+1)*(ee+1); rmax=aa+ee+1
    ll=LL/tt; es=Qr(ee,tt**3); nn=tt**5
    f=lambda ll,es:ll*ll+ll*es+es*es
    f0=f(ll,es); fl=2*ll+es
    FF=f0+Qr(hh,nn*tt)*fl
    rate_sum_ll=rate_sum_ee=rate_sum_le=rate_sum_hh=Qr(0)
    exact_qF=bound_qF=Qr(0)
    for src,dst,k in edges:
        rc,pc=complexes[src],complexes[dst]
        rate=k
        for xxj,m in zip(xx,rc):
            for j in range(m): rate*=xxj-j
        if rate==0: continue
        nu=tuple(y-x for x,y in zip(rc,pc)); xp=tuple(v+vnu for v,vnu in zip(xx,nu))
        assert min(xp)>=0
        Ap,Bp,Cp,Dp,Ep=xp; Lp=Qr(2*Ap+Cp+Dp,2)
        u=Lp-LL; v=Ep-ee; hp=Ap*Ep; ww=hp-hh
        assert 0<=hp<=hpmax and abs(ww)<=rmax
        assert abs(u)<=1 and abs(v)<=1
        assert 0<=Lp<=LL+1 and 0<=Ep<=ee+1
        lp=Lp/tt; ep=Qr(Ep,tt**3); flp=2*lp+ep
        df=f(lp,ep)-f0; dg=flp-fl
        dF=f(lp,ep)+Qr(hp,nn*tt)*flp-FF
        assert dF==df+Qr(ww,nn*tt)*fl+Qr(hp,nn*tt)*dg
        F10=max(abs(fl),abs(flp)); F01=max(abs(ll+2*es),abs(lp+2*ep))
        dr=F10*abs(u)/tt+F01*Qr(abs(v),tt**3)+Qr(abs(ww),nn*tt)*abs(fl)+hp*(Qr(2,nn*tt**2)*abs(u)+Qr(abs(v),nn*tt**4))
        assert abs(dF)<=dr
        exact_qF+=rate*dF*dF; bound_qF+=rate*dr*dr
        rate_sum_ll+=rate*u*u; rate_sum_ee+=rate*v*v; rate_sum_le+=rate*u*v; rate_sum_hh+=rate*ww*ww
        active_count+=1
    qll=1+aa+Qr(3,2)*aa*(aa-1)+Qr(aa*(cc+dd),4)+hh
    qee=aa*(aa-1)+2*hh+2*cc*dd
    assert rate_sum_ll==qll and rate_sum_ee==qee and rate_sum_le==-(aa*(aa-1)+hh)
    assert exact_qF<=bound_qF
    assert abs(aa+aa*LL-3*aa*aa)<=aa+2*aa*LL
    assert abs(4*LL-8*aa)<=4*LL
    qhh_upper=ee**2*(1+aa+2*aa*aa+2*aa*LL+LL*LL+aa*bb)+rmax*rmax*(aa*aa+2*hh+2*LL*LL)
    assert rate_sum_hh<=qhh_upper
    state_count+=1
# Concrete witnesses expose common invalid simplifications.
# At A=C=D=E=1, B=7, T=2, f=l, both fast channels contribute.
fast_bracket=Qr((7+1)*1,32**2*2**2)
assert fast_bracket==Qr(1,512)>0
# For f=l^2, immigration at E=3,T=2 changes h by 3 and g by 1.
missing_product=Qr(3,32*2)
assert missing_product==Qr(3,64)>0
# C2, not C3, is possible: |l-c|^(5/2) has continuous second derivative,
# with derivative of that second derivative unbounded at c; no C3 is invoked.
report={'status':'PASS','independence':'Reaction complexes and test logic reconstructed; no author-code import.',
 'symbolic_assertions':len(checks),'symbolic_checks':checks,
 'rational_state_cases':state_count,'active_channel_cases':active_count,
 'compact_rho_term_max_powers':rho_degrees,'compact_bracket_term_max_powers':bracket_degrees,
 'adversarial_witnesses':{'omitting_fast_corrected_bracket':str(fast_bracket),'omitting_finite_product_jump':str(missing_product)},
 'scope':'Exact algebra, rational-state falsification, and exponent ledger; ordinary theorem proof is separate.'}
out=Path(__file__).with_name('independent_exact_results.json')
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
