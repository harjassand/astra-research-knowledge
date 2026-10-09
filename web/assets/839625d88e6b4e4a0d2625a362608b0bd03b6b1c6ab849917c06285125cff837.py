"""High precision actual CMI for a qubit-reference ternary witness."""
import mpmath as mp
mp.mp.dps=80

def xlog(x): return x*mp.log(x) if x else mp.mpf(0)
def fX(p,s):
    q=1-p
    return 2*xlog(q/2)+xlog(p)-xlog(q*(1-s))-xlog(p+q*s)
def fY(p,s):
    q=1-p
    disc=mp.sqrt((1+p)**2-8*p*q*(1-s))
    lo=(1+p-disc)/8;hi=(1+p+disc)/8
    return 2*(xlog(lo)+xlog(hi))+xlog(q*(1-s)/2)+xlog(q*s/2)-xlog(q*(1-s))-xlog(p+q*s)
def calc(p,s,h):
    vals=[]
    for f in (fX,fY):vals.append((f(p+h,s)+f(p-h,s))/2-f(p,s))
    return vals+[vals[1]/vals[0]]
if __name__=='__main__':
    for pp,ss,hh in [('1/10','1/100','1/100'),('1/100','1/1000','1/1000'),('1/100','1/100000','1/1000'),('1/1000','1/100000','1/10000')]:
        p,s,h=map(mp.mpf,[pp,ss,hh])
        print(pp,ss,hh,*(mp.nstr(x,30) for x in calc(p,s,h)))
