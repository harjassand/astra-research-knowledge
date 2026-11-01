"""Exact independent checks of complex map contraction and sector separation.
The universal grouped bound is an external premise of the consequence proof;
this checker does not assert that premise from finite evaluations.
"""
from itertools import combinations,product
from pathlib import Path
import json
import random
import sympy as s
from exact_audit import ptrace


def embed(x,dims,keep):
    n=int(s.prod(dims)); out=s.zeros(n)
    allidx=list(product(*(range(d) for d in dims)))
    def flat(t,ds):
        v=0
        for j,d in zip(t,ds):v=v*d+j
        return v
    for ia,a in enumerate(allidx):
        for ib,b in enumerate(allidx):
            if all(a[j]==b[j] for j in range(len(dims)) if j not in keep):
                i=flat([a[j] for j in keep],[dims[j] for j in keep])
                k=flat([b[j] for j in keep],[dims[j] for j in keep])
                out[ia,ib]=x[i,k]
    return out


def phi(x,dims):
    out=s.zeros(x.rows)
    for k in range(len(dims)+1):
        for keep in combinations(range(len(dims)),k):
            out+=(-s.Rational(1,2))**k*embed(ptrace(x,dims,[j for j in range(len(dims)) if j not in keep]),dims,keep)
    return out


def qk(x,dims):
    out=s.Rational(0); rows={}
    for k in range(len(dims)+1):
        for rem in combinations(range(len(dims)),k):
            z=ptrace(x,dims,rem); norm=s.trace(z.H*z)
            rows[','.join(str(j) for j in rem)]=str(s.simplify(norm))
            out+=(-s.Rational(1,2))**k*norm
    return s.simplify(out),rows


def sector_example(d,terms):
    def ket(ts):
        z=s.zeros(d**3,1)
        for a,b,c in ts:z[d*d*a+d*b+c]=1
        return z
    u,x,v,y=map(ket,terms); K=u*v.H+x*y.H
    val,norms=qk(K,[d]*3)
    out={'dimension':d,'vectors_unnormalized':{key:[''.join(map(str,t)) for t in ts] for key,ts in zip(['u','x','v','y'],terms)},'rank_K':K.rank(),'K_squared_zero':K*K==s.zeros(d**3),'normal':K*K.H==K.H*K,'combined_support_dimension':s.Matrix.hstack(u,x,v,y).rank(),'q3':str(val),'partial_trace_norms_squared':norms,'range_local_support_ranks':[ptrace(u*u.H+x*x.H,[d]*3,[j for j in range(3) if j!=i]).rank() for i in range(3)],'corange_local_support_ranks':[ptrace(v*v.H+y*y.H,[d]*3,[j for j in range(3) if j!=i]).rank() for i in range(3)]}
    return out


def main():
    rng=random.Random(20261015)
    dims=[2,3,2]; n=12
    u,x,v,y=[s.Matrix([rng.randrange(-2,3)+s.I*rng.randrange(-2,3) for _ in range(n)]) for _ in range(4)]
    K=u*v.H+x*y.H
    actual,_=qk(K,dims)
    A=phi(u*u.H,dims); D=phi(x*x.H,dims); L=phi(x*u.H,dims)
    a=(v.H*A*v)[0];d=(y.H*D*y)[0];g=(y.H*L*v)[0]
    expected=s.simplify(a+d+2*s.re(g))
    out={'status':'EXACT_ALGEBRA_AUDIT','complex_contraction':{'seed':20261015,'dimensions':dims,'u_x_v_y_mutually_orthogonal_required':False,'qk':str(actual),'a':str(s.simplify(a)),'d':str(s.simplify(d)),'g':str(s.simplify(g)),'qk_equals_a_plus_d_plus_twice_real_g':s.simplify(actual-expected)==0},'examples':[]}
    out['examples'].append(sector_example(3,[[(0,0,0),(0,1,1)],[(1,2,2),(2,1,2)],[(1,0,0),(1,1,1)],[(0,2,2),(2,0,1)]]))
    out['examples'].append(sector_example(4,[[(0,0,0),(0,1,1)],[(1,0,1),(2,1,2),(3,2,3),(3,3,0)],[(1,0,0),(1,1,1)],[(0,0,2),(2,1,0),(0,2,1),(3,3,2),(3,0,3)]]))
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
