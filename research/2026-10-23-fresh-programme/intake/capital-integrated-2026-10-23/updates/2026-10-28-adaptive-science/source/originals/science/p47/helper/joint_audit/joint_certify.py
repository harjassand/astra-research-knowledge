"""Exact all-frequency joint compliance/stiffness certificate.

Uses the elementary outward interval arithmetic in certify.py. The existence
proof is nested scalar root isolation with a derivative enclosure, followed by
an entire-series Descartes count (finite coefficients + uniform tail bound).
"""
from fractions import Fraction as Q
from pathlib import Path
from certify import I, endpoints, bose, band, dual, conductance

C=Q(1,20);KAP=Q(1001,50)

def data(delta,H):
    A=4-delta;B=2*H/(H+delta)
    den=B*((1+C)/2-1/B+delta/(H*(H+delta)))
    t=(A-B)/den
    c=(B*t+(t+A)*(H+delta)-t*H)/4
    kap=t+H-c
    return A,B,t,c,kap

def kprime(delta,H):
    A,B,t,c,kap=data(delta,H)
    Bp=-2*H/(H+delta)**2
    qq=(1+C)/2-1/B+delta/(H*(H+delta))
    qp=Bp/(B*B)+1/(H+delta)**2
    den=B*qq;dp=Bp*qq+B*qp
    tp=((-1-Bp)*den-(A-B)*dp)/(den*den)
    cp=(Bp*t+B*tp+(tp-1)*(H+delta)+(t+A)-tp*H)/4
    return tp-cp

def hprime(delta,H):
    A,B,t,c,kap=data(delta,H)
    Bh=2*delta/(H+delta)**2
    qq=(1+C)/2-1/B+delta/(H*(H+delta))
    qh=Bh/(B*B)-delta*(2*H+delta)/(H*H*(H+delta)**2)
    den=B*qq;dp=Bh*qq+B*qh
    th=(-Bh*den-(A-B)*dp)/(den*den)
    ch=(Bh*t+B*th+delta*th+A)/4
    return th+1-ch

def edata(delta,H):
    A,B,t,c,kap=data(delta,H)
    ee=list(endpoints(t,A,B))+[H.sqrt(),(H+delta).sqrt()]
    return ee,kap

def fit(ee):
    z=[w*w for w in ee[:4]];h=[w**3*bose(w) for w in ee[:4]]
    d1=[(h[i+1]-h[i])/(z[i+1]-z[i]) for i in range(3)]
    d2=[(d1[i+1]-d1[i])/(z[i+2]-z[i]) for i in range(2)]
    d3=(d2[1]-d2[0])/(z[3]-z[0])
    b=-d3
    a=-d2[0]+d3*(z[0]+z[1]+z[2])
    la=-d1[0]+d2[0]*(z[0]+z[1])-d3*(z[0]*z[1]+z[0]*z[2]+z[1]*z[2])
    nu=-h[0]+d1[0]*z[0]-d2[0]*z[0]*z[1]+d3*z[0]*z[1]*z[2]
    last=ee[-1]
    f5=last**3*bose(last)+nu+la*last**2+a*last**4+b*last**6
    return (nu,la,a,b),f5

def isolate_delta(h):
    H=Q(h);lo=Q('0.00577');hi=Q('0.00578')
    assert data(lo,H)[-1]<KAP<data(hi,H)[-1]
    for _ in range(220):
        md=(lo+hi)/2
        if data(md,H)[-1]<KAP:lo=md
        else:hi=md
    return I(lo,hi)

