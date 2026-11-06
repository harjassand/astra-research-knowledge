"""Rational bounds for global mean-field free energy, including coexistence.

The adaptive bound is a convenience. A uniform rational Bloch-ball grid gives
the polynomial worst-case termination bound proved in RESEARCH_REPORT.txt.
Floating point only proposes entropy supporting planes; every resulting plane
is certified for its exact rational slope, so its quality cannot invalidate a
bound. No local optimizer's success is assumed.
"""
import heapq,math,time
from fractions import Fraction as Q
from polynomial_tools import evaluate,derivative,enclose
from entropy_bounds import entropy_of_squared_radius,sqrt_interval,log_two_cosh_upper


def dot(x,y): return sum((a*b for a,b in zip(x,y)),Q(0))


def point_value(p,r,beta):
    e=evaluate(p,r)
    if beta is None: return e,e
    slo,shi=entropy_of_squared_radius(dot(r,r))
    return e-shi/beta,e-slo/beta


def min_radius_point(box):
    return tuple(a if a>0 else b if b<0 else Q(0) for a,b in box)


def sphere_proposal(r):
    """Float guidance, but an exactly rational point of the unit sphere."""
    vals=[float(v) for v in r]; norm=math.sqrt(sum(v*v for v in vals))
    if norm==0: return None
    x,y,z=[v/norm for v in vals]
    if 1+z<1e-6: return (Q(0),Q(0),Q(-1))
    t=Q(round(x/(1+z)*(1<<16)),1<<16)
    w=Q(round(y/(1+z)*(1<<16)),1<<16)
    den=1+t*t+w*w
    return (2*t/den,2*w/den,(1-t*t-w*w)/den)


class StateOracle:
    def __init__(self,p,beta):
        self.p=p; self.beta=beta
        self.g=[derivative(p,j) for j in range(3)]
        self.h=[[derivative(self.g[i],j) for j in range(3)] for i in range(3)]
        self.bounds=0

    def bound(self,box):
        nearest=min_radius_point(box); rmin2=dot(nearest,nearest)
        if rmin2>1: return None
        c=tuple((a+b)/2 for a,b in box)
        d=tuple((b-a)/2 for a,b in box)
        pc=evaluate(self.p,c); g=tuple(evaluate(v,c) for v in self.g)
        natural=enclose(self.p,box)[0]
        b=(Q(0),)*3; constant=Q(0)
        if self.beta is not None:
            natural-=entropy_of_squared_radius(rmin2)[1]/self.beta
            # An arbitrary rational b gives the exact valid variational bound
            # -S(r)/beta >= b.r - log(2 cosh(beta |b|))/beta.
            cf=[float(v) for v in c]; rad=math.sqrt(sum(v*v for v in cf))
            if rad:
                rr=min(rad,0.999)
                factor=math.atanh(rr)/(rad*float(self.beta))
                b=tuple(Q(round(v*factor*(1<<16)),1<<16) for v in cf)
                normupper=sqrt_interval(dot(b,b))[1]
                constant=-log_two_cosh_upper(self.beta*normupper)/self.beta
            else:
                constant=-log_two_cosh_upper(Q(0))/self.beta
        a=tuple(x+y for x,y in zip(g,b))
        linear_box=sum((v*(lo if v>=0 else hi) for v,(lo,hi) in zip(a,box)),Q(0))
        linear_ball=-sqrt_interval(dot(a,a))[1]
        remainder=Q(0)
        for i in range(3):
            for j in range(3):
                lo,hi=enclose(self.h[i][j],box)
                remainder+=max(abs(lo),abs(hi))*d[i]*d[j]/2
        taylor=pc-dot(g,c)+constant+max(linear_box,linear_ball)-remainder
        low=max(natural,taylor)
        candidate=c if dot(c,c)<=1 else nearest
        self.bounds+=1
        return low,candidate

    def minimize(self,tolerance,model_radius=Q(0),cover_width=None,initial_points=()):
        t0=time.perf_counter(); tolerance=Q(tolerance)
        best=None; point=None
        candidates=[(Q(0),)*3]
        for j in range(3):
            for sign in [-1,1]: candidates.append(tuple(Q(sign if i==j else 0) for i in range(3)))
        candidates.extend(initial_points)
        for r in candidates:
            if dot(r,r)<=1:
                val=point_value(self.p,r,self.beta)[1]
                if best is None or val<best: best=val; point=r
        serial=0; heap=[]
        def add(box):
            nonlocal serial,best,point
            result=self.bound(box)
            if result is None: return
            lo,r=result
            value=point_value(self.p,r,self.beta)[1]
            if value<best: best=value; point=r
            if self.beta is None:
                sphere=sphere_proposal(tuple((a+b)/2 for a,b in box))
                if sphere is not None:
                    value=point_value(self.p,sphere,self.beta)[1]
                    if value<best: best=value; point=sphere
            if lo<=best+2*model_radius:
                serial+=1; heapq.heappush(heap,(lo,serial,box))
        add(tuple((Q(-1),Q(1)) for _ in range(3)))
        splits=0
        while heap and best-heap[0][0]>tolerance:
            low,_,box=heapq.heappop(heap)
            j=max(range(3),key=lambda j:box[j][1]-box[j][0])
            mid=sum(box[j])/2
            for interval in [(box[j][0],mid),(mid,box[j][1])]:
                child=list(box); child[j]=interval; add(tuple(child))
            splits+=1
        assert heap
        lower=heap[0][0]
        # Optional complete uncertainty-aware phase cover. Splitting is based
        # on a geometric width, never on the number of presumed phases.
        if cover_width is not None:
            pending=[item for item in heap if item[0]<=best+2*model_radius]
            heap=[]
            while pending:
                low,_,box=pending.pop()
                if low>best+2*model_radius: continue
                if max(b-a for a,b in box)<=cover_width:
                    serial+=1; heapq.heappush(heap,(low,serial,box)); continue
                j=max(range(3),key=lambda j:box[j][1]-box[j][0]); mid=sum(box[j])/2
                for interval in [(box[j][0],mid),(mid,box[j][1])]:
                    child=list(box); child[j]=interval; child=tuple(child)
                    result=self.bound(child)
                    if result is None: continue
                    lo,r=result; value=point_value(self.p,r,self.beta)[1]
                    if value<best: best=value; point=r
                    if lo<=best+2*model_radius:
                        serial+=1; pending.append((lo,serial,child))
                splits+=1
            assert heap
            lower=max(lower,heap[0][0])
        cover=[{'box':[[str(a),str(b)] for a,b in box],'lower':str(lo)}
               for lo,_,box in heap if lo<=best+2*model_radius]
        return {'lower':lower,'upper':best,'point':point,'cover':cover,
                'splits':splits,'bounds':self.bounds,'seconds':time.perf_counter()-t0}
