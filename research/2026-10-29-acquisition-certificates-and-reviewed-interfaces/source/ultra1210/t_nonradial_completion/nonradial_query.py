"""Full-vector floating diagnostic of the ideal-real nonradial operation.

No radial projection, population or evolved density/absolute-row integral
oracle is used. Every dummy/rejected kernel candidate is counted. Neither
binary64 nor seeded PRNG is represented as literal exact-bit sampling.
"""
from dataclasses import dataclass,asdict
from fractions import Fraction as F
from pathlib import Path
import bisect,json,math,random

BETA=.75
D=1/10000
DEFF=1/8000
DELTA=1/16384
PHIMAX=1.25
M0=(2*math.pi)**(-1.5)
ZBETA=(2*math.pi)**(3/8)*BETA**(-1.5)
M1BETA=2*math.sqrt(2/(math.pi*BETA))
MABSBETA=math.sqrt(2/(math.pi*BETA))


def norm2(v):return sum(x*x for x in v)
def dot(v,w):return sum(x*y for x,y in zip(v,w))
def add(v,w):return tuple(x+y for x,y in zip(v,w))
def scale(s,v):return tuple(s*x for x in v)
def minus(v,w):return tuple(x-y for x,y in zip(v,w))
def cross(v,w):return (v[1]*w[2]-v[2]*w[1],v[2]*w[0]-v[0]*w[2],v[0]*w[1]-v[1]*w[0])


def phi(v):
    x=norm2(v) if isinstance(v,tuple) else v*v
    return 1+4*((x-4)*(25-x))**2/194481 if 4<=x<=25 else 1.


def source_a(v):return (v[0]*v[0]-v[1]*v[1])/(1+norm2(v))


def initial_h(v):
    return DELTA*M0**(1-BETA)*math.exp(-(1-BETA)*norm2(v)/2)*source_a(v)/phi(v)


def nu(v):
    if v==0:return 2*math.sqrt(2/math.pi)
    return math.sqrt(2/math.pi)*math.exp(-v*v/2)+(v+1/v)*math.erf(v/math.sqrt(2))


def basis(v):
    speed=math.sqrt(norm2(v))
    if speed==0:return (0.,0.,1.),(1.,0.,0.),(0.,1.,0.)
    e1=scale(1/speed,v)
    axis=(0.,0.,1.) if abs(e1[2])<.9 else (0.,1.,0.)
    e2=cross(e1,axis);e2=scale(1/math.sqrt(norm2(e2)),e2)
    return e1,e2,cross(e1,e2)


@dataclass
class Counts:
    queries:int=0
    nodes:int=0
    waits:int=0
    source_evaluations:int=0
    uniforms:int=0
    normals:int=0
    exponentials:int=0
    factory_coins:int=0
    factory_stages:int=0
    envelope_candidates:int=0
    gain_dummy_rejections:int=0
    accepted_linear_children:int=0
    nonlinear_gain_proposals:int=0
    nonlinear_loss_proposals:int=0
    nonlinear_thinning_rejections:int=0
    nonlinear_partner_candidates:int=0
    kills:int=0
    terminal_exits:int=0
    max_stack:int=0
    observation_proposals:int=0
    observation_gaussian_candidates:int=0
    continuous_proposals:int=0
    continuous_beta_components:int=0
    negative_clippings:int=0


