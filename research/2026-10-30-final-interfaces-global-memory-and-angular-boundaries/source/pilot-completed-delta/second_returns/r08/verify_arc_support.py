"""Uniform global quartic minor support on the inherited parameter arc.

Extends the acquired Gram by keeping its rational free entries fixed and
solving the coefficient equations for the same pivot entries. The fixed
coefficient map is integral. Generic identities certify the missing
monomials; rational interval LDL certifies positivity on the full arc.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import isqrt
import json,time
import sympy as s
from verify_support import I,asI,fq,interval_ldl,BITS,SCALE,down,up

OUT=Path(__file__).resolve().parent
raw=json.loads((OUT/'support_gram.json').read_text())
t,u=s.symbols('t u')

def sqrtI(box):
    assert box.lo>=0
    low=isqrt((box.lo.numerator*SCALE*SCALE)//box.lo.denominator)
    high=isqrt((box.hi.numerator*SCALE*SCALE)//box.hi.denominator)+1
    return I(Q(low,SCALE),Q(high,SCALE))

zero=(0,0,0,0)
def padd(*polys):
    out={}
    for poly in polys:
        for pw,co in poly.items():out[pw]=out.get(pw,I(0))+co
    return out
def pscale(poly,co):return {pw:value*co for pw,value in poly.items()}
def pmul(left,right):
    out={}
    for pp,aa in left.items():
        for qq,bb in right.items():
            pw=tuple(a+b for a,b in zip(pp,qq));out[pw]=out.get(pw,I(0))+aa*bb
    return out
def sq(poly):return pmul(poly,poly)

def generic_missing_monomials():
    B=1-3*u*u;HH=1+3*u*u;be=B/HH;rr=4-12*u/HH
    m=s.Poly(B*B*(1-t*t)**2-(1-4*u+3*u*u)*HH*(1+t*t)**2,t,domain=s.QQ.frac_field(u)).monic()
    K=s.Matrix([-B*(u*(1-t*t)+HH*t*t)*(1+t*t),
        B*t*(HH-u*(1-t*t))*(1+t*t),
        B*B*t*(1-t*t)-u*HH*t*(1+t*t)**2,
        B*B*t*t*(1-t*t)+u*HH*(1+t*t)**2])
    a,b,c,d=s.symbols('a b c d');av=(a,b,c,d)
    T=sum(z*z for z in av);q=a*d-b*c;X=a*a+c*c-b*b-d*d
    F=T*T+4*(rr-1)*q*q+4*be*q*X
    R=s.Matrix([1,t,0,0])
    def rem(v):return s.Poly(v,t,domain=s.QQ.frac_field(u)).rem(m).is_zero
    HR=s.hessian(F,av).subs(dict(zip(av,R)),simultaneous=True)
    assert all(rem(v) for v in HR*K)
    HK=s.hessian(F,av).subs(dict(zip(av,K)),simultaneous=True)
    lam=(HK*R)[3]
    assert all(rem(v) for v in (HK-lam*s.hessian(q,av))*R)
    # These imply the quadratic z^2,z*v_i and cubic z^3 coefficients vanish.
    return True

def main():
    started=time.perf_counter()
    assert generic_missing_monomials()
    print('Generic missing-monomial identities checked over Q(u)[t]/m.',flush=True)
    radius=Q(1,2**206);center=Q(1,30)
    U=I(center-radius,center+radius)
    B=1-3*U**2;HH=1+3*U**2;be=B/HH;rr=4-12*U/HH
    C=(9*U**4-6*U**3-2*U+1)/(U*(3*U**2-3*U+1))
    assert C.lo>2
    root=sqrtI((C-sqrtI(C*C-4))/2)
    assert root.lo>0
    tt=root
    kk=[-B*(U*(1-tt*tt)+HH*tt*tt)*(1+tt*tt),
        B*tt*(HH-U*(1-tt*tt))*(1+tt*tt),
        B*B*tt*(1-tt*tt)-U*HH*tt*(1+tt*tt)**2,
        B*B*tt*tt*(1-tt*tt)+U*HH*(1+tt*tt)**2]
    assert kk[0].hi<0
    K=[value/kk[0] for value in kk]
    TK=sum((value*value for value in K),I(0))
    qK=K[0]*K[3]-K[1]*K[2]
    XK=K[0]*K[0]+K[2]*K[2]-K[1]*K[1]-K[3]*K[3]
    gq=[K[3],-K[2],-K[1],K[0]]
    gx=[2*K[0],-2*K[1],2*K[2],-2*K[3]]
    hq=[[0,0,0,1],[0,0,-1,0],[0,-1,0,0],[1,0,0,0]]
    hx=[2,-2,2,-2]
    HK=[]
    for i in range(4):
        row=[]
        for j in range(4):
            value=4*TK*int(i==j)+8*K[i]*K[j]
            value+=4*(rr-1)*(2*gq[i]*gq[j]+2*qK*hq[i][j])
            value+=4*be*(XK*hq[i][j]+qK*hx[i]*int(i==j)+gq[i]*gx[j]+gx[i]*gq[j])
            row.append(value)
        HK.append(row)
    support=HK[3][0]+HK[3][1]*tt
    variables=[{tuple(int(i==j) for i in range(4)):I(1)} for j in range(4)]
    coord=[variables[0],padd(pscale(variables[0],tt),variables[1]),variables[2],variables[3]]
    TP=padd(*(sq(co) for co in coord))
    qP=padd(pmul(coord[0],coord[3]),pscale(pmul(coord[1],coord[2]),-1))
    XP=padd(sq(coord[0]),sq(coord[2]),pscale(sq(coord[1]),-1),pscale(sq(coord[3]),-1))
    FP=padd(sq(TP),pscale(sq(qP),4*(rr-1)),pscale(pmul(qP,XP),4*be))
    cof=[coord[3],pscale(coord[2],-1),pscale(coord[1],-1),coord[0]]
    dx=[pscale(co,sign) for co,sign in zip(coord,(2,-2,2,-2))]
    cubic={}
    for i in range(4):
        grad=padd(pscale(pmul(TP,coord[i]),4),pscale(pmul(qP,cof[i]),8*(rr-1)),
                  pscale(padd(pmul(XP,cof[i]),pmul(qP,dx[i])),4*be))
        cubic=padd(cubic,pscale(grad,K[i]))
    quadratic={}
    for i in range(4):
        for j in range(4):quadratic=padd(quadratic,pscale(pmul(coord[i],coord[j]),HK[i][j]/2))
    margin=fq(s.Rational(raw['margin']))
    target=padd(quadratic,cubic,FP,pscale(qP,-support),pscale(sq(TP),-margin))
    # This integral feature coefficient map is the same at all parameters.
    features=[tuple(pw) for pw in raw['feature_powers']]
    entries=[(int(i),int(j)) for i,j,co in raw['gram_entries']]
    rowpowers=[tuple(pw) for pw in raw['active_monomial_powers']]
    pivots=raw['pivot_columns'];assert len(set(pivots))==len(pivots)
    vals=[None]*len(entries)
    for column,(i,j,co) in enumerate(raw['gram_entries']):
        if column not in pivots:
            expr=s.sympify(co,locals={'t':t});assert not expr.has(t)
            vals[column]=I(fq(expr))
    for pw,pivot in zip(rowpowers,pivots):
        others=I(0)
        for column,(i,j) in enumerate(entries):
            power=tuple(a+b for a,b in zip(features[i],features[j]))
            if power==pw and column!=pivot:
                assert vals[column] is not None
                others+=vals[column]*(1 if i==j else 2)
        i,j=entries[pivot]
        assert tuple(a+b for a,b in zip(features[i],features[j]))==pw
        vals[pivot]=(target.get(pw,I(0))-others)/(1 if i==j else 2)
    assert all(value is not None for value in vals)
    GI=[[I(0) for _ in range(13)] for _ in range(13)]
    for (i,j),value in zip(entries,vals):GI[i][j]=GI[j][i]=value
    diag=interval_ldl(GI)
    certificate={'tau_interval':[str(U.lo),str(U.hi)],'radius':'2^(-206)',
        'acoustic_root_interval':[str(root.lo),str(root.hi)],
        'outward_dyadic_bits':BITS,'margin':str(margin),
        'generic_missing_monomials_exact':True,
        'fixed_integral_coefficient_map':True,
        'positive_LDL_pivot_bounds':[str(value.lo) for value in diag],
        'positive_definiteness_uniform_exact':True,
        'gram_family':'Rational free entries fixed as in support_gram.json; each listed pivot solves its active monomial coefficient exactly.',
        'scope':'Global minor support with quartic gap at all four acoustic planes, for every parameter in the inherited arc. Does not prove general-mean quantitative rigidity.',
        'seconds':time.perf_counter()-started}
    (OUT/'arc_support_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps({'uniform_interval_LDL_positive':True,'radius':'2^(-206)',
        'margin':str(margin),'minimum_pivot_lower_bound':float(min(value.lo for value in diag)),
        'seconds':certificate['seconds']},indent=2),flush=True)

if __name__=='__main__':main()
