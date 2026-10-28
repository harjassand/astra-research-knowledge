"""Pay the same-model thermal mean comparators, including high peak/work.

U1 uses a proved small-field enclosure from the already acquired moment.
U=1/g uses a directed one-dimensional tilted integral, not a new topology
or trajectory. The classical scalar Gibbs competitor gets full source data.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D
import json,time,hashlib
from acquire_moments import I,DN,UP,NEAR,qi,abs_poly_upper

HERE=Path(__file__).resolve().parent

def positive_derivative(beta,h,m):
    p={m:I(1)}
    for _ in range(4):
        q={}
        def add(k,v):q[k]=q.get(k,I(0))+v
        for k,c in p.items():
            if k:add(k-1,k*c)
            add(k,h*c);add(k+1,c);add(k+3,beta*c)
        p=q
    return [p.get(k,I(0)).hi for k in range(max(p)+1)]

def high_field(case,cells=2048):
    start=time.perf_counter();d=F(case['Rpp_equals_Rvv']);g=F(case['Rpv'])
    beta=qi(F(case['standardized_quartic_beta']));h=1/qi(d).sqrt()
    xmax=D(12);step=xmax/D(cells);half=step/2
    xs=[D(j)*half for j in range(2*cells+1)]
    vals={0:[],2:[]};bounds=[]
    for x in xs:
        z=I(x);base=(-(z.sq()/2+beta*z.sq().sq()/4)).exp()
        t=h*z;ep=t.exp();em=(-t).exp()
        vals[0].append(base*(ep+em)/2)
        vals[2].append(base*z.sq()*((ep-em)/(2*t) if x else I(1)))
    coeff={m:positive_derivative(beta,h,m) for m in [0,2]}
    sim={m:I(0) for m in [0,2]};err={m:D(0) for m in [0,2]}
    factor=qi(F(step)**5/2880).hi
    for j in range(cells):
        xl=I(xs[2*j]);xr=I(xs[2*j+2])
        envelope=(-(xl.sq()/2+beta*xl.sq().sq()/4)+h*xr).exp().hi
        for m in [0,2]:
            f=vals[m];sim[m]=sim[m]+(f[2*j]+4*f[2*j+1]+f[2*j+2])*I(step)/6
            bound=UP.multiply(envelope,abs_poly_upper(coeff[m],xr.hi))
            err[m]=UP.add(err[m],UP.multiply(factor,bound))
    t=I(xmax)-h;assert t.lo>0
    envelope=(h.sq()/2-t.sq()/2).exp()
    tail0=(envelope/t).hi
    tail2=(envelope*(t+1/t+2*h+h.sq()/t)).hi
    integrals={m:I(DN.subtract(sim[m].lo,err[m]),UP.add(UP.add(sim[m].hi,err[m]),tail))
               for m,tail in [(0,tail0),(2,tail2)]}
    response=integrals[2]/integrals[0];assert 0<response.lo<response.hi<1
    contrast=qi(g/d)*(1-response)
    return {'name':case['name'],'peak_U':str(1/g),'hidden_Gaussian_mean_Ug':'1',
            'standardized_field':h.encode(),'response_ratio_EX_over_Ug':response.encode(),
            'thermal_port_mean_decrease_lower':str(contrast.lo),'thermal_port_mean_decrease_interval':contrast.encode(),
            'Simpson_cells':cells,'quadrature_nodes':len(xs),
            'half_line_integrals':{str(m):v.encode() for m,v in integrals.items()},
            'Simpson_remainders':{str(m):str(v) for m,v in err.items()},
            'Gaussian_tail_bounds':{'0':str(tail0),'2':str(tail2)},
            'reference_port_mean':str(d/g),'reference_quadratic_loading_energy':str(d/(2*g*g)),
            'seconds_afterimports':time.perf_counter()-start}

def weak_field(case):
    d=qi(F(case['Rpp_equals_Rvv']));g=qi(F(case['Rpv']));h=g/d.sqrt()
    m2=I(*case['standardized_second_moment'])
    upper=m2+h.sq()*(h.sq().sq()+6*h.sq()+3)*(h.sq()/2).exp()/6
    lower=m2*(-h.sq()/2).exp()
    response=I(lower.lo,upper.hi);assert response.hi<1
    contrast=g.sq()/d*(1-response)
    return {'name':case['name'],'peak_U':'1','response_ratio_EX_over_Ug':response.encode(),
            'thermal_port_mean_decrease_interval':contrast.encode(),
            'reference_port_mean':d.encode(),'reference_quadratic_loading_energy':(d/2).encode(),
            'new_quadratures':0,'scope':'Gaussian absolute-moment domination and sinhc Taylor bound; finite positive field, not a derivative asserted equal to a finite difference.'}

def main():
    start=time.perf_counter();raw=(HERE/'MOMENTS.json').read_bytes();m=json.loads(raw)
    weak=[weak_field(c) for c in m['cases']]
    high=[high_field(c) for c in m['cases']]
    out={'status':'SAME_MODEL_THERMAL_MEAN_COMPARATORS_ACQUIRED','weak_fixed_peak':weak,'high_peak':high,
         'input_moments_sha256':hashlib.sha256(raw).hexdigest(),'seconds_afterimports':time.perf_counter()-start,
         'new_topologies':0,'new_trajectories':0,'physical_readouts':0,
         'scope':'All-alpha>=Delta monotonicity of the positively tilted absolute scalar law is required. Peak U and harmonic-reference loading energy are reported, not granted free or claimed to be a universal work lower bound.'}
    (HERE/'ACTIVE_INPUTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='high_peak'},indent=2))
    print(json.dumps({'high_peak_summary':[{k:v for k,v in c.items() if k not in ['half_line_integrals','Simpson_remainders','Gaussian_tail_bounds']} for c in high]},indent=2))

if __name__=='__main__':main()
