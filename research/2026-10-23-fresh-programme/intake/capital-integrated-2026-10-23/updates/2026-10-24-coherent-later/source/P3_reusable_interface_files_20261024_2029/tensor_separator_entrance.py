"""New Pro3 research: certified correlated entrance through partial gates.

An autonomous controller opens once (0 -> 1 at gamma).  Initially stationary
independent binary modules evolve freely until opening.  While open, module i
produces a marked event at kappa_i when its state is 1.  The first marked event
resets its own module to 0.  The opening time is unobserved.

This file reuses the AVAILABLE directed-Decimal interval class in
pro3_gate_experiment.py.  It does not modify that file.  NumPy/SciPy are used only
for a small expanded-reference check; the main enclosure is interval arithmetic.
"""
from fractions import Fraction as F
from dataclasses import dataclass
import heapq
import itertools
import json
import time
from pro3_gate_experiment import I, D, DOWN, UP


@dataclass(frozen=True)
class BinaryModule:
    alpha: F
    beta: F
    kappa: F

    def prepare(self):
        a,b,k=I(self.alpha),I(self.beta),I(self.kappa)
        total=a+b+k
        gap=((a-b-k)*(a-b-k)+4*a*b).sqrt()
        slow=(total-gap)/2
        fast=(total+gap)/2
        return b/(a+b), a/(a+b), k, gap, slow, fast


class Entrance:
    def __init__(self, modules, gamma, t, mark):
        assert gamma>0 and t>0 and 0<=mark<len(modules)
        assert all(x.alpha>0 and x.beta>0 and x.kappa>0 for x in modules)
        self.modules=modules
        self.data=[x.prepare() for x in modules]
        self.gamma=F(gamma); self.t=F(t); self.mark=mark
        self.cache={}

    def vectors(self,u):
        if u in self.cache: return self.cache[u]
        ans=[]
        for p0,p1,k,gap,slow,fast in self.data:
            es=(-slow*I(u)).exp(); ef=(-fast*I(u)).exp()
            v0=p0*(fast*es-slow*ef)/gap
            v1=p1*((fast-k)*es+(k-slow)*ef)/gap
            ans.append((v0,v1))
        self.cache[u]=ans
        return ans

    def weight(self,u):
        return I(self.gamma)*(-I(self.gamma)*(I(self.t)-I(u))).exp()

    def cell(self,left,right):
        vl=self.vectors(left); vr=self.vectors(right)
        width=I(right-left)
        # v_i(u) decreases componentwise.  The controller density increases.
        rows_lo=[]; rows_hi=[]
        for i in range(len(self.modules)):
            if i==self.mark:
                # Include event hazard and local reset in the product row.
                k=I(self.modules[i].kappa)
                rows_lo.append(((k*vr[i][1]).lo,D(0)))
                rows_hi.append(((k*vl[i][1]).hi,D(0)))
            else:
                rows_lo.append(tuple(max(D(0),z.lo) for z in vr[i]))
                rows_hi.append(tuple(z.hi for z in vl[i]))
        coeff_lo=(width*I(self.weight(left).lo)).lo
        coeff_hi=(width*I(self.weight(right).hi)).hi
        def mass(coeff,rows):
            value=I(coeff)
            for row in rows: value=value*(I(row[0])+I(row[1]))
            return value
        ml=mass(coeff_lo,rows_lo); mu=mass(coeff_hi,rows_hi)
        return {'left':left,'right':right,'cl':coeff_lo,'cu':coeff_hi,
                'rows_l':rows_lo,'rows_u':rows_hi,'ml':ml,'mu':mu,
                'gap':float(UP.subtract(mu.hi,ml.lo))}

    @staticmethod
    def sums(cells,ones=()):
        lower=I(0); upper=I(0)
        for cell in cells:
            lo=I(cell['cl']); up=I(cell['cu'])
            for i,(rl,ru) in enumerate(zip(cell['rows_l'],cell['rows_u'])):
                if i in ones:
                    lo=lo*I(rl[1]); up=up*I(ru[1])
                else:
                    lo=lo*(I(rl[0])+I(rl[1])); up=up*(I(ru[0])+I(ru[1]))
            lower=lower+lo; upper=upper+up
        return lower,upper

    def build(self,tolerance=F(1,1000),max_cells=20000):
        count=0
        first=self.cell(F(0),self.t)
        heap=[(-first['gap'],count,first)]
        approx_l=first['ml'].midfloat(); approx_u=first['mu'].midfloat()
        while len(heap)<max_cells:
            if (approx_u-approx_l)/approx_u < float(tolerance)*.99:
                cells=[x[2] for x in heap]
                lo,up=self.sums(cells)
                eps=(I(1)-I(lo.lo)/I(up.hi)).hi
                if eps<=I(tolerance).lo: break
            _,_,old=heapq.heappop(heap)
            mid=(old['left']+old['right'])/2
            a=self.cell(old['left'],mid); b=self.cell(mid,old['right'])
            approx_l+=a['ml'].midfloat()+b['ml'].midfloat()-old['ml'].midfloat()
            approx_u+=a['mu'].midfloat()+b['mu'].midfloat()-old['mu'].midfloat()
            count+=1; heapq.heappush(heap,(-a['gap'],count,a))
            count+=1; heapq.heappush(heap,(-b['gap'],count,b))
        cells=sorted((x[2] for x in heap),key=lambda c:c['left'])
        lo,up=self.sums(cells)
        eps=(I(1)-I(lo.lo)/I(up.hi)).hi
        return cells,lo,up,eps

    def moment_bounds(self,cells,ones,lo,up):
        nl,nu=self.sums(cells,ones)
        return (I(nl.lo)/I(up.hi)).lo,(I(nu.hi)/I(lo.lo)).hi


