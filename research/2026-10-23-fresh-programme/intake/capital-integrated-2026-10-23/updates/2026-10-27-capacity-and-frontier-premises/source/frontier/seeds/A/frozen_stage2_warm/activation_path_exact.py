"""Exact full-rank PPT activation and a block-zero escape polynomial.
Auxiliary operator only: NOT a tensor-power Werner counterexample.
"""
from fractions import Fraction as F
from itertools import product, combinations
import json


def dd(a,b):return int(a==b)

def ii(a,b,c,d):return dd(a,c)*dd(b,d)

def ff(a,b,c,d):return dd(a,d)*dd(b,c)

def pp(a,b,c,d,dimen):return F(dd(a,b)*dd(c,d),dimen)

def sigma(a1,a2,b1,b2,c1,c2,d1,d2):
    # sigma_6 = [8 Pminus_3 tensor P2 + Pplus_3 tensor(P2+3 Q2)]/84.
    i=ii(a1,b1,c1,d1);f=ff(a1,b1,c1,d1)
    p=pp(a2,b2,c2,d2,2);j=ii(a2,b2,c2,d2)
    return (4*(i-f)*p+F(i+f,2)*(3*j-2*p))/84

def sg(a1,a2,b1,b2,c1,c2,d1,d2):return sigma(a1,a2,d1,d2,c1,c2,b1,b2)

def mixed_sg(a1,a2,b1,b2,c1,c2,d1,d2):
    ident=dd(a1,c1)*dd(a2,c2)*dd(b1,d1)*dd(b2,d2)
    return F(9,10)*sg(a1,a2,b1,b2,c1,c2,d1,d2)+F(ident,360)

def kernel(r,s):
    a0,a1,a2,b0,b1,b2=r;c0,c1,c2,d0,d1,d2=s
    k=ii(a0,b0,c0,d0)-F(dd(a0,b0)*dd(c0,d0),2)
    return k*mixed_sg(a1,a2,b1,b2,c1,c2,d1,d2)

def b(c,d):return sum(vc*vd*kernel(r,s) for r,vc in c.items() for s,vd in d.items())

def outer(x,y):return {r+s:vr*vs for r,vr in x.items() for s,vs in y.items()}

def add(*terms):
    ans={}
    for c in terms:
      for k,v in c.items():ans[k]=ans.get(k,F(0))+v
    return {k:v for k,v in ans.items() if v}

def scale(c,s):return {k:s*v for k,v in c.items()}

def q_werner(c,n=3):
    total=F(0)
    for size in range(n+1):
      for S in combinations(range(n),size):
        out={}
        for key,value in c.items():
            row,col=key[:n],key[n:]
            if all(row[i]==col[i] for i in S):
                k=tuple(row[i] for i in range(n) if i not in S)+tuple(col[i] for i in range(n) if i not in S)
                out[k]=out.get(k,F(0))+value
        total+=F(-1,2)**size*sum(v*v for v in out.values())
    return total

def main():
    # The unperturbed PPT state has three positive eigenspaces and one zero:
    # p(P3)=0,f(F2)=+1 -> 1/28;
    # p=0,f=-1 -> 0; p=1,f=+1 ->0; p=1,f=-1 ->1/7.
    tr=F(0);err=F(0)
    for a1,b1,c1,d1 in product(range(3),repeat=4):
      for a2,b2,c2,d2 in product(range(2),repeat=4):
        val=sg(a1,a2,b1,b2,c1,c2,d1,d2)
        p3=pp(a1,b1,c1,d1,3);i3=ii(a1,b1,c1,d1)
        i2=ii(a2,b2,c2,d2);f2=ff(a2,b2,c2,d2)
        rhs=F(1,56)*(i3-p3)*(i2+f2)+F(1,14)*p3*(i2-f2)
        err=max(err,abs(val-rhs))
        if (a1,a2,b1,b2)==(c1,c2,d1,d2):tr+=sigma(a1,a2,b1,b2,c1,c2,d1,d2)
    if tr!=1 or err:raise AssertionError((tr,err))
    # Base C0 has R=|2,0><2,0|; U0,V0 are its repeated two-column factors.
    u=[{(a,2,0):F(1)} for a in (0,1)]
    x=[{(i,i,a):F(1) for i in range(3)} for a in (0,1)]
    y=[{(i,i,1):F(1) for i in range(3)},{(i,i,0):F(-1) for i in range(3)}]
    c0=add(*(outer(u[a],u[a]) for a in (0,1)))
    h=add(*(outer(x[a],u[a]) for a in (0,1)),*(outer(u[a],y[a]) for a in (0,1)))
    d=add(*(outer(x[a],y[a]) for a in (0,1)))
    q0=b(c0,c0);linear=2*b(c0,h);quadratic=b(h,h)+2*b(c0,d);cubic=2*b(h,d);quartic=b(d,d)
    if q0 or linear or cubic:raise AssertionError((q0,linear,cubic))
    if quartic!=F(-73,840):raise AssertionError(quartic)
    if quadratic<=0:raise AssertionError(quadratic)
    # A rank-two factorization exists for every rational t, not merely tangent order.
    t=F(2)
    c=add(c0,scale(h,t),scale(d,t*t))
    observed=b(c,c);expected=quadratic*t*t+quartic*t**4
    if observed!=expected or observed>=0:raise AssertionError((observed,expected))
    # Compare the same exact rank-two path against the ACTUAL three-copy target.
    qh=q_werner(h);qd=q_werner(d);qz=q_werner(c0)
    actual_linear=q_werner(add(c0,h))-qz-qh
    actual_quad=qh+q_werner(add(c0,d))-qz-qd
    actual_cubic=q_werner(add(h,d))-qh-qd
    actual_value=q_werner(c)
    if qz or actual_linear or actual_cubic or qd!=F(33,2):raise AssertionError((qz,actual_linear,actual_cubic,qd))
    if actual_value!=actual_quad*t*t+qd*t**4 or actual_quad<0:raise AssertionError('actual target comparison failed')
    print(json.dumps({'scope':'Exact generalized-operator obstruction; sigma_mix is NOT a Werner tensor power',
      'sigma6_trace':str(tr),'sigma6_PPT_decomposition_entry_error':str(err),
      'epsilon':'1/10','B_and_BGamma_minimum_bound':'1/360',
      'integer_D_rank':2,'integer_D_norm_squared':str(sum(v*v for v in d.values())),
      'q_C0':str(q0),'linear':str(linear),'quadratic':str(quadratic),
      'cubic':str(cubic),'quartic':str(quartic),
      'escape_threshold_t_squared':str(-quadratic/quartic),
      't':str(t),'negative_value':str(observed),
      'actual_three_copy_quadratic':str(actual_quad),'actual_three_copy_cubic':str(actual_cubic),'actual_three_copy_quartic':str(qd),'actual_three_copy_q_at_t':str(actual_value),'normalized_D_negative_value':str(quartic/18),'normalized_Ct_negative_value':str(observed/(2*(1+3*t*t)**2))},indent=2))

if __name__=='__main__':main()
