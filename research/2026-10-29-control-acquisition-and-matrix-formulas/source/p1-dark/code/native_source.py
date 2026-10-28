"""Fresh rational affine-SPD fixtures, separate from unavailable Astra code.

Learners receive only call(u)->a calibrated raw-R interval. Hidden matrices
are inspected later by source-aware finite checkers, not by the learner.
"""
from fractions import Fraction as F
from math import isqrt


def dot(x,y):return sum((a*b for a,b in zip(x,y)),F(0))


def solve(A,b):
    n=len(b);a=[list(row)+[b[i]] for i,row in enumerate(A)]
    for j in range(n):
        k=next(i for i in range(j,n) if a[i][j]);a[j],a[k]=a[k],a[j]
        p=a[j][j];a[j]=[x/p for x in a[j]]
        for i in range(n):
            if i!=j:
                p=a[i][j];a[i]=[x-p*y for x,y in zip(a[i],a[j])]
    return [a[i][-1] for i in range(n)]


def determinant(A):
    if not A:return F(1)
    a=[list(row) for row in A];d=F(1)
    for j in range(len(a)):
        choices=[i for i in range(j,len(a)) if a[i][j]]
        if not choices:return F(0)
        k=choices[0]
        if k!=j:a[j],a[k]=a[k],a[j];d=-d
        p=a[j][j];d*=p
        for i in range(j+1,len(a)):
            q=a[i][j]/p
            for k in range(j+1,len(a)):a[i][k]-=q*a[j][k]
    return d


def sqrt_upper(x,bits=80):
    assert x>=0
    scale=1<<bits;k=isqrt((x.numerator*scale*scale)//x.denominator)
    if F(k*k,scale*scale)<x:k+=1
    return F(k,scale)


class NativeSource:
    def __init__(self,vectors,c0=F(1),label='fresh_source'):
        self.vectors=[list(map(F,v)) for v in vectors]
        self.n=len(vectors);self.m=len(vectors[0]);self.c0=F(c0);self.label=label
    def matrix(self,u):
        assert len(u)==self.n and all(x>=0 for x in u) and sum(u)<=F(1,5)
        q=[[F(int(i==j)) for j in range(self.m)] for i in range(self.m)]
        q[0][0]=self.c0
        for dose,v in zip(u,self.vectors):
            if dose:
                for i in range(self.m):
                    for j in range(self.m):q[i][j]+=dose*v[i]*v[j]
        return q
    def response(self,u):
        q=self.matrix(u);x=solve(q,[F(1)]+[F(0)]*(self.m-1))
        return F(3,2)+1/x[0]
    def independent_response(self,u):
        q=self.matrix(u);minor=[row[1:] for row in q[1:]]
        return F(3,2)+determinant(q)/determinant(minor)
    def state_and_gradient(self,u,prices=None):
        x=solve(self.matrix(u),[F(1)]+[F(0)]*(self.m-1))
        prices=prices or [F(0)]*self.n
        return x[0],1/self.c0-x[0]-dot(prices,u),[dot(v,x)**2-c for v,c in zip(self.vectors,prices)]


def fixture(n=32,rank=2,kind='bright'):
    vs=[]
    for i in range(n):
        g=F(5+(i*7)%6,10)
        s=[F(((i*(j+3)+j*2)%7)-3,5) for j in range(rank)]
        if i<rank:s=[F(int(i==j),2) for j in range(rank)]
        vs.append([g]+[g*x for x in s])
    if kind=='weak':vs[-1][0]=F(1,10**7)
    if kind=='dark':vs[-1]=[F(0),F(1,2)]+[F(0)]*(rank-1)
    if kind=='near_dependent' and rank>=2:
        vs[1]=[F(4,5),F(2,5),F(1,10**6)]+[F(0)]*(rank-2)
    return NativeSource(vs,label=f'{kind}_n{n}_r{rank}')


class CalibratedOracle:
    """Two standards; shared affine calibration; bounded correlated read error.

    G, Bdiag and c0 bounds are warranted specifications, not inferred physics.
    Finite dyadic actuation and ADC quantization are charged. No hardware.
    """
    def __init__(self,source,eta=F(1,10**10),dac_bits=44,adc_bits=64,
                 G_bound=F(1),Bdiag_bound=F(2),c0_lower=F(1,2)):
        self._source=source;self.n=source.n;self.eta=F(eta)
        self.dac_bits=dac_bits;self.adc_bits=adc_bits
        self._gain=F(1001,1000);self._offset=F(-3,1000)
        self._index=0;self.records=[];self.calibration=[]
        self.G_bound=G_bound;self.Bdiag_bound=Bdiag_bound;self.c0_lower=c0_lower
        vals=[]
        for standard in (F(2),F(4)):
            y=self._read(standard)
            self.calibration.append({'known_standard':standard,'raw':y})
            vals.append((y-self.read_error,y+self.read_error))
        self.alpha=((vals[1][0]-vals[0][1])/2,(vals[1][1]-vals[0][0])/2)
        assert self.alpha[0]>0
        self.beta=(vals[0][0]-2*self.alpha[1],vals[0][1]-2*self.alpha[0])
        self.actuation_lipschitz=G_bound**2*(1+sqrt_upper(F(1,5)*Bdiag_bound))**2
    @property
    def read_error(self):return self.eta+F(1,2*(1<<self.adc_bits))
    def _read(self,r):
        e=self.eta*F(2*(self._index%7)-6,6);self._index+=1
        z=self._gain*r+self._offset+e;scale=1<<self.adc_bits
        return F(round(z*scale),scale)
    def call(self,u):
        u=list(map(F,u));assert len(u)==self.n and all(x>=0 for x in u) and sum(u)<=F(1,5)
        scale=1<<self.dac_bits
        actual=[F((x*scale).numerator//(x*scale).denominator,scale) for x in u]
        y=self._read(self._source.response(actual))
        num=(y-self.read_error-self.beta[1],y+self.read_error-self.beta[0])
        corners=[a/b for a in num for b in self.alpha]
        acterr=self.actuation_lipschitz*sum(abs(a-b) for a,b in zip(u,actual))
        interval=(min(corners)-acterr,max(corners)+acterr)
        self.records.append({'requested_sparse':[(i,x) for i,x in enumerate(u) if x],
                             'actual_sparse':[(i,x) for i,x in enumerate(actual) if x],
                             'raw':y,'R_interval':interval,
                             'actuation_error_allowance':acterr,
                             'nonzero_settings':sum(bool(x) for x in actual)})
        return interval
    def ledger(self):
        writes=sum(r['nonzero_settings'] for r in self.records)
        return {'local_calibration_readings':len(self.calibration),
                'source_reaction_readings':len(self.records),
                'total_scalar_readings':len(self.calibration)+len(self.records),
                'reset_experiments':len(self.records),'nonzero_actuator_setting_writes':writes,
                'reset_writes_if_cleared_individually':writes,
                'total_programmed_dose':sum((sum(x for _,x in r['actual_sparse']) for r in self.records),F(0)),
                'maximum_programmed_dose':max([sum(x for _,x in r['actual_sparse']) for r in self.records]+[F(0)]),
                'dac_bits':self.dac_bits,'adc_bits':self.adc_bits,
                'timing_scope':'Every reaction pays preparation, settling, integration and reset; seconds and energy unacquired.'}


def jsonable(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):jsonable(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [jsonable(v) for v in x]
    return x
