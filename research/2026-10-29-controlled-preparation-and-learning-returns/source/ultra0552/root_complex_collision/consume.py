"""One fixed floating acquisition, not a finite-bit or all-law certificate."""
import json,time,importlib.util,sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from complex_dual import Counts,Model,model,ratio,rotation,complex_moment,exact_velocity,approximate_velocity,_a

def summarize(x,target):
    x=np.asarray(x);se=float(x.std(ddof=1)/np.sqrt(len(x)))
    return dict(n=len(x),mean=float(x.mean()),target=float(target),stderr=se,
                z=(float(x.mean())-float(target))/se if se else None)

def run():
    start=time.perf_counter();rng=np.random.default_rng(2026102951);out={}
    direction=np.array([.5,.5j,np.sqrt(.5)],complex)
    assert abs(np.vdot(direction,direction)-1)<1e-12
    alpha=float(direction.real@direction.real)
    for _ in range(128):
        r=rotation(rng);a=(np.eye(3)+r)/2
        uu=float(np.linalg.norm(a.T@(direction.real/np.linalg.norm(direction.real)))**2)
        uw=float(np.linalg.norm(a.T@(direction.imag/np.linalg.norm(direction.imag)))**2)
        u=float(np.vdot(a.T@direction,a.T@direction).real)
        assert abs(u-alpha*uu-(1-alpha)*uw)<2e-15
        for q in (2,3,5):
            phi=lambda z:z**q+(1-z)**q
            assert phi(u)<=alpha*phi(uu)+(1-alpha)*phi(uw)+2e-15
    out['jensen_controls']=384
    old=_a.declared_model();m=Model(old.matrices,old.probabilities,old.a,old.b)
    refpath=Path(__file__).resolve().parents[1]/'t_collision_operation'/'moment_reference.py'
    spec=importlib.util.spec_from_file_location('root_complex_reference',refpath)
    ref=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ref;spec.loader.exec_module(ref)
    data=ref.construct();out['complex_moments']=[]
    for t in (0.,3.):
        cov=m.covariance(t);m2=direction@cov@direction
        y=expm(t*data['matrix'])@data['initial']
        powers=np.array([np.prod(direction**np.array(p)) for p in data['monomials']])
        m4=powers@y[:15];zz=direction@direction
        target=(m4/3-2*m.c*zz*m2+m.c*m.c*zz*zz)/(m.h*m.h)
        count=Counts();values=np.array([complex_moment(2,direction,t,m.draw_e,rng,count) for _ in range(20000)])
        out['complex_moments'].append(dict(t=t,real=summarize(values.real,target.real),
                imag=summarize(values.imag,target.imag),counts=count.json()))
    out['ratio_controls']=[]
    for b in (1.1,1.8,3.):
        m=model(b=b);v=np.array([1.,.5,-.25]);count=Counts()
        f=sum(p*np.exp(-v@np.linalg.solve(s,v)/2)/np.sqrt(np.linalg.det(s))
              for p,s in zip(m.probabilities,m.matrices))/(2*np.pi)**1.5
        g=np.exp(-v@v/(2*m.b))/(2*np.pi*m.b)**1.5
        values=[ratio(v,0,m,rng,count) for _ in range(20000)]
        out['ratio_controls'].append(dict(b=b,C=m.C,estimate=summarize(values,f/g),counts=count.json()))
    out['exact_full_law']=[];m=model(b=1.8)
    for t in (0.,3.,1e6):
        count=Counts();tick=time.perf_counter()
        velocities=np.array([exact_velocity(t,m,rng,count) for _ in range(1000)])
        out['exact_full_law'].append(dict(t=t,n=1000,seconds=time.perf_counter()-tick,
                covariance_diagonal=[summarize(velocities[:,i]**2,m.covariance(t)[i,i]) for i in range(3)],
                counts=count.json(),qualification='floating realization of ideal exact-law algorithm'))
    m=model(b=3.);eps=.5;queries=int(np.ceil(m.C*m.C*(1+eps)**2/eps**2));count=Counts();tick=time.perf_counter()
    velocities=np.array([approximate_velocity(30.,m,queries,rng,count) for _ in range(64)])
    out['arbitrary_contrast_positive_consumer']=dict(b=m.b,epsilon_TV_ideal_bound=eps,
                queries_per_proposal=queries,n=64,seconds=time.perf_counter()-tick,
                counts=count.json(),qualification='small floating execution only; TV theorem is analytic')
    out['seconds']=time.perf_counter()-start
    out['scope']='new direct COMPLEX operation; all discrepancies retained; ideal theorem separate from floating samples'
    out['seed']=2026102951
    return out

if __name__=='__main__':
    result=run();Path(__file__).with_name('EXECUTION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(seconds=result['seconds'],jensen_controls=result['jensen_controls'],
          ratio_z=[(r['b'],r['estimate']['z']) for r in result['ratio_controls']],
          exact_seconds=[(r['t'],r['seconds']) for r in result['exact_full_law']],
          approximate=result['arbitrary_contrast_positive_consumer']),indent=2))
