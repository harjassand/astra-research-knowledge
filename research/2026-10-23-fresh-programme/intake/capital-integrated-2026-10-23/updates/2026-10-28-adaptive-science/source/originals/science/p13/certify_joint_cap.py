"""All-frequency 3-band candidate: C<=1/20 and total springs<=24.

This exact rational interval computation certifies the existence of a
positive finite star and the coefficient signs used by JOINT_CAP_PROOF.md.
"""
from fractions import Fraction as Q
from pathlib import Path
from intervals import I,sqrt,bose,full_conductance

HERE=Path(__file__).resolve().parent
C=Q(1,20);KAPPA=24

def poly(coeff,x):
    ans=I(0)
    for c in coeff:ans=ans*x+c
    return ans

def root(coeff,lo,hi):
    lo,hi=Q(lo),Q(hi)
    a,b=poly(coeff,I(lo)),poly(coeff,I(hi))
    assert (a.hi<0<b.lo) or (b.hi<0<a.lo)
    positive=a.lo>0
    for _ in range(245):
        mid=(lo+hi)/2;v=poly(coeff,I(mid))
        if v.lo<=0<=v.hi:break
        if (v.lo>0)==positive:lo=mid
        else:hi=mid
    return I(lo,hi)

def interpolate(edges):
    nodes=[w*w for w in edges[:4]]
    vals=[w**3*bose(w) for w in edges[:4]]
    c=[I(0)for _ in range(4)]
    for i in range(4):
        coeff=[I(1)];den=I(1)
        for j in range(4):
            if i==j:continue
            nxt=[I(0)for _ in range(len(coeff)+1)]
            for l,v in enumerate(coeff):nxt[l]-=v*nodes[j];nxt[l+1]+=v
            coeff=nxt;den*=nodes[i]-nodes[j]
        t=vals[i]/den
        for l in range(4):c[l]+=t*coeff[l]
    return -c[1],-c[2]/2,-c[3]/4,c[0]

def design(h,Ccap=C,kappa=KAPPA):
    h=h if isinstance(h,I)else I(h);b=1-h
    H=(Ccap*kappa-1+2*h+sqrt((1-2*h-Ccap*kappa)**2-4*Ccap*kappa*h*h))/(2*Ccap)
    k=kappa-H
    return components(h,H,k)

def components(h,H,k):
    h=h if isinstance(h,I) else I(h)
    H=H if isinstance(H,I) else I(H)
    k=k if isinstance(k,I) else I(k)
    b=1-h
    tr=H*(1+1/h)+k*(1+1/b)
    pair=2*H*k/(h*b)
    d=sqrt(tr*tr-4*pair)
    a1=2*pair/(tr+d);a2=(tr+d)/2
    coeff=[I(1),-(tr+4),pair+4*(H/h+k/b),-4*H*k/(h*b)]
    beta=[root(coeff,0,a1.lo),root(coeff,a1.hi,a2.lo),root(coeff,a2.hi,(tr+4).hi)]
    assert 0<beta[0].lo<beta[0].hi<a1.lo<a1.hi<beta[1].lo
    assert beta[1].hi<a2.lo<a2.hi<beta[2].lo
    edges=[sqrt(beta[0]),sqrt(a1),sqrt(beta[1]),sqrt(a2),sqrt(beta[2])]
    lm,mu,nu,eta=interpolate(edges)
    w=edges[4]
    residual=w**3*bose(w)+lm*w*w+2*mu*w**4+4*nu*w**6-eta
    return dict(h=h,b=b,H=H,k=k,edges=edges,lambda_=lm,mu=mu,nu=nu,eta=eta,res=residual)

def main():
    lo=Q('0.06552741459340005487388219669883060107690')
    hi=Q('0.06552741459340005487388219669883060107692')
    left,right=design(lo),design(hi)
    assert left['res'].lo>0>right['res'].hi
    row=design(I(lo,hi))
    assert row['h'].lo>0 and row['b'].lo>0 and row['H'].lo>0 and row['k'].lo>0
    lam,mu,nu,eta=[row[k]for k in ['lambda_','mu','nu','eta']]
    assert eta.lo>0 and nu.lo>0 and mu.hi<0
    B=[]
    for n in range(1,15):
        if n==1:v=lam-eta/3
        else:
            v=lam+mu*n*(2*n-1)-4*eta/((2*n+2)*(2*n+1))
            if n>=3:v+=nu*n*(n-1)*(2*n-1)*(2*n-3)
        B.append(v)
    expected=[-1]*5+[1]*4+[-1]*4+[1]
    assert all(v.hi<0 if sign<0 else v.lo>0 for v,sign in zip(B,expected))
    # P(n)=lambda+mu*n*(2n-1)+nu*n*(n-1)*(2n-1)*(2n-3).
    # P'''(n)=nu*(96n-72)>0 for n>=14. These two checks ensure
    # P'>0 thereafter; the remaining negative eta term increases too.
    Pp14=mu*55+nu*(16*14**3-36*14**2+22*14-3)
    Ppp14=4*mu+nu*(48*14**2-72*14+22)
    assert Pp14.lo>0 and Ppp14.lo>0
    J=full_conductance(row['edges'])
    lines=['PASS: exact existence bracket + five-root all-frequency certificate.',
           'C_CM=1/20, total internal stiffness=24, actual m=1,M=2,K=1.',
           'Fifth-edge residual at h_lo '+left['res'].decimal(52),
           'Fifth-edge residual at h_hi '+right['res'].decimal(52)]
    for k in ['h','b','H','k','lambda_','mu','nu','eta']:lines.append(k+' '+row[k].decimal())
    lines += ['positive edges:']+[v.decimal()for v in row['edges']]
    lines += ['J_joint_optimum '+J.decimal()]
    lines += [f'B{n+1} '+v.decimal()for n,v in enumerate(B)]
    lines += ['P_prime(14) '+Pp14.decimal(),
              'P_second(14) '+Ppp14.decimal(),
              'PASS: all B_n for n>=14 strictly positive; exactly five total',
              'coefficient sign variations after inserting constant and +w^3.']
    text='\n'.join(lines)+'\n'
    (HERE/'CERTIFIED_JOINT_CAP.txt').write_text(text)
    print(text)

if __name__=='__main__':main()
