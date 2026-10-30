"""Public exact binary Pauli/symplectic compiler. No unknown-source access.

Paulis are i**p X**x Z**z, with integer bit masks x,z and phase p mod4.
Thus canonical Hermitian Y on one site has x=z=1,p=1.
"""

from __future__ import annotations


def mul(a,b):
    x,z,p=a;u,v,q=b
    return x^u,z^v,(p+q+2*(z&u).bit_count())%4


def canonical(x,z,negative=False):
    return x,z,((x&z).bit_count()+2*bool(negative))%4


def sign(a):
    x,z,p=a
    d=(p-(x&z).bit_count())%4
    if d not in (0,2):raise ValueError('non-Hermitian Pauli')
    return 1 if d==0 else -1


def symp(a,b):
    return ((a[0]&b[1]).bit_count()+(a[1]&b[0]).bit_count())%2


def gate(a,g):
    x,z,p=a;t=g[0]
    if t in ('H','S','SDG','X','Z'):
        j=g[1];m=1<<j;xb=bool(x&m);zb=bool(z&m)
        if t=='H':
            p+=2*xb*zb
            if xb!=zb:x^=m;z^=m
        elif t=='S':p+=xb;z^=m if xb else 0
        elif t=='SDG':p-=xb;z^=m if xb else 0
        elif t=='X':p+=2*zb
        elif t=='Z':p+=2*xb
    elif t=='CX':
        c,j=g[1:]
        if (x>>c)&1:x^=1<<j
        if (z>>j)&1:z^=1<<c
    elif t=='SWAP':
        c,j=g[1:]
        if ((x>>c)^(x>>j))&1:x^=(1<<c)|(1<<j)
        if ((z>>c)^(z>>j))&1:z^=(1<<c)|(1<<j)
    else:raise ValueError(g)
    return x,z,p%4


def inverse(gates):
    return [(('SDG',g[1]) if g[0]=='S' else ('S',g[1]) if g[0]=='SDG' else tuple(g))
            for g in reversed(gates)]


def apply(a,gates):
    for g in gates:a=gate(a,g)
    return a


def make_tableau(n,gates):
    return ([apply((1<<j,0,0),gates) for j in range(n)],
            [apply((0,1<<j,0),gates) for j in range(n)])


def map_tableau(a,tableau):
    x,z,p=a;out=(0,0,p)
    for mask,images in ((x,tableau[0]),(z,tableau[1])):
        while mask:
            bit=mask&-mask;j=bit.bit_length()-1;mask^=bit
            out=mul(out,images[j])
    return out


def compile_pairs(pairs,n,outputs=None):
    """Map each supplied signed (X_j,Z_j) to positive output X/Z.

    Actual emitted gates: O(q*W), W=union of supplied supports+outputs;
    W can be2q*w for per-generator width w, giving O(q^2*w), notO(q*w).
    Classical tableau update cost has an additional O(q) factor.
    """
    q=len(pairs)
    outputs=list(range(q)) if outputs is None else list(outputs)
    if len(outputs)!=q or len(set(outputs))!=q:raise ValueError('distinct outputs required')
    flat=[tuple(a) for pair in pairs for a in pair]
    for a in flat:
        sign(a)
        if (a[0]|a[1])>>n:raise ValueError('out of range')
    for i,a in enumerate(flat):
        for j,b in enumerate(flat):
            if symp(a,b)!=int(i//2==j//2 and i!=j):
                raise ValueError('not canonical symplectic pairs')
    original=list(flat);gates=[]
    def emit(g):
        nonlocal flat
        gates.append(tuple(g));flat=[gate(a,g) for a in flat]
    locked=set()
    for j,dest in enumerate(outputs):
        if not 0<=dest<n:raise ValueError('bad output')
        zz=flat[2*j+1]
        support=[i for i in range(n) if ((zz[0]|zz[1])>>i)&1]
        if any(i in locked for i in support):raise AssertionError('locked support')
        pivot=dest if dest in support else support[0]
        if pivot!=dest:emit(('SWAP',pivot,dest))
        for i in range(n):
            if i in locked:continue
            a=flat[2*j+1];x=(a[0]>>i)&1;z=(a[1]>>i)&1
            if x and z:emit(('SDG',i));emit(('H',i))
            elif x:emit(('H',i))
        for i in range(n):
            if i!=dest and ((flat[2*j+1][1]>>i)&1):emit(('CX',i,dest))
        if sign(flat[2*j+1])<0:emit(('X',dest))
        assert flat[2*j+1]==(0,1<<dest,0)
        if (flat[2*j][1]>>dest)&1:emit(('SDG',dest))
        for i in range(n):
            if i==dest or i in locked:continue
            a=flat[2*j];x=(a[0]>>i)&1;z=(a[1]>>i)&1
            if x and z:emit(('SDG',i))
            elif z:emit(('H',i))
        for i in range(n):
            if i!=dest and ((flat[2*j][0]>>i)&1):emit(('CX',dest,i))
        if sign(flat[2*j])<0:emit(('Z',dest))
        assert flat[2*j]==(1<<dest,0,0)
        assert flat[2*j+1]==(0,1<<dest,0)
        locked.add(dest)
    for j in range(q):
        assert apply(original[2*j],gates)==(1<<outputs[j],0,0)
        assert apply(original[2*j+1],gates)==(0,1<<outputs[j],0)
    return gates


def route_line(gates):
    """Exact all-state nearest-neighbor implementation; arbitrary other data allowed."""
    out=[]
    def adjacent_swap(a,b):
        assert abs(a-b)==1
        out.extend([('CX',a,b),('CX',b,a),('CX',a,b)])
    def cx(a,b):
        step=1 if b>a else -1
        path=[];p=a
        while abs(p-b)>1:
            z=p+step;adjacent_swap(p,z);path.append((p,z));p=z
        out.append(('CX',p,b))
        for p,z in reversed(path):adjacent_swap(p,z)
    for g in gates:
        if g[0]=='CX':cx(*g[1:])
        elif g[0]=='SWAP':
            a,b=g[1:];cx(a,b);cx(b,a);cx(a,b)
        else:out.append(tuple(g))
    return out
