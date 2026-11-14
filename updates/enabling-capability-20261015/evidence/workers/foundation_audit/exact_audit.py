"""Independent exact-rational audit; no universal PSD assertion is inferred."""
from itertools import product
import json
from pathlib import Path
import sympy as sp


def units(n):
    return [sp.eye(n)[:,j] for j in range(n)]


def lambda_tensor_two(x,p,q):
    """Tr(X)I - (Tr_B(X)⊗I + I⊗Tr_A(X))/2 + X/4."""
    ta=sp.zeros(q); tb=sp.zeros(p)
    for a,b,c,d in product(range(p),range(q),range(p),range(q)):
        if a==c: ta[b,d]+=x[a*q+b,c*q+d]
        if b==d: tb[a,c]+=x[a*q+b,c*q+d]
    return sp.trace(x)*sp.eye(p*q)-(sp.kronecker_product(tb,sp.eye(q))+sp.kronecker_product(sp.eye(p),ta))/2+x/4


def matrices(u,p,q):
    n=p*q; e=units(n)
    A=lambda_tensor_two(u*u.H,p,q)
    L=[lambda_tensor_two(v*u.H,p,q) for v in e]
    Ai=A.inv()
    C=sp.zeros(n*n); S=sp.zeros(n*n)
    for a,b in product(range(n),repeat=2):
        C[b*n:(b+1)*n,a*n:(a+1)*n]=lambda_tensor_two(e[a]*e[b].H,p,q)
        S[b*n:(b+1)*n,a*n:(a+1)*n]=L[a]*Ai*L[b].H
    return A,C,S


def ptrace(x,dims,remove):
    keep=[i for i in range(len(dims)) if i not in remove]
    kd=[dims[i] for i in keep]
    n=sp.prod(kd); out=sp.zeros(n)
    allidx=list(product(*(range(d) for d in dims)))
    def flat(t,ds):
        v=0
        for j,d in zip(t,ds): v=v*d+j
        return v
    for a in allidx:
        for b in allidx:
            if all(a[i]==b[i] for i in remove):
                aa=flat([a[i] for i in keep],kd)
                bb=flat([b[i] for i in keep],kd)
                out[aa,bb]+=x[flat(a,dims),flat(b,dims)]
    return out


def q3(x):
    total=sp.Rational(0)
    import itertools
    for k in range(4):
        for remove in itertools.combinations(range(3),k):
            t=ptrace(x,[3,3,3],remove)
            total+=(-sp.Rational(1,2))**k*sp.trace(t.H*t)
    return sp.simplify(total)


def main():
    u=sp.Matrix([1,0,0,1]) # S invariant to scaling of nonzero reference.
    A,C,S=matrices(u,2,2)
    w=sp.Matrix([3,0,0,1,0,0,2,0,0,2,0,0,1,0,0,3])
    gen=C.inv()*S
    out={
      'status':'EXACT_FINITE_AUDIT_UNIVERSAL_BOUND_UNPROVED',
      'reference':'u=(1,0,0,1); normalized reference gives same C and S',
      'A_for_unnormalized_reference':str(A),
      'w_norm_squared':str((w.H*w)[0]),
      'w_C_w':str((w.H*C*w)[0]),
      'w_S_w':str((w.H*S*w)[0]),
      'w_C_plus_S_w':str((w.H*(C+S)*w)[0]),
      'generalized_S_spectrum':{str(k):v for k,v in gen.eigenvals().items()},
      'C_minus_S_PSD':bool((C-S).is_positive_semidefinite),
      'S_plus_3C_PSD':bool((S+3*C).is_positive_semidefinite),
      'S_plus_11C_over9_PSD':bool((S+sp.Rational(11,9)*C).is_positive_semidefinite),
    }
    # Exact single-site generalized spectrum for a qutrit reference |0>.
    d=3; e=units(d); lam=lambda x: sp.trace(x)*sp.eye(d)-x/2
    a0=lam(e[0]*e[0].H); ell=[lam(v*e[0].H) for v in e]
    c0=sp.zeros(d*d); s0=sp.zeros(d*d)
    for a,b in product(range(d),repeat=2):
        c0[b*d:(b+1)*d,a*d:(a+1)*d]=lam(e[a]*e[b].H)
        s0[b*d:(b+1)*d,a*d:(a+1)*d]=ell[a]*a0.inv()*ell[b].H
    out['single_qutrit_generalized_spectrum']={str(k):v for k,v in (c0.inv()*s0).eigenvals().items()}
    # Explicit independently verifiable separation from source sectors.
    def ket(*terms):
        v=sp.zeros(27,1)
        for a,b,c in terms: v[9*a+3*b+c]=1
        return v
    u=ket((0,0,0),(0,1,1),(0,2,2))
    x=ket((1,0,1),(2,1,2))
    v=ket((1,0,0),(1,1,1),(1,2,2))
    y=ket((0,0,2),(2,1,0))
    K=u*v.H+x*y.H
    out['sector_separation']={
      'vectors_unnormalized':{'u':['000','011','022'],'x':['101','212'],'v':['100','111','122'],'y':['002','210']},
      'coefficient':'K=|u><v|+|x><y|',
      'rank_K':K.rank(),'rank_combined_support':sp.Matrix.hstack(u,x,v,y).rank(),
      'K_squared_zero':K*K==sp.zeros(27),'normal':K*K.H==K.H*K,
      'q3_K':str(q3(K)),
      'range_local_support_ranks':[ptrace(u*u.H+x*x.H,[3,3,3],[j for j in range(3) if j!=i]).rank() for i in range(3)],
      'corange_local_support_ranks':[ptrace(v*v.H+y*y.H,[3,3,3],[j for j in range(3) if j!=i]).rank() for i in range(3)],
      'single_partial_trace_nonzero':[ptrace(K,[3,3,3],[i])!=sp.zeros(9) for i in range(3)],
      'no_product_ray_proof':'Projection of alpha*u+beta*x onto first-site |0> is alpha*(|00>+|11>+|22>); a product ray forces alpha=0, but x has first-site Schmidt rank 2. The input plane argument uses projection onto first-site |1> and v,y.',
    }
    p=Path(__file__).with_name('exact_audit.json')
    p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
