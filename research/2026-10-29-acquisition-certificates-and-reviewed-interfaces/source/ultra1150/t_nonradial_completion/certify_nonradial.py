"""Outward continuum admission of a fully angular invariant-deflated row.

Coordinates w=v-r*n remove the integrable r=0 pole BEFORE quadrature.
Tensor linear interpolation of the SIGNED smooth integrand, followed by
convex absolute value, pays a second-derivative error on each box.
Candidate controls are arbitrary rounded LP suggestions, never premises.
"""
from fractions import Fraction as F
from pathlib import Path
import heapq, itertools, json, math, sys, time
from flint import arb, fmpq, ctx
from suspect_resolution import fixed
from smooth_weight import phi as float_phi

ctx.prec=112
BETA=F(3,4)
ETA=F(199,200)


def ball(x):
    if isinstance(x,arb):return x
    x=F(x);return arb(fmpq(x.numerator,x.denominator))


def interval(a,b):
    return ball(a).union(ball(b))


def square(x):
    # Literal multiplication, not generic power/log across zero.
    if x.contains(0):
        m=max(abs(x.lower()),abs(x.upper()))
        return arb(0).union(point_upper(m*m))
    return (x*x).nonnegative_part()


def point_upper(x): return arb(x.upper())


def dyadic(x):
    m,e=x.man_exp();m,e=int(m),int(e)
    return F(m*(1<<e)) if e>=0 else F(m,1<<-e)


def ser(x):
    x=F(x);return [x.numerator,x.denominator]


def phi_jet(x):
    """Value and two x-derivatives of a C1, piecewise-polynomial weight."""
    if x.upper()<4 or x.lower()>25:
        return arb(1),arb(0),arb(0)
    xx=x.intersection(interval(4,25))
    h=((xx-4)*(25-xx)).intersection(interval(0,F(441,4)))
    slope=29-2*xx
    value=(1+4*square(h)/194481).intersection(interval(1,F(5,4)))
    first=8*h*slope/194481
    second=8*(square(slope)-2*h)/194481
    if x.lower()<4 or x.upper()>25:
        value=value.union(arb(1));first=first.union(arb(0));second=second.union(arb(0))
    return value,first,second


def nu(v):
    if v==0:return 2*(2/arb.pi()).sqrt()
    v=ball(v)
    return (2/arb.pi()).sqrt()*(-v*v/2).exp()+(v+1/v)*(v/arb(2).sqrt()).erf()


def signed(v,r,u,controls):
    a,b,c=map(ball,controls);beta=ball(BETA)
    x=(square(r-v*u)+square(v)*(1-square(u)).nonnegative_part()).nonnegative_part()
    ph=phi_jet(x)[0]
    e0=(-(1-beta)*square(v)/2-beta*x/2).exp()
    e1=(-beta*square(r-v*u)/2-(1-beta)*square(v)*square(u)/2).exp()
    p=a+b*(v-r*u)+c*x
    return ph*(4*r*e1-(r*r*r+r*r*p)*e0)


def derivatives(v,r,u,controls):
    """Pure second derivatives in r,u,v, without mixed derivatives."""
    a,b,c=map(ball,controls);be=ball(BETA)
    vv=square(v);rr=square(r);uu=square(u)
    x=(square(r-v*u)+vv*(1-uu).nonnegative_part()).nonnegative_part()
    ph,dp,ddp=phi_jet(x)
    e0=(-(1-be)*vv/2-be*x/2).exp()
    e1=(-be*square(r-v*u)/2-(1-be)*vv*uu/2).exp()
    p=a+b*(v-r*u)+c*x
    q=r*rr+rr*p
    g=4*r*e1-q*e0
    results=[]
    for er1,er0,err1,err0,qr,qrr,xr,xrr in (
        (-be*r+be*v*u,-be*r+be*v*u,-be,-be,
         3*rr+2*r*p+rr*(-b*u+2*c*(r-v*u)),
         6*r+2*p+4*r*(-b*u+2*c*(r-v*u))+2*c*rr,
         2*(r-v*u),arb(2)),
        (be*v*r-vv*u,be*v*r,-vv,arb(0),
         -rr*r*(b+2*c*v),arb(0),-2*v*r,arb(0)),
        (be*r*u-v*uu,-v+be*r*u,-uu,arb(-1),
         rr*(b+2*c*(v-r*u)),2*c*rr,2*(v-r*u),arb(2))):
        # Derivatives of 4*r are nonzero only for the r variable.
        is_r=(len(results)==0)
        g1=4*e1*((1 if is_r else 0)+r*er1)-e0*(qr+q*er0)
        g2=4*e1*((2*er1 if is_r else 0)+r*(square(er1)+err1))
        g2-=e0*(qrr+2*qr*er0+q*(square(er0)+err0))
        f2=ph*g2+2*dp*xr*g1+(ddp*square(xr)+dp*xrr)*g
        results.append(point_upper(abs(f2)))
    return results


