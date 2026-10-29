"""Exact acquisition of a strong-nilpotence inverse certificate and shared DAG.

The decoder receives only the chart.  The raw-field front end receives only raw
coefficients.  No triangular order or hidden chart enters either acquisition.
Polynomial expansion is paid in the front end/certificate, NEVER in the inverse.
"""
from pathlib import Path
from fractions import Fraction
import hashlib, json, time
import sympy as s
from circuit_jets import Circuit


class DAG(Circuit):
    def substitute(self, roots, replacements):
        # Compile one shared copy, not one recursive tree per output.
        old = list(self.nodes[:max(roots)+1]); remap = []
        for op, *a in old:
            if op == 'var': v = replacements[a[0]]
            elif op == 'const': v = self.const(a[0])
            elif op == 'add': v = self.add(remap[a[0]], remap[a[1]])
            else: v = self.mul(remap[a[0]], remap[a[1]])
            remap.append(v)
        return [remap[r] for r in roots]

    def reachable(self, roots):
        seen = set(); todo = list(roots)
        while todo:
            i = todo.pop()
            if i in seen: continue
            seen.add(i)
            if self.nodes[i][0] in ('add', 'mul'): todo += list(self.nodes[i][1:])
        return sorted(seen)

    def evaluate(self, roots, point):
        vals = {}; peak = 1
        for i in self.reachable(roots):
            op, *a = self.nodes[i]
            if op == 'var': v = Fraction(point[a[0]])
            elif op == 'const': v = a[0]
            elif op == 'add': v = vals[a[0]] + vals[a[1]]
            else: v = vals[a[0]] * vals[a[1]]
            vals[i] = v
            peak = max(peak, abs(v.numerator).bit_length(), v.denominator.bit_length())
        return [vals[r] for r in roots], peak

    def expand(self, roots, variables):
        vals = {}
        for i in self.reachable(roots):
            op, *a = self.nodes[i]
            if op == 'var': v = s.Poly(variables[a[0]], *variables)
            elif op == 'const': v = s.Poly(s.Rational(a[0].numerator, a[0].denominator), *variables)
            elif op == 'add': v = vals[a[0]] + vals[a[1]]
            else: v = vals[a[0]] * vals[a[1]]
            vals[i] = v
        return s.Matrix([vals[r].as_expr() for r in roots])


def raw_chart(raw, x):
    """General-n exact sparse Krylov acquisition, including global closure."""
    n = len(x); f = [s.Poly(v, *x) for v in raw]
    q = -sum((f[i].diff(x[i]) for i in range(n)), s.Poly(0, *x))/(n+1)
    def T(p): return sum((f[i]*p.diff(x[i]) for i in range(n)), q*p)
    basis = [s.Poly(1, *x)]; pivots = [(0,)*n]; rows = []; k = 0
    while k < len(basis):
        p = T(basis[k]); row = {}
        for j, (b, a) in enumerate(zip(basis, pivots)):
            c = p.coeff_monomial(a)
            if c: row[j] = c; p -= c*b
        if not p.is_zero:
            a, c = p.terms()[0]; row[len(basis)] = c
            basis.append(p/c); pivots.append(a)
            if len(basis) > n+1: return {'status':'RANK_EXCEEDED'}
        rows.append(row); k += 1
    if len(basis) != n+1: return {'status':'CYCLIC_RANK_DEFICIENT'}
    A = s.Matrix([[r.get(j, 0) for j in range(n+1)] for r in rows])
    for b, r in zip(basis, rows):
        assert (T(b)-sum((c*basis[j] for j,c in r.items()), s.Poly(0,*x))).is_zero
    return {'status':'EXACT_CHART_MODULE', 'chart':s.Matrix([v.as_expr() for v in basis[1:]]),
            'q':q.as_expr(), 'matrix':A}


