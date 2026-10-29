import sympy as s, random, json
from pathlib import Path
R=random.Random(20261028)
def fixture(m):
    cols=[]
    for i in range(m//2):
        v=[s.Rational(R.randint(-3,3),10) for _ in range(3)]
        for sign in [1,-1]: cols.append(s.Matrix([s.Rational(1,m)]+[sign*x/m for x in v]))
    return s.Matrix.hstack(*cols)
def nexts(A,w):
    active=[i for i,x in enumerate(w) if x]
    if len(active)<=4:return None
    vs=A[:,active].nullspace()[0]
    den=s.ilcm(*[x.q for x in vs]); v=[s.Integer(0)]*len(w)
    for i,x in zip(active,vs):v[i]=x*den
    pos=min(w[i]/(-v[i]) for i in active if v[i]<0)
    neg=-min(w[i]/v[i] for i in active if v[i]>0)
    q=-neg/(pos-neg)
    return [(q,[x+pos*y for x,y in zip(w,v)]),(1-q,[x+neg*y for x,y in zip(w,v)])]
checks=0;maxbits=0;maxsupport=0
for k in range(40):
    A=fixture(8); expected=s.zeros(8,1); stack=[(s.Integer(1),[s.Integer(1)]*8)]
    while stack:
        prob,w=stack.pop(); assert A*s.Matrix(w)==s.Matrix([1,0,0,0]);assert min(w)>=0
        z=nexts(A,w)
        if z is None:
            expected+=prob*s.Matrix(w);maxsupport=max(maxsupport,sum(bool(x) for x in w));checks+=1
        else:
            for q,v in z:stack.append((prob*q,v))
    assert expected==s.ones(8,1)
for k in range(50):
    A=fixture(20);w=[s.Integer(1)]*20
    while (z:=nexts(A,w)) is not None:
        # exact rational coin with Python uniform integer, no float rounding
        q=z[0][0]; choice=0 if R.randrange(int(q.q))<q.p else 1
        w=z[choice][1];assert A*s.Matrix(w)==s.Matrix([1,0,0,0]);assert min(w)>=0
        maxbits=max(maxbits,max(max(abs(int(x.p)).bit_length(),int(x.q).bit_length()) for x in w))
    assert sum(bool(x) for x in w)<=4
out={'exact_branching_fixtures':40,'exact_leaf_checks':checks,'random_path_fixtures':50,'max_final_support':maxsupport,'max_weight_integer_bits':maxbits,'all_exact_mean_effects_preserved':True,'scope':'rational noncommuting qubit effects, simulated classical pruning only; not source samples or hardware'}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
