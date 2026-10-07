"""Exact scoped checks, not an implementation of the imported FPRAS."""
import itertools, json
from pathlib import Path
import sympy as s

base=Path(__file__).resolve().parent
triples=list(itertools.combinations(range(6),3))
coefficients=[1,2,1,3,3,4,4,2,2,3,2,1,2,2,3,3,3,4,4,3]
p=dict(zip(triples,coefficients))
full=set(range(6))
dual={t:p[tuple(sorted(full-set(t)))] for t in triples}
cert={}
for label,table in [('p',p),('dual',dual)]:
    cert[label]=[]
    for i in range(6):
        others=[j for j in range(6) if j!=i]
        matrix=s.Matrix(5,5,lambda a,b:0 if a==b else table[tuple(sorted((i,others[a],others[b])))])
        minors=[int(matrix[:k,:k].det()) for k in range(2,6)]
        cert[label].append(minors)
        if label=='p':
            assert all(((-1)**(k+1))*d>0 for k,d in enumerate(minors,start=2))
        if label=='dual' and i in (3,5):
            assert minors[0]<0<minors[1] and minors[2]<0 and minors[3]<0

x,y=s.symbols('x y',positive=True)
partial_flip=1+x*y
hessian=s.hessian(s.log(partial_flip),(x,y)).subs({x:s.Rational(1,2),y:s.Rational(1,2)})
curvature=(s.Matrix([[1,1]])*hessian*s.Matrix([1,1]))[0]
assert curvature==s.Rational(24,25)

xs=s.symbols('x1:7')
pstar=sum(c*s.prod(xs[i] for i in full-set(t)) for t,c in p.items())
point={u:(1000 if i==3 else 1) for i,u in enumerate(xs)}
direction=s.Matrix([25,-23,41,0,25,-81])
full_curvature=(direction.T*s.hessian(s.log(pstar),xs).subs(point)*direction)[0]
assert full_curvature==s.Rational(286483357,169338169)

# Trace of a two-qubit circuit: pair gate, general X/Z field on qubit 0,
# and Z field on qubit 1. A wire joins each column to the next row.
pair=s.Matrix([[s.Rational(12,7),0,0,0],
               [0,2,s.Rational(4,7),0],
               [0,s.Rational(4,7),2,0],
               [0,0,0,s.Rational(12,7)]])
field=s.Matrix([[2,s.Rational(3,7)],[s.Rational(3,7),s.Rational(10,7)]])
zfield=s.diag(1,s.Rational(15,7))
tables=[pair,field,zfield]
qubits=[(0,1),(0,),(1,)]
halfedges=[]
for i,qs in enumerate(qubits):
    for kind in ('row','col'):
        for q in qs:halfedges.append((i,kind,q))
wires=[]
for q in range(2):
    nodes=[i for i,qs in enumerate(qubits) if q in qs]
    for k,i in enumerate(nodes):wires.append(((i,'col',q),(nodes[(k+1)%len(nodes)],'row',q)))
def value(bits):
    weight=s.Integer(1)
    for i,qs in enumerate(qubits):
        row=0; col=0
        for q in qs:
            row=2*row+bits[(i,'row',q)]
            col=2*col+(1-bits[(i,'col',q)])
        weight*=tables[i][row,col]
    return weight
z_exact_once=s.Integer(0)
for assignment in itertools.product((0,1),repeat=len(wires)):
    bits={}
    for (a,b),t in zip(wires,assignment):bits[a]=t; bits[b]=1-t
    z_exact_once+=value(bits)
trace=(pair*s.kronecker_product(field,s.eye(2))*s.kronecker_product(s.eye(2),zfield)).trace()
assert z_exact_once==trace

# Four-gate fixture with two X-field occurrences exercises the nonhomogeneous
# local 0- and 2-selected terms, then checks the two-dummy homogeneous lift.
tables4=[pair,field,zfield,field]
qubits4=[(0,1),(0,),(1,),(0,)]
wires4=[]
for q in range(2):
    nodes=[i for i,qs in enumerate(qubits4) if q in qs]
    for k,i in enumerate(nodes):wires4.append(((i,'col',q),(nodes[(k+1)%len(nodes)],'row',q)))
