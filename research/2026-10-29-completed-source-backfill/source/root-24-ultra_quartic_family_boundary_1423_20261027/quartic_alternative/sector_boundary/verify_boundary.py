"""Read-only exact replay from literal formulas and final JSON; stdlib only."""
from fractions import Fraction as F
from itertools import combinations_with_replacement as cwr, permutations
from pathlib import Path
import argparse,hashlib,json,time


class Q:
    """The real field Q(sqrt42); no floating point or interval oracle."""
    __slots__=('a','b')
    def __init__(self,a=0,b=0):
        if isinstance(a,Q):self.a,self.b=a.a,a.b
        else:self.a,self.b=F(a),F(b)
    def __add__(self,x):
        x=Q(x);return Q(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self):return Q(-self.a,-self.b)
    def __sub__(self,x):return self+-Q(x)
    def __rsub__(self,x):return Q(x)+-self
    def __mul__(self,x):
        x=Q(x);return Q(self.a*x.a+42*self.b*x.b,self.a*x.b+self.b*x.a)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=Q(x);d=x.a*x.a-42*x.b*x.b;assert d
        return self*Q(x.a/d,-x.b/d)
    def __pow__(self,n):
        assert n>=0;y=Q(1);x=self
        while n:
            if n&1:y=y*x
            x=x*x;n//=2
        return y
    def __bool__(self):return bool(self.a or self.b)
    def __eq__(self,x):
        x=Q(x);return self.a==x.a and self.b==x.b
    def positive(self):
        a,b=self.a,self.b
        if not b:return a>0
        if not a:return b>0
        if a>0 and b>0:return True
        if a<0 and b<0:return False
        return a*a>42*b*b if a>0 else 42*b*b>a*a
    def pair(self):return [str(self.a),str(self.b)]


N=9
def clean(p):return {e:c for e,c in p.items() if c}
def add(*ps):
    out={}
    for p in ps:
        for e,c in p.items():out[e]=out.get(e,Q())+c
    return clean(out)
def scale(p,c):return clean({e:v*c for e,v in p.items()})
def mul(p,q):
    out={}
    for e,c in p.items():
        for f,d in q.items():
            g=tuple(i+j for i,j in zip(e,f));out[g]=out.get(g,Q())+c*d
    return clean(out)
def product(ps):
    out=const(1)
    for p in ps:out=mul(out,p)
    return out
def power(p,n):return product([p]*n)
def const(c):return clean({(0,)*N:Q(c)})
def var(j):
    e=[0]*N;e[j]=1;return {tuple(e):Q(1)}
def diff(p,j):
    out={}
    for e,c in p.items():
        if e[j]:
            f=list(e);f[j]-=1;out[tuple(f)]=c*e[j]
    return out
def inv(y):
    a,b,c,d=y
    return (add(mul(a,a),mul(c,c)),add(mul(b,b),mul(d,d)),
            add(mul(a,b),mul(c,d)),add(mul(a,d),scale(mul(b,c),-1)))
def energy(y,tau):
    u,v,w,q=inv(y)
    return add(mul(u,u),mul(v,v),scale(mul(w,w),3),mul(tau,mul(q,q)),
               scale(mul(q,add(u,scale(v,-1))),4))
def cmul(p,q):
    return (add(mul(p[0],q[0]),scale(mul(p[1],q[1]),-1)),
            add(mul(p[0],q[1]),mul(p[1],q[0])))
def cprod(ps):
    z=(const(1),{})
    for p in ps:z=cmul(z,p)
    return z
def conjugate(p):return p[0],scale(p[1],-1)
def phase(p,k):
    for j in range(k%4):p=scale(p[1],-1),p[0]
    return p
def complex_blocks(a,x):
    ac=[(a[0],a[2]),(a[1],a[3])];xc=[(x[0],x[2]),(x[1],x[3])]
    one=[phase(cprod([ac[i],xc[j],conjugate(xc[k])]),i+j+k)
         for i in range(2) for j in range(2) for k in range(2)]
    one += [phase(cprod([conjugate(ac[i]),xc[j],xc[k]]),i+j+k)
            for i in range(2) for j,k in cwr(range(2),2)]
    one += [phase(cprod([xc[i],xc[j],conjugate(xc[k])]),i+j+k)
            for i,j in cwr(range(2),2) for k in range(2)]
    three=[phase(cprod([ac[i],xc[j],xc[k]]),i+j+k)
           for i in range(2) for j,k in cwr(range(2),2)]
    three += [phase(cprod([xc[i],xc[j],xc[k]]),i+j+k) for i,j,k in cwr(range(2),3)]
    return [one,three]
def ldl(A):
    n=len(A);L=[[Q(i==j) for j in range(n)] for i in range(n)];D=[]
    for j in range(n):
        d=A[j][j]-sum((L[j][k]**2*D[k] for k in range(j)),Q())
        assert d.positive(),(j,d.pair());D.append(d)
        for i in range(j+1,n):
            L[i][j]=(A[i][j]-sum((L[i][k]*D[k]*L[j][k] for k in range(j)),Q()))/d
    assert all(A[i][j]==sum((L[i][k]*D[k]*L[j][k] for k in range(n)),Q())
               for i in range(n) for j in range(n))
    return D
