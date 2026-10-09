"""Rigorous interval utilities for the radial Coulomb N=3 candidate.
Uses mpmath's outward-rounded interval context; see certificate report for parameters.
"""
from mpmath import mp, iv
from heapq import heappush, heappop
mp.dps=80
iv.dps=60

# Exact decimal rational data from the candidate; s2 is subsequently isolated by force equality.
R=[iv.mpf('1'),iv.mpf('3.7632172480656902'),iv.mpf('0.4252867292159305'),iv.mpf('1.7669840027711121'),iv.mpf(['0.65122969438317767334','0.65122969438317767335'])]

# Point/box interval Coulomb cost.
def F(r,a,b):
    r0,r1,r2=r
    d01=r0*r0+r1*r1-2*r0*r1*iv.cos(a)
    d02=r0*r0+r2*r2-2*r0*r2*iv.cos(b)
    d12=r1*r1+r2*r2-2*r1*r2*iv.cos(a-b)
    return 1/iv.sqrt(d01)+1/iv.sqrt(d02)+1/iv.sqrt(d12)

def gradang(r,a,b):
    r0,r1,r2=r
    def fp(x,y,t):
        d=x*x+y*y-2*x*y*iv.cos(t)
        return -x*y*iv.sin(t)/(d*iv.sqrt(d))
    p=fp(r0,r1,a);q=fp(r0,r2,b);w=fp(r1,r2,a-b)
    return p+w,q-w

def hessang(r,a,b):
    r0,r1,r2=r
    def fpp(x,y,t):
        c=iv.cos(t);s=iv.sin(t);d=x*x+y*y-2*x*y*c
        return -x*y*c/(d*iv.sqrt(d))+3*x*x*y*y*s*s/(d*d*iv.sqrt(d))
    p=fpp(r0,r1,a);q=fpp(r0,r2,b);w=fpp(r1,r2,a-b)
    return ((p+w,-w),(-w,q+w))

def angular_lower(r,a0,a1,b0,b1):
    a=iv.mpf([a0,a1]); b=iv.mpf([b0,b1])
    r0,r1,r2=r
    d01=r0*r0+r1*r1-2*r0*r1*iv.cos(a)
    d02=r0*r0+r2*r2-2*r0*r2*iv.cos(b)
    d12=r1*r1+r2*r2-2*r1*r2*iv.cos(a-b)
    if d01.b <= 0 or d02.b <= 0 or d12.b <= 0:
        return iv.mpf([0,mp.inf])
    return 1/iv.sqrt(d01.b)+1/iv.sqrt(d02.b)+1/iv.sqrt(d12.b)

def bnb(r, threshold, rects, max_nodes=5_000_000, max_depth=80):
    """Prove F > threshold over union of rectangles. Endpoints are exact mpf dyadics/rationals.
    The returned smallest leaf margin is the interval lower endpoint minus threshold upper endpoint.
    """
    heap=[]; serial=0; nodes=0; leaves=0; maxd=0; min_margin=mp.inf
    for a0,a1,b0,b1 in rects:
        lb=angular_lower(r,a0,a1,b0,b1)
        heappush(heap,(float(lb.a),serial,a0,a1,b0,b1,0,lb));serial+=1
    while heap:
        _,_,a0,a1,b0,b1,d,lb=heappop(heap); nodes+=1; maxd=max(maxd,d)
        if lb.a > threshold.b:
            leaves+=1
            margin=mp.mpf(lb.a)-mp.mpf(threshold.b)
            if margin < min_margin: min_margin=margin
            continue
        if nodes >= max_nodes:
            return {'certified':False,'nodes':nodes,'leaves':leaves,'max_depth':maxd,'remaining':len(heap)+1,'min_margin':str(min_margin)}
        if d >= max_depth:
            return {'certified':False,'nodes':nodes,'leaves':leaves,'max_depth':maxd,'remaining':len(heap)+1,'min_margin':str(min_margin),'depth_fail':(str(a0),str(a1),str(b0),str(b1),str(lb))}
        wa=a1-a0; wb=b1-b0
        if wa >= wb:
            m=(a0+a1)/2
            for lo,hi in ((a0,m),(m,a1)):
                z=angular_lower(r,lo,hi,b0,b1)
                heappush(heap,(float(z.a),serial,lo,hi,b0,b1,d+1,z));serial+=1
        else:
            m=(b0+b1)/2
            for lo,hi in ((b0,m),(m,b1)):
                z=angular_lower(r,a0,a1,lo,hi)
                heappush(heap,(float(z.a),serial,a0,a1,lo,hi,d+1,z));serial+=1
    return {'certified':True,'nodes':nodes,'leaves':leaves,'max_depth':maxd,'min_margin':str(min_margin)}

if __name__=='__main__':
    q=(0,0,0); rr=[R[i] for i in q]
    # Threshold for u_0+u_0+u_0 + 0.006; candidate u_0=0.57511124.
    t=3*iv.mpf('0.57511124')+iv.mpf('0.006')
    B=iv.mpf('22')/7
    print('threshold',t,'r',rr)
    print(bnb(rr,t,[(-B,B,-B,B)],max_nodes=5000000))