exact4=s.Integer(0); lifted4=s.Integer(0); positive_nonhomogeneous=0
fields4=[1,2,3]
for assignment in itertools.product((0,1),repeat=len(wires4)):
    bits={}
    for (a,b),t in zip(wires4,assignment):bits[a]=t; bits[b]=1-t
    w=s.Integer(1)
    for i,qs in enumerate(qubits4):
        row=0;col=0
        for q in qs:
            row=2*row+bits[(i,'row',q)]
            col=2*col+(1-bits[(i,'col',q)])
        w*=tables4[i][row,col]
    exact4+=w
    if w>0 and any(sum(bits[(i,kind,0)] for kind in ('row','col'))!=1 for i in (1,3)):
        positive_nonhomogeneous+=1
    # The pair gate has exactly degree two; its transformed coefficient.
    row=2*bits[(0,'row',0)]+bits[(0,'row',1)]
    col=2*(1-bits[(0,'col',0)])+1-bits[(0,'col',1)]
    pairweight=pair[row,col]
    for aux in itertools.combinations(range(6),3):
        aux=set(aux); lw=pairweight
        for k,i in enumerate(fields4):
            q=qubits4[i][0]
            xbit=bits[(i,'col',q)]; ybit=bits[(i,'row',q)]
            count=(2*k in aux)+(2*k+1 in aux)
            if xbit+ybit==0 and count==2:
                lw*=tables4[i][0,1]
            elif xbit+ybit==2 and count==0:
                lw*=tables4[i][1,0]
            elif xbit+ybit==1 and count==1:
                lw*=tables4[i][0,0]/2 if xbit else tables4[i][1,1]/2
            else:
                lw=0; break
        lifted4+=lw
trace4=(pair*s.kronecker_product(field,s.eye(2))*s.kronecker_product(s.eye(2),zfield)*s.kronecker_product(field,s.eye(2))).trace()
assert exact4==lifted4==trace4
assert positive_nonhomogeneous>0

# The pair-polynomial Hessian has explicit integer/rational eigenvalues.
a=s.Rational(12,7); b=s.Integer(2); c=s.Rational(4,7)
pair_eigenvalues=[a+b+c,a-b-c,-a+b-c,-a-b+c]
assert sum(int(bool(v>0)) for v in pair_eigenvalues)==1
field_lc_margin=2*2*s.Rational(10,7)-s.Rational(3,7)**2
assert field_lc_margin>0

# Ordinary equality and exact-once cannot be identified even on one edge.
one_edge_equality=1*3+2*5
one_edge_exact_once=2*3+1*5
assert one_edge_equality==13 and one_edge_exact_once==11

result={
    'status':'ALL_EXACT_ASSERTIONS_PASSED',
    'cubic_coefficients':coefficients,
    'derivative_leading_principal_determinants':cert,
    'partial_flip_curvature_at_half':str(curvature),
    'full_reciprocal_curvature_at_positive_point':str(full_curvature),
    'two_qubit_circuit_trace':str(trace),
    'same_exact_once_contraction':str(z_exact_once),
    'four_gate_trace':str(trace4),
    'four_gate_exact_once_contraction':str(exact4),
    'four_gate_homogeneous_lift_contraction':str(lifted4),
    'positive_configs_using_nonhomogeneous_field_terms':positive_nonhomogeneous,
    'pair_gate_hessian_eigenvalues':[str(v) for v in pair_eigenvalues],
    'single_field_logconcavity_margin':str(field_lc_margin),
    'one_edge_equality':one_edge_equality,
    'one_edge_exact_once':one_edge_exact_once,
    'not_executed':'Chen-Liu FPRAS or physical thermal sampling',
}
(base/'tensor_contraction_exact_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