def run():
    hlo='73.33846366923165';hhi='73.33846366923166'
    Hb=I(hlo,hhi)
    broad=I('0.00577','0.00578')
    # Unique continuous delta(H) throughout the H interval.
    assert (I(KAP)-data(I('0.00577'),Hb)[-1]).pos()
    assert (data(I('0.00578'),Hb)[-1]-KAP).pos()
    assert kprime(broad,Hb).pos() and hprime(broad,Hb).pos()
    dl=isolate_delta(hlo);dh=isolate_delta(hhi)
    # Positive kappa_H implies delta(H) decreases, so endpoints bound it.
    db=I(dh.lo,dl.hi,raw=True)
    el,kl=edata(dl,I(hlo));eh,kh=edata(dh,I(hhi))
    cl,fl=fit(el);ch,fh=fit(eh)
    assert fl.neg() and fh.pos()
    # IVT gives a root on this branch. Every remaining enclosure applies there.
    ee,kap=edata(db,Hb);cf,ff=fit(ee)
    nu,la,a,b=cf
    assert nu.neg() and b.pos()
    assert all((ee[j+1]-ee[j]).pos() for j in range(4))
    # Q(w)=w^3 +nu*sinh^2(w)/w^2 +la*sinh^2(w)
    #      +a*w^2*sinh^2(w)+b*w^4*sinh^2(w).
    # The odd cubic has positive coefficient. Check every even coefficient
    # until a uniform positive-tail bound takes over.
    import math
    def dn(j):return Q(2**(2*j-1),math.factorial(2*j)) if j>=1 else Q(0)
    cs=[]
    for n in range(18):
        coef=nu*dn(n+1)+la*dn(n)+a*dn(n-1)+b*dn(n-2)
        assert coef.pos() or coef.neg()
        cs.append(coef)
    expected=[-1]*6+[1]*3+[-1]*4+[1]*5
    assert [1 if q.pos() else -1 for q in cs]==expected
    # For n>=18: la>0 can be dropped, negative a/nu terms decrease in
    # magnitude. This bound is thus valid over the entire infinite tail.
    assert la.pos() and a.neg()
    n=18;U=(2*n-2)*(2*n-3);V=U*(2*n)*(2*n-1);W=V*(2*n+2)*(2*n+1)
    tailbound=b+4*a/U+64*nu/W
    assert tailbound.pos()
    signs=[]
    for n in range(18):
        signs.append(1 if cs[n].pos() else -1)
        if n==1:signs.append(1) # cubic term between x^2 and x^4
    changes=sum(u!=v for u,v in zip(signs,signs[1:]))
    assert changes==5
    # Thus exactly the five prescribed roots exhaust the Descartes bound.
    A,B,t,c,kap=data(db,Hb)
    d=B*t*(Hb+db)/4
    sq=(c*c-4*d).sqrt();s1=(c-sq)/2;s2=(c+sq)/2
    k1=(t*Hb-d-kap*s1)/(s2-s1);k2=kap-k1
    m1=k1/s1;m2=k2/s2
    assert all(v.pos() for v in [s1,s2,k1,k2,m1,m2])
    jj=band(0,ee[0])+band(ee[1],ee[2])+band(ee[3],ee[4])
    jp=conductance(endpoints(40))
    assert (jp-jj).pos()
    lines=['# Joint compliance and finite-stiffness global certificate','',
           'Original physical masses m=1,M=2, intercell K=1, theta=1/2.',
           'Both charged budgets: C_CM<=1/20 and total internal spring sum<=1001/50.',
           'A unique active-spectrum finite optimum is certified below.','']
    def show(n,v):lines.append(n+' = '+v.fmt())
    for n,v in [('delta_root',db),('H_root',Hb),('kappa_delta_derivative_on_box',kprime(db,Hb)),
                ('F5_at_lower_H',fl),('F5_at_upper_H',fh),('nu',nu),('lambda',la),('a',a),('b',b),
                ('p',ee[0]),('r',ee[1]),('s',ee[2]),('u',ee[3]),('v',ee[4]),
                ('branch_mass_1',m1),('branch_mass_2',m2),('branch_spring_1',k1),
                ('branch_spring_2',k2),('kappa_interval',kap),('J_joint_optimum',jj),
                ('optimized_pendant_minus_joint',jp-jj),('uniform_even_tail_lower_bound',tailbound)]:show(n,v)
    lines+=['','Even coefficient signs for n=0..17: '+str(expected),
            'The additional cubic coefficient is positive; full sign changes = '+str(changes)+'.',
            'All even coefficients n>=18 are positive by the displayed uniform tail bound.',
            'Five distinct endpoint roots + Descartes => exact all-frequency occupied-band signs.',
            'Exact budgets hold at the IVT-defined root; interval widths reflect the enclosing box.',
            'PASS: positive finite star, nested exact root existence, full Bose integral,',
            'correct budget multipliers and complete all-frequency sign certificate.','']
    return '\n'.join(lines)

if __name__=='__main__':
    out=run();Path(__file__).with_name('JOINT_CERTIFICATE.md').write_text(out);print(out)
