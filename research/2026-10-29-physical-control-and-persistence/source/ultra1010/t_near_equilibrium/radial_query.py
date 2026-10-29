"""Uniform-time radial hard-sphere perturbation query and positive cell output.

Floating diagnostic of an ideal-real construction. All kernel samplers are
explicit; no evolved density/row-mass oracle or finite-population law is used.
"""
from dataclasses import dataclass,asdict
from fractions import Fraction as F
from pathlib import Path
import bisect,json,math,random

BETA=.75
D=1/3200
DELTA=1/16384
M0=(2*math.pi)**(-1.5)
ZBETA=(2*math.pi)**(1.5*(1-BETA))*BETA**(-1.5)
M1BETA=2*math.sqrt(2/(math.pi*BETA))

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
    accepted_linear_children:int=0
    nonlinear_events:int=0
    nonlinear_partner_candidates:int=0
    kills:int=0
    terminal_exits:int=0
    max_stack:int=0
    cell_proposals:int=0
    cell_radius_proposals:int=0

def nu(v):
    if v==0:return 2*math.sqrt(2/math.pi)
    return math.sqrt(2/math.pi)*math.exp(-v*v/2)+(v+1/v)*math.erf(v/math.sqrt(2))

def chi_cdf(v,variance):
    if math.isinf(v):return 1.
    z=v/math.sqrt(variance)
    return math.erf(z/math.sqrt(2))-math.sqrt(2/math.pi)*z*math.exp(-z*z/2)

def initial_h(v):
    density=0.
    if v<=2:density+=(41/189)*3/(32*math.pi)
    if 1.5<=v<=2:density+=(148/189)*6/(37*math.pi)
    if v>2:return -DELTA*M0**(1-BETA)*math.exp(-(1-BETA)*v*v/2)
    mm=M0*math.exp(-v*v/2)
    return DELTA*(density-mm)/(mm**BETA)

