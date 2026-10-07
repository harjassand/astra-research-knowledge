"""Exact rational spin-projector tensor compiler and bounded diagnostics.

This is NOT a Chen--Liu FPRAS. The coefficient-oracle compiler is acquired;
the optional enumerator is exponential and is used only on tiny fixtures.
All arrays in the diagnostics have at most eight rows.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import json
from pathlib import Path


def ceil_log2(q):
    q = F(q)
    k = 0
    while q > 1:
        q /= 2
        k += 1
    return k


@dataclass(frozen=True)
class Gate:
    qubits: tuple
    kind: str
    table: tuple = ()

    def entry(self, row, col):
        if self.kind == "projector":
            if row.bit_count() != col.bit_count():
                return F(0)
            return F(1, comb(len(self.qubits), row.bit_count()))
        return self.table[row][col]


def edge_gate(qubits, alpha, gamma, s):
    alpha, gamma, s = map(F, (alpha, gamma, s))
    assert alpha >= abs(gamma)
    a, b, c = 1+s*(3*alpha+gamma), 1+s*(3*alpha-gamma), 2*s*alpha
    return Gate(tuple(qubits), "edge", ((a,0,0,0),(0,b,c,0),(0,c,b,0),(0,0,0,a)))


def field_gate(qubit, b, c, s):
    b, c, s = map(F, (b,c,s))
    assert b >= 0
    r = b + abs(c)
    return Gate((qubit,), "field", ((1+s*(r+c),s*b),(s*b,1+s*(r-c))))


@dataclass
class Factor:
    gate: Gate
    rows: tuple
    cols: tuple
    dummies: tuple

    @property
    def variables(self):
        return self.rows+self.cols+self.dummies

    @property
    def degree(self):
        return 2 if self.gate.kind == "field" else len(self.rows)

    def coefficient(self, mask):
        selected = lambda v: (mask >> v) & 1
        if sum(selected(v) for v in self.variables) != self.degree:
            return F(0)
        row = sum(selected(v) << i for i,v in enumerate(self.rows))
        col = sum((1-selected(v)) << i for i,v in enumerate(self.cols))
        value = F(self.gate.entry(row,col))
        if self.gate.kind == "field" and row == col:
            value /= 2
        return value

    def options(self):
        for selected in combinations(self.variables,self.degree):
            mask = sum(1 << v for v in selected)
            value = self.coefficient(mask)
            if value:
                yield mask,value

    def range_bit_bound(self):
        if self.gate.kind == "projector":
            return len(self.rows)  # binomial(q,r) <= 2**q
        vals = [v for _,v in self.options()]
        return ceil_log2(max(vals)/min(vals))


class CompiledCircuit:
    def __init__(self,nqubits,gates):
        self.factors=[]
        self.wires=[]
        self.dummies=[]
        incidences=[[] for _ in range(nqubits)]
        cursor=0
        for gate in gates:
            k=len(gate.qubits)
            rows=tuple(range(cursor,cursor+k)); cursor+=k
            cols=tuple(range(cursor,cursor+k)); cursor+=k
            dummy=tuple(range(cursor,cursor+2)) if gate.kind == "field" else ()
            cursor+=len(dummy)
            self.dummies.extend(dummy)
            self.factors.append(Factor(gate,rows,cols,dummy))
            for i,q in enumerate(gate.qubits):
                incidences[q].append((rows[i],cols[i]))
        self.isolated=sum(not h for h in incidences)
        for h in incidences:
            if h:
                self.wires.extend((h[i][1],h[(i+1)%len(h)][0]) for i in range(len(h)))
        self.n=cursor
        self.f=len(self.dummies)//2
        self.degree=sum(f.degree for f in self.factors)
        assert 2*self.degree == self.n
        assert len(self.wires)+self.f == self.degree
        self.range_bits=sum(f.range_bit_bound() for f in self.factors)
        self.p_seed=0
        for factor in self.factors:
            # Positive zero-to-zero diagonal. Fields use one of their dummies.
            selected=factor.cols+(factor.dummies[:1] if factor.dummies else ())
            self.p_seed |= sum(1 << v for v in selected)
        self.q_seed=sum(1 << a for a,b in self.wires)
        self.q_seed |= sum(1 << v for v in self.dummies[:self.f])
        assert self.p_coefficient(self.p_seed)>0
        assert self.q_coefficient(self.q_seed)>0

    def p_coefficient(self,mask):
        if mask.bit_count()!=self.degree:
            return F(0)
        value=F(1)
        for factor in self.factors:
            value*=factor.coefficient(mask)
            if not value:
                break
        return value

    def q_coefficient(self,mask):
        if mask.bit_count()!=self.degree:
            return F(0)
        if any(((mask>>a)&1)+((mask>>b)&1)!=1 for a,b in self.wires):
            return F(0)
        if sum((mask>>v)&1 for v in self.dummies)!=self.f:
            return F(0)
        return F(1)

    def exact_diagnostic_count(self,cap=20000):
        choices=[list(f.options()) for f in self.factors]
        work=1
        for choices_i in choices: work*=len(choices_i)
        if work>cap:
            raise ValueError("Fixture exceeds the explicit enumeration cap")
        value=F(0); accepted=0
        for local in product(*choices):
            mask=0; weight=F(1)
            for m,w in local: mask|=m; weight*=w
            if self.q_coefficient(((1<<self.n)-1)^mask):
                value+=weight; accepted+=1
        return (2**self.isolated)*value,work,accepted


def identity(n):
    return [[F(int(i==j)) for j in range(n)] for i in range(n)]


def matmul(a,b):
    n=len(a)
    return [[sum((a[i][k]*b[k][j] for k in range(n)),F(0)) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def embed(gate,nqubits):
    n=1<<nqubits
    qset=set(gate.qubits)
    result=[[F(0) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if any(((i>>q)&1)!=((j>>q)&1) for q in range(nqubits) if q not in qset):
                continue
            r=sum(((i>>q)&1)<<k for k,q in enumerate(gate.qubits))
            c=sum(((j>>q)&1)<<k for k,q in enumerate(gate.qubits))
            result[i][j]=F(gate.entry(r,c))
    return result


def trace(a):
    return sum((a[i][i] for i in range(len(a))),F(0))


def circuit_trace(gates,nqubits):
    a=identity(1<<nqubits)
    for gate in gates: a=matmul(a,embed(gate,nqubits))
    return trace(a)


def verify_projector_derivatives(qmax=12):
    checks=0
    for q in range(2,qmax+1):
        for a in range(q-1):
            b=q-2-a; m=q-a; ell=q-b
            aa=F(1,comb(q,a+2)); bb=F(1,comb(q,a+1)); cc=F(1,comb(q,a))
            determinant=aa*cc*(m-1)*(ell-1)-bb*bb*m*ell
            assert determinant==0
            assert aa>0 and cc>0
            checks+=1
    return checks


def diagnostics():
    checks=verify_projector_derivatives()
    fixtures=[]
    for s in (F(1,7),F(2,11),F(1,100)):
        e=edge_gate((0,2),F(1,4),F(-1,8),s)
        f=field_gate(2,F(1,3),F(-1,5),s)
        projector=Gate((0,1),"projector")
        gates=[projector,e,f,f,e]
        c=CompiledCircuit(3,gates)
        tensor,work,accepted=c.exact_diagnostic_count()
        matrix=circuit_trace(gates,3)
        assert tensor==matrix
        fixtures.append({"s":str(s),"N":c.n,"degree":c.degree,"trace":str(matrix),
                         "enumerated_P_monomials":work,"accepted":accepted,
                         "range_bits":c.range_bits})
    projector=embed(Gate((0,1),"projector"),3)
    assert matmul(projector,projector)==projector
    assert trace(projector)==6
    # H embedded symmetrically across both constituents of the spin-1 site.
    edges=[edge_gate((i,2),F(1,4),F(-1,8),F(1)) for i in (0,1)]
    field=field_gate(2,F(1,3),F(-1,5),F(1))
    eye=identity(8)
    shifted=[[F(0) for j in range(8)] for i in range(8)]
    for g in edges+[field]:
        table=embed(g,3)
        for i in range(8):
            for j in range(8): shifted[i][j]+=table[i][j]-eye[i][j]
    assert matmul(projector,shifted)==matmul(shifted,projector)
    # Exact two-positive-direction certificate for I+s*Pi_4 at 0<s<2.
    s=F(1,10)
    restriction=((8+13*s/3,5*s/3),(5*s/3,s/3))
    det=restriction[0][0]*restriction[1][1]-restriction[0][1]**2
    assert det==4*s*(2-s)/3>0
    return {"status":"PASS","scope":"exact finite identities; no FPRAS executed",
            "projector_derivative_types":checks,"projector_max_q":12,
            "compiled_lift_fixtures":fixtures,"symmetric_embedding_commutes":True,
            "projector_trace":str(trace(projector)),
            "failed_I_plus_s_projector_q4":{"s":str(s),"positive_restriction":[[str(x) for x in r] for r in restriction],"determinant":str(det)}}


if __name__=="__main__":
    output=diagnostics()
    destination=Path(__file__).with_name("spin_projection_checks.json")
    destination.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps(output,indent=2))