class Query:
    def __init__(self,seed=0,trace=False):
        raw=(Path(__file__).parent/'NONRADIAL_CERTIFICATE.json').read_bytes()
        self.certificate=json.loads(raw)
        if self.certificate['status']!='PASS_FULL_CONTINUUM':raise ValueError('unqualified operator')
        self.rows=[]
        for row in self.certificate['admitted']:
            lo,hi=(float(F(*x)) for x in row['v_interval'])
            co=tuple(float(F(*x)) for x in row['controls'])
            self.rows.append((lo,hi,co,float(F(*row['row_upper']))))
        self.rows.sort();self.ends=[r[1] for r in self.rows]
        self.rng=random.Random(seed);self.counts=Counts();self.trace=[] if trace else None

    def u(self):
        self.counts.uniforms+=1;return self.rng.random()

    def exp1(self):
        self.counts.exponentials+=1;return -math.log(1-self.u())

    def normal(self):
        self.counts.normals+=1
        return math.sqrt(2*self.exp1())*math.cos(2*math.pi*self.u())

    def sphere(self):
        z=2*self.u()-1;angle=2*math.pi*self.u();rr=math.sqrt(max(0.,1-z*z))
        return (rr*math.cos(angle),rr*math.sin(angle),z)

    def gaussian(self):return tuple(self.normal()/math.sqrt(BETA) for _ in range(3))

    def biased_gaussian(self,dimension):
        if dimension==4:r=math.sqrt(2*(self.exp1()+self.exp1())/BETA)
        elif dimension==5:r=math.sqrt((self.normal()**2+2*self.exp1()+2*self.exp1())/BETA)
        else:raise ValueError('native biased Gaussian shape')
        return scale(r,self.sphere())

    def categorical(self,weights):
        x=self.u()*sum(weights)
        for j,p in enumerate(weights):
            x-=p
            if x<0:return j
        return len(weights)-1

    def controls(self,V):
        if V>=8:
            eta=PHIMAX*(4/(BETA*(1-BETA)*V*V)+BETA**(-1.5)*math.exp(-(1-BETA)*V*V/2)*(1+M1BETA/V))
            return (0.,0.,0.),eta
        row=self.rows[bisect.bisect_left(self.ends,V)]
        return row[2],row[3]

    def envelope(self,V,co):
        a,b,c=co;fac=BETA**(-1.5)*math.exp(-(1-BETA)*V*V/2)
        gain=(8*math.sqrt(2/math.pi)*math.exp(BETA*V*V/2)/BETA if V<1 else
              4/(BETA*(1-BETA)*V))
        weights=[gain,fac*(V+abs(a)),fac*M1BETA,fac*abs(b)*MABSBETA,fac*abs(c)*3/BETA]
        scale0=PHIMAX/phi(V)
        return [x*scale0 for x in weights]

    def candidate(self,v,co,weights):
        self.counts.envelope_candidates+=1
        V=math.sqrt(norm2(v));a,b,c=co;e1,e2,e3=basis(v)
        component=self.categorical(weights)
        if component==0:
            if V>=1:
                r=math.sqrt(2*self.exp1()/(BETA*(1-BETA)))
                tt=BETA*r+self.normal()
                if abs(tt)>V:
                    self.counts.gain_dummy_rejections+=1
                    return None,0.,0.
                cosine=tt/V;angle=2*math.pi*self.u()
                n=add(scale(cosine,e1),scale(math.sqrt(max(0.,1-cosine*cosine)),
                      add(scale(math.cos(angle),e2),scale(math.sin(angle),e3))))
            else:
                r=math.sqrt(4*self.exp1()/BETA);n=self.sphere()
            w=minus(v,scale(r,n))
        elif component==1:w=self.gaussian()
        elif component==2:w=self.biased_gaussian(4)
        elif component==3:
            zz=math.sqrt(2*self.exp1()/BETA)*(1 if self.u()<.5 else -1)
            xx=self.normal()/math.sqrt(BETA);yy=self.normal()/math.sqrt(BETA)
            w=add(scale(zz,e1),add(scale(xx,e2),scale(yy,e3)))
        else:w=self.biased_gaussian(5)
        rel=minus(v,w);r=math.sqrt(norm2(rel));s=math.sqrt(norm2(w));z=dot(w,e1)
        if r==0:raise ArithmeticError('zero relative norm floating endpoint')
        tt=dot(v,rel)/r
        E1=-BETA*(r-tt)**2/2-(1-BETA)*tt*tt/2
        E0=-(1-BETA)*V*V/2-BETA*s*s/2
        logg=math.log(4*M0/r)+E1
        logenv=(logg if V>=1 else math.log(4*M0/r)+BETA*V*V/2-BETA*r*r/4)
        logm=math.log(M0)+E0
        common=max(logenv,logm)
        gm=math.exp(logg-common);em=math.exp(logenv-common);mm=math.exp(logm-common)
        P=a+b*z+c*s*s
        signed=gm-(r+P)*mm
        upper=em+(V+s+abs(a)+abs(b)*abs(z)+abs(c)*s*s)*mm
        probability=phi(w)/PHIMAX*abs(signed)/upper
        if not 0<=probability<=1+2e-12:raise ArithmeticError('invalid full-vector envelope')
        return w,probability,1. if signed>=0 else -1.

    def factory(self,pcoin,multiplier,epsilon):
        # Huber GENERAL linear factory; all base/geometric work is charged.
        threshold=4.6/epsilon;epsilon=min(epsilon,.644);i=1;c=multiplier
        while True:
            self.counts.factory_stages+=1
            while True:
                self.counts.factory_coins+=1;b=pcoin();g=1
                while self.u()>=(c-1)/c:g+=1
                i+=-1+(1-int(b))*g
                if i==0 or i>=threshold:break
            if i==0:return True
            if self.u()>=(1+.5*epsilon)**(-i):return False
            c*=1+.5*epsilon;epsilon*=.5;threshold*=2

    def nonlinear_partner(self,v):
        V=math.sqrt(norm2(v))
        while True:
            self.counts.nonlinear_partner_candidates+=1
            w=self.gaussian() if self.u()<V/(V+M1BETA) else self.biased_gaussian(4)
            s=math.sqrt(norm2(w));r=math.sqrt(norm2(minus(v,w)))
            if self.u()<r/(V+s):return w

    def wait_exp(self):return self.exp1()
    def top_uniform(self,pg,pl):return self.u()
    def thin_uniform(self):return self.u()

    def query(self,v,t):
        self.counts.queries+=1;origin=v;stack=[(v,t)];out=1.
        while stack:
            self.counts.max_stack=max(self.counts.max_stack,len(stack))
            v,left=stack.pop();self.counts.nodes+=1;self.counts.waits+=1
            V=math.sqrt(norm2(v));freq=nu(V);wait=self.wait_exp()/freq
            if wait>=left:
                self.counts.terminal_exits+=1;self.counts.source_evaluations+=1
                out*=initial_h(v)/D;continue
            left-=wait
            nub=ZBETA*nu(math.sqrt(BETA)*V)/math.sqrt(BETA)
            pg=D*(25/16)*nub/freq;pl=D*(5/4)*nub/freq;pq=pg+pl
            chosen=self.top_uniform(pg,pl)
            if chosen<pq:
                w=self.nonlinear_partner(v)
                if chosen<pg:
                    self.counts.nonlinear_gain_proposals+=1
                    half=scale(.5,add(v,w));rad=.5*math.sqrt(norm2(minus(v,w)))
                    direction=self.sphere();p=add(half,scale(rad,direction));q=minus(half,scale(rad,direction))
                    accept=phi(p)*phi(q)/((25/16)*phi(v));children=(p,q)
                else:
                    self.counts.nonlinear_loss_proposals+=1
                    accept=phi(w)/(5/4);children=(v,w)
                if self.thin_uniform()>=accept:
                    self.counts.nonlinear_thinning_rejections+=1;return 0.
                if chosen>=pg:out=-out
                if self.trace is not None:self.trace.append({'kind':'gain' if chosen<pg else 'loss','v':v,'children':children,'left':left,'thin_probability':accept})
                stack.extend([(child,left) for child in children]);continue
            co,eta=self.controls(V);weights=self.envelope(V,co);rate=sum(weights)
            base=freq*(1-pq);total=rate+2*base;multiplier=total/base;epsilon=1-eta/(1-pq)
            def coin():
                if self.u()>=rate/total:return False
                _,prob,_=self.candidate(v,co,weights)
                return self.u()<prob
            if not self.factory(coin,multiplier,epsilon):
                self.counts.kills+=1;return 0.
            while True:
                child,prob,sign=self.candidate(v,co,weights)
                if self.u()<prob:break
            self.counts.accepted_linear_children+=1;out*=sign;stack.append((child,left))
        if abs(out)>1+1e-11:raise ArithmeticError('mark exceeds unit bound')
        return D*phi(origin)*out

    def observation(self,t):
        while True:
            self.counts.observation_proposals+=1;cell=0 if self.u()<.5 else 1
            while True:
                self.counts.observation_gaussian_candidates+=1;v=self.gaussian()
                if int(v[0]*v[0]<v[1]*v[1])==cell:break
            mark=self.query(v,t)
            accept=(1+ZBETA*mark)/(1+DEFF*ZBETA)
            if not 0<=accept<=1+1e-12:raise ArithmeticError('nonpositive angular completion')
            if self.u()<accept:return cell

    def continuous(self,t):
        """Positive normalized approximate full law; analytic TV is separate."""
        while True:
            self.counts.continuous_proposals+=1
            use_beta=self.u()<DEFF*ZBETA/(1+DEFF*ZBETA)
            self.counts.continuous_beta_components+=int(use_beta)
            precision=BETA if use_beta else 1.
            v=tuple(self.normal()/math.sqrt(precision) for _ in range(3))
            mark=self.query(v,t)
            relative=M0**(1-BETA)*math.exp(-(1-BETA)*norm2(v)/2)
            numerator=relative+mark
            if numerator<0:self.counts.negative_clippings+=1
            accept=max(0.,numerator)/(relative+DEFF)
            if not 0<=accept<=1+1e-12:raise ArithmeticError('continuous acceptance outside[0,1]')
            if self.u()<accept:return v

    def receipt(self):return asdict(self.counts)