class Query:
    def __init__(self,seed):
        raw=(Path(__file__).parent/'RADIAL_ROW_CERTIFICATE.json').read_bytes()
        self.certificate=json.loads(raw)
        if self.certificate['status']!='PASS_continuum_row_certificate':raise ValueError('unqualified rows')
        self.rows=[]
        for row in self.certificate['head_admission']:
            lo,hi=(float(F(*x)) for x in row['v_interval'])
            a,c=(float(F(*x)) for x in row['controls'])
            self.rows.append((lo,hi,a,c,float(F(*row['row_bound_upper']))))
        self.rows.sort();self.ends=[row[1] for row in self.rows]
        self.rng=random.Random(seed);self.counts=Counts()
        self.edges=(0.,1.,2.,float('inf'))
        self.mass=[chi_cdf(b,1)-chi_cdf(a,1) for a,b in zip(self.edges,self.edges[1:])]
        self.bmass=[ZBETA*(chi_cdf(b,1/BETA)-chi_cdf(a,1/BETA)) for a,b in zip(self.edges,self.edges[1:])]
        self.cell_upper=[a+D*b for a,b in zip(self.mass,self.bmass)]
        assert all(a>D*b for a,b in zip(self.mass,self.bmass))
        self.total=sum(self.cell_upper)

    def u(self):
        self.counts.uniforms+=1
        return self.rng.random()

    def exp1(self):
        self.counts.exponentials+=1
        return -math.log(1-self.u())

    def normal(self):
        self.counts.normals+=1
        return math.sqrt(-2*math.log(1-self.u()))*math.cos(2*math.pi*self.u())

    def chi(self,dimension):
        if dimension==3:return math.sqrt((self.normal()**2+2*self.exp1())/BETA)
        if dimension==4:return math.sqrt(2*(self.exp1()+self.exp1())/BETA)
        if dimension==5:return math.sqrt((self.normal()**2+2*self.exp1()+2*self.exp1())/BETA)
        raise ValueError('unsupported native chi shape')

    def categorical(self,weights):
        value=self.u()*sum(weights)
        for i,w in enumerate(weights):
            value-=w
            if value<0:return i
        return len(weights)-1

    def controls(self,v):
        if v>=8:
            eta=4/(BETA*(1-BETA)*v*v)+BETA**(-1.5)*math.exp(-(1-BETA)*v*v/2)*(1+M1BETA/v)
            return 0.,0.,eta
        index=bisect.bisect_left(self.ends,v)
        _,_,a,c,eta=self.rows[index]
        return a,c,eta

    def envelope(self,v,a,c):
        factor=BETA**(-1.5)*math.exp(-(1-BETA)*v*v/2)
        if v==0:low=0.;high=4*math.sqrt(2/math.pi)/BETA
        else:
            low=4/((1-BETA)*v)*(-math.expm1(-(1-BETA)*v*v/2))
            high=4/(BETA*v)*math.erf(v/math.sqrt(2))
        weights=[low,high,factor*(v+abs(a)),factor*M1BETA,factor*abs(c)*3/BETA]
        return weights,sum(weights)

    def candidate(self,v,a,c,weights):
        self.counts.envelope_candidates+=1
        component=self.categorical(weights)
        if component==0:
            aa=(1-BETA)/2;zz=aa*v*v;u=self.u()
            y=math.log1p(u*math.expm1(zz))/aa if zz<20 else v*v+math.log(u+(1-u)*math.exp(-zz))/aa
            s=math.sqrt(max(0.,y))
        elif component==1:s=math.sqrt(v*v+2*self.exp1()/BETA)
        else:s=self.chi(component+1)
        if s==0:raise ArithmeticError('zero radius floating endpoint')
        if v==0:
            log_gain=math.log(4/s);relative_gain=1.
        elif s<v:
            log_gain=math.log(4*math.sqrt(math.pi/2)/(v*s))+s*s/2
            relative_gain=math.erf(s/math.sqrt(2))
        else:
            log_gain=math.log(4*math.sqrt(math.pi/2)/(v*s))+v*v/2+math.log(math.erf(v/math.sqrt(2)))
            relative_gain=1.
        inv_gain=math.exp(-log_gain)
        maximum,minimum=max(v,s),min(v,s)
        loss=maximum+minimum*minimum/(3*maximum)
        residual=relative_gain-(loss+a+c*s*s)*inv_gain
        upper=1+(v+s+abs(a)+abs(c)*s*s)*inv_gain
        probability=abs(residual)/upper
        if not 0<=probability<=1+1e-12:raise ArithmeticError('invalid envelope ratio')
        return s,probability,1. if residual>=0 else -1.

    def factory(self,pcoin,multiplier,epsilon):
        threshold=4.6/epsilon;epsilon=min(epsilon,.644)
        i=1;c=multiplier
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
        while True:
            self.counts.nonlinear_partner_candidates+=1
            s=self.chi(3 if self.u()<v/(v+M1BETA) else 4)
            cosine=2*self.u()-1
            relative=math.sqrt(max(0.,v*v+s*s-2*v*s*cosine))
            if self.u()<relative/(v+s):return s,cosine

    def query(self,v,t):
        self.counts.queries+=1
        stack=[(v,t)];out=1.
        while stack:
            self.counts.max_stack=max(self.counts.max_stack,len(stack))
            v,left=stack.pop();self.counts.nodes+=1;self.counts.waits+=1
            wait=self.exp1()/nu(v)
            if wait>=left:
                self.counts.terminal_exits+=1;self.counts.source_evaluations+=1
                out*=initial_h(v)/D
                continue
            left-=wait
            nub=ZBETA*nu(math.sqrt(BETA)*v)/math.sqrt(BETA)
            pq=2*D*nub/nu(v)
            if self.u()<pq:
                self.counts.nonlinear_events+=1
                s,cosine=self.nonlinear_partner(v)
                if self.u()<.5:
                    total=v*v+s*s
                    span=math.sqrt(max(0.,total*total-4*v*v*s*s*cosine*cosine))
                    e=.5*(total+span*(2*self.u()-1))
                    stack.extend([(math.sqrt(max(0.,e)),left),(math.sqrt(max(0.,total-e)),left)])
                else:
                    out=-out;stack.extend([(v,left),(s,left)])
                continue
            a,c,eta=self.controls(v);weights,rate=self.envelope(v,a,c)
            base=nu(v)*(1-pq);total_rate=rate+2*base
            multiplier=total_rate/base;epsilon=1-eta/(1-pq)
            def pcoin():
                if self.u()>=rate/total_rate:return False
                _,prob,_=self.candidate(v,a,c,weights)
                return self.u()<prob
            if not self.factory(pcoin,multiplier,epsilon):
                self.counts.kills+=1;return 0.
            while True:
                s,prob,sign=self.candidate(v,a,c,weights)
                if self.u()<prob:break
            self.counts.accepted_linear_children+=1;out*=sign;stack.append((s,left))
        if abs(out)>1+1e-10:raise ArithmeticError('mark left unit interval')
        return D*out

    def observation(self,t):
        while True:
            self.counts.cell_proposals+=1
            cell=self.categorical(self.cell_upper)
            lo,hi=self.edges[cell:cell+2]
            while True:
                self.counts.cell_radius_proposals+=1;v=self.chi(3)
                if lo<=v<hi:break
            mark=self.query(v,t)
            probability=(self.mass[cell]+self.bmass[cell]*mark)/self.cell_upper[cell]
            if not 0<=probability<=1+1e-12:raise ArithmeticError('invalid positive cell completion')
            if self.u()<probability:return cell

    def receipt(self):return asdict(self.counts)