class Integrator:
    def __init__(self,lo,hi,controls):
        self.lo,self.hi,self.controls=lo,hi,controls
        self.v=interval(lo,hi);self.dv=ball(hi-lo)
        self.corner_cache={};self.serial=itertools.count()
        self.box_evaluations=0

    def corner(self,v,r,u):
        key=(v,r,u)
        if key not in self.corner_cache:
            self.corner_cache[key]=point_upper(abs(signed(ball(v),ball(r),ball(u),self.controls)))
        return self.corner_cache[key]

    def cell(self,rl,rh,ul,uh):
        self.box_evaluations+=1
        r,u=interval(rl,rh),interval(ul,uh)
        dr,du=ball(rh-rl),ball(uh-ul);area=dr*du
        mrr,muu,mvv=derivatives(self.v,r,u,self.controls)
        er=point_upper(area*dr*dr*mrr/8)
        eu=point_upper(area*du*du*muu/8)
        ev=point_upper(area*self.dv*self.dv*mvv/8)
        traps=[]
        for v in (self.lo,self.hi):
            traps.append(point_upper(area*sum((self.corner(v,r0,u0) for r0 in (rl,rh) for u0 in (ul,uh)),arb(0))/4))
        err=point_upper(er+eu+ev)
        return {'box':(rl,rh,ul,uh),'t0':traps[0],'t1':traps[1],
                'er':er,'eu':eu,'ev':ev,'error':err}

    def tail(self,R=F(16)):
        a,b,c=map(abs,self.controls);v=self.hi
        q=ball(R-v);be=ball(BETA);ee=(-be*q*q/2).exp()
        moments=[(arb.pi()/(2*be)).sqrt()*(q*(be/2).sqrt()).erfc(),ee/be]
        for j in range(2,5):
            moments.append(q**(j-1)*ee/be+(j-1)*moments[j-2]/be)
        coeff=[F(0),F(4),a+b*v+c*v*v,1+b+2*c*v,c]
        total=arb(0)
        for i,ci in enumerate(coeff):
            for j in range(i+1):
                total+=ball(ci*math.comb(i,j)*v**(i-j))*moments[j]
        return point_upper(ball(F(5,2))*total)

    def run(self,max_cells=24000):
        heap=[];total0=arb(0);total1=arb(0);errors=arb(0)
        nodes={};rs=list(map(F,(0,1,2,3,4,5,6,8,10,12,16)))
        us=[F(-1),F(-1,2),F(0),F(1,2),F(1)]
        def add(cell):
            nonlocal total0,total1,errors
            key=next(self.serial);nodes[key]=cell
            priority=float((cell['er']+cell['eu']).upper())
            heapq.heappush(heap,(-priority,key))
            total0+=cell['t0'];total1+=cell['t1'];errors+=cell['error']
        for rl,rh in zip(rs,rs[1:]):
            for ul,uh in zip(us,us[1:]):add(self.cell(rl,rh,ul,uh))
        phmin=min(phi_jet(ball(self.lo*self.lo))[0].lower(),phi_jet(ball(self.hi*self.hi))[0].lower())
        factor=1/((2*arb.pi()).sqrt()*arb(phmin)*nu(self.lo))
        tail=self.tail()
        while True:
            upper=point_upper(factor*(max(total0.upper(),total1.upper())+errors+tail))
            if upper<ball(ETA): status='PASS';break
            if len(nodes)>=max_cells:status='NOT_ADMITTED';break
            _,key=heapq.heappop(heap);old=nodes.pop(key)
            total0-=old['t0'];total1-=old['t1'];errors-=old['error']
            rl,rh,ul,uh=old['box']
            if old['er']>=old['eu']:
                mid=(rl+rh)/2
                add(self.cell(rl,mid,ul,uh));add(self.cell(mid,rh,ul,uh))
            else:
                mid=(ul+uh)/2
                add(self.cell(rl,rh,ul,mid));add(self.cell(rl,rh,mid,uh))
        return {'status':status,'v_interval':[ser(self.lo),ser(self.hi)],
                'controls':[ser(x) for x in self.controls],
                'row_upper':ser(dyadic(upper.upper())),
                'row_display':float(upper), 'leaf_boxes':len(nodes),
                'box_evaluations':self.box_evaluations,
                'quadrature_error_display':float(factor*errors),
                'tail_display':float(factor*tail),
                'endpoint_trapezoid_display':[float(factor*total0),float(factor*total1)]}


def controls(v):
    proposed=fixed(float(v),192,128,weight=float_phi)
    return [F(round(x*2**24),2**24) for x in proposed['controls']]


def main():
    start=time.perf_counter()
    # One hardest-region pilot before a full cover is authorized by its result.
    lo,hi=F(107,32),F(109,32)
    coef=controls((lo+hi)/2)
    result=Integrator(lo,hi,coef).run(max_cells=24000)
    result.update({'scope':'SINGLE_CONTINUUM_SPEED_INTERVAL_PILOT',
                   'eta':str(ETA),'seconds':time.perf_counter()-start,
                   'global_admission':False})
    Path(__file__).with_name('NONRADIAL_INTERVAL_PILOT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
