"""Exact witnesses for rank-one jet closure and its precision boundaries.

Python standard library only. All arithmetic is Fraction. A truncated formal
power-series calculation obtains the native 3-jet independently of the
claimed gradient/Hessian closure. No data here are physical measurements.
"""
from pathlib import Path
from fractions import Fraction as F
from math import factorial, isqrt
import json
from itertools import product

ZERO=(0,0,0)
class P:
    """Three-variable power series through total degree three."""
    def __init__(self,v=0):
        self.c=dict(v) if isinstance(v,dict) else ({ZERO:F(v)} if v else {})
        self.c={k:F(x) for k,x in self.c.items() if x and sum(k)<=3}
    def __add__(self,v):
        v=asP(v); out=self.c.copy()
        for k,x in v.c.items():out[k]=out.get(k,F(0))+x
        return P(out)
    __radd__=__add__
    def __neg__(self):return P({k:-x for k,x in self.c.items()})
    def __sub__(self,v):return self+-asP(v)
    def __rsub__(self,v):return asP(v)+-self
    def __mul__(self,v):
        v=asP(v);out={}
        for k,x in self.c.items():
            for l,y in v.c.items():
                e=tuple(a+b for a,b in zip(k,l))
                if sum(e)<=3:out[e]=out.get(e,F(0))+x*y
        return P(out)
    __rmul__=__mul__
    def inv(self):
        a=self.c.get(ZERO,F(0));assert a
        q=-(self-a)*(1/a);total=P(1);power=P(1)
        for _ in range(3):power=power*q;total=total+power
        return total*(1/a)
    def __truediv__(self,v):return self*asP(v).inv()
    def __rtruediv__(self,v):return asP(v)*self.inv()
    def derivative(self,*indices):
        e=[0,0,0]
        for i in indices:e[i]+=1
        val=self.c.get(tuple(e),F(0))
        for a in e:val*=factorial(a)
        return val

def asP(v):return v if isinstance(v,P) else P(v)
def variable(i,x=0):
    e=[0,0,0];e[i]=1
    return P({ZERO:F(x),tuple(e):F(1)})
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def transpose(A):return [list(c) for c in zip(*A)]
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def add(A,B):return [[a+b for a,b in zip(ar,br)] for ar,br in zip(A,B)]
def diag(v):return [[(a if i==j else 0) for j in range(len(v))] for i,a in enumerate(v)]
def inv(A):
    n=len(A); W=[list(row)+I for row,I in zip(A,eye(n))]
    for k in range(n):
        # All calls are SPD or a diagonally scaled SPD, so these pivots exist.
        q=W[k][k];W[k]=[a/q for a in W[k]]
        for i in range(n):
            if i==k:continue
            q=W[i][k];W[i]=[a-q*b for a,b in zip(W[i],W[k])]
    return [r[n:] for r in W]
def determinant(A):
    W=[r[:] for r in A];out=F(1)
    for k in range(len(W)):
        q=W[k][k];assert q;out*=q
        for i in range(k+1,len(W)):
            f=W[i][k]/q
            for j in range(k,len(W)):W[i][j]-=f*W[k][j]
    return out

def native(B,g,u):
    # Profile hidden energy directly, without response-quotient formulas.
    d=len(B); n=len(g); U=diag(u);bv=mm(mm(B,U),[[a] for a in g])
    M=add(eye(d),mm(mm(B,U),transpose(B)))
    return 1+sum(ui*gi*gi for ui,gi in zip(u,g))-mm(mm(transpose(bv),inv(M)),bv)[0][0]
def square_root(x):
    a,b=isqrt(x.numerator),isqrt(x.denominator)
    assert a*a==x.numerator and b*b==x.denominator
    return F(a,b)
def valstr(x):return str(x)