def determinant(A):
    out={};n=len(A)
    for p in permutations(range(n)):
        sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        out=add(out,scale(product([A[i][p[i]] for i in range(n)]),sign))
    return out
def reduce_critical_z(p,mc):
    assert all(all(e[j]==0 for j in range(N) if j!=4) for e in p)
    d={e[4]:c for e,c in p.items()}
    for k in range(max(d,default=-1),3,-1):
        c=d.pop(k,Q())
        if c:
            d[k-2]=d.get(k-2,Q())+c*mc
            d[k-4]=d.get(k-4,Q())-c
    return clean({tuple(k if j==4 else 0 for j in range(N)):c for k,c in d.items()})
def acoustic(tau,z):
    zero=const(0);c=const;t2=scale(tau,2)
    m11=[[c(12),zero,zero,c(12)],[zero,c(6),c(-4),zero],
         [zero,c(-4),c(4),zero],[c(12),zero,zero,t2]]
    m12=[[zero,c(6),c(-4),zero],[c(6),zero,zero,c(-4)],
         [c(-4),zero,zero,add(c(3),scale(tau,-1))],
         [zero,c(-4),add(c(3),scale(tau,-1)),zero]]
    m22=[[c(6),zero,zero,c(-4)],[zero,c(12),c(12),zero],
         [zero,c(12),t2,zero],[c(-4),zero,zero,c(4)]]
    return [[add(m11[i][j],scale(mul(z,m12[i][j]),2),mul(mul(z,z),m22[i][j]))
             for j in range(4)] for i in range(4)]