def strong_decoder(chart, x):
    n = len(x); chart = s.Matrix(chart); origin = dict.fromkeys(x, 0)
    c = chart.subs(origin); J0 = chart.jacobian(x).subs(origin)
    if J0.det() == 0: return {'status':'SINGULAR_BASEPOINT'}
    F = (J0.inv()*(chart-c)).applyfunc(s.expand); N = F-s.Matrix(x)
    JN = N.jacobian(x); coeff = {}
    for i in range(n):
        for j in range(n):
            for a, v in s.Poly(JN[i,j], *x).terms():
                if v:
                    if a not in coeff: coeff[a] = s.zeros(n)
                    coeff[a][i,j] = v
    # Exact complete coefficient family; no sampling or pointwise shortcut.
    matrices = list(coeff.values()); V = s.eye(n); dims = [n]; flags = [V]
    for k in range(1, n+1):
        W = s.Matrix.hstack(*(M*V for M in matrices)) if matrices and V.cols else s.zeros(n, 0)
        cols = W.columnspace(); V = s.Matrix.hstack(*cols) if cols else s.zeros(n, 0)
        dims.append(V.cols); flags.append(V)
        if V.cols == 0: break
        if dims[-1] == dims[-2]: return {'status':'NOT_STRONGLY_NILPOTENT', 'flag_dimensions':dims}
    if V.cols: return {'status':'NOT_STRONGLY_NILPOTENT', 'flag_dimensions':dims}
    ell = len(dims)-1
    circuit = DAG(n); nr = [circuit.compile(v, x) for v in N]; g = circuit.variables
    stage_sizes = []
    for _ in range(ell):
        ng = circuit.substitute(nr, g)
        g = [circuit.add(z, circuit.scale(-1, v)) for z,v in zip(circuit.variables,ng)]
        stage_sizes.append(len(circuit.reachable(g)))
    # Complete original-chart inverse: substitute J0^-1(y-c) in G.
    targets = J0.inv()*(s.Matrix(x)-c)
    tr = [circuit.compile(v,x) for v in targets]
    g = circuit.substitute(g, tr)
    return {'status':'EXACT_FLAG_CERTIFIED_INVERSE_DAG', 'normalized_chart':F, 'normalizer':J0,
            'offset':c, 'coefficient_matrices':matrices, 'flag':flags,
            'flag_dimensions':dims, 'nilpotence_length':ell, 'dag':circuit, 'roots':g,
            'stage_reachable_nodes':stage_sizes, 'inverse_reachable_nodes':len(circuit.reachable(g)),
            'inverse_total_allocated_nodes':len(circuit.nodes),
            'source_normalized_chart_nodes':len(DAG_from(F,x)[0].nodes)}


def DAG_from(F, x):
    c = DAG(len(x)); return c, [c.compile(v,x) for v in F]


def quasi_decoder(chart, x):
    """Classical quasi-translation admission: (JN)N=0, not strong nilpotence."""
    n=len(x); chart=s.Matrix(chart); origin=dict.fromkeys(x,0)
    c=chart.subs(origin); J0=chart.jacobian(x).subs(origin)
    if J0.det()==0:return {'status':'SINGULAR_BASEPOINT'}
    F=(J0.inv()*(chart-c)).applyfunc(s.expand); N=F-s.Matrix(x)
    if any(s.expand(v)!=0 for v in N.jacobian(x)*N):return {'status':'NOT_QUASI_TRANSLATION'}
    circuit=DAG(n); nr=[circuit.compile(v,x) for v in N]
    gr=[circuit.add(z,circuit.scale(-1,v)) for z,v in zip(circuit.variables,nr)]
    tr=[circuit.compile(v,x) for v in J0.inv()*(s.Matrix(x)-c)]
    gr=circuit.substitute(gr,tr)
    return {'status':'EXACT_QUASI_TRANSLATION_INVERSE_DAG','dag':circuit,'roots':gr,
            'normalized_chart':F,'inverse_reachable_nodes':len(circuit.reachable(gr)),
            'inverse_total_allocated_nodes':len(circuit.nodes),
            'certificate':'Every component of (JN)N is the exact zero polynomial'}


