"""Exact local response-control calculation in ROOT's introduced hidden graph.

No material, global controller or novelty is claimed. All algebra is rebuilt
from Kirchhoff equations with Fractions; no producer code/data are used.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json

EDGES=[(0,2),(1,3),(0,5),(1,5),(2,5),(3,5),(5,4)]
PATTERNS=[(-1,-1,-1,-1),(-1,-1,-1,0),(-1,-1,-1,1),
          (-1,-1,0,-1),(-1,-1,0,0),(-1,-1,0,1),(-1,0,-1,-1)]


def solve(a,b):
    a=[list(row)+[v] for row,v in zip(a,b)]
    for j in range(len(a)):
        k=next(k for k in range(j,len(a)) if a[k][j])
        a[j],a[k]=a[k],a[j];q=a[j][j];a[j]=[x/q for x in a[j]]
        for k in range(len(a)):
            if k!=j:
                q=a[k][j];a[k]=[x-q*y for x,y in zip(a[k],a[j])]
    return [row[-1] for row in a]


def determinant(a):
    a=[list(row) for row in a];out=F(1)
    for j in range(len(a)):
        k=next((k for k in range(j,len(a)) if a[k][j]),None)
        if k is None:return F(0)
        if k!=j:a[j],a[k]=a[k],a[j];out=-out
        q=a[j][j];out*=q
        for k in range(j+1,len(a)):
            q=a[k][j]/a[j][j]
            for l in range(j,len(a)):a[k][l]-=q*a[j][l]
    return out


def matrix_data(resistances):
    free=[2,3,5];A=[[F(0)]*3 for _ in free]
    for (a,b),r in zip(EDGES,resistances):
        for x,y in ((a,b),(b,a)):
            if x in free:
                i=free.index(x);A[i][i]+=1/r
                if y in free:A[i][free.index(y)]-=1/r
    columns=[];J=[[] for _ in range(4)]
    for driven in (0,1):
        rhs=[F(0)]*3
        for (a,b),r in zip(EDGES,resistances):
            for x,y in ((a,b),(b,a)):
                if x in free and y==driven:rhs[free.index(x)]+=1/r
        sol=solve(A,rhs)
        p=[F(int(i==driven)) for i in range(6)]
        for node,value in zip(free,sol):p[node]=value
        columns.append(sol[:2])
        for (a,b),r in zip(EDGES,resistances):
            q=[F(int(x==a)-int(x==b))*(p[a]-p[b])/r**2 for x in free]
            derivative=solve(A,q)
            J[2*driven].append(derivative[0])
            J[2*driven+1].append(derivative[1])
    W=[list(row) for row in zip(*columns)]
    fields={}
    for power in (1,3):
        vectors=[]
        for pattern in PATTERNS:
            p=list(map(F,pattern))+[F(0)]
            g=[1/r for r in resistances[2:]]
            p.append(sum(g[i]*p[i] for i in range(5))/sum(g))
            vectors.append([(p[a]-p[b])**power for a,b in EDGES])
        C=[[sum(J[i][e]*v[e] for e in range(7)) for v in vectors] for i in range(4)]
        minor=next((ids for ids in combinations(range(7),4)
                    if determinant([[C[i][j] for j in ids] for i in range(4)])),None)
        fields[str(power)]={"selected_indices":minor,
                            "observable_minor_determinant":str(determinant([[C[i][j] for j in minor] for i in range(4)])) if minor else "0",
                            "response_write_jacobian":C}
    return W,J,fields


def rational_strings(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,list):return [rational_strings(v) for v in x]
    if isinstance(x,dict):return {k:rational_strings(v) for k,v in x.items()}
    return x


def main():
    r=[F(1)]*7;W,J,fields=matrix_data(r)
    assert W==[[F(11,16),F(3,16)],[F(3,16),F(11,16)]]
    assert fields['1']['selected_indices'] is not None
    assert fields['3']['observable_minor_determinant']=='49257/2560000000'
    # Independent central differences of the passive read map check the exact
    # analytical parameter derivative; the exact rational result governs.
    h=F(1,10**5);max_error=F(0)
    for e in range(7):
        rp=list(r);rm=list(r);rp[e]+=h;rm[e]-=h
        wp=matrix_data(rp)[0];wm=matrix_data(rm)[0]
        for driven in range(2):
            for output in range(2):
                finite=(wp[output][driven]-wm[output][driven])/(2*h)
                max_error=max(max_error,abs(finite-J[2*driven+output][e]))
    assert max_error<F(1,10**9)
    result={
        "status":"EXACT_CONDITIONAL_LOCAL_RESPONSE_RESULT_NOT_MATERIAL_OR_GLOBAL_LEARNING",
        "edges":EDGES,"hidden_vertex":5,"exposed_ports":[0,1,2,3,4],
        "initial_read_map":W,"read_map_derivative_order":"W00,W10,W01,W11",
        "read_map_parameter_jacobian":J,
        "boundary_patterns":PATTERNS,"linear_and_cubic_observable_write_fields":fields,
        "derivation":"For read-state Kirchhoff L_ff u=b, du/dr_e=L_ff^-1 q_e,free*(p_a-p_b)/r_e^2. Compose this exact observable derivative with each actual boundary write field, whose hidden pressure follows conductance-weighted equilibrium.",
        "consequence":"Both linear and cubic local adaptation have four independent boundary-accessible RESPONSE directions at this hidden-graph state. The linear law need not control all seven internal resistances to reach a local open family of useful four-coefficient maps.",
        "local_theorem":"Fix four patterns with nonzero observable minor. Compose their smooth signed-time write flows and read the four transfer coefficients. Its derivative at zero is invertible, so the inverse-function theorem gives local target-response reachability near the specified initial state. Negative times are implemented by reversing pressures only because the introduced law is odd and reversible.",
        "limits":["This does not construct a boundary-observed noisy teacher or an explicit uniform reachable radius.","Individual state identifiability is unnecessary for this local response theorem; it is not proved unnecessary for global efficient learning.","No global initial-state box, material implementation, gate, pressure bandwidth, useful-life or energy advantage is supplied.","The theorem remains conditional on the introduced positive resistor and local adaptation model. It is not a90-level discovery or a novelty verdict."],
        "central_difference_max_error":float(max_error),
    }
    out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(rational_strings(result),indent=2,sort_keys=True)+'\n')
    print(json.dumps({"output":str(out),"linear_selected":fields['1']['selected_indices'],
                      "linear_determinant":fields['1']['observable_minor_determinant'],
                      "cubic_selected":fields['3']['selected_indices'],
                      "cubic_determinant":fields['3']['observable_minor_determinant'],
                      "derivative_error":float(max_error)},indent=2))


if __name__=='__main__':main()