def expanded_reference(modules,gamma,t,mark,cells):
    import numpy as np
    from scipy.linalg import expm
    n=len(modules); states=list(itertools.product((0,1),repeat=n+1))
    index={x:i for i,x in enumerate(states)}; Q=np.zeros((len(states),len(states)))
    mu=np.zeros(len(states))
    for row,x in enumerate(states):
        c=x[0]
        if c==0:
            y=(1,)+x[1:]; Q[row,index[y]]+=float(gamma)
            p=1.
            for i,m in enumerate(modules):
                on=float(m.alpha/(m.alpha+m.beta)); p*=on if x[i+1] else 1-on
            mu[row]=p
        for i,m in enumerate(modules):
            y=list(x); y[i+1]=1-y[i+1]
            Q[row,index[tuple(y)]]+=float(m.alpha if x[i+1]==0 else m.beta)
        Q[row,row]=-sum(Q[row])
        if c: Q[row,row]-=sum(float(m.kappa)*x[i+1] for i,m in enumerate(modules))
    surviving=mu@expm(float(t)*Q)
    entrance={s:0. for s in itertools.product((0,1),repeat=n)}
    for x,p in zip(states,surviving):
        if x[0] and x[mark+1]:
            y=list(x[1:]); y[mark]=0
            entrance[tuple(y)]+=p*float(modules[mark].kappa)
    max_violation=-1.
    for x,true in entrance.items():
        lower=0.; upper=0.
        for cell in cells:
            a=float(cell['cl']); b=float(cell['cu'])
            for i,state in enumerate(x):
                a*=float(cell['rows_l'][i][state]); b*=float(cell['rows_u'][i][state])
            lower+=a; upper+=b
        max_violation=max(max_violation,lower-true,true-upper)
    density=sum(entrance.values())
    means=[sum(p for x,p in entrance.items() if x[i])/density for i in range(n)]
    pair=sum(p for x,p in entrance.items() if x[1] and x[2])/density
    return {'expanded_states':len(states),'density':density,'posterior_marginals':means,
            'posterior_covariance_1_2':pair-means[1]*means[2],
            'maximum_signed_componentwise_violation':max_violation}


def run_case(n,gamma,t,tolerance,check=False):
    modules=[BinaryModule(F(3,5)+F(i,100),F(2,5)+F(i%5,50),F(3,2)+F(i%3,10)) for i in range(n)]
    started=time.time(); model=Entrance(modules,F(gamma),F(t),0)
    cells,lo,up,eps=model.build(F(tolerance))
    m1=model.moment_bounds(cells,(1,),lo,up)
    m2=model.moment_bounds(cells,(2,),lo,up)
    p12=model.moment_bounds(cells,(1,2),lo,up)
    cov_lower=DOWN.subtract(p12[0],UP.multiply(m1[1],m2[1]))
    cov_upper=UP.subtract(p12[1],DOWN.multiply(m1[0],m2[0]))
    out={'new_work':True,'modules':n,'configuration_count':str(2**(n+1)),
         'gamma':str(gamma),'event_time':str(t),'event_mark':0,
         'positive_product_terms':len(cells),'entrance_density_lower':str(lo.lo),
         'entrance_density_upper':str(up.hi),'posterior_TV_upper':str(eps),
         'requested_posterior_TV':str(tolerance),
         'requested_tolerance_met':eps<=I(tolerance).lo,
         'posterior_marginal_1_interval':[str(x) for x in m1],
         'posterior_marginal_2_interval':[str(x) for x in m2],
         'posterior_pair_probability_interval':[str(x) for x in p12],
         'posterior_covariance_interval':[str(cov_lower),str(cov_upper)],
         'elapsed_seconds':time.time()-started}
    if check: out['independent_expanded_reference']=expanded_reference(modules,F(gamma),F(t),0,cells)
    return out


if __name__=='__main__':
    results=[run_case(3,F(7,10),F(2),F(1,10000),True),
             run_case(24,F(7,10),F(3,2),F(1,500),False)]
    print(json.dumps(results,indent=2))
    with open('tensor_separator_entrance_results.json','w') as handle:
        json.dump(results,handle,indent=2)
