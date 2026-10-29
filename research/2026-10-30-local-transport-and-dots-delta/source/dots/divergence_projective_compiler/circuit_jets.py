"""Circuit-jet acquisition: no multivariate monomial expansion during discovery.

The final optional verifier expands exact polynomials and is reported separately.
The input circuit is compiled from raw coefficient equations, never a hidden chart.
"""
from fractions import Fraction as F
from math import factorial
import random, time, json
from pathlib import Path
import sympy as sp
import experiment as exact

class Circuit:
    def __init__(self,n):
        self.n=n;self.nodes=[];self.ids={};self.variables=[self.node('var',i) for i in range(n)]
        self.zero=self.const(0);self.one=self.const(1)
    def node(self,op,*args):
        key=(op,*args)
        if key not in self.ids:self.ids[key]=len(self.nodes);self.nodes.append(key)
        return self.ids[key]
    def const(self,c):return self.node('const',F(c))
    def add(self,a,b):
        if a==self.zero:return b
        if b==self.zero:return a
        return self.node('add',a,b)
    def mul(self,a,b):
        if a==self.zero or b==self.zero:return self.zero
        if a==self.one:return b
        if b==self.one:return a
        return self.node('mul',a,b)
    def scale(self,c,a):return self.mul(self.const(c),a)
    def power(self,a,k):
        if k==0:return self.one
        if k==1:return a
        b=self.power(a,k//2);out=self.mul(b,b)
        return self.mul(out,a) if k%2 else out
    def compile(self,expr,variables):
        if expr in variables:return self.variables[variables.index(expr)]
        if expr.is_Rational:return self.const(F(int(expr.p),int(expr.q)))
        if expr.is_Add:
            out=self.zero
            for a in expr.args:out=self.add(out,self.compile(a,variables))
            return out
        if expr.is_Mul:
            out=self.one
            for a in expr.args:out=self.mul(out,self.compile(a,variables))
            return out
        if expr.is_Pow and expr.exp.is_Integer and expr.exp>=0:
            return self.power(self.compile(expr.base,variables),int(expr.exp))
        raise ValueError(expr)
    def derivative(self,root,j):
        d=[]
        for i,node in enumerate(self.nodes[:root+1]):
            op,*a=node
            if op=='var':v=self.one if a[0]==j else self.zero
            elif op=='const':v=self.zero
            elif op=='add':v=self.add(d[a[0]],d[a[1]])
            else:v=self.add(self.mul(d[a[0]],a[1]),self.mul(a[0],d[a[1]]))
            d.append(v)
        return d[root]
    def manufacture_q(self,roots):
        out=self.zero
        for i,r in enumerate(roots):out=self.add(out,self.derivative(r,i))
        return self.scale(F(-1,self.n+1),out)
    def jets(self,roots,q,m,point,order):
        # Arrays store Taylor coefficients, not derivatives.
        X=[[F(a)]+[F(0)]*order for a in point]
        W=[F(1)]+[F(0)]*order
        vals=[[F(0)]*(order+1) for _ in self.nodes]
        for k in range(order):
            for i,node in enumerate(self.nodes):
                op,*a=node
                if op=='var':v=X[a[0]][k]
                elif op=='const':v=a[0] if k==0 else F(0)
                elif op=='add':v=vals[a[0]][k]+vals[a[1]][k]
                else:v=sum((vals[a[0]][j]*vals[a[1]][k-j] for j in range(k+1)),F(0))
                vals[i][k]=v
            for j,r in enumerate(roots):X[j][k+1]=vals[r][k]/(k+1)
            W[k+1]=m*sum((vals[q][j]*W[k-j] for j in range(k+1)),F(0))/(k+1)
        outputs=[[factorial(k)*W[k] for k in range(order+1)]]
        outputs += [[factorial(k)*sum((W[j]*xi[k-j] for j in range(k+1)),F(0)) for k in range(order+1)] for xi in X]
        maxbits=max(max(abs(v.numerator).bit_length(),v.denominator.bit_length()) for arr in vals+X+[W] for v in arr)
        return outputs,maxbits

def linadd(a,b,scale=F(1)):
    out=a.copy()
    for k,v in b.items():out[k]=out.get(k,F(0))+scale*v
    return {k:v for k,v in out.items() if v}
def lineval(f,jet):return sum((c*jet[i][k] for (i,k),c in f.items()),F(0))
def shift(f):return {(i,k+1):c for (i,k),c in f.items()}

def acquire_circuit(circuit,roots,q,m,R,seed=92644,sample_size=65536,verify_points=4):
    if R<circuit.n+1:
        return dict(status='EXACT_EVALUATION_RANK_LOWER_BOUND',rank_lower_bound=circuit.n+1,weight=m,seconds=0.,reason='Independent original coordinate seeds already exceed budget.')
    rng=random.Random(seed);order=R+1
    start=time.perf_counter()
    train=[];peakbits=0
    for _ in range(R+1):
        point=[rng.randrange(sample_size) for _ in range(circuit.n)]
        jet,bits=circuit.jets(roots,q,m,point,order);train.append(jet);peakbits=max(peakbits,bits)
    # Keep normalized evaluation-echelon rows AND their original circuit functions.
    basis=[];evaluations=[];pivots=[]
    # Preserve original seed locations via a seed reconstruction matrix.
    seed_rows=[]
    for i in range(circuit.n+1):
        f={(i,0):F(1)};vec=[lineval(f,j) for j in train];row={}
        for j,(b,e,p) in enumerate(zip(basis,evaluations,pivots)):
            c=vec[p]
            if c:
                row[j]=c;f=linadd(f,b,-c);vec=[a-c*z for a,z in zip(vec,e)]
        if not any(vec):
            return dict(status='INCONCLUSIVE_TRAINING_SKETCH',weight=m,seconds=time.perf_counter()-start,reason='The independent original coordinate seeds lost rank in the sampled evaluation sketch.')
        p=next(k for k,v in enumerate(vec) if v);c=vec[p]
        row[len(basis)]=c
        basis.append({a:v/c for a,v in f.items()});evaluations.append([v/c for v in vec]);pivots.append(p);seed_rows.append(row)
    rows=[];idx=0
    while idx<len(basis):
        f=shift(basis[idx]);vec=[lineval(f,j) for j in train];row={}
        for j,(b,e,p) in enumerate(zip(basis,evaluations,pivots)):
            c=vec[p]
            if c:
                row[j]=c;f=linadd(f,b,-c);vec=[a-c*z for a,z in zip(vec,e)]
        if any(vec):
            p=next(k for k,v in enumerate(vec) if v);c=vec[p]
            row[len(basis)]=c
            basis.append({a:v/c for a,v in f.items()});evaluations.append([v/c for v in vec]);pivots.append(p)
            if len(basis)>R:
                return dict(status='EXACT_EVALUATION_RANK_LOWER_BOUND',rank_lower_bound=len(basis),weight=m,seconds=time.perf_counter()-start,peak_jet_bits=peakbits,gate_count=len(circuit.nodes))
        rows.append(row);idx+=1
    residuals=[]
    for b,row in zip(basis,rows):
        res=shift(b)
        for j,c in row.items():res=linadd(res,basis[j],-c)
        residuals.append(res)
    for i,row in enumerate(seed_rows):
        res={(i,0):F(1)}
        for j,c in row.items():res=linadd(res,basis[j],-c)
        residuals.append(res)
    for _ in range(verify_points):
        point=[rng.randrange(sample_size) for _ in range(circuit.n)]
        jet,bits=circuit.jets(roots,q,m,point,order);peakbits=max(peakbits,bits)
        if any(lineval(f,jet) for f in residuals):
            return dict(status='CANDIDATE_REJECTED_BY_FRESH_EXACT_POINT',weight=m,seconds=time.perf_counter()-start)
    coeffs=[c for b in basis for c in b.values()]+[c for row in rows+seed_rows for c in row.values()]
    maxoutbits=max(max(abs(c.numerator).bit_length(),c.denominator.bit_length()) for c in coeffs)
    return dict(status='MONTE_CARLO_CLOSURE',dimension=len(basis),weight=m,core_acquisition_seconds=time.perf_counter()-start,peak_jet_bits=peakbits,output_coefficient_peak_bits=maxoutbits,gate_count=len(circuit.nodes),training_points=R+1,verification_points=verify_points,sample_set_size=sample_size,max_krylov_order=max(k for f in basis for i,k in f)+1,basis_jet_combinations=[[[i,k,str(c)] for (i,k),c in b.items()] for b in basis],matrix=[[str(row.get(j,F(0))) for j in range(len(basis))] for row in rows],seed_reconstruction=[[str(row.get(j,F(0))) for j in range(len(basis))] for row in seed_rows],_residuals=residuals,_basis=basis)

def exact_residual_verifier(raw_poly,m,residuals):
    q={}
    for i,f in enumerate(raw_poly):q=exact.add(q,exact.deriv(f,i),F(-1,len(raw_poly)+1))
    def T(p):
        r=exact.mul(q,p);r={a:m*c for a,c in r.items()}
        for j,f in enumerate(raw_poly):r=exact.add(r,exact.mul(exact.deriv(p,j),f))
        return r
    cache={(0,0):{(0,0):F(1)},(1,0):{(1,0):F(1)},(2,0):{(0,1):F(1)}}
    def value(i,k):
        if (i,k) not in cache:cache[i,k]=T(value(i,k-1))
        return cache[i,k]
    for r in residuals:
        p={}
        for (i,k),c in r.items():p=exact.add(p,value(i,k),c)
        assert not p

def main():
    source=json.loads(Path(__file__).with_name('results.json').read_text())
    raw=[sp.sympify(s,locals={'x':exact.x,'y':exact.y}) for s in source['raw_vector_field']]
    circuit=Circuit(2);roots=[circuit.compile(f,exact.VARS) for f in raw];q=circuit.manufacture_q(roots)
    results=[]
    for m in [0,4]:
        result=acquire_circuit(circuit,roots,q,m,16)
        print({k:v for k,v in result.items() if not k.startswith('_')},flush=True)
        if result['status']=='MONTE_CARLO_CLOSURE':
            start=time.perf_counter();exact_residual_verifier(list(map(exact.fromsym,raw)),m,result['_residuals'])
            result['deterministic_identity_replay_seconds']=time.perf_counter()-start
            result['deterministic_identity_replay']='PASS';result['status']='EXACTLY_REPLAYED_CIRCUIT_CLOSURE'
            # Validate the decoder built from THIS circuit-acquired basis, not
            # the separately constructed coefficient basis. High precision is
            # necessary because evaluation normalization may be ill-conditioned.
            import mpmath as mp
            mp.mp.dps=180
            cv=lambda s:mp.mpf(str(F(s).numerator))/F(s).denominator
            A=mp.matrix([[cv(c) for c in row] for row in result['matrix']])
            C=mp.matrix([[cv(c) for c in row] for row in result['seed_reconstruction']])
            u0,v0=F(1,5),F(1,10);x0=u0+v0*v0;y0=v0+x0*x0
            jet,_=circuit.jets(roots,q,m,[x0,y0],17)
            b0=mp.matrix([cv(lineval(b,jet)) for b in result['_basis']])
            t=mp.mpf('0.2');z=C*mp.expm(t*A)*b0
            den=1+cv(u0)*(mp.exp(t)-1);ut=cv(u0)*mp.exp(t)/den;vt=cv(v0)*mp.exp(7*t)/den
            expected=[ut+vt*vt,vt+(ut+vt*vt)**2]
            err=max(abs(z[i+1]/z[0]-expected[i]) for i in range(2))
            assert err<mp.mpf('1e-60')
            result['own_decoder_check_absolute_error']=str(err)
            result['own_decoder_check_precision_digits']=180
        results.append({k:v for k,v in result.items() if not k.startswith('_')})
    Path(__file__).with_name('circuit_results.json').write_text(json.dumps(results,indent=2))

if __name__=='__main__':main()
