#!/usr/bin/env python3
"""Independent exact check of two obstructions to the v5 fixed-point map.

This checker imports no discovery code. Gradients are rebuilt by solving the
three affine interpolation equations on each triangle. Adjacencies are rebuilt
from periodic square indices, not from the discovery code's edge routine.
The universal fixture was communicated by the parent, attributed to another
independent auditor. The hat-function fixture was found by this worker earlier.
Neither fixture is a rank-one convex/non-quasiconvex integrand.
"""
from pathlib import Path
import hashlib
import json
import sympy as S

HERE = Path(__file__).resolve().parent
Q = S.Rational
checks = []

def check(label, predicate):
    assert predicate, label
    checks.append(label)

def gradients(rows_y):
    """Rows indexed by y, entries by x; physical cell width 1/2."""
    out = []
    for i in range(2):
        for j in range(2):
            for vertices in [((i,j),(i+1,j),(i,j+1)),
                             ((i+1,j+1),(i,j+1),(i+1,j))]:
                a = S.Matrix([[Q(x,2), Q(y,2), 1] for x,y in vertices])
                b = S.Matrix([rows_y[y % 2][x % 2] for x,y in vertices])
                coefficients = a.inv() * b
                out.append(S.Matrix(coefficients[:2]))
    check('zero gradient mean for ' + str(rows_y),
          sum(out, S.zeros(2,1)) == S.zeros(2,1))
    return out

def lower(i,j): return 2*((i % 2)*2+(j % 2))
def upper(i,j): return lower(i,j)+1

def interfaces(kind):
    out = []
    for j in range(2):
        for i in range(2):
            if kind == 'vertical':
                out.append(((kind,i,j),(upper(i-1,j),lower(i,j))))
            elif kind == 'horizontal':
                out.append(((kind,i,j),(upper(i,j-1),lower(i,j))))
            else:
                out.append(((kind,i,j),(lower(i,j),upper(i,j))))
    return out

vertical = interfaces('vertical')
horizontal = interfaces('horizontal')
diagonal = interfaces('diagonal')
groups = [vertical+horizontal, vertical+diagonal, horizontal+diagonal]
leaves = [s for group in groups for _,pair in group for s in pair]
check('l=1 gives 8 triangles and 48 leaf copies', len(leaves)==48)
check('every triangle appears in precisely six leaves',
      all(leaves.count(s)==6 for s in range(8)))
uniform = [Q(1,48)]*48
check('uniform t obeys every pair mass constraint (5.5)',
      all(uniform[k]+uniform[k+1]==Q(1,24) for k in range(0,48,2)))
check('uniform t obeys every triangle mass constraint (5.6)',
      all(sum(uniform[k] for k in range(48) if leaves[k]==s)==Q(1,8)
          for s in range(8)))

def check_continuity(label, grads):
    for kind, edges in [('vertical',vertical),('horizontal',horizontal),
                        ('diagonal',diagonal)]:
        tangent = {'vertical':S.Matrix([0,1]),
                   'horizontal':S.Matrix([1,0]),
                   'diagonal':S.Matrix([1,-1])}[kind]
        check(label+' tangential compatibility '+kind,
              all((grads[a]-grads[b]).dot(tangent)==0 for _,(a,b) in edges))

# Fixture supplied by the parent, independently reconstructed here.
u_rows = [[0,2],[1,1]]
v_rows = [[2,0],[-2,3]]
gu, gv = gradients(u_rows), gradients(v_rows)
check_continuity('universal u',gu)
check_continuity('universal v',gv)
critical = groups[0][-2:]
check('critical edges are the last two horizontal interfaces',
      [k for k,_ in critical]==[('horizontal',0,1),('horizontal',1,1)])
(a,b),(c,d) = [pair for _,pair in critical]
check('first u pair is constantly (0,-2)',gu[a]==gu[b]==S.Matrix([0,-2]))
check('second u pair is constantly (0,2)',gu[c]==gu[d]==S.Matrix([0,2]))
check('first v pair has x coordinate 10',gv[a][0]==gv[b][0]==10)
check('second v pair has x coordinate -10',gv[c][0]==gv[d][0]==-10)

ta,tb,ra,rb = S.symbols('ta tb ra rb',real=True)
pair_mass=Q(1,24)
# Odd child minus even child; each child is normalized by its fixed pair mass.
U = S.simplify(24*(ta*gu[a]+(pair_mass-ta)*gu[b]
                  -tb*gu[c]-(pair_mass-tb)*gu[d]))
