"""Exact rational 2x2 minors-Jensen witness compiler; standard library only."""
from fractions import Fraction as Q
from pathlib import Path
import json

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(t,a):return tuple(t*x for x in a)
def det(a):return a[0]*a[3]-a[1]*a[2]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def l1(a):return sum(abs(x) for x in a)
def monomial(a,e):
    v=Q(1)
    for x,n in zip(a,e):v*=x**n
    return v
def evaluate(poly,a):return sum(c*monomial(a,e) for e,c in poly.items())
def derivative(poly,a):
    v=[]
    for j in range(4):
        z=Q(0)
        for e,c in poly.items():
            if e[j]:
                ee=list(e);ee[j]-=1;z+=c*e[j]*monomial(a,ee)
        v.append(z)
    return tuple(v)
def mul(p,q):
    r={}
    for a,x in p.items():
        for b,y in q.items():
            e=tuple(i+j for i,j in zip(a,b));r[e]=r.get(e,Q(0))+x*y
    return {e:c for e,c in r.items() if c}
def plus(p,q):
    r=dict(p)
    for e,c in q.items():r[e]=r.get(e,Q(0))+c
    return {e:c for e,c in r.items() if c}
def times(t,p):return {e:t*c for e,c in p.items() if t*c}
def hessian_bound(poly,a):
    r=max(Q(1),l1(a)+1)
    return sum(abs(c)*sum(e)*(sum(e)-1)*r**(sum(e)-2)
               for e,c in poly.items() if sum(e)>=2)
def encode(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    return x
def compile_pair(poly,a,x,y):
    df=derivative(poly,a)
    def b(z):return evaluate(poly,add(a,z))-evaluate(poly,a)-dot(df,z)
    d,e=det(x),-det(y)
    assert d>0 and e>0
    eta=-(b(x)+d/e*b(y))
    if eta<=0:raise ValueError('Input is not a genuine negative support pair')
    h=det(add(x,scale(-1,y)));aa=2*d/e
    w=l1(x)+aa*l1(y);hh=hessian_bound(poly,a)
    ll=2*d*abs(h)*abs(b(y))/e**2;dd=ll+2*hh*w*w
    bounds={'base':Q(1,2),'positive_third':1/(2*(1+aa))}
    if h:bounds['denominator']=e/(2*abs(h))
    if w:bounds['unit_remainder']=1/(2*w)
    if dd:bounds['negative_margin']=eta/(2*dd)
    p=Q(1);exponent=0
    while p>min(bounds.values()):p/=2;exponent+=1
    q=p*d/(e+p*h);r=1-p-q
    z=scale(-1/r,add(scale(p,x),scale(q,y)))
    weights=(p,q,r);atoms=tuple(add(a,t) for t in (x,y,z))
    assert all(t>0 for t in weights) and sum(weights)==1
    # Independent direct moment/energy checks, not Bregman approximations.
    mean=tuple(sum(t*v[j] for t,v in zip(weights,atoms)) for j in range(4))
    determinant_mean=sum(t*det(v) for t,v in zip(weights,atoms))
    actual=sum(t*evaluate(poly,v) for t,v in zip(weights,atoms))-evaluate(poly,a)
    assert mean==a and determinant_mean==det(a)
    assert actual<=-eta*p/2<0
    return {'pair_margin':eta,'H':hh,'bounds':bounds,'dyadic_exponent':exponent,
            'weights':weights,'atoms':atoms,'matrix_mean':mean,
            'determinant_mean':determinant_mean,'jensen_defect':actual,
            'proved_upper_bound':-eta*p/2,'largest_output_bit_length':max(
                max(t.numerator.bit_length(),t.denominator.bit_length())
                for t in weights+sum(atoms,())+(actual,))}
def scale_cut(poly,a,r):
    f=evaluate(poly,r);df=derivative(poly,r)
    assert f>0
    t=-dot(df,a)/(2*f)
    assert t
    return scale(t,r),t
def main():
    norm2={tuple(2 if j==i else 0 for j in range(4)):Q(1) for i in range(4)}
    determinant={(1,0,0,1):Q(1),(0,1,1,0):Q(-1)}
    uv_difference={(2,0,0,0):Q(1),(0,0,2,0):Q(1),
                   (0,2,0,0):Q(-1),(0,0,0,2):Q(-1)}
    norm4=mul(norm2,norm2)
    target=plus(plus(norm4,times(Q(252,25),mul(determinant,determinant))),
                times(Q(99,25),mul(determinant,uv_difference)))
    a=tuple(map(Q,(36,0,0,35)))
    rp=tuple(map(Q,(0,55,-4,0)));rm=tuple(map(Q,(1,0,0,-2)))
    # If the minimizing scale vanishes, a rational perturbation would be needed.
    # For the positive cut here DF(Rp):A=0, use small nonzero rational scale.
    fp=evaluate(target,rp); dp=dot(derivative(target,rp),a)
    fm=evaluate(target,rm); dm=dot(derivative(target,rm),a)
    tm=-dm/(2*fm)
    # The exact negative interval gap survives sufficiently small nonzero tp.
    tp=Q(1,1024)
    report={'even_hopf_target':compile_pair(target,a,scale(tp,rp),scale(tm,rm))}
    report['even_hopf_target']['increment_scales']=(tp,tm)
    report['even_hopf_target']['positive_cut_linear_coefficient']=dp
    dm_poly=plus(norm4,times(Q(-9,4),mul(norm2,determinant)))
    coercive=plus(dm_poly,times(Q(1,1000000),mul(norm4,norm2)))
    zero=(Q(0),)*4;x=tuple(map(Q,(5,0,0,5)));y=tuple(map(Q,(1,0,0,-1)))
    report['dm_control']=compile_pair(dm_poly,zero,x,y)
    report['coercive_control']=compile_pair(coercive,zero,x,y)
    try:compile_pair(norm4,zero,x,y)
    except ValueError:report['positive_control']='CORRECTLY_REJECTED'
    else:raise AssertionError('False positive')
    Path(__file__).with_name('EXACT_WITNESSES.json').write_text(json.dumps(encode(report),indent=2)+'\n')
    for name,data in report.items():
        if isinstance(data,dict):
            print(name,'eta',float(data['pair_margin']),'p=2^-',data['dyadic_exponent'],
                  'J',float(data['jensen_defect']),'maxbits',data['largest_output_bit_length'])
        else:print(name,data)
if __name__=='__main__':main()