def main():
    B=[[F(1),F(1,3),F(-1,2)],[F(1,4),F(-2,3),F(1,5)]]
    g=[F(1),F(2,3),F(-1,2)]
    x=[F(1,10),F(1,9),F(1,8)]
    f=native(B,g,[variable(i,a) for i,a in enumerate(x)])
    p=[f.derivative(i) for i in range(3)]
    H=[[f.derivative(i,j) for j in range(3)] for i in range(3)]
    r=[square_root(a) for a in p]
    K=[[-H[i][j]/(2*r[i]*r[j]) for j in range(3)] for i in range(3)]
    points=[]
    for y in [[0,0,0],[F(1,2),0,0],[0,F(1,3),F(1,4)],[F(1,5)]*3]:
        D=diag([a-b for a,b in zip(y,x)])
        pred=f.derivative()+mm(mm(mm([r],D),inv(add(eye(3),mm(K,D)))),[[a] for a in r])[0][0]
        actual=native(B,g,y)
        assert pred==actual
        points.append({'point':list(map(str,y)),'value':str(actual)})
    for i,j,k in product(range(3),repeat=3):
        rhs=H[i][j]*H[i][k]/(2*p[i])+H[i][j]*H[j][k]/(2*p[j])+H[i][k]*H[j][k]/(2*p[k])
        assert f.derivative(i,j,k)==rhs
    def jet(f):
        return [f.derivative(),f.derivative(0),f.derivative(1),f.derivative(0,0),f.derivative(0,1),f.derivative(1,1)]
    darks=[native([[1,a]],[1,0],[variable(0),variable(1)]) for a in [F(1,2),F(1)]]
    dark_jets=[jet(z) for z in darks]
    assert dark_jets[0]==dark_jets[1]
    target=[F(1,2),F(1,2)]
    gap=native([[1,1]],[1,0],target)-native([[1,F(1,2)]],[1,0],target)
    assert gap==F(3,104)
    near=[]
    for e in [F(1,10),F(1,1000),F(1,10**6)]:
        fs=[native([[1,a]],[1,e],[variable(0),variable(1)]) for a in [F(1,2),F(1)]]
        maxerr=max(abs(a-b) for a,b in zip(jet(fs[0]),jet(fs[1])))
        d=native([[1,1]],[1,e],target)-native([[1,F(1,2)]],[1,e],target)
        near.append({'epsilon':str(e),'max_jet_difference':str(maxerr),'task_difference':str(d),'task_difference_float':float(d)})
    u=variable(0)
    fa=F(1,2)*u/(1+u/4)+F(1,2)*u/(1+3*u/4)
    fb=u/(1+u/2)
    ja=[fa.derivative(*([0]*k)) for k in range(3)]
    jb=[fb.derivative(*([0]*k)) for k in range(3)]
    assert ja==jb
    r2gap=F(1,2)/(1+F(1,4))+F(1,2)/(1+F(3,4))-1/(1+F(1,2))
    assert r2gap==F(2,105)
    chains=[];delta=F(1);h=delta/2;b=F(1,4)
    for m,n in [(2,64),(3,256),(4,256),(6,1024)]:
        Kc=eye(m)
        for i in range(m-1):Kc[i][i+1]=Kc[i+1][i]=b
        # SPD by strict symmetric diagonal dominance, confirmed principal minors.
        assert all(determinant([r[:j] for r in Kc[:j]])>0 for j in range(1,m+1))
        gc=[[F(i==0)] for i in range(m)]
        t=delta/(2*n)
        Mb=add(eye(m),[[t*a for a in row] for row in Kc])
        rb=mm(inv(Mb),gc)
        assert rb[-1][0]==(-b*t)**(m-1)/determinant(Mb)
        pb=rb[-1][0]**2
        tp=delta/(2*(m-1))
        Up=diag([tp]*(m-1)+[F(0)])
        Mp=add(eye(m),mm(Kc,Up));rp=mm(inv(Mp),gc)
        small=add(eye(m-1),[[tp*a for a in row[:m-1]] for row in Kc[:m-1]])
        assert rp[-1][0]==(-b*tp)**(m-1)/determinant(small)
        pp=rp[-1][0]**2
        Kb=mm(inv(Mb),Kc);Kp=mm(inv(Mp),Kc)
        incb=h*pb/(1+h*Kb[-1][-1]);incp=h*pp/(1+h*Kp[-1][-1])
        chains.append({'m':m,'n':n,'balanced_end_gradient':str(pb),
                       'balanced_added_dose_response':str(incb),'balanced_added_dose_float':float(incb),
                       'concentrated_added_dose_response':str(incp),'concentrated_added_dose_float':float(incp),
                       'response_ratio':str(incp/incb),'response_ratio_float':float(incp/incb)})
    # Projected-quotient certificate at a nonzero anchor, including signed d.
    Bproj=[[F(1),F(0),F(3,5)],[F(0),F(1),F(4,5)]]
    gproj=[F(1),F(2,3),F(1,2)]
    anchor=[F(3),F(0),F(0)]  # delta=4, kappa=1; Mx=diag(4,1).
    Cproj=[[F(1,2),F(0),F(3,10)],[F(0),F(1),F(4,5)]]
    rproj=[F(1,4),F(2,3),F(1,20)]
    Jx=native(Bproj,gproj,anchor)
    projected=[]
    for target in [[0,0,0],[0,2,2],[2,1,1],[F(1,2),F(1,4),F(3,4)]]:
        dd=[F(a)-b for a,b in zip(target,anchor)]
        aa=1+sum(d*c*c for d,c in zip(dd,Cproj[0]))
        bb=sum(d*c*r for d,c,r in zip(dd,Cproj[0],rproj))
        assert aa>=F(1,5)
        zz=-bb/aa
        rhat=[r+c*zz for r,c in zip(rproj,Cproj[0])]
        restricted=Jx+sum(d*r*r for d,r in zip(dd,rproj))-bb*bb/aa
        actual=native(Bproj,gproj,list(map(F,target)))
        bound=5*sum(abs(d)*abs(r)*abs(c) for d,r,c in zip(dd,rhat,Cproj[1]))**2
        assert F(0)<=restricted-actual<=bound
        projected.append({'target':list(map(str,target)),'signed_displacement':list(map(str,dd)),
                          'actual_error':str(restricted-actual),'certificate':str(bound)})
    result={'scope':'Exact algebraic witnesses and formula checks; no physical acquisition, rank test, shot-noise law or general algorithmic lower bound.',
            'rank_one_reconstruction_points':points,'third_partial_checks':27,
            'dark_equal_two_jet':list(map(str,dark_jets[0])),'dark_task_gap':str(gap),
            'near_dark_sequence':near,'rank_two_equal_jet':list(map(str,ja)),
            'rank_two_task_gap':str(r2gap),'chains':chains,'projected_model_certificates':projected}
    Path(__file__).with_name('JET_CLOSURE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
