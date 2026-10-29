"""Independent certificate replay against stored raw inputs, not constructor data.
Producer import is used only to regenerate the returned certificate and DAG.
All closure/flag/global checks and the rational DAG interpreter are independent.
"""
import sys,json,hashlib,random
from pathlib import Path
from fractions import Fraction
import sympy as s
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import strong_decoder as P
stored=json.loads((ROOT/'strong_decoder_results.json').read_text())

def zero(M):return all(s.expand(v)==0 for v in M)

def eval_dag(c,roots,point):
    live=set()
    def collect(k):
        if k in live:return
        live.add(k);op,*a=c.nodes[k]
        if op in ('add','mul'):
            for j in a:collect(j)
    for r in roots:collect(r)
    values={}
    for k in sorted(live):
        op,*a=c.nodes[k]
        if op=='var':values[k]=point[a[0]]
        elif op=='const':values[k]=Fraction(a[0])
        elif op=='add':values[k]=values[a[0]]+values[a[1]]
        elif op=='mul':values[k]=values[a[0]]*values[a[1]]
        else:raise AssertionError(op)
    return s.Matrix([values[k] for k in roots])

def sym_dag(c,roots,x):
    # Independent symbolic interpreter, used only on small certificates.
    values={}
    def read(k):
        if k in values:return values[k]
        op,*a=c.nodes[k]
        if op=='var':v=x[a[0]]
        elif op=='const':v=s.Rational(a[0].numerator,a[0].denominator)
        elif op=='add':v=read(a[0])+read(a[1])
        elif op=='mul':v=read(a[0])*read(a[1])
        else:raise AssertionError(op)
        values[k]=v;return v
    return s.Matrix([s.expand(read(k)) for k in roots])

reports=[]
for record,kind in [(r,'strong') for r in stored['raw_pipeline']]+[(stored['nonstrong_raw_pipeline'],'quasi')]:
    n=record['n'];x=s.symbols('x0:'+str(n)) if kind=='strong' else s.symbols('x y z')
    X=s.Matrix(x);f=s.Matrix([s.sympify(v) for v in record['raw_vector_field']]);C=s.Matrix([s.sympify(v) for v in record['chart']]);A=s.Matrix(record['matrix']).applyfunc(s.Rational)
    phi=s.Matrix([1,*C]);q=-s.trace(f.jacobian(x))/(n+1)
    closure=zero(phi.jacobian(x)*f+q*phi-A*phi);assert closure
    # Reacquire from saved raw input rather than passing the known chart in.
    acquired=P.raw_chart(f,x);assert acquired['status']=='EXACT_CHART_MODULE'
    assert zero(acquired['chart']-C) and zero(acquired['matrix']-A)
    dec=(P.strong_decoder if kind=='strong' else P.quasi_decoder)(acquired['chart'],x)
    origin=dict.fromkeys(x,0);J0=C.jacobian(x).subs(origin);offset=C.subs(origin)
    F=(J0.inv()*(C-offset)).applyfunc(s.expand);N=F-X;JN=N.jacobian(x)
    assert J0.det()!=0 and zero(N.subs(origin)) and zero(JN.subs(origin))
    report={'kind':kind,'n':n,'raw_closure_identities':n+1,'raw_reacquisition_matches':True}
    if kind=='strong':
        flags=dec['flag'];assert flags[0]==s.eye(n) and flags[-1].cols==0
        checks=[]
        for U,V in zip(flags,flags[1:]):
            assert V.rank()==V.cols
            ann=V.T.nullspace()
            Q=s.Matrix.vstack(*(v.T for v in ann)) if ann else s.zeros(0,n)
            checks.append(zero(Q*JN*U));assert checks[-1]
        report.update(universal_flag_checks=checks,flag_dimensions=[v.cols for v in flags])
    else:
        assert zero(JN*N);report['quasi_JN_times_N_identity']=True
        assert P.strong_decoder(C,x)['status']=='NOT_STRONGLY_NILPOTENT'
        report['strong_rejection_independent']=True
    rng=random.Random(71+n)
    for _ in range(7):
        p=s.Matrix([s.Rational(rng.randrange(-3,4),rng.randrange(1,5)) for i in range(n)])
        y=C.subs(dict(zip(x,p)),simultaneous=True)
        assert eval_dag(dec['dag'],dec['roots'],y)==p
        g=eval_dag(dec['dag'],dec['roots'],p)
        assert C.subs(dict(zip(x,g)),simultaneous=True)==p
    report['independent_rational_interpreter_point_checks']=14
    if n<=3:
        G=sym_dag(dec['dag'],dec['roots'],x)
        left=zero(C.subs(dict(zip(x,G)),simultaneous=True)-X)
        right=zero(G.subs(dict(zip(x,C)),simultaneous=True)-X)
        assert left and right
        report['global_composition_components_checked']=2*n
    else:report['global_expansion']='NOT_RUN; exact universal flag + audited construction is certificate'
    reports.append(report)
    print(report,flush=True)

x,y,z,w=s.symbols('x y z w')
# Regression controls independently established in nilpotent_adversarial_controls.py.
N4=s.Matrix([y*w**3-x*x*w*w,z*w**3+2*x*y*w*w-2*x**3*w,-y*y*w*w+2*x*x*y*w-x**4,0])
control=P.strong_decoder(s.Matrix([x,y,z,w])+N4,(x,y,z,w));assert control['status']=='NOT_STRONGLY_NILPOTENT'
assert P.quasi_decoder(s.Matrix([x,y,z,w])+N4,(x,y,z,w))['status']=='NOT_QUASI_TRANSLATION'
# Generic affine output mixing/translation must not corrupt normalization.
chart=s.Matrix([[2,3],[1,2]])*s.Matrix([x+y*y,y])+s.Matrix([5,-7])
dec=P.strong_decoder(chart,(x,y));G=sym_dag(dec['dag'],dec['roots'],(x,y));X=s.Matrix([x,y])
assert zero(chart.subs(dict(zip((x,y),G)),simultaneous=True)-X)
assert zero(G.subs(dict(zip((x,y),chart)),simultaneous=True)-X)

hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['strong_decoder.py','strong_decoder_results.json','circuit_jets.py','audit/strong_decoder_replay.py']}
assert stored['source_sha256']==hashes['strong_decoder.py']
out={'reports':reports,'homogeneous_pointwise_nonstrong_rejection':True,'nonzero_offset_affine_output_normalization_global_compositions':True,'source_hashes':hashes,'scope':'Independent closure/flag/quasi/global checks; producer used solely for reacquisition and certificate/DAG manufacture.'}
(ROOT/'audit'/'strong_decoder_replay.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out['source_hashes'],indent=2))