def hidden_family(n):
    """Test constructor. Its hidden data is NOT an acquisition argument."""
    x = s.symbols('x0:'+str(n)); L = s.eye(n)
    for j in range(0,n-1,2): L[j,j+1]=1; L[j+1,j]=1; L[j+1,j+1]=2
    u = L*s.Matrix(x)
    H = s.Matrix([u[i] + (u[i+1]**2 if i<n-1 else 0) for i in range(n)])
    F = (L.inv()*H).applyfunc(s.expand)
    JN = (F-s.Matrix(x)).jacobian(x)
    g = s.Matrix([(i+1)*F[i]-F[i]*sum(F) for i in range(n)])
    # Polynomial Neumann solve, no supplied inverse map.
    term = g; raw = g
    for _ in range(1,n): term = (-JN*term).applyfunc(s.expand); raw += term
    return x, F, raw.applyfunc(s.expand)


def summary(dec):
    return {k:v for k,v in dec.items() if k in ['status','flag_dimensions','nilpotence_length',
          'stage_reachable_nodes','inverse_reachable_nodes','inverse_total_allocated_nodes','source_normalized_chart_nodes']}


def main():
    out = {'raw_pipeline':[], 'decoder_scaling':[], 'controls':{},
           'identity_admission':'Exact complete Jacobian coefficient-space flag; implies BOTH compositions globally.',
           'pit':'No randomized identity admission used in this run.',
           'timing_scope':'All stages measured separately; no matched dynamical-speed claim.'}
    for n in [2,3,4,5]:
        t = time.perf_counter(); x, hidden, raw = hidden_family(n); build = time.perf_counter()-t
        t = time.perf_counter(); module = raw_chart(raw,x); acquisition = time.perf_counter()-t
        assert module['status']=='EXACT_CHART_MODULE', module
        t = time.perf_counter(); dec = strong_decoder(module['chart'],x); invtime=time.perf_counter()-t
        assert dec['status']=='EXACT_FLAG_CERTIFIED_INVERSE_DAG', dec
        assert all(s.expand(v)==0 for v in dec['normalized_chart']-hidden)
        rec = {'n':n, 'raw_degree':max(s.Poly(v,*x).total_degree() for v in raw),
               'raw_terms':sum(len(s.Poly(v,*x).terms()) for v in raw),
               'chart_dimension':n+1, 'inverse_degree_test_family':2**(n-1),
               'constructor_seconds_excluded':build, 'raw_acquisition_seconds':acquisition,
               'certificate_and_decoder_seconds':invtime, **summary(dec),
               'raw_vector_field':[str(v) for v in raw], 'chart':[str(v) for v in module['chart']],
               'matrix':[[str(v) for v in row] for row in module['matrix'].tolist()]}
        if n <= 3:
            t=time.perf_counter(); inv=dec['dag'].expand(dec['roots'],x)
            left=module['chart'].subs(dict(zip(x,inv)),simultaneous=True)-s.Matrix(x)
            right=inv.subs(dict(zip(x,module['chart'])),simultaneous=True)-s.Matrix(x)
            assert all(s.expand(v)==0 for v in list(left)+list(right))
            rec['expanded_global_compositions']='BOTH_PASS';rec['supplemental_expansion_seconds']=time.perf_counter()-t
        else: rec['expanded_global_compositions']='NOT_RUN; exact flag theorem is admission'
        out['raw_pipeline'].append(rec); print('RAW',n,{k:v for k,v in rec.items() if k not in ['raw_vector_field','chart','matrix']},flush=True)
    # Exponential inverse degree, no inverse coefficient expansion. Forward chart
    # supplied to this decoder-only scaling test; DO NOT call it raw acquisition.
    for n in [4,8,12,16]:
        x=s.symbols('z0:'+str(n)); chart=s.Matrix([x[i]+(x[i+1]**2 if i<n-1 else 0) for i in range(n)])
        t=time.perf_counter();dec=strong_decoder(chart,x);seconds=time.perf_counter()-t
        vals,bits=dec['dag'].evaluate(dec['roots'],[3]*n)
        forward,_=DAG_from(chart,x);fr=[forward.compile(v,x) for v in chart]
        back,_=forward.evaluate(fr,vals);assert back==[3]*n
        # Reverse test on noninteger input, exercises rational arithmetic.
        point=[Fraction(i+1,3) for i in range(n)]
        y,_=forward.evaluate(fr,point);back,bits2=dec['dag'].evaluate(dec['roots'],y);assert back==point
        out['decoder_scaling'].append({'n':n, 'inverse_degree':2**(n-1),**summary(dec),
              'certificate_and_build_seconds':seconds,'integer_evaluation_peak_bits':bits,
              'rational_roundtrip_peak_bits':bits2,'roundtrip_checks':'BOTH_DIRECTIONS_EXACT_POINTS_NOT_IDENTITY_PROOF'})
        print('SCALE',out['decoder_scaling'][-1],flush=True)
    x,y=s.symbols('x y')
    controls={'noninvertible_local':[x+x*x,y], 'invertible_notstrong':[x+y*y,y+(x+y*y)**2],
              'singular':[x*x,y], 'identity':[x,y]}
    for name,chart in controls.items():out['controls'][name]=summary(strong_decoder(chart,(x,y)))
    assert out['controls']['noninvertible_local']['status']=='NOT_STRONGLY_NILPOTENT'
    assert out['controls']['invertible_notstrong']['status']=='NOT_STRONGLY_NILPOTENT'
    assert out['controls']['singular']['status']=='SINGULAR_BASEPOINT'
    assert out['controls']['identity']['status']=='EXACT_FLAG_CERTIFIED_INVERSE_DAG'
    # Pointwise nilpotence alone is NOT sufficient for the strong flag. This
    # normalized quasi-translation is globally invertible but not strong.
    x,y,z=s.symbols('x y z');xyz=(x,y,z)
    N=s.Matrix([z*(x+z*y)**2,-(x+z*y)**2,0]);F=s.Matrix(xyz)+N;JN=N.jacobian(xyz)
    assert all(s.expand(v)==0 for v in JN**3)
    a={x:1,y:0,z:0};b={x:1,y:0,z:1}
    witness=JN.subs(a)*JN.subs(b)*JN.subs(a);assert witness!=s.zeros(3)
    strong=strong_decoder(F,xyz);quasi=quasi_decoder(F,xyz)
    assert strong['status']=='NOT_STRONGLY_NILPOTENT'
    assert quasi['status']=='EXACT_QUASI_TRANSLATION_INVERSE_DAG'
    inv=quasi['dag'].expand(quasi['roots'],xyz)
    assert all(s.expand(v)==0 for v in F.subs(dict(zip(xyz,inv)),simultaneous=True)-s.Matrix(xyz))
    assert all(s.expand(v)==0 for v in inv.subs(dict(zip(xyz,F)),simultaneous=True)-s.Matrix(xyz))
    out['controls']['pointwise_nilpotent_notstrong']={**summary(strong),
         'JN_cubed_identically_zero':True,'mixed_product_nonzero':[list(map(str,row)) for row in witness.tolist()],
         'quasi_fallback':summary(quasi),'expanded_global_compositions':'BOTH_PASS'}
    # Raw acquisition of this nonstrong chart; hidden chart excluded at call.
    g=s.Matrix([(i+1)*F[i]-F[i]*sum(F) for i in range(3)])
    raw=((s.eye(3)-JN+JN**2)*g).applyfunc(s.expand)
    t=time.perf_counter();module=raw_chart(raw,xyz);acqtime=time.perf_counter()-t
    assert module['status']=='EXACT_CHART_MODULE'
    acquired=quasi_decoder(module['chart'],xyz)
    assert acquired['status']=='EXACT_QUASI_TRANSLATION_INVERSE_DAG'
    assert all(s.expand(v)==0 for v in acquired['normalized_chart']-F)
    out['nonstrong_raw_pipeline']={'n':3,'raw_degree':max(s.Poly(v,*xyz).total_degree() for v in raw),
         'raw_acquisition_seconds':acqtime,'chart_dimension':4,**summary(acquired),
         'raw_vector_field':[str(v) for v in raw],'chart':[str(v) for v in module['chart']],
         'matrix':[[str(v) for v in row] for row in module['matrix'].tolist()]}
    root=Path(__file__).parent
    out['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (root/'strong_decoder_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out['controls'],indent=2))


if __name__=='__main__':main()