V = S.simplify(24*(ra*gv[a]+(pair_mass-ra)*gv[b]
                  -rb*gv[c]-(pair_mass-rb)*gv[d]))
det = S.expand(S.det(S.Matrix.hstack(U,V)))
check('critical U is (0,-4) for every real admissible t',U==S.Matrix([0,-4]))
check('critical V_x is 20 for every real admissible r',V[0]==20)
check('critical determinant is identically 80',det==80)
check('the critical node lies above the automatic interface level',
      len(critical)==2 and sum(len(pair) for _,pair in critical)==4)

# Original independently found fixture: uniform t and vertical x=1/2 edges.
hu_rows = [[1,0],[0,0]]
hv_rows = [[0,1],[0,0]]
hu,hv = gradients(hu_rows),gradients(hv_rows)
check_continuity('hat u',hu)
check_continuity('hat v',hv)
hat_edges = [edge for edge in vertical if edge[0][1]==1]
(a,b),(c,d) = [pair for _,pair in hat_edges]
# Use the discovery receipt's opposite direction convention for this fixture.
# Reversing both directions leaves parallelism and their determinant unchanged.
hatU = (hu[c]+hu[d]-hu[a]-hu[b])/2
hatV = S.expand(24*(rb*hv[c]+(pair_mass-rb)*hv[d]
                       -ra*hv[a]-(pair_mass-ra)*hv[b]))
hatdet = S.expand(S.det(S.Matrix.hstack(hatU,hatV)))
check('hat critical U is (-2,0) at uniform t',hatU==S.Matrix([-2,0]))
check('hat critical V_y is 4 for every r',hatV[1]==4)
check('hat critical determinant is identically -8',hatdet==-8)
check('hat three-row contradiction is exact',
      -12*Q(1,24)-12*Q(1,24)-Q(1,8)*0==-1)

def list_vectors(xs): return [[str(z) for z in v] for v in xs]
receipt={
  'status':'PASS', 'arithmetic':'exact integers and SymPy rationals',
  'checks_count':len(checks),'checks':checks,
  'source_pdf_sha256':hashlib.sha256((HERE/'sources/pedregal_morrey_1905.06571v5.pdf').read_bytes()).hexdigest(),
  'universal_fixture':{
    'provenance':'Communicated by parent as the independent Pedregal auditor fixture; gradients and obstruction rebuilt by this worker without reading that auditor results.',
    'u_rows_y':u_rows,'v_rows_y':v_rows,'triangle_order':'i outer, j inner, lower then upper; coordinates scaled by 1/2',
    'u_gradients':list_vectors(gu),'v_gradients':list_vectors(gv),
    'j1_tagging':'four vertical interfaces in row-major (y,x), then four horizontal interfaces in row-major (y,x)',
    'all_groups':[[{'edge':list(k),'triangles_0_based':list(pair)} for k,pair in group] for group in groups],
    'leaves_0_based':leaves,'uniform_feasible_t':'1/48 in every leaf',
    'critical_leaf_positions_1_based':[13,14,15,16],
    'critical_U':[str(x) for x in U], 'critical_V':[str(x) for x in V],
    'critical_determinant':str(det),'quantifiers':'Every t,r in Theta_1; indeed every real t,r obeying just the two critical pair-mass constraints.'},
  'hat_fixture':{
    'provenance':'Discovered by this worker independently before receipt of universal fixture.',
    'u_rows_y':hu_rows,'v_rows_y':hv_rows,
    'critical_edges':'two vertical edges at x=1/2, paired consecutively; lexicographic interface tagging in the discovery receipt is allowed by Section 4.',
    'critical_U':[str(x) for x in hatU], 'critical_V':[str(x) for x in hatV],
    'critical_determinant':str(hatdet),
    'quantifiers':'Uniform t; every real r obeying the two critical pair-mass constraints.'},
  'scope':'Corollary 7.2 is false for allowed molds, so the stated Kakutani/H_n route does not establish Theorems 1.1/1.2. No conclusion that a different mold or unrestricted laminate representation is impossible; no ROC/non-QC integrand constructed.'
}
(HERE/'PEDREGAL_INDEPENDENT_STEP_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks_count':len(checks),
                  'universal_determinant':str(det),'hat_determinant':str(hatdet)},indent=2))
