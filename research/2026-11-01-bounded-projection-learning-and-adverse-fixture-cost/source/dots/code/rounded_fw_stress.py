"""Small exact-rational rounded-FW solver diagnostic, NOT physical acquisition."""
from fractions import Fraction as F
from receiver import mv,quad,ceil_log2,psd

def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def toward_zero_grid(x,D):
    n=abs(x.numerator)*D//x.denominator
    return F(n if x>=0 else -n,D)

def main():
    m=2;B=2;t=F(1,10**24)
    A=[[F(1),1-t],[1-t,F(1)]];k=[F(1,2),F(-1,4)]
    assert psd(A,strict=True)
    delta=F(1,4);C=16*m*B*B;theta=delta/C
    hmax=delta*delta/(24*C*B*m);D=1<<ceil_log2(1/hmax);h=F(1,D)
    q=lambda c:quad(A,c)-2*dot(k,c)
    c=[F(0)]*m;maxbits=0;stopped=False
    for iteration in range(10000):
        grad=[2*(x-y) for x,y in zip(mv(A,c),k)]
        j=max(range(m),key=lambda j:abs(grad[j]));s=[F(0)]*m
        s[j]=F(-B if grad[j]>0 else B)
        gap=dot(grad,[x-y for x,y in zip(c,s)])
        if gap<=delta:stopped=True;break
        exact=[(1-theta)*x+theta*y for x,y in zip(c,s)]
        rounded=[toward_zero_grid(x,D) for x in exact]
        assert sum(map(abs,rounded))<=B
        assert q(rounded)-q(exact)<=6*B*m*h
        assert q(c)-q(rounded)>=delta*delta/(4*C)
        assert all((x*D).denominator==1 for x in rounded)
        maxbits=max(maxbits,max(x.numerator.bit_length()+x.denominator.bit_length() for x in rounded))
        c=rounded
    assert stopped,'diagnostic cap exceeded; no huge loop permitted'
    print('PASS exact rounded-FW convergence in',iteration,'steps; final gap',float(gap),'<=',float(delta))
    print('PASS every step: feasibility, fixed dyadic grid, rounded descent >= delta^2/(4C)')
    print('Physical Gram-like determinant',1-(1-t)**2,'; no eigenvalue-floor premise')
    print('Grid denominator bits',D.bit_length(),'maximum coefficient bitheight',maxbits)
    print('Synthetic optimization diagnostic only; source reports and physical episodes: 0')

if __name__=='__main__':main()