def main(write=False):
    start=time.monotonic();root=Path(__file__).resolve().parent
    path=root/'EXACT_BOUNDARY_SUPPORT.json';raw=path.read_bytes();cert=json.loads(raw)
    tau0=Q(89,-12);assert Q(*cert['tau'])==tau0
    a=[var(i) for i in range(4)];x=[var(i+4) for i in range(4)]
    f=energy(a,const(tau0));u,v,w,q=inv(a);qx=inv(x)[3]
    alpha=Q(*cert['selector_alpha']);delta=Q(*cert['selector_delta'])
    selector=add(scale(add(u,scale(v,-1)),alpha),scale(q,delta))
    norm=add(*(mul(t,t) for t in x))
    target=mul(norm,add(energy([add(ai,xi) for ai,xi in zip(a,x)],const(tau0)),
                        scale(f,-1),*(scale(mul(diff(f,i),x[i]),-1) for i in range(4)),
                        scale(mul(selector,qx),-1)))
    rebuilt={};allpivots=[]
    for k,features in enumerate(complex_blocks(a,x)):
        V=[[Q(*e) for e in row] for row in cert['basis_matrices'][k]]
        S=[[Q(*e) for e in row] for row in cert['positive_blocks'][k]];n=len(S)
        assert len(V)==len(features) and all(len(row)==n for row in V)
        assert all(len(row)==n for row in S)
        assert all(S[i][j]==S[j][i] for i in range(n) for j in range(n))
        real=[add(*(scale(features[i][0],V[i][j]) for i in range(len(V)))) for j in range(n)]
        imag=[add(*(scale(features[i][1],V[i][j]) for i in range(len(V)))) for j in range(n)]
        for i in range(n):
            for j in range(i,n):
                p=add(mul(real[i],real[j]),mul(imag[i],imag[j]))
                rebuilt=add(rebuilt,scale(p,S[i][j]*(1 if i==j else 2)))
        rho=Q(F(cert['positive_shift']));assert rho==Q(F(1,200))
        D=ldl([[S[i][j]-(rho if i==j else Q()) for j in range(n)] for i in range(n)])
        assert D==[Q(*e) for e in cert['shifted_LDL_pivots'][k]]
        allpivots.extend(D)
    assert target==rebuilt
    relation=Q(162,-21)-alpha*Q(F(-3,2),F(1,3))
    assert delta==relation

    # Universal acoustic polynomial and exact one-parameter edge identities.
    t=var(8);z=var(4);y=mul(z,z);Qp=acoustic(t,z);fp=energy(a,t)
    aq=add(diff(diff(fp,0),0),scale(mul(z,diff(diff(fp,0),1)),2),
           mul(y,diff(diff(fp,1),1)))
    assert aq==add(*(mul(mul(a[i],a[j]),Qp[i][j]) for i in range(4) for j in range(4)))
    det_expected=scale(add(mul(add(scale(t,4),const(-24)),add(power(y,4),const(1))),
                           mul(add(scale(t,34),const(-494)),add(power(y,3),y)),
                           mul(add(scale(t,74),const(-639)),power(y,2))),48)
    assert determinant(Qp)==det_expected
    assert determinant([row[:1] for row in Qp[:1]])==scale(add(y,const(2)),6)
    assert determinant([row[:2] for row in Qp[:2]])==scale(add(scale(power(y,2),2),y,const(2)),36)
    third=scale(add(mul(add(scale(t,6),const(-36)),power(y,3)),
                    mul(add(scale(t,3),const(-164)),power(y,2)),
                    mul(add(scale(t,6),const(66)),y),const(4)),24)
    assert determinant([row[:3] for row in Qp[:3]])==third
    mc=Q(F(-39,58),F(15,29));assert (mc-2).positive()
    Q0=acoustic(const(tau0),z)
    assert determinant(Q0)==scale(power(add(power(y,2),scale(y,-mc),const(1)),2),192*(tau0-6))
    assert tau0*tau0-178*tau0+1873==0
    assert (tau0-Q(F(1123,100))).positive() and (Q(F(59,5))-tau0).positive()
    # A positive cubic bounds the third minor below tau0, for every y>=0.
    p=lambda yy:add(scale(power(yy,3),3138),scale(power(yy,2),-13031),scale(yy,13338),const(400))
    bernstein=[Q(400),Q(9292),Q(F(2428,3)),Q(56)]
    from math import comb
    assert p(scale(z,2))==add(*(scale(mul(power(z,k),power(add(const(1),scale(z,-1)),3-k)),
                                      bernstein[k]*comb(3,k)) for k in range(4)))
    assert all(c.positive() for c in bernstein)
    assert p(add(z,const(2)))==add(scale(power(z,3),3138),scale(power(z,2),5797),scale(z,-1130),const(56))
    assert 4*5797*56-1130**2==21628>0
    # Complete-square discriminant used for the sharp necessity proof.
    aa=add(scale(t,4),const(-24));bb=add(scale(t,34),const(-494));cc=add(scale(t,66),const(-591))
    assert add(scale(mul(aa,cc),4),scale(mul(bb,bb),-1))==scale(add(power(t,2),scale(t,-178),const(1873)),-100)
    # The same exact pair supplies negative acoustic curvature for ALL lower
    # parameters, avoiding any numerical eigenvector or limiting argument.
    pair_path=root/'CRITICAL_PAIR.json';pair_raw=pair_path.read_bytes();critical=json.loads(pair_raw)
    assert Q(*critical['tau'])==tau0 and Q(*critical['critical_m'])==mc
    assert (mc-Q(F(5,2))).positive()
    A0=[add(*(scale(power(z,k),Q(*c)) for k,c in enumerate(row)))
        for row in critical['A_polynomial_coefficients']]
    assert len(A0)==4
    for i in range(4):
        assert not reduce_critical_z(add(*(mul(Q0[i][j],A0[j]) for j in range(4))),mc)
    g0=Q(*critical['cofactor_pairing_g0']);g2=Q(*critical['cofactor_pairing_g2'])
    g=reduce_critical_z(add(A0[3],scale(mul(z,A0[2]),-1)),mc)
    assert g==add(const(g0),scale(y,g2))
    assert (-g2).positive() and (-(g0+2*g2)).positive()
    h=[{}, {},scale(z,-1),const(1)]
    for i in range(4):
        for j in range(4):
            assert add(Qp[i][j],scale(Q0[i][j],-1))==scale(mul(add(t,const(-tau0)),mul(h[i],h[j])),2)
    bits=max(max(abs(c.numerator).bit_length(),c.denominator.bit_length())
             for d in allpivots for c in [d.a,d.b])
    out={'status':'EXACT_BOUNDARY_SUPPORT_AND_UNIVERSAL_ACOUSTIC_IDENTITIES_VERIFIED',
         'certificate_sha256':hashlib.sha256(raw).hexdigest(),
         'critical_pair_sha256':hashlib.sha256(pair_raw).hexdigest(),
         'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'tau_boundary':'89-12sqrt42','positive_blocks':cert['block_dimensions'],
         'shifted_positive_pivots':len(allpivots),'positive_shift':'1/200',
         'support_polynomial_nonzero_coefficients':len(target),
         'support_identity':'EXACT_LITERAL_F_RECONSTRUCTION_OVER_Q_SQRT42',
         'acoustic_formula':'EXACT_LITERAL_HESSIAN_AND_UNIVERSAL_DETERMINANT',
         'boundary_determinant':'EXACT_POSITIVE_FACTOR_TIMES_SQUARE',
         'third_minor_positivity':'EXACT_BERNSTEIN_AND_SHIFTED_QUADRATIC_CERTIFICATE',
         'fixed_lower_parameter_witness':'EXACT_KERNEL_MOD_QUARTIC_AND_NONZERO_COFACTOR_PAIRING',
         'maximum_pivot_component_bits':bits,'imports':'PYTHON_STDLIB_ONLY',
         'wall_seconds':time.monotonic()-start,
         'scope':'Finite exact facts; analytic PC/ROC/QC classification is proved in PRIMARY_PROOF.md.'}
    if write:(root/'VERIFY_BOUNDARY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write-receipt',action='store_true')
    main(parser.parse_args().write_receipt)
