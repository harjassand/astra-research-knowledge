"""Paired replay: both acquisition functions receive identical raw fields and x0."""
import sys,json,hashlib,time,traceback
from pathlib import Path
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from toda_tensor_acquisition import acquire
from toda_selfadjoint_comparator import recognize,standard,mix

def main():
    out={'sympy_version':s.__version__,'cases':[]}
    for N in [3,4,5]:
        n=2*N;x=s.symbols('x:'+str(n));y=s.symbols('y:'+str(n));M=mix(n)
        f=(M*standard(y)).subs(dict(zip(y,M.inv()*s.Matrix(x))),simultaneous=True).applyfunc(s.expand)
        x0=M*s.Matrix(list(range(1,N+1))+[(i%3)-1 for i in range(N)])
        raw={'variables':list(map(str,x)),'f':list(map(str,f)),'x0':list(map(str,x0))}
        a=acquire(f,x,x0);b=recognize(f,x,x0);B=b.pop('chart');A=s.Matrix(a['acquired_chart']).applyfunc(s.sympify)
        H=B*A.inv();Y=s.Matrix(y)
        assert (H*standard(y)-standard(H*Y)).applyfunc(s.expand)==s.zeros(n,1)
        rec={'N':N,'raw_sha256':hashlib.sha256(json.dumps(raw,sort_keys=True).encode()).hexdigest(),'raw':raw,'tensor':a,'selfadjoint':b,'chart_transition_is_exact_toda_symmetry':True}
        out['cases'].append(rec)
        print(N,a['seconds'],b['acquisition_seconds'],flush=True)
    N=4;n=8;x=s.symbols('x:8');a=x[:N];b=x[N:];edges=[(0,1),(1,2),(2,0),(0,3)]
    bad=s.Matrix([a[i]*(b[v]-b[u]) for i,(u,v) in enumerate(edges)]+[sum(2*a[i]**2*((u==k)-(v==k)) for i,(u,v) in enumerate(edges)) for k in range(N)])
    out['negative_controls']=[]
    for label,M in [('unmixed',s.eye(n)),('mixed',mix(n))]:
        f=(M*bad).subs(dict(zip(x,M.inv()*s.Matrix(x))),simultaneous=True).applyfunc(s.expand)
        x0=M*s.Matrix([1,2,3,4,0,1,2,3]);res={'case':label}
        for name,fn in [('tensor',acquire),('selfadjoint',recognize)]:
            try:fn(f,x,x0);res[name]='ACCEPTED'
            except AssertionError as e:res[name]='rejected: '+traceback.extract_tb(e.__traceback__)[-1].line
        assert all(res[k].startswith('rejected') for k in ['tensor','selfadjoint'])
        out['negative_controls'].append(res)
    out['jordan_identity_counterexamples']=[]
    for N in [3,4,5]:
        y=s.symbols('y:'+str(2*N));f=standard(y)
        T=[s.hessian(v,y)/2 for v in f]
        def product(v,w):return s.Matrix([(v.T*t*w)[0] for t in T])
        z=s.eye(2*N)[:,0];zz=product(z,z)
        residual=product(z,product(zz,z))-product(zz,product(z,z))
        assert residual==-2*zz and residual!=s.zeros(2*N,1)
        out['jordan_identity_counterexamples'].append({'N':N,'z':list(map(str,z)),'residual':list(map(str,residual))})
    out['source_sha256']={str(p.name):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_name('toda_selfadjoint_comparator.py'),Path(__file__).parents[1]/'toda_tensor_acquisition.py']}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
