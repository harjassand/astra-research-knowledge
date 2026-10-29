"""Floating anisotropic Haar-reset consumer, NOT a Choi implementation."""
from pathlib import Path
import importlib.util,sys,json,time
import numpy as np
from scipy.linalg import expm
sys.dont_write_bytecode=True
p=Path(__file__).resolve().parents[1]/'root_complex_collision'/'complex_dual.py'
s=importlib.util.spec_from_file_location('root_rotation_complex',p)
c=importlib.util.module_from_spec(s);sys.modules[s.name]=c;s.loader.exec_module(c)

class Kernel:
    def __init__(self,eta=.25):
        self.eta=eta;self.fixed=np.array([[0.,-1,0],[1,0,0],[0,0,1.]])
        vec=np.eye(3).ravel();twirl=np.outer(vec,vec)/3
        self.generator=(eta*twirl+(1-eta)*np.kron(self.fixed,self.fixed)-np.eye(9))/2
        self.singleton_rotations=0;self.singleton_resets=0
    def draw(self,rng):return c.rotation(rng) if rng.random()<self.eta else self.fixed
    def covariance(self,t,m):return (expm(t*self.generator)@m.ravel()).reshape(3,3)
    def singleton(self,z,t,draw_e,rng):
        e=draw_e(rng)
        if rng.random()>=np.exp(-self.eta*t/2):
            self.singleton_resets+=1;return np.trace(e)/3*(z@z)
        n=int(rng.poisson((1-self.eta)*t/2));self.singleton_rotations+=n
        # Explicitly perform/charge every rare finite rotation, no free long path.
        for _ in range(n):z=self.fixed.T@z
        return z@e@z

def marked(q,z,t,model,kernel,rng,count):
    stack=[(q,z,t)];out=1.+0j
    while stack:
        q,z,left=stack.pop();count.blocks+=1
        if q==1:
            out*=kernel.singleton(z,left,model.draw_e,rng);count.initial_draws+=1;continue
        wait=rng.exponential()
        if wait>=left:
            out*=(z@model.draw_e(rng)@z)**q;count.initial_draws+=1;continue
        count.rotations+=1;r=kernel.draw(rng);za=(z+r.T@z)/2;zb=(z-r.T@z)/2
        ua=float(np.vdot(za,za).real);ub=float(np.vdot(zb,zb).real)
        assert abs(ua+ub-1)<1e-9;j=int(rng.binomial(q,ua/(ua+ub)))
        if j:stack.append((j,za/np.sqrt(ua),left-wait))
        if j<q:stack.append((q-j,zb/np.sqrt(ub),left-wait))
        if 0<j<q:count.splits+=1
    assert abs(out)<1+1e-8
    return out

def ratio(v,t,model,kernel,rng,count):
    count.queries+=1;xi=rng.normal(size=3)/np.sqrt(model.a);z=xi-1j*v/model.b
    r2=float(np.vdot(z,z).real);q=int(rng.poisson(model.h*r2/2))
    count.degree+=q;count.max_degree=max(count.max_degree,q)
    h=marked(q,z/np.sqrt(r2),t,model,kernel,rng,count) if q else 1
    return model.C*(((-1)**q)*np.exp(1j*(model.c/model.b-1)*float(xi@v))*h).real

def velocity(t,model,kernel,rng,count):
    while True:
        count.proposals+=1;v=np.sqrt(model.b)*rng.normal(size=3)
        ell=np.exp(-float(v@v)*(1/model.a-1/model.b)/2)
        def coin():return rng.random()<(1-ratio(v,t,model,kernel,rng,count)/model.C)/2
        if not c._a.linear_factory(coin,ell/model.C,rng,count):return v

def estimate(x,truth):
    x=np.asarray(x);se=float(x.std(ddof=1)/np.sqrt(len(x)))
    return dict(mean=float(x.mean()),reference=float(truth),stderr=se,z=(float(x.mean())-truth)/se if se else None)

def run():
    start=time.perf_counter();rng=np.random.default_rng(2026102962);model=c.model(b=1.1);kernel=Kernel();rows=[]
    z=np.array([.5,.5j,np.sqrt(.5)]);controls=[]
    for t in (0.,.1,3.,30.,1e6):
        mean=(model.mean-model.c*np.eye(3))/model.h;target=z@kernel.covariance(t,mean)@z
        before=kernel.singleton_rotations
        values=np.array([kernel.singleton(z,t,model.draw_e,rng) for _ in range(5000)])
        controls.append(dict(t=t,real=estimate(values.real,target.real),imag=estimate(values.imag,target.imag),
              rotations=kernel.singleton_rotations-before,expected_rotations=5000*np.exp(-kernel.eta*t/2)*(1-kernel.eta)*t/2))
    for t in (0.,3.,1e6):
        count=c.Counts();tick=time.perf_counter()
        vs=np.array([velocity(t,model,kernel,rng,count) for _ in range(500)])
        cov=kernel.covariance(t,model.mean)
        rows.append(dict(t=t,n=500,seconds=time.perf_counter()-tick,counts=count.json(),
                         covariance_controls=[estimate(vs[:,i]**2,cov[i,i]) for i in range(3)]))
    return dict(scope='FLOATING Haar-reset singleton/full-law execution; no Choi circuit, bit-exact or hardware claim',
                seed=2026102962,eta=kernel.eta,kernel='eta Haar + remaining fixed z-axis pi/2 rotation',
                singleton_controls=controls,full_law=rows,singleton_resets=kernel.singleton_resets,
                charged_singleton_rotations=kernel.singleton_rotations,seconds=time.perf_counter()-start)

if __name__=='__main__':
    r=run();Path(__file__).with_name('EXECUTION.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(dict(seconds=r['seconds'],exact_algorithm_floating_seconds=[(x['t'],x['seconds']) for x in r['full_law']],
                         singleton_rotations=r['charged_singleton_rotations']),indent=2))
